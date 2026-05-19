#!/usr/bin/env python3
"""抖音搜索测试 - 等待动态加载完成"""

from playwright.sync_api import sync_playwright
import json
import time
import os

COOKIE_FILE = "/Users/zhijian/workspace/sentiment-monitoring/douyin_cookies.json"

def test_douyin_search():
    """用无头浏览器+Cookie测试抖音搜索，等待动态加载"""
    
    print("[→] 抖音搜索测试（等待动态加载）...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1280, 'height': 900}
        )
        
        # 加载cookie
        if os.path.exists(COOKIE_FILE):
            with open(COOKIE_FILE, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            context.add_cookies(cookies)
            print("[✓] 已加载抖音cookie")
        
        page = context.new_page()
        
        # 访问搜索页
        page.goto('https://www.douyin.com/search/%E7%BD%91%E7%BA%A2%E7%99%BD%E5%86%B0%E5%81%B7%E7%A8%8E', wait_until='networkidle')
        
        # 等待动态内容加载
        print("[→] 等待页面加载...")
        time.sleep(10)
        
        # 尝试滚动触发加载
        print("[→] 滚动页面触发加载...")
        for i in range(5):
            page.evaluate('window.scrollBy(0, 800)')
            time.sleep(2)
        
        # 再等一下
        time.sleep(5)
        
        html = page.content()
        print(f"[✓] 页面HTML大小: {len(html)} 字符")
        
        # 检查是否有登录提示
        if '登录后即可搜索' in html:
            print("[✗] 仍需登录！Cookie可能已过期")
            browser.close()
            return []
        
        # 保存HTML
        with open('/Users/zhijian/workspace/sentiment-monitoring/douyin_search_full.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("[✓] HTML已保存")
        
        # 截图
        page.screenshot(path='/Users/zhijian/workspace/sentiment-monitoring/douyin_search_full.png')
        print("[✓] 截图已保存")
        
        browser.close()
        return html

if __name__ == '__main__':
    test_douyin_search()
