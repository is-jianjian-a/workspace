import json

# 读取数据
with open('/Users/zhijian/workspace/mind-mining/v1.0/batches/batch_067.json', 'r') as f:
    data = json.load(f)

def classify(item):
    title = item.get('title', '')
    content = item.get('content', '')
    nickname = item.get('nickname', '')
    text = (title + ' ' + content).lower()
    
    # === career: 求职/面试/职场相关 ===
    career_keywords = ['面试', '入池', 'offer', '求职', '招聘', '校招', '实习', '简历', 'hr ', '主管面', '技术面', '机试', '泡池', '114525']
    for kw in career_keywords:
        if kw in text:
            return 'career'
    
    # === marketing: 营销/推广/抽奖/广告 ===
    if nickname == '淘宝':
        return 'marketing'
    marketing_keywords = ['抽奖', '奖品', '获奖人数', '开奖时间', '参与方式', '关注+', '转发', '将通过', '中奖后']
    for kw in marketing_keywords:
        if kw in text:
            return 'marketing'
    # 京东mall购买分享带营销性质
    if '京东mall' in text and '开业' in text:
        return 'marketing'
    
    # === tutorial: 教程/攻略/技巧分享 ===
    tutorial_indicators = ['小技巧', '设置>', '快捷指令', '步骤', '教程', '攻略', '怎么设置', '如何关闭']
    if '养护小技巧' in content:
        return 'tutorial'
    if '设置>' in content and '关闭' in content:
        return 'tutorial'
    # 开发技术教程
    if 'swift' in text and ('开发' in text or '构建' in text):
        return 'tutorial'
    
    # === news: 新闻/资讯/爆料 ===
    news_indicators = ['首个跑分', '跑分出来了', '爆料', '搜集整理', '预测更新', '剧透', '发布会', '来袭', '曝光']
    for kw in news_indicators:
        if kw in text:
            return 'news'
    # 安全漏洞新闻
    if '被ai用' in text and '攻破' in text:
        return 'news'
    if '首次被' in text and '攻击' in text:
        return 'news'
    
    # === spec_comparison: 规格对比/产品对比 ===
    if ('对比' in text or 'vs' in text or '比不过' in text) and ('小米' in text or '安卓' in text or '红米' in text or 'oppo' in text):
        return 'spec_comparison'
    
    # === real_ugc: 真实用户原创内容 ===
    # 个人长期使用计划
    if '打算用' in text and '年' in text:
        return 'real_ugc'
    # 个人二手/闲置分享
    if '自用' in text and ('备用机' in text or '学生' in text):
        return 'real_ugc'
    # 个人使用体验
    if '还能再战' in text or '用了' in text and '年' in text:
        return 'real_ugc'
    # 购买体验分享
    if '入手' in text and ('用了' in text or '两周' in text or '体验' in text):
        return 'real_ugc'
    # 系统升级体验
    if '升级了' in text and ('把玩' in text or '体验' in text or '感受' in text):
        return 'real_ugc'
    # 情绪吐槽但属于UGC
    if ('矫情' in text or '全网也就' in text) and '苹果用户' in text:
        return 'real_ugc'
    # 输入法使用感受
    if '输入法' in text and ('坚持' in text or '流畅' in text or '联想' in text):
        return 'real_ugc'
    # 电池使用感受
    if '电池健康' in text and ('省电' in text or '续航' in text or '焦虑' in text):
        return 'real_ugc'
    # 工具使用体验
    if 'macbook' in text and ('ai' in text or '接入' in text or '对接' in text):
        return 'real_ugc'
    # 鸿蒙输入法体验
    if '小艺输入法' in text or ('鸿蒙' in text and '输入法' in text):
        return 'real_ugc'
    # 配色讨论UGC
    if '配色' in text and ('应援' in text or 'tfboys' in text or '早出' in text):
        return 'real_ugc'
    # 简单的产品讨论
    if '会卖爆吗' in text or '卖爆' in text:
        return 'real_ugc'
    # 极速性能模式疑问
    if '极速性能模式' in text and '为什么' in text:
        return 'real_ugc'
    # 屏幕灵敏度问题
    if '屏幕' in text and '灵敏' in text and '怎么办' in text:
        return 'real_ugc'
    
    # === invalid: 无效内容 ===
    if len(content.strip()) < 5:
        return 'invalid'
    
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
        'nickname': item['nickname']
    })

# 输出到文件
output_path = '/Users/zhijian/workspace/mind-mining/v1.0/batches/result_batch_067.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# 打印分类统计
from collections import Counter
counts = Counter([r['category'] for r in results])
print('分类统计:')
for cat in ['real_ugc', 'tutorial', 'news', 'spec_comparison', 'marketing', 'info_missing', 'invalid', 'career']:
    count = counts.get(cat, 0)
    print(f'  {cat}: {count}')

print(f'\n输出文件: {output_path}')

# 打印详细分类
print('\n详细分类:')
for r in results:
    print(f"  {r['id']}: [{r['category']}] {r['nickname']} - {r['title'][:45]}")
