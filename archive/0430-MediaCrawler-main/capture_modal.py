import asyncio
import sys
sys.path.insert(0, '.')

from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else await context.new_page()
        
        # 注入脚本：自动捕获弹层内容
        await page.evaluate("""
            () => {
                window.__xhsModalData = null;
                
                // 监听DOM变化
                const observer = new MutationObserver((mutations) => {
                    for (const mutation of mutations) {
                        for (const node of mutation.addedNodes) {
                            if (node.nodeType === 1) { // Element
                                const el = node;
                                // 检查是否是弹层
                                if (el.className && el.className.includes('mask')) {
                                    window.__xhsModalData = {
                                        className: el.className,
                                        html: el.outerHTML.substring(0, 2000),
                                        text: el.textContent.substring(0, 500)
                                    };
                                    console.log('[Modal] Captured!', el.className);
                                }
                            }
                        }
                    }
                });
                
                observer.observe(document.body, {
                    childList: true,
                    subtree: true
                });
                
                console.log('[Modal] Observer started');
            }
        """)
        
        print('✓ 弹层监控已启动')
        print('请在浏览器中点击帖子...')
        
        # 等待弹层出现
        for i in range(60):
            await asyncio.sleep(1)
            
            modal = await page.evaluate("""
                () => window.__xhsModalData
            """)
            
            if modal:
                print(f'\n✓ 弹层出现！')
                print(f'  Class: {modal["className"]}')
                print(f'  Text: {modal["text"]}')
                print(f'  HTML preview: {modal["html"][:500]}...')
                break
            
            if i % 10 == 0:
                print(f'  等待中... {60-i}秒剩余')
        
        print('\n✓ 完成')
        await browser.close()

asyncio.run(test())
