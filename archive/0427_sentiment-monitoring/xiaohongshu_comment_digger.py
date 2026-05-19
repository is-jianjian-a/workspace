#!/usr/bin/env python3
"""
小红书评论深挖 - 有头浏览器+登录
"""

import json
import time
import re
import os
from playwright.sync_api import sync_playwright

class XiaohongshuCommentDigger:
    def __init__(self, output_dir='./output'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.cookie_file = "xiaohongshu_cookies.json"
    
    def search_and_dig(self, keyword, max_comments=50):
        """
        搜索关键词 -> 点击第一个笔记 -> 深挖评论
        """
        print(f"[→] 小红书搜索: {keyword}")
        
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
                print("[✓] 已加载小红书cookie")
            
            page = context.new_page()
            
            # 1. 搜索关键词
            search_url = f"https://www.xiaohongshu.com/search_result?keyword={keyword}"
            try:
                page.goto(search_url, wait_until='networkidle', timeout=30000)
            except:
                page.goto(search_url, wait_until='domcontentloaded')
            time.sleep(10)
            
            print("[→] 查找笔记...")
            
            # 2. 找到笔记链接
            note_links = page.evaluate('''() => {
                const links = document.querySelectorAll('a');
                const notes = [];
                for (const link of links) {
                    const href = link.href;
                    if (href && href.includes('/explore/')) {
                        const title = link.innerText || '';
                        notes.push({href, title: title.substring(0, 100)});
                    }
                }
                return notes.slice(0, 5);
            }''')
            
            if not note_links:
                print("[✗] 未找到笔记")
                browser.close()
                return []
            
            print(f"[✓] 找到 {len(note_links)} 个笔记")
            for i, n in enumerate(note_links[:3], 1):
                print(f"  [{i}] {n['title'][:60]}...")
            
            # 3. 点击第一个笔记
            first_note = note_links[0]
            print(f"\n[→] 点击进入笔记...")
            
            href = first_note['href']
            if href.startswith('//'):
                href = 'https:' + href
            
            page.goto(href, wait_until='domcontentloaded')
            time.sleep(10)
            
            # 4. 检查是否需要登录
            html = page.content()
            if '登录' in html or '手机号登录' in html:
                print("\n" + "="*60)
                print("[!] 小红书需要登录")
                print("请在弹出窗口中完成登录")
                print("等待120秒...")
                print("="*60)
                
                # 播放声音提醒
                try:
                    import subprocess
                    subprocess.run(['say', '小红书需要登录，请在浏览器窗口中完成登录操作'], check=False)
                except:
                    pass
                
                for i in range(120):
                    time.sleep(1)
                    html = page.content()
                    if '登录' not in html and '手机号登录' not in html:
                        print(f"\n[✓] 登录成功！（{i+1}秒）")
                        # 保存cookie
                        cookies = context.cookies()
                        with open(self.cookie_file, 'w', encoding='utf-8') as f:
                            json.dump(cookies, f, ensure_ascii=False, indent=2)
                        break
                    if (i+1) % 10 == 0:
                        print(f"  ...等待中 ({i+1}/120秒)")
            
            # 5. 滚动加载评论
            print("\n[→] 滚动加载评论...")
            for i in range(10):
                page.evaluate('window.scrollBy(0, 1500)')
                time.sleep(2)
            
            time.sleep(5)
            
            # 6. 提取评论
            print("[→] 提取评论...")
            
            comments_data = page.evaluate('''() => {
                const results = [];
                const allDivs = document.querySelectorAll('div');
                
                for (const div of allDivs) {
                    const text = div.innerText || '';
                    // 评论特征：包含中文，长度适中
                    if (text.length > 15 && text.length < 300 && /[\u4e00-\u9fff]/.test(text)) {
                        // 排除导航和推荐
                        const exclude = ['首页', '发现', '关注', '消息', '我',
                                        '登录', '注册', '搜索', '小红书',
                                        '广告', '推广', '收藏', '点赞', '评论'];
                        
                        const hasExclude = exclude.some(kw => text.includes(kw));
                        if (!hasExclude) {
                            const childDivs = div.querySelectorAll('div');
                            if (childDivs.length >= 2 && childDivs.length <= 6) {
                                results.push(text.substring(0, 300));
                            }
                        }
                    }
                }
                
                return results;
            }''')
            
            print(f"[✓] 找到 {len(comments_data)} 条可能评论")
            
            # 去重和过滤
            seen = set()
            comments = []
            for text in comments_data:
                h = hash(text[:80])
                if h not in seen:
                    seen.add(h)
                    comments.append({'text': text})
                
                if len(comments) >= max_comments:
                    break
            
            print(f"[✓] 提取 {len(comments)} 条有效评论")
            
            # 7. 保存结果
            if comments:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"xiaohongshu_comments_{keyword}_{timestamp}.json"
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump({
                        'keyword': keyword,
                        'note_url': href,
                        'note_title': first_note['title'],
                        'count': len(comments),
                        'comments': comments
                    }, f, ensure_ascii=False, indent=2)
                
                print(f"[✓] 结果已保存: {filepath}")
            
            browser.close()
            return comments

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='小红书评论深挖')
    parser.add_argument('keyword', help='搜索关键词')
    parser.add_argument('--max', type=int, default=50, help='最大评论数')
    args = parser.parse_args()
    
    digger = XiaohongshuCommentDigger()
    comments = digger.search_and_dig(args.keyword, args.max)
    
    print(f"\n{'='*60}")
    print(f"评论列表 - 共 {len(comments)} 条")
    print(f"{'='*60}\n")
    
    for i, comment in enumerate(comments[:20], 1):
        text = comment.get('text', '')
        print(f"[{i}] {text[:200]}...")
        print()
