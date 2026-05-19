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
        
        print('✓ 搜索页已加载')
        print('请在浏览器中点击帖子...')
        
        # 等待弹层出现
        for i in range(60):
            await asyncio.sleep(1)
            
            # 检查弹层
            modal = await page.evaluate("""
                () => {
                    const mask = document.querySelector('.mask-paper');
                    const modal = document.querySelector('[class*="modal"]');
                    const drawer = document.querySelector('[class*="drawer"]');
                    
                    // 检查固定定位的大元素
                    const fixed = Array.from(document.querySelectorAll('*')).filter(el => {
                        const style = window.getComputedStyle(el);
                        return style.position === 'fixed' && 
                               el.offsetWidth > window.innerWidth * 0.5 &&
                               el.offsetHeight > window.innerHeight * 0.5 &&
                               el !== document.body;
                    });
                    
                    return {
                        hasMask: !!mask,
                        hasModal: !!modal,
                        hasDrawer: !!drawer,
                        fixedCount: fixed.length,
                        fixedClasses: fixed.slice(0, 3).map(f => f.className.substring(0, 50))
                    };
                }
            """)
            
            if modal['hasMask'] or modal['hasModal'] or modal['hasDrawer'] or modal['fixedCount'] > 0:
                print(f'\n✓ 检测到弹层！')
                print(f'  mask: {modal["hasMask"]}, modal: {modal["hasModal"]}, drawer: {modal["hasDrawer"]}')
                print(f'  fixed elements: {modal["fixedCount"]}')
                print(f'  classes: {modal["fixedClasses"]}')
                
                # 提取内容
                content = await page.evaluate("""
                    () => {
                        // 找到弹层容器
                        const container = document.querySelector('.mask-paper') || 
                                         document.querySelector('[class*="modal"]') ||
                                         document.querySelector('[class*="drawer"]') ||
                                         document.querySelector('[style*="position: fixed"]');
                        
                        if (!container) return null;
                        
                        // 提取所有文本
                        const allText = container.textContent;
                        
                        // 尝试找到内容区域
                        const contentArea = container.querySelector('.content, .detail, .note-content, [class*="content"]');
                        
                        return {
                            textLength: allText.length,
                            textPreview: allText.substring(0, 800),
                            contentLength: contentArea ? contentArea.textContent.length : 0,
                            contentPreview: contentArea ? contentArea.textContent.substring(0, 400) : ''
                        };
                    }
                """)
                
                if content:
                    print(f'\n  文本长度: {content["textLength"]}')
                    print(f'  内容预览:')
                    print(f'  {content["textPreview"][:500]}...')
                
                break
            
            if i % 10 == 0:
                print(f'  等待中... {60-i}秒剩余')
        
        print('\n✓ 完成')
        await browser.close()

asyncio.run(test())
