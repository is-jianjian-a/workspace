#!/usr/bin/env python3
"""抖音搜索 - 有头浏览器直接抓取（不依赖持久化cookie）"""

from playwright.sync_api import sync_playwright
import json
import time
import os
import re

OUTPUT_DIR = "/Users/zhijian/workspace/sentiment-monitoring/output"

def douyin_search_direct(keyword, max_results=15):
    """
    抖音搜索 - 有头浏览器直接访问
    如果已登录则直接抓取，如果需要登录则提示用户
    """
    print(f"[→] 抖音搜索: {keyword}")
    print("[!] 注意: 抖音需要已登录状态才能搜索")
    
    import urllib.parse
    encoded_keyword = urllib.parse.quote(keyword)
    
    with sync_playwright() as p:
        # 有头浏览器
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': 1280, 'height': 900}
        )
        
        # 尝试加载之前的cookie（可能部分有效）
        cookie_file = "/Users/zhijian/workspace/sentiment-monitoring/douyin_cookies.json"
        if os.path.exists(cookie_file):
            try:
                with open(cookie_file, 'r', encoding='utf-8') as f:
                    cookies = json.load(f)
                context.add_cookies(cookies)
                print("[✓] 已加载历史cookie")
            except:
                pass
        
        page = context.new_page()
        
        # 先访问首页建立session
        print("[→] 访问抖音首页...")
        page.goto('https://www.douyin.com', wait_until='domcontentloaded')
        time.sleep(3)
        
        # 再访问搜索页
        url = f'https://www.douyin.com/search/{encoded_keyword}'
        print(f"[→] 访问搜索页...")
        page.goto(url, wait_until='domcontentloaded')
        
        # 检测登录状态
        print("[→] 检测登录状态...")
        time.sleep(5)
        
        html = page.content()
        
        # 检查是否需要登录
        if '登录后即可搜索' in html or '请登录' in html:
            print("\n" + "="*60)
            print("[!] 抖音需要登录")
            print("请在弹出窗口中完成扫码登录")
            print("等待90秒...")
            print("="*60 + "\n")
            
            # 循环检测，最多90秒
            logged_in = False
            for i in range(90):
                time.sleep(1)
                html = page.content()
                
                # 检测登录成功标志
                if '登录后即可搜索' not in html and ('搜索结果' in html or len(html) > 100000):
                    print(f"[✓] 登录成功！（{i+1}秒）")
                    logged_in = True
                    
                    # 保存所有存储数据
                    cookies = context.cookies()
                    with open(cookie_file, 'w', encoding='utf-8') as f:
                        json.dump(cookies, f, ensure_ascii=False, indent=2)
                    
                    # 保存localStorage
                    local_storage = page.evaluate('() => JSON.stringify(localStorage)')
                    with open('/Users/zhijian/workspace/sentiment-monitoring/douyin_localstorage.json', 'w') as f:
                        f.write(local_storage)
                    
                    print("[✓] Cookie和localStorage已保存")
                    break
                
                if (i+1) % 15 == 0:
                    print(f"  ...等待中 ({i+1}/90秒)")
            
            if not logged_in:
                print("[✗] 登录超时")
                browser.close()
                return []
        else:
            print("[✓] 已登录状态")
        
        # 等待搜索结果加载
        print("[→] 等待搜索结果加载...")
        time.sleep(8)
        
        # 滚动加载更多
        print("[→] 滚动加载更多...")
        for i in range(5):
            page.evaluate('window.scrollBy(0, 1000)')
            time.sleep(2)
        
        time.sleep(3)
        
        # 获取最终HTML
        html = page.content()
        print(f"[✓] 页面HTML大小: {len(html)} 字符")
        
        # 保存HTML用于调试
        with open('/Users/zhijian/workspace/sentiment-monitoring/douyin_search_final.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("[✓] HTML已保存到 douyin_search_final.html")
        
        # 解析视频数据
        videos = parse_douyin_videos(page, html, max_results)
        
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

def parse_douyin_videos(page, html, max_results=15):
    """解析抖音搜索页面视频"""
    
    videos = []
    
    # 方式1: Playwright选择器提取
    print("[→] 方式1: 通过选择器提取...")
    
    # 尝试多种选择器
    selectors = [
        '[data-e2e="search-card-video"]',
        '[class*="search-card"]',
        '[class*="video-card"]',
        'div[class*="card"]',
        'a[href*="/video/"]',
    ]
    
    for selector in selectors:
        elements = page.query_selector_all(selector)
        print(f"  选择器 '{selector}': {len(elements)} 个元素")
        
        for elem in elements[:max_results]:
            try:
                # 获取元素文本
                text = elem.inner_text()
                if text and len(text) > 10:
                    # 清理文本
                    lines = [l.strip() for l in text.split('\n') if l.strip()]
                    if lines:
                        title = lines[0][:100]
                        videos.append({
                            'title': title,
                            'full_text': '\n'.join(lines[:5]),
                            'selector': selector
                        })
            except:
                continue
        
        if videos:
            break
    
    # 方式2: 从HTML中提取所有可见文本
    if not videos:
        print("[→] 方式2: 从HTML提取文本...")
        
        # 提取所有div/span中的文本
        text_pattern = r'<(?:div|span|p|h[1-6])[^\u003e]*>([^\u003c]{20,200})</'
        texts = re.findall(text_pattern, html)
        
        seen = set()
        for text in texts:
            clean = re.sub(r'\s+', ' ', text).strip()
            if clean and len(clean) > 15 and clean not in seen:
                seen.add(clean)
                if '白冰' in clean or '偷税' in clean or '网红' in clean or '探店' in clean:
                    videos.append({'title': clean})
            
            if len(videos) >= max_results:
                break
    
    # 去重
    unique_videos = []
    seen_titles = set()
    for v in videos:
        title = v.get('title', '')
        if title and title not in seen_titles:
            seen_titles.add(title)
            unique_videos.append(v)
    
    print(f"[✓] 提取 {len(unique_videos)} 条视频")
    return unique_videos[:max_results]

if __name__ == '__main__':
    import sys
    keyword = sys.argv[1] if len(sys.argv) > 1 else "网红白冰偷税"
    results = douyin_search_direct(keyword)
    
    print(f"\n{'='*60}")
    print(f"🎵 抖音搜索结果 - {len(results)} 条")
    print(f"{'='*60}")
    
    for i, video in enumerate(results[:15], 1):
        print(f"\n[{i}] {video.get('title', '')[:80]}...")
        if video.get('full_text'):
            print(f"    {video['full_text'][:150]}...")

