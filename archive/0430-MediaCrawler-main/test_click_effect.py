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
        
        # 记录点击前的body子元素
        before = await page.evaluate("""
            () => {
                return Array.from(document.body.children).map(c => ({
                    tag: c.tagName,
                    class: c.className.substring(0, 50),
                    textLength: c.textContent.length
                }));
            }
        """)
        print('点击前Body子元素：')
        for b in before:
            print(f'  {b["tag"]}.{b["class"]} text={b["textLength"]}')
        
        print('\n请在浏览器中点击帖子...')
        
        # 等待变化
        for i in range(60):
            await asyncio.sleep(1)
            
            after = await page.evaluate("""
                () => {
                    return Array.from(document.body.children).map(c => ({
                        tag: c.tagName,
                        class: c.className.substring(0, 50),
                        textLength: c.textContent.length
                    }));
                }
            """)
            
            # 比较变化
            if len(after) != len(before):
                print(f'\n✓ Body子元素数量变化！{len(before)} -> {len(after)}')
                print('新增元素：')
                for a in after[len(before):]:
                    print(f'  {a["tag"]}.{a["class"]} text={a["textLength"]}')
                
                # 获取新增元素的HTML
                new_html = await page.evaluate("""
                    () => {
                        const children = Array.from(document.body.children);
                        const newChild = children[children.length - 1];
                        return newChild.outerHTML.substring(0, 2000);
                    }
                """)
                print(f'\n新增元素HTML预览：')
                print(new_html[:500])
                break
            
            # 检查是否有元素的文本长度大幅增加
            for j, a in enumerate(after):
                if j < len(before) and a['textLength'] > before[j]['textLength'] + 500:
                    print(f'\n✓ 元素[{j}]文本大幅增加！{before[j]["textLength"]} -> {a["textLength"]}')
                    print(f'  class: {a["class"]}')
                    break
            else:
                continue
            break
            
            if i % 10 == 0:
                print(f'  等待中... {60-i}秒剩余')
        
        print('\n✓ 完成')
        await browser.close()

asyncio.run(test())
