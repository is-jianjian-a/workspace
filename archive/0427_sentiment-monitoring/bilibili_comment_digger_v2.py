#!/usr/bin/env python3
"""
B站评论深挖 V2 - 先搜索再点视频
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
    
    def search_and_dig(self, keyword, max_comments=50):
        """
        搜索关键词 -> 点击第一个视频 -> 深挖评论
        """
        print(f"[→] B站搜索: {keyword}")
        
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
            
            # 1. 搜索关键词
            search_url = f"https://search.bilibili.com/all?keyword={keyword}"
            page.goto(search_url, wait_until='networkidle')
            time.sleep(5)
            
            print("[→] 查找视频...")
            
            # 2. 找到第一个视频链接
            video_links = page.evaluate('''() => {
                const links = document.querySelectorAll('a');
                const videos = [];
                for (const link of links) {
                    const href = link.href;
                    if (href && href.includes('/video/BV')) {
                        const title = link.innerText || '';
                        videos.push({href, title: title.substring(0, 100)});
                    }
                }
                return videos.slice(0, 5);
            }''')
            
            if not video_links:
                print("[✗] 未找到视频")
                browser.close()
                return []
            
            print(f"[✓] 找到 {len(video_links)} 个视频")
            for i, v in enumerate(video_links[:3], 1):
                print(f"  [{i}] {v['title'][:60]}...")
            
            # 3. 点击第一个视频
            first_video = video_links[0]
            print(f"\n[→] 点击进入视频: {first_video['title'][:60]}...")
            
            # 使用goto而不是click，更稳定
            bvid_match = re.search(r'/video/(BV[\w]+)', first_video['href'])
            if bvid_match:
                bvid = bvid_match.group(1)
            else:
                bvid = 'unknown'
            
            page.goto(first_video['href'], wait_until='networkidle')
            time.sleep(10)
            
            # 4. 检查是否需要登录
            html = page.content()
            if '登录后你可以' in html or '立即登录' in html:
                print("\n" + "="*60)
                print("[!] B站需要登录才能查看评论")
                print("请在弹出窗口中完成登录")
                print("等待120秒...")
                print("="*60)
                
                # 播放声音提醒
                try:
                    os.system('say "B站需要登录，请在浏览器窗口中点击登录按钮完成登录"')
                except:
                    pass
                
                for i in range(120):
                    time.sleep(1)
                    html = page.content()
                    if '登录后你可以' not in html and '立即登录' not in html:
                        print(f"\n[✓] 登录成功！（{i+1}秒）")
                        # 保存cookie
                        cookies = context.cookies()
                        with open(self.cookie_file, 'w', encoding='utf-8') as f:
                            json.dump(cookies, f, ensure_ascii=False, indent=2)
                        break
                    if (i+1) % 10 == 0:
                        print(f"  ...等待中 ({i+1}/120秒)")
            
            # 5. 滚动到评论区域
            print("\n[→] 滚动到评论区域...")
            
            # 先滚动几次让页面加载
            for i in range(5):
                page.evaluate('window.scrollBy(0, 1500)')
                time.sleep(2)
            
            # 查找评论区域
            print("[→] 查找评论区域...")
            
            # 尝试找到评论区域
            comment_section = None
            selectors = [
                '#comment',
                '.reply-box',
                '[class*="reply"]',
                '[class*="comment"]'
            ]
            
            for selector in selectors:
                elem = page.query_selector(selector)
                if elem:
                    print(f"[✓] 找到评论区域: {selector}")
                    comment_section = elem
                    break
            
            # 6. 提取评论
            print("[→] 提取评论...")
            comments = []
            
            # 使用JS提取评论 - 专门针对B站评论结构
            comments_data = page.evaluate('''() => {
                const results = [];
                
                // B站评论通常在 .reply-item 或特定结构中
                // 尝试多种可能的评论选择器
                const selectors = [
                    '.reply-item',
                    '.reply-content',
                    '[class*="reply"]',
                    '[class*="comment"]',
                    '#comment .content',
                    '.bili-comment'
                ];
                
                for (const selector of selectors) {
                    const elements = document.querySelectorAll(selector);
                    for (const elem of elements) {
                        const text = elem.innerText || '';
                        if (text.length > 10 && text.length < 500 && /[\u4e00-\u9fff]/.test(text)) {
                            results.push(text.substring(0, 400));
                        }
                    }
                    if (results.length > 0) break;
                }
                
                // 如果选择器没找到，尝试从页面所有div中找
                if (results.length === 0) {
                    const allDivs = document.querySelectorAll('div');
                    for (const div of allDivs) {
                        const text = div.innerText || '';
                        // 评论特征：包含中文，长度适中，有用户名+内容格式
                        if (text.length > 20 && text.length < 400 && /[\u4e00-\u9fff]/.test(text)) {
                            // 排除明显的非评论内容
                            const exclude = ['首页', '番剧', '直播', '游戏中心', '会员购', 
                                            '下载客户端', '大会员', '消息', '动态', '收藏', 
                                            '历史', '创作中心', '投稿', '热门', '电影', '国创',
                                            '电视剧', '综艺', '纪录片', '动画', '鬼畜', '音乐',
                                            '舞蹈', '影视', '娱乐', '知识', '科技数码', '资讯',
                                            '美食', '专栏', '活动', '课堂', '社区中心', '广告',
                                            '弹幕', '黑体', '宋体', '微软雅黑', '背景不透明度',
                                            '浏览器还未开启', '本地网络访问', '未经作者授权',
                                            '禁止转载', '成为UP主', '老粉', '助力UP成长',
                                            '记笔记', '发布笔记', '分享链接', '手机扫码',
                                            '高能进度条', '弹幕随屏幕缩放', '防挡字幕',
                                            '智能防挡弹幕', '弹幕观看屏蔽词', '同步屏蔽列表'];
                            
                            const hasExclude = exclude.some(kw => text.includes(kw));
                            if (!hasExclude) {
                                // 检查是否有嵌套结构（评论通常有用户名+内容+时间）
                                const childDivs = div.querySelectorAll('div');
                                if (childDivs.length >= 2 && childDivs.length <= 8) {
                                    results.push(text.substring(0, 400));
                                }
                            }
                        }
                    }
                }
                
                return results;
            }''')
            
            print(f"[✓] 找到 {len(comments_data)} 条可能评论")
            
            # 去重和过滤
            seen = set()
            for text in comments_data:
                # 进一步过滤：要求有实质性内容
                lines = [l.strip() for l in text.split('\n') if l.strip()]
                
                # 检查是否有真正的评论内容（不是只有时间/地点）
                has_content = False
                for line in lines:
                    # 排除纯时间格式
                    if re.match(r'^\d{1,2}[-:]\d{2}', line):
                        continue
                    # 排除纯数字（点赞数）
                    if line.isdigit():
                        continue
                    # 排除"回复"、"点赞"等操作词
                    if line in ['回复', '点赞', '投币', '收藏', '转发']:
                        continue
                    # 如果行长度合适且有中文，认为是内容
                    if len(line) > 5 and re.search(r'[\u4e00-\u9fff]', line):
                        has_content = True
                        break
                
                if has_content:
                    h = hash(text[:80])
                    if h not in seen:
                        seen.add(h)
                        comments.append({'text': text})
                
                if len(comments) >= max_comments:
                    break
            
            print(f"[✓] 提取 {len(comments)} 条有效评论")
            
            # 保存结果
            if comments:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"bilibili_comments_{keyword}_{timestamp}.json"
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump({
                        'keyword': keyword,
                        'video_url': first_video['href'],
                        'video_title': first_video['title'],
                        'count': len(comments),
                        'comments': comments
                    }, f, ensure_ascii=False, indent=2)
                
                print(f"[✓] 结果已保存: {filepath}")
            
            browser.close()
            return comments

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='B站评论深挖V2')
    parser.add_argument('keyword', help='搜索关键词')
    parser.add_argument('--max', type=int, default=50, help='最大评论数')
    args = parser.parse_args()
    
    digger = BilibiliCommentDigger()
    comments = digger.search_and_dig(args.keyword, args.max)
    
    print(f"\n{'='*60}")
    print(f"评论列表 - 共 {len(comments)} 条")
    print(f"{'='*60}\n")
    
    for i, comment in enumerate(comments[:20], 1):
        text = comment.get('text', '')
        print(f"[{i}] {text[:200]}...")
        print()
