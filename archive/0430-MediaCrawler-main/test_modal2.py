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
        for i in range(120):
            await asyncio.sleep(1)
            
            # 检查弹层
            modal = await page.evaluate("""
                () => {
                    const mask = document.querySelector('.mask-paper');
                    return {
                        hasMask: !!mask,
                        textLength: mask ? mask.textContent.length : 0,
                        htmlPreview: mask ? mask.outerHTML.substring(0, 1000) : ''
                    };
                }
            """)
            
            if modal['hasMask'] and modal['textLength'] > 100:
                print(f'\n✓ 弹层已加载！')
                print(f'  文本长度: {modal["textLength"]}')
                print(f'  HTML preview: {modal["htmlPreview"][:500]}...')
                
                # 详细分析弹层结构
                detail = await page.evaluate("""
                    () => {
                        const mask = document.querySelector('.mask-paper');
                        if (!mask) return null;
                        
                        // 获取所有子元素
                        const children = Array.from(mask.children);
                        
                        return {
                            childCount: children.length,
                            childrenInfo: children.map(c => ({
                                tag: c.tagName,
                                class: c.className.substring(0, 80),
                                width: c.offsetWidth,
                                height: c.offsetHeight,
                                textLength: c.textContent.length
                            })),
                            fullText: mask.textContent.substring(0, 2000)
                        };
                    }
                """)
                
                print(f'\n  子元素数: {detail["childCount"]}')
                for c in detail['childrenInfo']:
                    print(f'    {c["tag"]}.{c["class"]} size={c["width"]}x{c["height"]} text={c["textLength"]}')
                
                print(f'\n  完整文本（前2000字符）:')
                print(detail['fullText'])
                
                break
            elif modal['hasMask']:
                if i % 5 == 0:
                    print(f'  弹层出现但内容加载中... textLength={modal["textLength"]}')
            
            if i % 10 == 0 and not modal['hasMask']:
                print(f'  等待弹层... {120-i}秒剩余')
        
        print('\n✓ 完成')
        await browser.close()

asyncio.run(test())
