#!/usr/bin/env node
/**
 * 国际社交媒体监控工具
 * 支持 Twitter/X, Reddit, YouTube (通过代理)
 * 使用 ClashX Meta 代理: http://127.0.0.1:7890
 */

const PROXY = 'http://127.0.0.1:7890';

// 通用 fetch 带代理
async function fetchWithProxy(url, options = {}) {
    const fetch = (await import('node-fetch')).default;
    const HttpsProxyAgent = (await import('https-proxy-agent')).HttpsProxyAgent;
    
    const agent = new HttpsProxyAgent(PROXY);
    return fetch(url, {
        ...options,
        agent,
        timeout: 30000
    });
}

// ===== Twitter/X 监控 =====
async function monitorTwitter(username) {
    console.log(`\n=== Twitter/X 监控: @${username} ===`);
    
    try {
        // 使用 nitter 镜像获取推文 (无需认证)
        const nitterInstances = [
            'https://nitter.net',
            'https://nitter.it',
            'https://nitter.cz'
        ];
        
        for (const instance of nitterInstances) {
            try {
                const response = await fetchWithProxy(`${instance}/${username}/rss`);
                if (response.ok) {
                    const text = await response.text();
                    console.log(`✅ 通过 ${instance} 获取到数据`);
                    console.log(`数据长度: ${text.length} 字符`);
                    return { success: true, source: instance, data: text };
                }
            } catch (e) {
                console.log(`❌ ${instance} 失败: ${e.message}`);
            }
        }
        
        return { success: false, error: '所有 Nitter 实例都失败' };
    } catch (error) {
        console.error('❌ Twitter 监控失败:', error.message);
        return { success: false, error: error.message };
    }
}

// ===== Reddit 监控 =====
async function monitorReddit(subreddit, sort = 'hot', limit = 10) {
    console.log(`\n=== Reddit 监控: r/${subreddit} ===`);
    
    try {
        const url = `https://www.reddit.com/r/${subreddit}/${sort}.json?limit=${limit}`;
        const response = await fetchWithProxy(url, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        const posts = data.data.children.map(child => ({
            title: child.data.title,
            author: child.data.author,
            score: child.data.score,
            comments: child.data.num_comments,
            url: `https://reddit.com${child.data.permalink}`,
            created: new Date(child.data.created_utc * 1000).toISOString()
        }));
        
        console.log(`✅ 获取到 ${posts.length} 条帖子`);
        posts.slice(0, 3).forEach((post, i) => {
            console.log(`  [${i+1}] ${post.title.substring(0, 60)}...`);
            console.log(`      👍 ${post.score} | 💬 ${post.comments} | u/${post.author}`);
        });
        
        return { success: true, posts };
    } catch (error) {
        console.error('❌ Reddit 监控失败:', error.message);
        return { success: false, error: error.message };
    }
}

// ===== YouTube 监控 =====
async function monitorYouTube(channelId, maxResults = 10) {
    console.log(`\n=== YouTube 监控: ${channelId} ===`);
    
    try {
        // 使用 RSS feed (无需 API Key)
        const rssUrl = `https://www.youtube.com/feeds/videos.xml?channel_id=${channelId}`;
        const response = await fetchWithProxy(rssUrl);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const text = await response.text();
        console.log(`✅ 获取到 RSS feed (${text.length} 字符)`);
        
        // 简单解析 (实际使用需要 XML 解析器)
        const videoMatches = text.match(/<yt:videoId>([^<]+)<\/yt:videoId>/g);
        const titleMatches = text.match(/<title>([^<]+)<\/title>/g);
        
        if (videoMatches) {
            console.log(`📹 找到 ${videoMatches.length} 个视频`);
            
            const videos = videoMatches.slice(0, 3).map((match, i) => {
                const videoId = match.replace(/<\/?yt:videoId>/g, '');
                const title = titleMatches && titleMatches[i+1] 
                    ? titleMatches[i+1].replace(/<\/?title>/g, '') 
                    : 'Unknown';
                return { videoId, title, url: `https://youtube.com/watch?v=${videoId}` };
            });
            
            videos.forEach((v, i) => {
                console.log(`  [${i+1}] ${v.title.substring(0, 60)}`);
                console.log(`      ${v.url}`);
            });
            
            return { success: true, videos };
        }
        
        return { success: true, raw: text.substring(0, 500) };
    } catch (error) {
        console.error('❌ YouTube 监控失败:', error.message);
        return { success: false, error: error.message };
    }
}

// ===== 主函数 =====
async function main() {
    console.log('🌍 国际社交媒体监控工具');
    console.log(`代理: ${PROXY}`);
    console.log('=' .repeat(50));
    
    // 检查依赖
    try {
        await import('node-fetch');
        await import('https-proxy-agent');
    } catch {
        console.error('❌ 缺少依赖。请运行: npm install node-fetch https-proxy-agent');
        process.exit(1);
    }
    
    // 测试各平台
    const results = {
        twitter: await monitorTwitter('elonmusk'),
        reddit: await monitorReddit('technology'),
        youtube: await monitorYouTube('UC_x5XG1OV2P6uZZ5FSM9Ttw') // Google Developers
    };
    
    // 汇总
    console.log('\n' + '='.repeat(50));
    console.log('📊 监控结果汇总');
    console.log('='.repeat(50));
    
    Object.entries(results).forEach(([platform, result]) => {
        const status = result.success ? '✅' : '❌';
        console.log(`${status} ${platform}: ${result.success ? '成功' : result.error}`);
    });
}

main().catch(console.error);
