#!/usr/bin/env python3
"""头条有头浏览器登录测试 - 60秒等待用户操作"""

from playwright.sync_api import sync_playwright
import json
import time
import os

COOKIE_FILE = "/Users/zhijian/workspace/sentiment-monitoring/toutiao_cookies.json"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=['--start-maximized']
        )
        context = browser.new_context(
            viewport={'width': 1280, 'height': 900},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        page = context.new_page()
        
        print('[→] 打开头条搜索页面...')
        page.goto('https://so.toutiao.com/search/?dvpf=pc&keyword=test', wait_until='domcontentloaded')
        
        print('\n' + '='*60)
        print('浏览器窗口已弹出！')
        print('如果有验证码，请完成验证。')
        print('如果需要登录，请完成登录。')
        print('你有60秒时间...')
        print('='*60 + '\n')
        
        time.sleep(60)
        
        # 保存cookie
        cookies = context.cookies()
        with open(COOKIE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)
        
        print(f'[✓] Cookie已保存: {COOKIE_FILE} ({len(cookies)} 个)')
        
        # 测试搜索
        print('\n[→] 测试搜索: 网红白冰偷税')
        page.goto('https://so.toutiao.com/search/?dvpf=pc&keyword=%E7%BD%91%E7%BA%A2%E7%99%BD%E5%86%B0%E5%81%B7%E7%A8%8E', wait_until='domcontentloaded')
        time.sleep(5)
        
        # 检查是否有验证码
        iframe = page.query_selector('iframe[src*="verifycenter"]')
        if iframe:
            print('[✗] 仍有验证码！')
        else:
            print('[✓] 页面正常！')
            # 截图
            page.screenshot(path='/Users/zhijian/workspace/sentiment-monitoring/toutiao_test.png', full_page=True)
            print('[✓] 截图已保存')
        
        print('\n30秒后关闭浏览器...')
        time.sleep(30)
        browser.close()

if __name__ == '__main__':
    main()
