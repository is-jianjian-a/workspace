import json

# 读取batch_030.json
with open('/Users/zhijian/workspace/ai-demand-research-v3/projects/看视频时想要的AI功能-2026-05-18/02-cleaned/batches/batch_030.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 8类UGC分类定义
categories = {
    '3x69etpeiepv5us': '教程攻略',   # 手把手教快手可灵如何进入 - AI工具教程
    '3xrmagh3cmdejyg': '教程攻略',   # 60秒教你制作百万播放AI爆款视频 - AI视频制作教程
    '3xu46r7zcfdia56': '教程攻略',   # 微信搜一搜AI功能大揭秘 - AI功能揭秘/教程
    '3xtateuqi3vxdi4': '教程攻略',   # ai带货，短视频带货的新玩法 - AI带货教程
    '3x8wxwxm66ismsi': '教程攻略',   # AI动画小短片，人物一致性教程 - AI动画教程
    '3xcf5a75gcacdh6': '教程攻略',   # #短视频创业 #短视频变现 #短视频教学 #AI - AI短视频教学
    '3xm565zd5kcyj4w': '教程攻略',   # ai对话功能使用 - AI功能使用教程
    '3xzk9c6x4ws49ww': '教程攻略',   # 如何用AI一键生成橘猫做饭视频 - AI视频生成教程
    '3x3ab3uqyc68m2m': '教程攻略',   # 如何免费生成数字人说话 - 数字人生成教程
    '3xm9kiu2b6axws2': '教程攻略',   # ai短视频怎么没流量了... - AI短视频制作教程/攻略
}

# 添加category字段
for item in data['ugcs']:
    item['category'] = categories.get(item['id'], '其他')

# 写入result_batch_030.json
output_path = '/Users/zhijian/workspace/result_batch_030.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 打印分类统计
from collections import Counter
stats = Counter(item['category'] for item in data['ugcs'])
print("分类统计:")
for cat, count in stats.most_common():
    print(f"  {cat}: {count}")

print(f"\n总计: {len(data['ugcs'])} 条")
print(f"输出文件: {output_path}")
