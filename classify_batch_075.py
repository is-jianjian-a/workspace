import json

# 读取batch_075.json
with open('/Users/zhijian/workspace/mind-mining/v1.0/batches/batch_075.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 8类UGC分类
categories = {
    4739: '问题求助',   # 17pro电池续航问题求助
    4740: '资讯爆料',   # 2026 iPhone全家桶新品爆料
    4741: '其他',       # 显化实验（非数码UGC，玄学内容）
    4742: '使用体验',   # 苹果店参加活动体验分享
    4743: '购买攻略',   # AppleCare购买分析/攻略
    4744: '购买攻略',   # 年年换新vs几年一换分析
    4745: '使用体验',   # MagSafe外接电池使用吐槽
    4746: '资讯爆料',   # 苹果办公三件套更新资讯
    4747: '问题求助',   # iPhone到底卡不卡疑问
    4748: '开箱晒单',   # 降价入手17pro晒单
    4749: '使用体验',   # 7年从xs到16长期使用体验
    4750: '问题求助',   # 定制v/微x会不会被封求助
    4751: '其他',       # iCloud拼车广告
    4752: '资讯爆料',   # iPhone屏蔽更新失效资讯
    4753: '其他',       # 苹果股价与大盘分析（投资内容）
    4754: '其他',       # iCloud拼车广告
    4755: '使用体验',   # 隔空投送使用吐槽
    4756: '其他',       # 苹果股价投资分析
    4757: '资讯爆料',   # 2026款新品可自己换电池资讯
    4758: '购买攻略',   # 16换18pro换机策略
    4759: '使用体验',   # iOS26.5升级体验分享
    4760: '问题求助',   # 苹果黑屏问题求助
    4761: '产品评测',   # Apple Watch S11拔草评测
    4762: '开箱晒单',   # 17pro顶配配置晒单
    4763: '资讯爆料',   # iPhone限量配件返场资讯
}

# 添加category字段
for item in data:
    item['category'] = categories.get(item['id'], '其他')

# 写入result_batch_075.json
with open('/Users/zhijian/workspace/result_batch_075.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 打印分类统计
from collections import Counter
stats = Counter(item['category'] for item in data)
print("分类统计:")
for cat, count in stats.most_common():
    print(f"  {cat}: {count}")

print(f"\n总计: {len(data)} 条")
print("输出文件: /Users/zhijian/workspace/result_batch_075.json")
