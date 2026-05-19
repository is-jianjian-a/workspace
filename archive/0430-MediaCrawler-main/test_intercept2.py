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
        
        # 注入脚本：捕获所有xiaohongshu API的响应
        script = """
(() => {
    window.__xhsCapturedData = { feeds: [], comments: [], allApis: [] };
    
    const originalFetch = window.fetch;
    window.fetch = async function(url, options) {
        const response = await originalFetch.apply(window, arguments);
        
        if (url && url.includes('xiaohongshu.com/api/')) {
            const clone = response.clone();
            clone.text().then(text => {
                try {
                    const data = JSON.parse(text);
                    window.__xhsCapturedData.allApis.push({
                        type: 'fetch', 
                        url: url, 
                        time: Date.now(),
                        hasData: !!data.data,
                        keys: Object.keys(data)
                    });
                    
                    // 分类存储
                    if (url.includes('/feed')) {
                        window.__xhsCapturedData.feeds.push({url, data});
                        console.log('[XHS-Capture] Feed:', url);
                    } else if (url.includes('comment')) {
                        window.__xhsCapturedData.comments.push({url, data});
                        console.log('[XHS-Capture] Comment:', url);
                    }
                } catch(e) {
                    window.__xhsCapturedData.allApis.push({
                        type: 'fetch', 
                        url: url, 
                        time: Date.now(),
                        error: e.message
                    });
                }
            });
        }
        return response;
    };
    
    // 也拦截XHR
    const originalXHR = window.XMLHttpRequest.prototype.open;
    const originalXHRSend = window.XMLHttpRequest.prototype.send;
    
    window.XMLHttpRequest.prototype.open = function(method, url) {
        this._url = url;
        return originalXHR.apply(this, arguments);
    };
    
    window.XMLHttpRequest.prototype.send = function() {
        const self = this;
        const url = this._url;
        
        if (url && url.includes('xiaohongshu.com/api/')) {
            const onReady = function() {
                if (self.readyState === 4) {
                    try {
                        const data = JSON.parse(self.responseText);
                        window.__xhsCapturedData.allApis.push({
                            type: 'xhr', 
                            url: url, 
                            time: Date.now(),
                            hasData: !!data.data
                        });
                    } catch(e) {}
                }
            };
            self.addEventListener('readystatechange', onReady);
        }
        return originalXHRSend.apply(this, arguments);
    };
    
    console.log('[XHS-Capture] All API interception active');
})();
"""
        await page.evaluate(script)
        print('✓ 拦截脚本已注入')
        print('✓ 请在浏览器中点击帖子...')
        
        # 等待30秒
        for i in range(30):
            await asyncio.sleep(1)
            
            data = await page.evaluate("""
                () => {
                    return {
                        apis: window.__xhsCapturedData.allApis.slice(-10),
                        feeds: window.__xhsCapturedData.feeds.length,
                        comments: window.__xhsCapturedData.comments.length
                    };
                }
            """)
            
            if data['feeds'] > 0 or data['comments'] > 0:
                print(f'\n✓ 捕获到数据！Feeds: {data["feeds"]}, Comments: {data["comments"]}')
                
                # 获取feed详情
                feeds = await page.evaluate("""
                    () => {
                        return window.__xhsCapturedData.feeds.map(f => ({
                            url: f.url,
                            hasData: !!f.data,
                            keys: Object.keys(f.data || {}),
                            dataKeys: f.data && f.data.data ? Object.keys(f.data.data) : []
                        }));
                    }
                """)
                
                for f in feeds:
                    print(f'\n  Feed URL: {f["url"][:100]}...')
                    print(f'  Response keys: {f["keys"]}')
                    if f['dataKeys']:
                        print(f'  data.keys: {f["dataKeys"]}')
                
                break
            
            # 显示API活动
            if data['apis']:
                print(f'\n  API活动 ({len(data["apis"])}个请求):')
                for api in data['apis'][-3:]:
                    print(f'    {api["type"]}: {api["url"][:80]}...')
        
        print('\n✓ 完成')
        await browser.close()

asyncio.run(test())
