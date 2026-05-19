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
        
        # 记录初始URL
        initial_url = page.url
        print(f'初始URL: {initial_url}')
        
        # 监听URL变化
        async def watch_url():
            for i in range(60):
                current = page.url
                if current != initial_url:
                    print(f'\n✓ URL变化了！')
                    print(f'  新URL: {current}')
                    return True
                await asyncio.sleep(1)
            return False
        
        print('请在浏览器中点击帖子...')
        changed = await watch_url()
        
        if changed:
            # 检查页面内容
            title = await page.title()
            print(f'  页面标题: {title}')
            
            # 检查是否有帖子内容
            has_content = await page.evaluate("""
                () => {
                    const content = document.querySelector('.note-content, .content, .desc');
                    return content ? content.textContent.substring(0, 100) : 'No content found';
                }
            """)
            print(f'  内容: {has_content}')
        else:
            print('60秒内URL没有变化')
        
        await browser.close()

asyncio.run(test())
