const store = require('app-store-scraper');
const fs = require('fs');

async function monitorAppStoreReviews(appName, appId, options = {}) {
    const {
        numReviews = 100,
        sortBy = 'recent'
    } = options;
    
    console.log(`=== 监控 App Store 评论: ${appName} ===\n`);
    
    try {
        // 获取评论
        const reviews = await store.reviews({
            id: appId,
            sort: sortBy === 'recent' ? store.sort.RECENT : store.sort.HELPFUL,
            page: 1
        });
        
        console.log(`获取到 ${reviews.length} 条评论\n`);
        
        // 分析评论
        const analysis = {
            total: reviews.length,
            ratings: { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 },
            issues: [],
            praise: [],
            recentReviews: []
        };
        
        reviews.forEach(review => {
            analysis.ratings[review.score]++;
            
            const text = review.text.toLowerCase();
            const title = review.title.toLowerCase();
            const combined = text + ' ' + title;
            
            // 检测问题
            const issueKeywords = ['crash', 'bug', 'broken', 'slow', 'freeze', 'error', 'problem', 
                                   '闪退', '卡顿', '崩溃', 'bug', '问题', '无法', '不能', '失败'];
            const praiseKeywords = ['great', 'love', 'excellent', 'perfect', 'amazing', 'best',
                                    '好用', '不错', '满意', '喜欢', '推荐', '完美', '棒'];
            
            if (issueKeywords.some(k => combined.includes(k))) {
                analysis.issues.push({
                    rating: review.score,
                    text: review.text.substring(0, 80),
                    title: review.title
                });
            }
            
            if (praiseKeywords.some(k => combined.includes(k))) {
                analysis.praise.push({
                    rating: review.score,
                    text: review.text.substring(0, 80),
                    title: review.title
                });
            }
            
            // 保存最近评论
            analysis.recentReviews.push({
                rating: review.score,
                title: review.title,
                text: review.text.substring(0, 100),
                date: review.date
            });
        });
        
        // 输出分析结果
        console.log('评分分布:');
        Object.entries(analysis.ratings).forEach(([rating, count]) => {
            const pct = ((count / analysis.total) * 100).toFixed(1);
            const bar = '█'.repeat(Math.round(pct / 5));
            console.log(`  ${rating}星: ${bar} ${count} (${pct}%)`);
        });
        
        console.log(`\n问题反馈 (${analysis.issues.length}条):`);
        analysis.issues.slice(0, 5).forEach((issue, i) => {
            console.log(`  ${i+1}. [${issue.rating}星] ${issue.title}`);
            console.log(`     ${issue.text}...`);
        });
        
        console.log(`\n好评亮点 (${analysis.praise.length}条):`);
        analysis.praise.slice(0, 5).forEach((item, i) => {
            console.log(`  ${i+1}. [${item.rating}星] ${item.title}`);
            console.log(`     ${item.text}...`);
        });
        
        console.log('\n最新评论样本:');
        analysis.recentReviews.slice(0, 3).forEach((r, i) => {
            console.log(`  [${i+1}] ${r.rating}/5 ${r.title}`);
            console.log(`      ${r.text}...`);
        });
        
        // 保存结果
        const output = {
            appName,
            appId,
            timestamp: new Date().toISOString(),
            analysis
        };
        
        const filename = `app_store_${appId}_${Date.now()}.json`;
        fs.writeFileSync(filename, JSON.stringify(output, null, 2));
        console.log(`\n✅ 分析完成，结果已保存到 ${filename}`);
        
        return analysis;
        
    } catch (error) {
        console.error('❌ 监控失败:', error.message);
        throw error;
    }
}

// 测试: 监控微信评论
monitorAppStoreReviews('WeChat', 414478124, { numReviews: 50 })
    .then(() => console.log('\n监控完成'))
    .catch(err => {
        console.error('监控失败:', err);
        process.exit(1);
    });
