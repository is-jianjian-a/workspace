#!/usr/bin/env python3
"""
B站评论深挖 V3 - 使用API获取评论
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
        搜索关键词 -> 点击第一个视频 -> 通过API获取评论
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
            
            # 3. 提取BV号并获取评论
            first_video = video_links[0]
            href = first_video['href']
            if href.startswith('//'):
                href = 'https:' + href
            
            bvid_match = re.search(r'/video/(BV\w+)', href)
            bvid = bvid_match.group(1) if bvid_match else None
            
            if not bvid:
                print("[✗] 无法提取BV号")
                browser.close()
                return []
            
            print(f"\n[→] BV号: {bvid}")
            
            # 4. 通过API获取视频信息和评论
            print("[→] 通过API获取评论...")
            
            # 先获取视频信息
            video_info = page.evaluate('''async (bvid) => {
                try {
                    const response = await fetch('https://api.bilibili.com/x/web-interface/view?bvid=' + bvid);
                    const data = await response.json();
                    return {
                        aid: data.data?.aid,
                        title: data.data?.title
                    };
                } catch (e) {
                    return {error: e.message};
                }
            }''', bvid)
            
            if 'error' in video_info:
                print(f"[✗] 获取视频信息失败: {video_info['error']}")
                browser.close()
                return []
            
            aid = video_info.get('aid')
            video_title = video_info.get('title', '')
            
            if not aid:
                print("[✗] 无法获取aid")
                browser.close()
                return []
            
            print(f"[✓] 视频标题: {video_title}")
            print(f"[✓] aid: {aid}")
            
            # 获取评论 - 分页获取
            all_comments = []
            for page_num in range(1, 4):
                comment_result = page.evaluate('''async (params) => {
                    try {
                        const url = 'https://api.bilibili.com/x/v2/reply?type=1&oid=' + params.aid + '&sort=2&ps=20&pn=' + params.page;
                        const response = await fetch(url);
                        const data = await response.json();
                        return {
                            replies: data.data?.replies || [],
                            count: data.data?.replies?.length || 0
                        };
                    } catch (e) {
                        return {error: e.message};
                    }
                }''', {'aid': str(aid), 'page': str(page_num)})
                
                if 'error' in comment_result:
                    print(f"  第{page_num}页错误: {comment_result['error']}")
                    break
                
                replies = comment_result.get('replies', [])
                if not replies:
                    break
                
                all_comments.extend(replies)
                print(f"  第{page_num}页: {len(replies)} 条评论")
            
            print(f"[✓] 总共获取 {len(all_comments)} 条原始评论")
            
            # 5. 解析评论
            comments = []
            for r in all_comments[:max_comments]:
                content = r.get('content', {}).get('message', '')
                author = r.get('member', {}).get('uname', '')
                like = r.get('like', 0)
                ctime = r.get('ctime', 0)
                
                if content and len(content) > 5:
                    comments.append({
                        'author': author,
                        'text': content,
                        'likes': like,
                        'time': time.strftime('%Y-%m-%d %H:%M', time.localtime(ctime)) if ctime else ''
                    })
            
            print(f"[✓] 解析出 {len(comments)} 条有效评论")
            
            # 6. 保存结果
            if comments:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"bilibili_comments_{keyword}_{timestamp}.json"
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump({
                        'keyword': keyword,
                        'bvid': bvid,
                        'aid': aid,
                        'video_title': video_title,
                        'video_url': href,
                        'count': len(comments),
                        'comments': comments
                    }, f, ensure_ascii=False, indent=2)
                
                print(f"[✓] 结果已保存: {filepath}")
            
            browser.close()
            return comments

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='B站评论深挖V3 - API方式')
    parser.add_argument('keyword', help='搜索关键词')
    parser.add_argument('--max', type=int, default=50, help='最大评论数')
    args = parser.parse_args()
    
    digger = BilibiliCommentDigger()
    comments = digger.search_and_dig(args.keyword, args.max)
    
    print(f"\n{'='*60}")
    print(f"评论列表 - 共 {len(comments)} 条")
    print(f"{'='*60}\n")
    
    for i, comment in enumerate(comments[:20], 1):
        author = comment.get('author', '匿名')
        text = comment.get('text', '')
        likes = comment.get('likes', 0)
        print(f"[{i}] [{author}] (赞{likes}): {text[:150]}...")
        print()
