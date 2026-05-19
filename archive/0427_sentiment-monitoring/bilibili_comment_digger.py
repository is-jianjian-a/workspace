#!/usr/bin/env python3
"""
B站评论深挖 - 有头浏览器+登录
需要用户手动登录
"""

import json
import time
import re
import os
from playwright.sync_api import sync_playwright

class BilibiliCommentDigger:
    def __init__(self, output_dir='./output'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.cookie_file = "bilibili_cookies.json"
    
    def dig_comments(self, bvid, max_comments=50):
        """
        深挖B站视频评论
        """
        print(f"[→] 深挖B站评论: {bvid}")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(
                viewport={'width': 1280, 'height': 900}
            )
            
            # 加载cookie
            if os.path.exists(self.cookie_file):
                with open(self.cookie_file, 'r', encoding='utf-8') as f:
                    cookies = json.load(f)
                context.add_cookies(cookies)
                print("[✓] 已加载B站cookie")
            
            page = context.new_page()
            url = f"https://www.bilibili.com/video/{bvid}"
            
            # 使用networkidle等待页面完全加载
            try:
                page.goto(url, wait_until='networkidle', timeout=30000)
            except:
                page.goto(url, wait_until='domcontentloaded')
            
            print("[→] 等待页面加载...")
            time.sleep(15)
            
            # 检查是否需要登录
            html = page.content()
            if '登录后你可以' in html or '立即登录' in html:
                print("\n" + "="*60)
                print("[!] B站需要登录才能查看评论")
                print("请在弹出窗口中完成登录")
                print("等待120秒...")
                print("="*60 + "\n")
                
                # 播放声音提醒
                try:
                    os.system('say "B站需要登录，请在浏览器窗口中完成登录"')
                except:
                    pass
                
                for i in range(120):
                    time.sleep(1)
                    html = page.content()
                    if '登录后你可以' not in html and '立即登录' not in html:
                        print(f"[✓] 登录成功！（{i+1}秒）")
                        # 保存cookie
                        cookies = context.cookies()
                        with open(self.cookie_file, 'w', encoding='utf-8') as f:
                            json.dump(cookies, f, ensure_ascii=False, indent=2)
                        break
                    if (i+1) % 10 == 0:
                        print(f"  ...等待中 ({i+1}/120秒)")
            
            # 滚动到评论区域 - B站评论在页面很下方
            print("[→] 滚动到评论区域...")
            
            # 多次滚动到页面底部
            for i in range(10):
                page.evaluate('window.scrollBy(0, 1500)')
                time.sleep(2)
                
                # 检查是否出现评论
                html = page.content()
                if '评论' in html and len(html) > 500000:
                    print(f"  滚动{i+1}: 页面内容充足，可能已加载评论")
                    break
                
                if (i+1) % 3 == 0:
                    print(f"  滚动{i+1}...")
            
            time.sleep(5)
            
            # 查找评论元素 - B站评论在特定结构中
            print("[→] 查找评论...")
            
            # 先检查页面中是否有评论相关的文本
            page_text = page.inner_text('body')
            if '评论' in page_text:
                print("[✓] 页面包含'评论'文本")
            
            # 尝试通过evaluate查找评论
            comments_data = page.evaluate('''() => {
                // B站评论通常在特定的div结构中
                const allDivs = document.querySelectorAll('div');
                const results = [];
                
                for (const div of allDivs) {
                    const text = div.innerText || '';
                    // 评论特征：包含中文，长度适中，有用户名的格式
                    if (text.length > 20 && text.length < 500 && /[\u4e00-\u9fff]/.test(text)) {
                        // 排除导航和推荐内容
                        const exclude = ['首页', '番剧', '直播', '游戏中心', '会员购', '下载客户端', 
                                        '大会员', '消息', '动态', '收藏', '历史', '创作中心', '投稿',
                                        '热门', '电影', '国创', '电视剧', '综艺', '纪录片', '动画',
                                        '鬼畜', '音乐', '舞蹈', '影视', '娱乐', '知识', '科技数码',
                                        '资讯', '美食', '专栏', '活动', '课堂', '社区中心', '新歌',
                                        '广告', '点赞', '投币', '收藏', '转发', '关注'];
                        
                        const hasExclude = exclude.some(kw => text.includes(kw));
                        if (!hasExclude) {
                            // 检查是否有嵌套结构（评论通常有用户名+内容+时间）
                            const childDivs = div.querySelectorAll('div');
                            if (childDivs.length >= 2) {
                                results.push(text.substring(0, 300));
                            }
                        }
                    }
                }
                
                return results;
            }''')
            
            print(f"[✓] 通过JS找到 {len(comments_data)} 条可能评论")
            
            # 去重
            seen = set()
            comments = []
            for text in comments_data[:max_comments]:
                h = hash(text[:50])
                if h not in seen:
                    seen.add(h)
                    comments.append({'text': text})
            
            # 如果从JS没找到，尝试传统选择器
            if not comments:
                print("[→] 尝试传统选择器...")
                selectors = [
                    '[class*="reply"]',
                    '[class*="comment"]',
                    '[class*="Comment"]',
                    '[class*="Reply"]'
                ]
                
                for selector in selectors:
                    elements = page.query_selector_all(selector)
                    print(f"  选择器 '{selector}': {len(elements)} 个元素")
                    
                    for elem in elements[:max_comments]:
                        try:
                            text = elem.inner_text()
                            if text and len(text) > 10 and re.search(r'[\u4e00-\u9fff]', text):
                                exclude = ['登录', '注册', '高清', '倍速', '弹幕']
                                if not any(kw in text for kw in exclude):
                                    h = hash(text[:50])
                                    if h not in seen:
                                        seen.add(h)
                                        comments.append({'text': text[:500]})
                        except:
                            continue
                        
                        if len(comments) >= max_comments:
                            break
                    
                    if comments:
                        break
            
            print(f"[✓] 提取 {len(comments)} 条评论")
            
            # 保存结果
            if comments:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"bilibili_comments_{bvid}_{timestamp}.json"
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump({
                        'bvid': bvid,
                        'url': url,
                        'count': len(comments),
                        'comments': comments
                    }, f, ensure_ascii=False, indent=2)
                
                print(f"[✓] 结果已保存: {filepath}")
            
            browser.close()
            return comments

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='B站评论深挖')
    parser.add_argument('bvid', help='B站视频BV号')
    parser.add_argument('--max', type=int, default=50, help='最大评论数')
    args = parser.parse_args()
    
    digger = BilibiliCommentDigger()
    comments = digger.dig_comments(args.bvid, args.max)
    
    print(f"\n{'='*60}")
    print(f"评论列表 - 共 {len(comments)} 条")
    print(f"{'='*60}\n")
    
    for i, comment in enumerate(comments[:20], 1):
        text = comment.get('text', '')
        print(f"[{i}] {text[:150]}...")
        print()
