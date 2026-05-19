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
        
        print('当前页面: 搜索结果页')
        
        # 注入弹层监控
        await page.evaluate("""
            () => {
                window.__modalCaptured = false;
                window.__modalHTML = '';
                
                const observer = new MutationObserver((mutations) => {
                    for (const mutation of mutations) {
                        for (const node of mutation.addedNodes) {
                            if (node.nodeType === 1) {
                                const el = node;
                                if (el.className && typeof el.className === 'string' && 
                                    (el.className.includes('mask') || el.className.includes('modal'))) {
                                    window.__modalCaptured = true;
                                    window.__modalHTML = el.outerHTML.substring(0, 3000);
                                    console.log('[AutoClick] Modal detected!', el.className);
                                }
                            }
                        }
                    }
                });
                
                observer.observe(document.body, { childList: true, subtree: true });
            }
        """)
        
        # 找到第一个帖子并点击
        print('正在点击第一个帖子...')
        clicked = await page.evaluate("""
            () => {
                const firstNote = document.querySelector('section.note-item a[href*="/explore/"]');
                if (firstNote) {
                    firstNote.click();
                    return true;
                }
                return false;
            }
        """)
        
        if not clicked:
            print('✗ 没有找到帖子')
            await browser.close()
            return
        
        print('✓ 已点击第一个帖子')
        
        # 等待弹层出现
        for i in range(10):
            await asyncio.sleep(1)
            
            modal_info = await page.evaluate("""
                () => {
                    return {
                        captured: window.__modalCaptured,
                        html: window.__modalHTML
                    };
                }
            """)
            
            if modal_info['captured']:
                print(f'\n✓ 弹层出现！')
                print(f'HTML preview: {modal_info["html"][:500]}...')
                break
            
            print(f'  等待弹层... {10-i}秒')
        
        # 检查页面URL是否变化
        print(f'\n当前URL: {page.url}')
        
        # 检查是否有新内容
        content = await page.evaluate("""
            () => {
                return {
                    bodyChildren: document.body.children.length,
                    textLength: document.body.textContent.length
                };
            }
        """)
        print(f'Body子元素: {content["bodyChildren"]}, 文本长度: {content["textLength"]}')
        
        await browser.close()

asyncio.run(test())
