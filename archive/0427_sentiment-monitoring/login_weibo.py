#!/usr/bin/env python3
"""启动有头浏览器，让用户手动登录微博，然后保存cookie"""

import asyncio
import json
import sys
from playwright.async_api import async_playwright

COOKIE_FILE = "/Users/zhijian/workspace/sentiment-monitoring/weibo_cookies.json"

async def main():
    async with async_playwright() as p:
        # 启动有头浏览器（visible=True）
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        # 打开微博登录页
        print("正在打开微博登录页面...")
        await page.goto("https://weibo.com/login.php")
        
        print("\n" + "="*60)
        print("请在微博页面完成登录！")
        print("你有90秒时间完成登录...")
        print("="*60 + "\n")
        
        # 等待90秒让用户登录
        await asyncio.sleep(90)
        
        # 保存cookie
        cookies = await context.cookies()
        with open(COOKIE_FILE, "w", encoding="utf-8") as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)
        
        print(f"\nCookie已保存到: {COOKIE_FILE}")
        print(f"共保存 {len(cookies)} 个cookie")
        
        # 测试搜索
        print("\n测试搜索: 网红白冰偷税")
        await page.goto("https://s.weibo.com/weibo?q=网红白冰偷税")
        await page.wait_for_timeout(3000)
        
        # 截图保存
        await page.screenshot(path="/Users/zhijian/workspace/sentiment-monitoring/weibo_search_result.png")
        print("搜索结果已截图保存到 weibo_search_result.png")
        
        print("\n按回车键关闭浏览器...")
        await asyncio.sleep(30)
        
        await browser.close()
        print("浏览器已关闭")

if __name__ == "__main__":
    asyncio.run(main())
