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
        
        print('请在浏览器中点击帖子...')
        
        # 监听DOM变化
        for i in range(60):
            await asyncio.sleep(1)
            
            # 检查是否有弹层/模态框
            modal_info = await page.evaluate("""
                () => {
                    const modals = document.querySelectorAll(
                        '[class*="modal"], [class*="overlay"], [class*="mask"], ' +
                        '[class*="drawer"], [class*="popup"], [class*="detail"], ' +
                        '[class*="note-detail"], [class*="slide"], [role="dialog"]'
                    );
                    
                    const largeContainers = Array.from(document.querySelectorAll('div')).filter(
                        div => div.offsetWidth > window.innerWidth * 0.5 && 
                               div.offsetHeight > window.innerHeight * 0.5 &&
                               div !== document.body
                    );
                    
                    return {
                        modals: modals.length,
                        modalClasses: Array.from(modals).slice(0, 3).map(m => m.className.substring(0, 50)),
                        largeContainers: largeContainers.length,
                        bodyChildren: document.body.children.length
                    };
                }
            """)
            
            if modal_info['modals'] > 0 or modal_info['largeContainers'] > 0:
                print(f'\n✓ 检测到弹层/容器变化！')
                print(f'  Modals: {modal_info["modals"]}')
                print(f'  Modal classes: {modal_info["modalClasses"]}')
                print(f'  Large containers: {modal_info["largeContainers"]}')
                print(f'  Body children: {modal_info["bodyChildren"]}')
                
                # 获取z-index较高的元素
                structure = await page.evaluate("""
                    () => {
                        const all = document.querySelectorAll('*');
                        return Array.from(all).slice(-30).map(el => ({
                            tag: el.tagName,
                            class: el.className?.substring(0, 50),
                            id: el.id,
                            zIndex: window.getComputedStyle(el).zIndex
                        })).filter(s => s.zIndex !== 'auto' && parseInt(s.zIndex) > 10);
                    }
                """)
                for s in structure:
                    print(f'    {s["tag"]}.{s["class"]} zIndex={s["zIndex"]}')
                
                break
            
            if i % 10 == 0:
                print(f'  等待中... {60-i}秒剩余')
        
        print('\n✓ 完成')
        await browser.close()

asyncio.run(test())
