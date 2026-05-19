#!/usr/bin/env python3
"""抖音搜索 - 通过Playwright提取页面元素"""

from playwright.sync_api import sync_playwright
import json
import time
import os
import re

COOKIE_FILE = "/Users/zhijian/workspace/sentiment-monitoring/douyin_cookies.json"
OUTPUT_DIR = "/Users/zhijian/workspace/sentiment-monitoring/output"

def douyin_search(keyword, max_results=15):
    """抖音搜索 - 必须使用有头浏览器，提取页面元素"""
    
    print(f"[→] 抖音搜索: {keyword}")
    
    import urllib.parse
    encoded_keyword = urllib.parse.quote(keyword)
    
    with sync_playwright() as p:
        # 必须使用有头浏览器
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': 1280, 'height': 900}
        )
        
        # 加载cookie
        if os.path.exists(COOKIE_FILE):
            with open(COOKIE_FILE, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            context.add_cookies(cookies)
            print("[✓] 已加载cookie")
        
        page = context.new_page()
        
        # 访问搜索页
        url = f'https://www.douyin.com/search/{encoded_keyword}'
        page.goto(url, wait_until='domcontentloaded')
        
        print("[→] 等待页面加载...")
        time.sleep(8)
        
        # 检查是否需要登录
        login_prompt = page.query_selector('text=登录后即可搜索')
        if login_prompt:
            print("\n" + "="*60)
            print("[!] 需要登录抖音")
            print("请完成扫码或手机验证码登录...")
            print("等待60秒...")
            print("="*60 + "\n")
            
            for i in range(60):
                time.sleep(1)
                login_prompt = page.query_selector('text=登录后即可搜索')
                if not login_prompt:
                    print(f"[✓] 登录成功！（{i+1}秒）")
                    # 保存cookie
                    cookies = context.cookies()
                    with open(COOKIE_FILE, 'w', encoding='utf-8') as f:
                        json.dump(cookies, f, ensure_ascii=False, indent=2)
                    print("[✓] Cookie已保存")
                    break
                if (i+1) % 10 == 0:
                    print(f"  ...等待中 ({i+1}/60秒)")
        
        # 等待搜索结果加载
        print("[→] 等待搜索结果...")
        time.sleep(5)
        
        # 滚动加载更多
        print("[→] 滚动加载更多...")
        for i in range(3):
            page.evaluate('window.scrollBy(0, 800)')
            time.sleep(2)
        
        time.sleep(3)
        
        # 提取视频卡片 - 通过data-e2e属性
        videos = []
        
        # 方式1: 通过data-e2e="search-card-video"查找
        cards = page.query_selector_all('[data-e2e="search-card-video"]')
        print(f"[→] 找到 {len(cards)} 个视频卡片 (data-e2e)")
        
        for card in cards[:max_results]:
            try:
                # 提取标题
                title_elem = card.query_selector('[data-e2e="search-card-title"]')
                title = title_elem.inner_text() if title_elem else ''
                
                # 提取作者
                author_elem = card.query_selector('[data-e2e="search-card-user"]')
                author = author_elem.inner_text() if author_elem else ''
                
                # 提取点赞数
                like_elem = card.query_selector('[data-e2e="search-card-like-count"]')
                likes = like_elem.inner_text() if like_elem else ''
                
                # 提取链接
                link_elem = card.query_selector('a')
                link = link_elem.get_attribute('href') if link_elem else ''
                
                if title:
                    videos.append({
                        'title': title,
                        'author': author,
                        'likes': likes,
                        'url': f'https://www.douyin.com{link}' if link and not link.startswith('http') else link
                    })
            except Exception as e:
                print(f"  提取失败: {e}")
                continue
        
        # 方式2: 如果没有找到，尝试其他选择器
        if not videos:
            print("[→] 尝试其他选择器...")
            
            # 尝试查找所有包含视频链接的a标签
            links = page.query_selector_all('a[href*="/video/"]')
            print(f"  找到 {len(links)} 个视频链接")
            
            for link in links[:max_results]:
                try:
                    href = link.get_attribute('href')
                    # 查找父元素中的标题
                    parent = link.query_selector('xpath=..')
                    if parent:
                        # 尝试多种标题选择器
                        title = ''
                        for selector in ['span', 'div', 'p', 'h1', 'h2', 'h3']:
                            elem = parent.query_selector(selector)
                            if elem:
                                text = elem.inner_text().strip()
                                if len(text) > 5 and len(text) < 200:
                                    title = text
                                    break
                        
                        if title:
                            videos.append({
                                'title': title,
                                'url': f'https://www.douyin.com{href}' if not href.startswith('http') else href
                            })
                except:
                    continue
        
        # 方式3: 从页面文本中提取
        if not videos:
            print("[→] 尝试从页面文本提取...")
            html = page.content()
            
            # 查找所有包含"白冰"的文本
            texts = re.findall(r'>[^<]{10,200}白冰[^<]{0,100}<', html)
            for t in texts[:max_results]:
                clean = re.sub(r'<[^>]+>', '', t)
                clean = re.sub(r'\s+', ' ', clean).strip()
                if len(clean) > 10 and clean not in [v['title'] for v in videos]:
                    videos.append({'title': clean})
        
        print(f"[✓] 共提取 {len(videos)} 条视频")
        
        # 保存结果
        if videos:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"douyin_{keyword}_{timestamp}.json"
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(videos, f, ensure_ascii=False, indent=2)
            
            print(f"[✓] 结果已保存: {filepath}")
        
        browser.close()
        return videos

if __name__ == '__main__':
    import sys
    keyword = sys.argv[1] if len(sys.argv) > 1 else "网红白冰偷税"
    results = douyin_search(keyword)
    
    print(f"\n{'='*60}")
    print(f"🎵 抖音搜索结果 - {len(results)} 条")
    print(f"{'='*60}")
    
    for i, video in enumerate(results[:10], 1):
        print(f"\n[{i}] {video.get('title', '')[:70]}...")
        if video.get('author'):
            print(f"    👤 作者: {video['author']}")
        if video.get('likes'):
            print(f"    👍 点赞: {video['likes']}")
        if video.get('url'):
            print(f"    🔗 {video['url'][:80]}...")
