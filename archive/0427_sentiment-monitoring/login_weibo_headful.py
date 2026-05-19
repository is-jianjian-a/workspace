#!/usr/bin/env python3
"""启动有头浏览器，让用户手动登录微博，然后保存cookie"""

from playwright.sync_api import sync_playwright
import json
import time
import sys

COOKIE_FILE = "/Users/zhijian/workspace/sentiment-monitoring/weibo_cookies.json"

def main():
    with sync_playwright() as p:
        # 启动有头浏览器 - 使用args参数确保窗口显示
        browser = p.chromium.launch(
            headless=False,
            args=['--start-maximized']
        )
        
        context = browser.new_context(
            viewport={'width': 1280, 'height': 900},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        page = context.new_page()
        
        print('正在打开微博登录页面...', flush=True)
        page.goto('https://weibo.com/login.php', wait_until='domcontentloaded')
        
        print('\n' + '='*60, flush=True)
        print('浏览器窗口应该已经弹出！', flush=True)
        print('如果没看到窗口，请检查Dock栏是否有Chrome图标。', flush=True)
        print('你有120秒时间完成微博登录...', flush=True)
        print('='*60 + '\n', flush=True)
        
        # 等待120秒让用户登录
        time.sleep(120)
        
        # 保存cookie
        cookies = context.cookies()
        with open(COOKIE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)
        
        print(f'\nCookie已保存到: {COOKIE_FILE}', flush=True)
        print(f'共保存 {len(cookies)} 个cookie', flush=True)
        
        # 测试搜索
        print('\n测试搜索: 网红白冰偷税', flush=True)
        page.goto('https://s.weibo.com/weibo?q=%E7%BD%91%E7%BA%A2%E7%99%BD%E5%86%B0%E5%81%B7%E7%A8%8E', wait_until='domcontentloaded')
        time.sleep(5)
        
        screenshot_path = '/Users/zhijian/workspace/sentiment-monitoring/weibo_search_result.png'
        page.screenshot(path=screenshot_path, full_page=True)
        print(f'搜索结果已截图保存到: {screenshot_path}', flush=True)
        
        # 获取页面内容
        content = page.content()
        with open('/Users/zhijian/workspace/sentiment-monitoring/weibo_search_html.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print('页面HTML已保存到 weibo_search_html.html', flush=True)
        
        # 再等待30秒让用户查看结果
        print('\n30秒后自动关闭浏览器...', flush=True)
        time.sleep(30)
        
        browser.close()
        print('浏览器已关闭', flush=True)

if __name__ == '__main__':
    main()
