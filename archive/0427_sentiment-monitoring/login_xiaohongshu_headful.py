#!/usr/bin/env python3
"""小红书有头浏览器登录 - 60秒等待用户扫码"""

from playwright.sync_api import sync_playwright
import json
import time
import os

COOKIE_FILE = "/Users/zhijian/workspace/sentiment-monitoring/xiaohongshu_cookies.json"

def login_xiaohongshu():
    print("[→] 打开小红书搜索页面...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': 1280, 'height': 900}
        )
        page = context.new_page()
        
        # 访问小红书
        page.goto('https://www.xiaohongshu.com/search_result?keyword=网红白冰偷税', wait_until='domcontentloaded')
        
        print("\n" + "="*60)
        print("浏览器窗口已弹出！")
        print("小红书需要扫码或手机验证码登录。")
        print("请完成登录，等待页面加载出搜索结果...")
        print("你有120秒时间...")
        print("="*60 + "\n")
        
        # 循环检测登录状态
        logged_in = False
        for i in range(120):
            time.sleep(1)
            html = page.content()
            
            # 检测是否已登录（出现搜索结果）
            if '登录' not in html and len(html) > 200000:
                print(f"[✓] 检测到已登录！（{i+1}秒）")
                logged_in = True
                break
            
            # 每10秒提示一次
            if (i+1) % 10 == 0:
                print(f"  ...等待中 ({i+1}/120秒)")
        
        # 保存cookie
        cookies = context.cookies()
        with open(COOKIE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)
        
        print(f"[✓] Cookie已保存: {COOKIE_FILE} ({len(cookies)} 个)\n")
        
        # 测试搜索
        if logged_in:
            print("[→] 测试搜索: 网红白冰偷税")
            time.sleep(3)
            html = page.content()
            
            # 检查是否有搜索结果
            if '笔记' in html or '点赞' in html:
                print("[✓] 页面正常！有搜索结果")
                page.screenshot(path='/Users/zhijian/workspace/sentiment-monitoring/xiaohongshu_test.png')
                print("[✓] 截图已保存")
                
                # 保存HTML
                with open('/Users/zhijian/workspace/sentiment-monitoring/xiaohongshu_search_html.html', 'w', encoding='utf-8') as f:
                    f.write(html)
                print("[✓] HTML已保存")
            else:
                print("[!] 页面内容较少，可能没有搜索结果")
        else:
            print("[✗] 超时，可能未登录")
        
        print("\n10秒后关闭浏览器...")
        time.sleep(10)
        browser.close()

if __name__ == '__main__':
    login_xiaohongshu()
