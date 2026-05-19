import asyncio
import sys
sys.path.insert(0, '.')

from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else await context.new_page()
        
        print(f'当前URL: {page.url}')
        
        # 检查页面中是否有帖子详情特征
        features = await page.evaluate("""
            () => {
                return {
                    // 检查是否有评论输入框
                    hasCommentInput: !!document.querySelector('input[placeholder*="评论"], textarea[placeholder*="评论"]'),
                    
                    // 检查是否有"评论"文字
                    commentText: Array.from(document.querySelectorAll('*')).filter(el => el.textContent.includes('评论')).length,
                    
                    // 检查是否有"点赞"按钮
                    likeText: Array.from(document.querySelectorAll('*')).filter(el => el.textContent.includes('点赞')).length,
                    
                    // 检查是否有大量文本内容（帖子详情）
                    longText: Array.from(document.querySelectorAll('p, div, span')).filter(el => el.textContent.length > 200).length,
                    
                    // 检查是否有图片网格
                    imageGrid: document.querySelectorAll('img').length,
                    
                    // 页面总文本长度
                    totalText: document.body.textContent.length
                };
            }
        """)
        
        print(f'\n页面特征：')
        print(f'  评论输入框: {features["hasCommentInput"]}')
        print(f'  "评论"出现次数: {features["commentText"]}')
        print(f'  "点赞"出现次数: {features["likeText"]}')
        print(f'  长文本元素: {features["longText"]}')
        print(f'  图片数: {features["imageGrid"]}')
        print(f'  总文本长度: {features["totalText"]}')
        
        # 获取页面文本预览
        text_preview = await page.evaluate("""
            () => document.body.textContent.substring(0, 1000)
        """)
        print(f'\n文本预览（前1000字符）：')
        print(text_preview)
        
        await browser.close()

asyncio.run(test())
