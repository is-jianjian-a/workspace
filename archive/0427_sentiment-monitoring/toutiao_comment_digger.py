#!/usr/bin/env python3
"""
头条评论深挖 - 无需登录
"""

import json
import time
import re
import os
from playwright.sync_api import sync_playwright

class ToutiaoCommentDigger:
    def __init__(self, output_dir='./output'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.cookie_file = "toutiao_cookies.json"
    
    def search_and_dig(self, keyword, max_comments=50):
        """
        搜索关键词 -> 点击第一个文章 -> 深挖评论
        """
        print(f"[→] 头条搜索: {keyword}")
        
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
                print("[✓] 已加载头条cookie")
            
            page = context.new_page()
            
            # 1. 搜索关键词
            search_url = f"https://so.toutiao.com/search?dvpf=pc&keyword={keyword}"
            try:
                page.goto(search_url, wait_until='networkidle', timeout=30000)
            except:
                page.goto(search_url, wait_until='domcontentloaded')
            time.sleep(10)
            
            print("[→] 查找文章...")
            
            # 2. 找到文章链接
            article_links = page.evaluate('''() => {
                const links = document.querySelectorAll('a');
                const articles = [];
                for (const link of links) {
                    const href = link.href;
                    // 匹配头条文章链接（包含article或trending）
                    if (href && (href.includes('/article/') || href.includes('/trending/') || href.includes('toutiao.com'))) {
                        const title = link.innerText || '';
                        if (title.length > 10) {
                            articles.push({href, title: title.substring(0, 100)});
                        }
                    }
                }
                return articles.slice(0, 5);
            }''')
            
            if not article_links:
                print("[✗] 未找到文章")
                browser.close()
                return []
            
            print(f"[✓] 找到 {len(article_links)} 篇文章")
            for i, a in enumerate(article_links[:3], 1):
                print(f"  [{i}] {a['title'][:60]}...")
            
            # 3. 点击第一篇文章
            first_article = article_links[0]
            print(f"\n[→] 点击进入文章...")
            
            href = first_article['href']
            if href.startswith('//'):
                href = 'https:' + href
            
            page.goto(href, wait_until='domcontentloaded')
            time.sleep(10)
            
            # 4. 滚动加载评论
            print("[→] 滚动加载评论...")
            for i in range(10):
                page.evaluate('window.scrollBy(0, 1500)')
                time.sleep(2)
            
            time.sleep(5)
            
            # 5. 提取评论
            print("[→] 提取评论...")
            
            comments_data = page.evaluate('''() => {
                const results = [];
                const allDivs = document.querySelectorAll('div');
                
                for (const div of allDivs) {
                    const text = div.innerText || '';
                    // 评论特征：包含中文，长度适中
                    if (text.length > 15 && text.length < 300 && /[\u4e00-\u9fff]/.test(text)) {
                        // 排除导航和推荐
                        const exclude = ['首页', '推荐', '关注', '热点', '视频',
                                        '登录', '注册', '搜索', '头条',
                                        '广告', '推广', '收藏', '点赞', '评论',
                                        '今日头条', 'toutiao'];
                        
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
            
            # 6. 保存结果
            if comments:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"toutiao_comments_{keyword}_{timestamp}.json"
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump({
                        'keyword': keyword,
                        'article_url': href,
                        'article_title': first_article['title'],
                        'count': len(comments),
                        'comments': comments
                    }, f, ensure_ascii=False, indent=2)
                
                print(f"[✓] 结果已保存: {filepath}")
            
            browser.close()
            return comments

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='头条评论深挖')
    parser.add_argument('keyword', help='搜索关键词')
    parser.add_argument('--max', type=int, default=50, help='最大评论数')
    args = parser.parse_args()
    
    digger = ToutiaoCommentDigger()
    comments = digger.search_and_dig(args.keyword, args.max)
    
    print(f"\n{'='*60}")
    print(f"评论列表 - 共 {len(comments)} 条")
    print(f"{'='*60}\n")
    
    for i, comment in enumerate(comments[:20], 1):
        text = comment.get('text', '')
        print(f"[{i}] {text[:200]}...")
        print()
