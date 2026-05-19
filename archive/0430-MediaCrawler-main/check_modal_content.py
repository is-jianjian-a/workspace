import asyncio
import sys
sys.path.insert(0, '.')

from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else await context.new_page()
        
        # 检查弹层内容
        content = await page.evaluate("""
            () => {
                // 查找弹层容器
                const mask = document.querySelector('.mask-paper');
                if (!mask) return { error: 'No mask-paper found' };
                
                // 获取弹层内的文本内容
                const text = mask.textContent;
                
                // 查找评论相关元素
                const comments = mask.querySelectorAll('[class*="comment"], [class*="reply"]');
                
                // 查找标题
                const title = mask.querySelector('h1, h2, h3, .title');
                
                // 查找内容
                const desc = mask.querySelector('.desc, .content, .detail');
                
                return {
                    textLength: text.length,
                    textPreview: text.substring(0, 500),
                    commentElements: comments.length,
                    hasTitle: !!title,
                    titleText: title ? title.textContent.substring(0, 100) : '',
                    hasDesc: !!desc,
                    descText: desc ? desc.textContent.substring(0, 200) : '',
                };
            }
        """)
        
        print('弹层内容分析：')
        print(f'  文本长度: {content.get("textLength", 0)}')
        print(f'  标题: {content.get("titleText", "N/A")}')
        print(f'  描述: {content.get("descText", "N/A")}')
        print(f'  评论元素数: {content.get("commentElements", 0)}')
        print(f'\n文本预览（前500字符）：')
        print(content.get('textPreview', 'N/A')[:500])
        
        await browser.close()

asyncio.run(test())
