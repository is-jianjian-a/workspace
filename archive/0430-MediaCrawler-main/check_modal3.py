import asyncio
import sys
sys.path.insert(0, '.')

from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else await context.new_page()
        
        # 检查所有z-index > 100的元素
        high_z = await page.evaluate("""
            () => {
                const all = document.querySelectorAll('*');
                return Array.from(all).map(el => ({
                    tag: el.tagName,
                    class: (el.className && typeof el.className === 'string') ? el.className.substring(0, 80) : '',
                    id: el.id,
                    zIndex: window.getComputedStyle(el).zIndex,
                    width: el.offsetWidth,
                    height: el.offsetHeight,
                    textPreview: el.textContent.substring(0, 100)
                })).filter(s => s.zIndex !== 'auto' && parseInt(s.zIndex) > 100)
                  .sort((a, b) => parseInt(b.zIndex) - parseInt(a.zIndex));
            }
        """)
        
        print('z-index > 100 的元素：')
        for h in high_z[:20]:
            print(f'  zIndex={h["zIndex"]} {h["tag"]}.{h["class"]} size={h["width"]}x{h["height"]}')
            print(f'    text: {h["textPreview"]}')
        
        await browser.close()

asyncio.run(test())
