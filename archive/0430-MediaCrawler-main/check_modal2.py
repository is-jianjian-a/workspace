import asyncio
import sys
sys.path.insert(0, '.')

from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else await context.new_page()
        
        # 检查body下的所有直接子元素
        structure = await page.evaluate("""
            () => {
                const children = Array.from(document.body.children);
                return children.map((child, i) => ({
                    index: i,
                    tag: child.tagName,
                    class: child.className?.substring(0, 100) || '',
                    id: child.id,
                    width: child.offsetWidth,
                    height: child.offsetHeight,
                    textLength: child.textContent.length
                }));
            }
        """)
        
        print('Body直接子元素：')
        for s in structure:
            print(f'  [{s["index"]}] {s["tag"]}.{s["class"]} id={s["id"]} size={s["width"]}x{s["height"]} text={s["textLength"]}')
        
        # 找到最大的非body容器
        largest = await page.evaluate("""
            () => {
                const divs = Array.from(document.querySelectorAll('div'));
                const sorted = divs
                    .filter(d => d !== document.body)
                    .map(d => ({
                        class: d.className?.substring(0, 50) || '',
                        width: d.offsetWidth,
                        height: d.offsetHeight,
                        textLength: d.textContent.length,
                        zIndex: window.getComputedStyle(d).zIndex
                    }))
                    .filter(d => d.width > 100 && d.height > 100)
                    .sort((a, b) => (b.width * b.height) - (a.width * a.height));
                return sorted.slice(0, 10);
            }
        """)
        
        print('\n最大的10个容器：')
        for l in largest:
            print(f'  {l["class"]} size={l["width"]}x{l["height"]} text={l["textLength"]} zIndex={l["zIndex"]}')
        
        await browser.close()

asyncio.run(test())
