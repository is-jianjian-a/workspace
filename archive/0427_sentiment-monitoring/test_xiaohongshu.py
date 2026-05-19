#!/usr/bin/env python3
"""小红书有头浏览器搜索测试"""

from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    # 有头浏览器
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        viewport={'width': 1280, 'height': 900}
    )
    page = context.new_page()
    
    # 访问小红书搜索
    print("[→] 访问小红书搜索...")
    page.goto('https://www.xiaohongshu.com/search_result?keyword=网红白冰偷税', wait_until='domcontentloaded')
    
    print("[→] 等待10秒...")
    time.sleep(10)
    
    # 检查页面状态
    title = page.title()
    print(f"[✓] 页面标题: {title}")
    
    # 保存截图和HTML
    page.screenshot(path='/Users/zhijian/workspace/sentiment-monitoring/xiaohongshu_test.png')
    html = page.content()
    with open('/Users/zhijian/workspace/sentiment-monitoring/xiaohongshu_test.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"[✓] HTML大小: {len(html)} 字符")
    
    # 检查是否有登录提示或限制
    if '安全限制' in html or 'IP存在风险' in html:
        print("[✗] 小红书IP限制！")
    elif '登录' in html:
        print("[!] 需要登录")
    else:
        print("[✓] 页面正常")
    
    browser.close()
