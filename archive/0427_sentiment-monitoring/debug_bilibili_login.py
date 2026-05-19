#!/usr/bin/env python3
"""B站有头浏览器评论测试 - 需要登录"""

from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    # 有头浏览器
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(viewport={'width': 1280, 'height': 900})
    page = context.new_page()
    
    # 访问B站视频
    page.goto('https://www.bilibili.com/video/BV1faL3zBEmy', wait_until='networkidle')
    
    print("[→] 等待页面加载...")
    time.sleep(10)
    
    # 检查是否需要登录
    html = page.content()
    if '登录后' in html or '立即登录' in html:
        print("\n" + "="*60)
        print("[!] B站需要登录才能查看评论")
        print("请在弹出窗口中完成登录（扫码或账号密码）")
        print("等待60秒...")
        print("="*60 + "\n")
        
        for i in range(60):
            time.sleep(1)
            html = page.content()
            if '登录后' not in html:
                print(f"[✓] 登录成功！（{i+1}秒）")
                break
            if (i+1) % 10 == 0:
                print(f"  ...等待中 ({i+1}/60秒)")
    
    # 滚动到评论区
    print("[→] 滚动到评论区...")
    for i in range(10):
        page.evaluate('window.scrollBy(0, 1000)')
        time.sleep(2)
    
    # 保存HTML
    html = page.content()
    with open('/Users/zhijian/workspace/sentiment-monitoring/bilibili_comments_debug.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    # 截图
    page.screenshot(path='/Users/zhijian/workspace/sentiment-monitoring/bilibili_comments_debug.png', full_page=True)
    
    print(f"[✓] HTML已保存: {len(html)} 字符")
    
    # 检查评论
    import re
    comment_classes = re.findall(r'class="([^"]*(?:comment|reply)[^"]*)"', html)
    print(f"评论相关class: {len(comment_classes)}")
    
    browser.close()
