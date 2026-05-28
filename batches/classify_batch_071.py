import json

# 读取数据
with open('/Users/zhijian/workspace/mind-mining/v1.0/batches/batch_071.json', 'r') as f:
    data = json.load(f)

def classify(item):
    title = item.get('title', '')
    content = item.get('content', '')
    nickname = item.get('nickname', '')
    text = (title + ' ' + content).lower()
    
    # === invalid: 无效内容 ===
    if len(content.strip()) < 5:
        return 'invalid'
    
    # === marketing: 营销/推广/招聘广告 ===
    if nickname == 'SimpleHR':
        return 'marketing'
    marketing_keywords = ['紧急补招', '底薪', '月入', '名额', '招满', '私我', '锁定名额', '免费夜宵', '物业式宿舍']
    for kw in marketing_keywords:
        if kw in text:
            return 'marketing'
    
    # === career: 求职/面试/职场相关 ===
    career_keywords = ['面试', '入池', 'offer', '求职', '招聘', '校招', '实习', '简历', 'hr ', '主管面', '技术面', '机试', '泡池', '入职体检', '体检复查', '体检不合格', '选offer', '秋招', '春招', '补录', '开奖']
    for kw in career_keywords:
        if kw in text:
            return 'career'
    
    # === news: 新闻/资讯/爆料 ===
    news_indicators = ['营收', '净利润', '市场份额', '销量', '累计', '业绩解读', '发布节奏', '全年擂台', '数码资讯', '科技资讯']
    for kw in news_indicators:
        if kw in text:
            return 'news'
    
    # === spec_comparison: 规格对比/产品对比 ===
    if ('对比' in text or 'vs' in text or '比不过' in text) and ('小米' in text or '安卓' in text or '红米' in text or 'oppo' in text or '大疆' in text):
        return 'spec_comparison'
    
    # === tutorial: 教程/攻略/技巧分享 ===
    tutorial_indicators = ['小技巧', '设置>', '快捷指令', '步骤', '教程', '攻略', '怎么设置', '如何关闭', '如何', '指南']
    for kw in tutorial_indicators:
        if kw in text:
            return 'tutorial'
    
    # === real_ugc: 真实用户原创内容 ===
    # 个人离职经历分享
    if '离职' in text and ('lastday' in text or '华为再见' in text or '重启人生' in text or '从华为' in text or '离开华为' in text or '华为离职' in text or '菊厂离职' in text):
        return 'real_ugc'
    # 个人工作感受/吐槽
    if ('工作' in text or '加班' in text or '绩效' in text) and ('感受' in text or '体验' in text or '吐槽' in text or '碎碎念' in text or '心理' in text):
        return 'real_ugc'
    # 个人职业记录/经历
    if '职业记录' in text or '工作第' in text or ('在华为' in text and ('年' in text or '天' in text)):
        return 'real_ugc'
    # 个人避雷/建议
    if '避雷' in text and ('华为' in text or '部门' in text):
        return 'real_ugc'
    # 适合/不适合某公司的分析
    if '适合来' in text or ('适合' in text and ('华子' in text or '大厂' in text)):
        return 'real_ugc'
    # 工资/薪酬相关UGC
    if ('工资' in text or '薪酬' in text) and ('收到' in text or '晒' in text):
        return 'real_ugc'
    # 简单吐槽
    if '扛不住了' in text or ('魔鬼' in text and '华为' in text):
        return 'real_ugc'
    # 个人上岸/考公经历
    if '上岸' in text and ('体制内' in text or '考公' in text):
        return 'real_ugc'
    # 点赞离职类
    if ('个赞' in text or '赞就' in text) and '离职' in text:
        return 'real_ugc'
    # 个人OD经历
    if 'od岗' in text or 'od ' in text:
        return 'real_ugc'
    # 海思工作经历
    if '海思' in text or '海屌丝' in text:
        return 'real_ugc'
    # 工作日常吐槽
    if '天天都是' in text or '无休止' in text:
        return 'real_ugc'
    # 职业选择思考
    if '职业选择' in text or '工作方向' in text or '未来发展方向' in text:
        return 'real_ugc'
    # 跳槽/跳出后发现差距
    if '跳出来' in text or '跳出去' in text or '跳出来之后' in text:
        return 'real_ugc'
    # 华为vs其他公司对比（UGC讨论）
    if '为什么' in text and '华为' in text and ('大疆' in text or '小米' in text or '苹果' in text):
        return 'real_ugc'
    # 只有话题标签的
    if content.strip().startswith('#') and len(content.strip()) < 30:
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
output_path = '/Users/zhijian/workspace/batches/result_batch_071.json'
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
