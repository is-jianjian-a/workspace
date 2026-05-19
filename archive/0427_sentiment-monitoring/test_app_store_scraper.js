const store = require('app-store-scraper');

async function testAppStoreScraper() {
    console.log('=== 测试 App Store Scraper ===\n');
    
    try {
        // 1. 搜索应用
        console.log('1. 搜索应用 (微信)...');
        const searchResults = await store.search({
            term: '微信',
            num: 5
        });
        console.log(`   找到 ${searchResults.length} 个结果`);
        if (searchResults.length > 0) {
            const app = searchResults[0];
            console.log(`   第一个: ${app.title} (ID: ${app.id})`);
            console.log(`   评分: ${app.score} (${app.ratings} 评分)`);
            
            // 2. 获取应用详情
            console.log('\n2. 获取应用详情...');
            const details = await store.app({ id: app.id });
            console.log(`   应用: ${details.title}`);
            console.log(`   开发者: ${details.developer}`);
            console.log(`   评分: ${details.score} (${details.reviews} 评论)`);
            console.log(`   版本: ${details.version}`);
            
            // 3. 获取评论
            console.log('\n3. 获取应用评论...');
            const reviews = await store.reviews({
                id: app.id,
                sort: store.sort.RECENT,
                page: 1
            });
            console.log(`   获取到 ${reviews.length} 条评论`);
            
            if (reviews.length > 0) {
                console.log('\n   最新评论样本:');
                reviews.slice(0, 3).forEach((review, i) => {
                    console.log(`   [${i+1}] 评分: ${review.score}/5`);
                    console.log(`       标题: ${review.title}`);
                    console.log(`       内容: ${review.text.substring(0, 80)}...`);
                    console.log(`       日期: ${review.date}`);
                    console.log();
                });
            }
            
            return {
                appId: app.id,
                appName: app.title,
                totalReviews: details.reviews,
                sampleReviews: reviews.length
            };
        }
    } catch (error) {
        console.error('❌ App Store Scraper 错误:', error.message);
        throw error;
    }
}

testAppStoreScraper()
    .then(result => {
        console.log('\n✅ App Store Scraper 测试通过!');
        console.log(`应用: ${result.appName} (ID: ${result.appId})`);
        console.log(`总评论数: ${result.totalReviews}`);
        console.log(`本次获取: ${result.sampleReviews} 条`);
    })
    .catch(err => {
        console.log('\n❌ 测试失败');
        process.exit(1);
    });
