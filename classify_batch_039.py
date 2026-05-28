import json
from collections import Counter

# 读取batch_039.json
with open('/Users/zhijian/workspace/mind-mining/v1.0/batches/batch_039.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 8类UGC分类定义
def classify(item):
    title = item.get('title', '')
    content = item.get('content', '')
    text = (title + ' ' + content).lower()
    
    # === tutorial: 教程攻略/技巧分享 ===
    tutorial_keywords = ['设置-', '小技巧', '步骤', '教程', '攻略', '怎么设置', '如何关闭', '亲测有效', '几步就能']
    for kw in tutorial_keywords:
        if kw in text:
            return 'tutorial'
    
    # === spec_comparison: 规格对比/产品对比 ===
    if ('对比' in text or 'vs' in text or '换' in text) and ('iphone' in text or 'vivo' in text or 'oppo' in text or '小米' in text):
        return 'spec_comparison'
    
    # === news: 新闻/资讯/爆料 ===
    news_keywords = ['爆料', '搜集整理', '预测', '剧透', '发布会', '曝光', '首个跑分']
    for kw in news_keywords:
        if kw in text:
            return 'news'
    
    # === marketing: 营销/推广/抽奖/广告 ===
    marketing_keywords = ['抽奖', '奖品', '获奖', '开奖', '关注+', '转发', '中奖', '将通过']
    for kw in marketing_keywords:
        if kw in text:
            return 'marketing'
    
    # === career: 求职/面试/职场相关 ===
    career_keywords = ['面试', '入池', 'offer', '求职', '招聘', '校招', '实习', '简历', 'hr ', '主管面', '技术面', '机试']
    for kw in career_keywords:
        if kw in text:
            return 'career'
    
    # === invalid: 无效内容 ===
    if len(content.strip()) < 5:
        return 'invalid'
    
    # === real_ugc: 真实用户原创内容 ===
    # 个人使用体验/吐槽/分享
    ugc_indicators = [
        '用了', '入手', '体验', '感觉', '卡顿', '卡死', '崩溃', '后悔', '太无语',
        '你们的', '大家的', '求助', '怎么办', '怎么回事', '有没有同款',
        '第一天', '用了几天', '用了多久', '买了', '换新机', '再也不买',
        '使用感', '反应迟钝', '闪退', '死机', '白屏', '发热', '烫',
        '超级', '真的', '服了', '寒心', '被迫'
    ]
    for kw in ugc_indicators:
        if kw in text:
            return 'real_ugc'
    
    # === info_missing: 信息缺失/无法判断 ===
    return 'info_missing'

# 分类并输出结果
results = []
for item in data:
    category = classify(item)
    results.append({
        'id': item['id'],
        'note_id': item['note_id'],
        'category': category,
        'title': item['title'],
        'nickname': item['nickname'],
        'content': item['content'],
        'source_keyword': item.get('source_keyword', ''),
        'liked_count': item.get('liked_count', 0),
        'comment_count': item.get('comment_count', 0)
    })

# 输出到result_batch_039.json
output_path = '/Users/zhijian/workspace/result_batch_039.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# 打印分类统计
stats = Counter([r['category'] for r in results])
print('分类统计:')
for cat in ['real_ugc', 'tutorial', 'news', 'spec_comparison', 'marketing', 'career', 'invalid', 'info_missing']:
    count = stats.get(cat, 0)
    print(f'  {cat}: {count}')

print(f'\n总计: {len(results)} 条')
print(f'输出文件: {output_path}')

# 打印详细分类
print('\n详细分类:')
for r in results:
    print(f"  {r['id']}: [{r['category']}] {r['nickname']} - {r['title'][:50]}")
