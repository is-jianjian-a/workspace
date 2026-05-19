#!/usr/bin/env python3
"""抖音有头浏览器登录脚本 - 60秒等待用户扫码/登录"""

from playwright.sync_api import sync_playwright
import json
import time
import os

COOKIE_FILE = "/Users/zhijian/workspace/sentiment-monitoring/douyin_cookies.json"

def login_douyin():
    """弹出浏览器让用户登录抖音，保存cookie供后续无头使用"""
    
    print("[→] 打开抖音搜索页面...")
    
    with sync_playwright() as p:
        # 有头浏览器（可见窗口）
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': 1280, 'height': 900}
        )
        page = context.new_page()
        
        # 访问抖音搜索页
        page.goto('https://www.douyin.com/search/%E7%BD%91%E7%BA%A2%E7%99%BD%E5%86%B0%E5%81%B7%E7%A8%8E', wait_until='domcontentloaded')
        
        print("\n" + "="*60)
        print("浏览器窗口已弹出！")
        print("抖音需要扫码或手机验证码登录。")
        print("请完成登录，等待页面加载出搜索结果...")
        print("你有120秒时间...")
        print("="*60 + "\n")
        
        # 循环检测登录状态，最多120秒
        logged_in = False
        for i in range(120):
            time.sleep(1)
            html = page.content()
            
            # 检测是否已登录（出现搜索结果或没有登录提示）
            if '登录后即可搜索' not in html and ('搜索结果' in html or '视频' in html or '用户' in html):
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
        print("[→] 测试搜索: 网红白冰偷税")
        time.sleep(3)
        html = page.content()
        
        # 检查是否还有登录提示
        if '登录后即可搜索' in html:
            print("[✗] 仍需登录！请重新运行脚本并完成登录")
        elif logged_in:
            print("[✓] 页面正常！")
            # 截图
            page.screenshot(path='/Users/zhijian/workspace/sentiment-monitoring/douyin_test.png')
            print("[✓] 截图已保存")
            
            # 保存HTML用于分析
            with open('/Users/zhijian/workspace/sentiment-monitoring/douyin_search_html.html', 'w') as f:
                f.write(html)
            print("[✓] HTML已保存")
        else:
            print("[!] 超时，不确定登录状态")
        
        print("\n10秒后关闭浏览器...")
        time.sleep(10)
        browser.close()

if __name__ == '__main__':
    login_douyin()
