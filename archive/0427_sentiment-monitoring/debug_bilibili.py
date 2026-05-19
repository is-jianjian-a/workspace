#!/usr/bin/env python3
"""B站页面调试 - 检查评论区域HTML结构"""

from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width': 1280, 'height': 900})
    page = context.new_page()
    
    page.goto('https://www.bilibili.com/video/BV1faL3zBEmy', wait_until='networkidle')
    time.sleep(10)
    
    # 保存HTML
    html = page.content()
    with open('/Users/zhijian/workspace/sentiment-monitoring/bilibili_debug.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    # 截图
    page.screenshot(path='/Users/zhijian/workspace/sentiment-monitoring/bilibili_debug.png', full_page=True)
    
    print(f"HTML大小: {len(html)} 字符")
    
    # 检查页面文本
    text = page.inner_text('body')
    print(f"\n页面文本（前1000字符）:")
    print(text[:1000])
    
    browser.close()
