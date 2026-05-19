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
        
        # 注入拦截脚本
        script = """
(() => {
    if (!window.__xhsCapturedData) {
        window.__xhsCapturedData = { feeds: [], comments: [], subComments: [] };
    }
    
    const originalFetch = window.fetch;
    window.fetch = async function(url, options) {
        const response = await originalFetch.apply(window, arguments);
        if (url && url.includes('/api/sns/web/')) {
            const clone = response.clone();
            clone.text().then(text => {
                try {
                    const data = JSON.parse(text);
                    if (url.includes('feed')) {
                        window.__xhsCapturedData.feeds.push({url, data});
                        console.log('[XHS-Capture] Feed:', url);
                    } else if (url.includes('comment')) {
                        window.__xhsCapturedData.comments.push({url, data});
                        console.log('[XHS-Capture] Comments:', url);
                    }
                } catch(e) {}
            });
        }
        return response;
    };
    console.log('[XHS-Capture] Script injected');
})();
"""
        await page.evaluate(script)
        print('✓ 拦截脚本已注入')
        
        # 显示提示
        await page.evaluate("""
            () => {
                const div = document.createElement('div');
                div.id = 'crawler-hint';
                div.style.cssText = `
                    position: fixed; top: 20px; left: 50%; transform: translateX(-50%);
                    background: linear-gradient(135deg, #ff2442, #ff5c7f); color: white;
                    padding: 20px 40px; border-radius: 12px; font-size: 18px;
                    font-weight: bold; z-index: 99999; text-align: center;
                `;
                div.innerHTML = `
                    <div style="font-size: 24px; margin-bottom: 8px;">🔴 测试模式</div>
                    <div>请点击任意帖子，我会捕获API数据</div>
                    <div style="font-size: 14px; margin-top: 8px;">超时: 60秒</div>
                `;
                document.body.appendChild(div);
            }
        """)
        print('✓ 提示已显示，请在浏览器中点击帖子...')
        
        # 等待60秒，轮询捕获的数据
        for i in range(60):
            await asyncio.sleep(1)
            
            data = await page.evaluate("""
                () => {
                    const d = window.__xhsCapturedData || {feeds: [], comments: []};
                    return {
                        feeds: d.feeds.length,
                        comments: d.comments.length
                    };
                }
            """)
            
            if data['feeds'] > 0 or data['comments'] > 0:
                print(f'\n✓ 捕获到数据！Feeds: {data["feeds"]}, Comments: {data["comments"]}')
                
                # 获取详细数据
                feeds = await page.evaluate("""
                    () => {
                        return window.__xhsCapturedData.feeds.map(f => ({
                            url: f.url,
                            hasData: !!f.data,
                            keys: Object.keys(f.data || {})
                        }));
                    }
                """)
                
                for f in feeds:
                    print(f'  Feed URL: {f["url"][:80]}...')
                    print(f'  Keys: {f["keys"]}')
                
                break
            
            if i % 10 == 0:
                print(f'  等待中... {60-i}秒剩余')
        
        # 移除提示
        await page.evaluate('() => { const d = document.getElementById("crawler-hint"); if(d) d.remove(); }')
        
        await browser.close()
        print('\n✓ 测试完成')

asyncio.run(test())
