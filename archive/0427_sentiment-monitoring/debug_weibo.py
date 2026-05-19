#!/usr/bin/env python3
"""微博页面调试 - 检查评论区域结构"""

from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(viewport={'width': 1280, 'height': 900})
    
    # 加载cookie
    import json
    import os
    if os.path.exists('weibo_cookies.json'):
        with open('weibo_cookies.json', 'r') as f:
            cookies = json.load(f)
        context.add_cookies(cookies)
        print("[✓] Cookie已加载")
    
    page = context.new_page()
    page.goto('https://weibo.com/1893867081/Po3nM0S6C', wait_until='networkidle')
    
    print("[→] 等待页面加载...")
    time.sleep(10)
    
    # 保存HTML和截图
    html = page.content()
    with open('/Users/zhijian/workspace/sentiment-monitoring/weibo_debug.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    page.screenshot(path='/Users/zhijian/workspace/sentiment-monitoring/weibo_debug.png', full_page=True)
    
    print(f"[✓] HTML已保存: {len(html)} 字符")
    
    # 检查页面文本
    text = page.inner_text('body')
    print(f"\n页面文本（前1500字符）:")
    print(text[:1500])
    
    browser.close()
