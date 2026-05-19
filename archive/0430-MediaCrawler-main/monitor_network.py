import asyncio
from playwright.async_api import async_playwright

async def monitor():
    async with async_playwright() as p:
        # 连接到你的 Chrome
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        
        # 获取现有页面或创建新页面
        contexts = browser.contexts
        if contexts:
            context = contexts[0]
            pages = context.pages
            if pages:
                page = pages[0]
            else:
                page = await context.new_page()
        else:
            context = await browser.new_context()
            page = await context.new_page()
        
        print(f"Connected to page: {page.url}")
        
        # 监听所有网络请求
        def handle_request(request):
            url = request.url
            if 'xiaohongshu.com' in url and ('explore' in url or 'note' in url or 'comment' in url):
                print(f"\n[REQUEST] {request.method} {url[:120]}")
                print(f"  Headers: {dict(request.headers)}")
        
        def handle_response(response):
            url = response.url
            if 'xiaohongshu.com' in url and ('explore' in url or 'note' in url or 'comment' in url):
                print(f"\n[RESPONSE] {response.status} {url[:120]}")
        
        page.on("request", handle_request)
        page.on("response", handle_response)
        
        print("\n=== Network monitoring started ===")
        print("Please click on a XiaoHongShu note now...")
        print("Press Ctrl+C to stop\n")
        
        # 保持运行
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(monitor())
