#!/usr/bin/env python3
"""小红书搜索 - 使用已保存的cookie"""

from playwright.sync_api import sync_playwright
import json
import time
import os
import re

COOKIE_FILE = "/Users/zhijian/workspace/sentiment-monitoring/xiaohongshu_cookies.json"
OUTPUT_DIR = "/Users/zhijian/workspace/sentiment-monitoring/output"

def xiaohongshu_search(keyword, max_results=15):
    """小红书搜索 - 有头浏览器+cookie"""
    
    print(f"[→] 小红书搜索: {keyword}")
    
    import urllib.parse
    encoded_keyword = urllib.parse.quote(keyword)
    
    with sync_playwright() as p:
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
        url = f'https://www.xiaohongshu.com/search_result?keyword={encoded_keyword}'
        page.goto(url, wait_until='domcontentloaded')
        
        print("[→] 等待页面加载...")
        time.sleep(8)
        
        # 检查是否需要登录
        html = page.content()
        
        if '登录' in html and len(html) < 300000:
            print("\n" + "="*60)
            print("[!] 小红书需要登录")
            print("请在弹出窗口中完成扫码登录")
            print("等待90秒...")
            print("="*60 + "\n")
            
            logged_in = False
            for i in range(90):
                time.sleep(1)
                html = page.content()
                if '登录' not in html and len(html) > 300000:
                    print(f"[✓] 登录成功！（{i+1}秒）")
                    logged_in = True
                    
                    # 保存cookie
                    cookies = context.cookies()
                    with open(COOKIE_FILE, 'w', encoding='utf-8') as f:
                        json.dump(cookies, f, ensure_ascii=False, indent=2)
                    print("[✓] Cookie已保存")
                    break
                
                if (i+1) % 15 == 0:
                    print(f"  ...等待中 ({i+1}/90秒)")
            
            if not logged_in:
                print("[✗] 登录超时")
                browser.close()
                return []
        else:
            print("[✓] 已登录状态或页面正常")
        
        # 滚动加载
        print("[→] 滚动加载更多...")
        for i in range(3):
            page.evaluate('window.scrollBy(0, 800)')
            time.sleep(2)
        
        time.sleep(3)
        
        # 获取最终HTML
        html = page.content()
        print(f"[✓] 页面HTML: {len(html)} 字符")
        
        # 解析笔记
        notes = parse_xiaohongshu_html(page, html, max_results)
        
        # 保存结果
        if notes:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"xiaohongshu_{keyword}_{timestamp}.json"
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(notes, f, ensure_ascii=False, indent=2)
            
            print(f"[✓] 结果已保存: {filepath}")
        
        browser.close()
        return notes

def parse_xiaohongshu_html(page, html, max_results=15):
    """解析小红书搜索页面"""
    
    notes = []
    
    # 方式1: 通过常见class选择器
    selectors = [
        '[class*="note-item"]',
        '[class*="feed-item"]',
        '[class*="card"]',
        'a[href*="/explore/"]',
    ]
    
    for selector in selectors:
        elements = page.query_selector_all(selector)
        print(f"  选择器 '{selector}': {len(elements)} 个元素")
        
        for elem in elements[:max_results]:
            try:
                text = elem.inner_text()
                if text and len(text) > 10:
                    lines = [l.strip() for l in text.split('\n') if l.strip()]
                    if lines:
                        title = lines[0][:100]
                        notes.append({
                            'title': title,
                            'full_text': '\n'.join(lines[:5])
                        })
            except:
                continue
        
        if notes:
            break
    
    # 方式2: 从HTML提取文本
    if not notes:
        print("[→] 从HTML提取文本...")
        text_pattern = r'<(?:div|span|p)[^>]*>([^<]{20,200})</'
        texts = re.findall(text_pattern, html)
        
        seen = set()
        for text in texts:
            clean = re.sub(r'\s+', ' ', text).strip()
            if clean and len(clean) > 15 and clean not in seen:
                seen.add(clean)
                if any(kw in clean for kw in ['白冰', '偷税', '网红', '探店']):
                    notes.append({'title': clean})
            
            if len(notes) >= max_results:
                break
    
    # 去重
    unique = []
    seen_titles = set()
    for n in notes:
        title = n.get('title', '')
        if title and title not in seen_titles:
            seen_titles.add(title)
            unique.append(n)
    
    print(f"[✓] 提取 {len(unique)} 条笔记")
    return unique[:max_results]

if __name__ == '__main__':
    import sys
    keyword = sys.argv[1] if len(sys.argv) > 1 else "网红白冰偷税"
    results = xiaohongshu_search(keyword)
    
    print(f"\n{'='*60}")
    print(f"📕 小红书搜索结果 - {len(results)} 条")
    print(f"{'='*60}")
    
    for i, note in enumerate(results[:15], 1):
        print(f"\n[{i}] {note.get('title', '')[:80]}...")
        if note.get('full_text'):
            text = note['full_text'].replace('\n', ' | ')
            print(f"    {text[:150]}...")
