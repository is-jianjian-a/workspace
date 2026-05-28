import json

# 读取batch_064.json
with open('/Users/zhijian/workspace/mind-mining/v1.0/batches/batch_064.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 根据内容手动分类
categories = {
    4464: '资讯爆料',   # 2026苹果秋季发布会前瞻 - 新品爆料
    4465: '产品评测',   # Mac mini AI时代神机 - 详细评测分析
    4466: '资讯爆料',   # Mac Mini火爆程度现状 - 市场动态
    4467: '使用体验',   # iPhone Air钛金属摔了 - 使用体验分享
    4468: '购买攻略',   # 不要乱买苹果手机 - 购买建议
    4469: '对比分析',   # 13pm换17pm感受 - 换机对比
    4470: '资讯爆料',   # MacBook Neo卖太好 - 产品新闻
    4471: '产品评测',   # iPhone17PM性能超标 - 性能评测
    4472: '开箱晒单',   # 苹果手机验机自测 - 验机/配置
    4473: '对比分析',   # iPhone14pro换17pro感受 - 换机对比
    4474: '开箱晒单',   # 抽到赛级17Pro - 开箱/配置
    4475: '使用体验',   # 11对比17pro频闪 - 屏幕体验
    4476: '对比分析',   # 反向升级Air之后 - 产品对比
    4477: '资讯爆料',   # 苹果赢得AI之战 - 行业分析/资讯
    4478: '购买攻略',   # 买Air不如看17 - 购买建议
    4479: '产品评测',   # HIFI佬详评AirPods Max2 - 详细评测
    4480: '问题求助',   # 为什么都喜欢16pro - 疑问/求助
    4481: '资讯爆料',   # iPhone18系列十大升级 - 新品爆料
    4482: '资讯爆料',   # 苹果芯片性能排行榜 - 资讯/排行
    4483: '问题求助',   # 为什么安卓电池大 - 疑问
    4484: '开箱晒单',   # 挑战17pm最低配置 - 配置展示
    4485: '资讯爆料',   # 最长寿的iPhone - 产品资讯
    4486: '资讯爆料',   # iOS性能榜 - 资讯/排行
    4487: '资讯爆料',   # 国行iPhone17阉割 - 产品资讯
    4488: '资讯爆料',   # 苹果折叠屏来了 - 新品资讯
}

# 添加category字段
for item in data:
    item['category'] = categories.get(item['id'], '其他')

# 写入result_batch_064.json
with open('/Users/zhijian/workspace/result_batch_064.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 打印分类统计
from collections import Counter
stats = Counter(item['category'] for item in data)
print("分类统计:")
for cat, count in stats.most_common():
    print(f"  {cat}: {count}")

print(f"\n总计: {len(data)} 条")
print("输出文件: /Users/zhijian/workspace/result_batch_064.json")
