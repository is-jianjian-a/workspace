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
        
        initial_url = page.url
        print(f'初始URL: {initial_url}')
        print('请在浏览器中点击帖子...')
        
        # 持续监控URL变化
        for i in range(60):
            await asyncio.sleep(0.5)
            
            current = page.url
            if current != initial_url:
                print(f'\n✓ URL变化！')
                print(f'  新URL: {current}')
                
                # 等待页面加载
                await asyncio.sleep(3)
                
                # 检查页面内容
                info = await page.evaluate("""
                    () => {
                        return {
                            title: document.title,
                            textLength: document.body.textContent.length,
                            hasCommentInput: !!document.querySelector('input[placeholder*="评论"], textarea[placeholder*="评论"]'),
                            commentCount: document.querySelectorAll('[class*="comment"]').length,
                            imageCount: document.querySelectorAll('img').length
                        };
                    }
                """)
                
                print(f'  标题: {info["title"]}')
                print(f'  文本长度: {info["textLength"]}')
                print(f'  评论输入框: {info["hasCommentInput"]}')
                print(f'  评论元素: {info["commentCount"]}')
                print(f'  图片数: {info["imageCount"]}')
                
                # 获取文本预览
                preview = await page.evaluate("""
                    () => document.body.textContent.substring(0, 1000)
                """)
                print(f'\n  文本预览:')
                print(f'  {preview[:500]}...')
                
                break
            
            if i % 20 == 0:
                print(f'  监控中... {30-i//2}秒剩余')
        
        print('\n✓ 完成')
        await browser.close()

asyncio.run(test())
