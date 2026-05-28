import json

# 读取数据
with open('/Users/zhijian/workspace/mind-mining/v1.0/batches/batch_067.json', 'r') as f:
    data = json.load(f)

# 8类分类定义
# real_ugc: 真实用户原创内容（个人使用体验、真实感受、生活分享）
# tutorial: 教程/攻略/技巧分享
# news: 新闻/资讯/爆料
# spec_comparison: 规格对比/产品对比
# marketing: 营销/推广/抽奖/广告
# info_missing: 信息缺失/无法判断
# invalid: 无效内容/不相关
# career: 求职/面试/职场相关

def classify(item):
    title = item.get('title', '')
    content = item.get('content', '')
    nickname = item.get('nickname', '')
    text = (title + ' ' + content).lower()
    
    # 检查是否职业相关内容
    career_keywords = ['面试', '入池', 'offer', '求职', '招聘', '校招', '实习', '简历', 'hr', '华为 面试', '主管面', '技术面', '机试', '泡池']
    for kw in career_keywords:
        if kw in text:
            return 'career'
    
    # 检查是否营销/抽奖/广告
    marketing_keywords = ['抽奖', '奖品', '获奖', '开奖', '参与方式', '关注', '转发', '淘宝', '京东mall', '店铺', '优惠', '国补', '店补']
    if nickname == '淘宝':
        return 'marketing'
    for kw in marketing_keywords:
        if kw in text:
            return 'marketing'
    
    # 检查是否教程/攻略
    tutorial_keywords = ['技巧', '教程', '攻略', '设置', '怎么', '如何', '方法', '步骤', '快捷指令', '养护']
    if '养护小技巧' in content or '设置>' in content or '快捷指令' in content:
        return 'tutorial'
    
    # 检查是否新闻/资讯
    news_keywords = ['发布', '发布会', '跑分', '首个', '爆料', '曝光', '预测', '剧透', '来袭', '升级', '配备']
    if '跑分' in text or '首个' in text or '爆料' in text or '发布会' in text or '剧透' in text:
        return 'news'
    if '搜集整理' in content or '预测更新' in content:
        return 'news'
    
    # 检查是否规格对比
    if '对比' in text or 'vs' in text or '比不过' in text or '相差' in text:
        if '小米' in text or '安卓' in text or '红米' in text or 'oppo' in text or 'ophone' in text:
            return 'spec_comparison'
    
    # 检查是否真实UGC（个人体验分享）
    ugc_indicators = ['自用', '用了', '入手', '升级', '体验', '感受', '打算', '计划', '我的', '我 ', '本人']
    if '长期主义' in text or '打算用10年' in text:
        return 'real_ugc'
    if '自用' in text and '备用机' in text:
        return 'real_ugc'
    if '还能再战' in text or '用了4年' in text:
        return 'real_ugc'
    if '入手了一台' in text and '用了两周' in text:
        return 'real_ugc'
    if 'iPhone14 Pro' in content and '升级了' in content:
        return 'real_ugc'
    if '丝滑下车' in text and '付款' in text:
        return 'real_ugc'
    if '坚持' in text and '输入法' in text:
        return 'real_ugc'
    
    # 检查无效/不相关
    if len(content.strip()) < 10 and '不懂就问' in text:
        return 'info_missing'
    
    # 默认根据内容判断
    if '体验' in text and ('用了' in text or '入手' in text or '我的' in text):
        return 'real_ugc'
    
    # 技术/开发相关内容
    if 'swift' in text or 'electron' in text or '原生开发' in text:
        return 'tutorial'
    
    # 安全/漏洞新闻
    if '攻破' in text or '漏洞' in text or '安全' in text:
        return 'news'
    
    # 情绪/吐槽类UGC
    if '矫情' in text or '吐槽' in text or '骂' in text:
        return 'real_ugc'
    
    # 工具/使用体验
    if '输入法' in text or '电池' in text:
        return 'real_ugc'
    
    # AI/MacBook工具
    if 'macbook' in text and 'ai' in text:
        return 'real_ugc'
    
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
for cat, count in counts.most_common():
    print(f'  {cat}: {count}')

print(f'\n输出文件: {output_path}')

# 打印详细分类
print('\n详细分类:')
for r in results:
    print(f"  {r['id']}: [{r['category']}] {r['nickname']} - {r['title'][:40]}")
