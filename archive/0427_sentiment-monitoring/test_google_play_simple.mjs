import gplay from 'google-play-scraper';

async function test() {
    console.log('=== 测试 Google Play Scraper ===');
    
    try {
        console.log('1. 搜索微信...');
        const results = await gplay.search({ term: '微信', num: 3 });
        console.log(`找到 ${results.length} 个结果`);
        
        if (results.length > 0) {
            const app = results[0];
            console.log(`应用: ${app.title} (${app.appId})`);
            
            console.log('\n2. 获取评论...');
            const reviews = await gplay.reviews({
                appId: app.appId,
                num: 10
            });
            console.log(`获取到 ${reviews.data.length} 条评论`);
            
            reviews.data.slice(0, 2).forEach((r, i) => {
                console.log(`\n[${i+1}] ${r.score}/5 - ${r.text.substring(0, 60)}...`);
            });
            
            console.log('\n✅ Google Play Scraper 测试通过!');
        }
    } catch (err) {
        console.error('❌ 错误:', err.message);
    }
}

test();
