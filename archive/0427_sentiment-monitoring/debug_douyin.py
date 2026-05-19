#!/usr/bin/env python3
"""抖音页面调试 - 保存完整HTML分析"""

from playwright.sync_api import sync_playwright
import json
import time
import os

COOKIE_FILE = "/Users/zhijian/workspace/sentiment-monitoring/douyin_cookies.json"

def debug_douyin():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1280, 'height': 900})
        
        if os.path.exists(COOKIE_FILE):
            with open(COOKIE_FILE, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            context.add_cookies(cookies)
            print("[✓] Cookie已加载")
        
        page = context.new_page()
        page.goto('https://www.douyin.com/search/%E7%BD%91%E7%BA%A2%E7%99%BD%E5%86%B0%E5%81%B7%E7%A8%8E', wait_until='domcontentloaded')
        
        print("[→] 等待10秒...")
        time.sleep(10)
        
        # 保存HTML
        html = page.content()
        with open('/Users/zhijian/workspace/sentiment-monitoring/douyin_debug.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"[✓] HTML已保存: {len(html)} 字符")
        
        # 截图
        page.screenshot(path='/Users/zhijian/workspace/sentiment-monitoring/douyin_debug.png', full_page=True)
        print("[✓] 截图已保存")
        
        # 检查页面文本
        text = page.inner_text('body')
        print(f"\n页面文本（前1000字符）:")
        print(text[:1000])
        
        # 查找视频卡片
        cards = page.query_selector_all('[data-e2e="search-card-video"]')
        print(f"\n找到 {len(cards)} 个视频卡片")
        
        browser.close()

if __name__ == '__main__':
    debug_douyin()
