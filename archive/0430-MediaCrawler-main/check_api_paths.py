import asyncio
import sys
sys.path.insert(0, '.')

from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else await context.new_page()
        
        # 导航到搜索页
        await page.goto('https://www.xiaohongshu.com/search_result?keyword=哪吒2&type=51', wait_until='networkidle')
        await asyncio.sleep(3)
        
        # 注入脚本：记录所有API请求URL
        script = """
(() => {
    window.__allApiUrls = [];
    
    const originalFetch = window.fetch;
    window.fetch = async function(url, options) {
        if (url && url.includes('/api/')) {
            window.__allApiUrls.push({type: 'fetch', url: url, time: Date.now()});
            console.log('[API]', url);
        }
        return originalFetch.apply(window, arguments);
    };
    
    const originalXHR = window.XMLHttpRequest.prototype.open;
    window.XMLHttpRequest.prototype.open = function(method, url) {
        if (url && url.includes('/api/')) {
            window.__allApiUrls.push({type: 'xhr', url: url, time: Date.now()});
            console.log('[API-XHR]', url);
        }
        return originalXHR.apply(this, arguments);
    };
})();
"""
        await page.evaluate(script)
        print('✓ API监控脚本已注入')
        print('✓ 请在浏览器中点击帖子，我会记录所有API请求...')
        
        # 等待30秒
        for i in range(30):
            await asyncio.sleep(1)
            
            urls = await page.evaluate("""
                () => {
                    return window.__allApiUrls.slice(-5);
                }
            """)
            
            if urls:
                print(f'\n  最近API请求 ({len(urls)}个):')
                for u in urls:
                    print(f'    {u["type"]}: {u["url"][:100]}...')
        
        print('\n✓ 完成')
        await browser.close()

asyncio.run(test())
