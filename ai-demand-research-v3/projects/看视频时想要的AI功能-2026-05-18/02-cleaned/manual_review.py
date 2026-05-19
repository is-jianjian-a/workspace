#!/usr/bin/env python3
"""对需审核UGC进行人工判断分类"""

import json

project_dir = "/Users/zhijian/workspace/ai-demand-research-v3/projects/看视频时想要的AI功能-2026-05-18"

with open(f"{project_dir}/02-cleaned/needs_review_ugcs.json", 'r', encoding='utf-8') as f:
    needs_review = json.load(f)

with open(f"{project_dir}/02-cleaned/strict_consumer_ugcs.json", 'r', encoding='utf-8') as f:
    strict_consumer = json.load(f)

with open(f"{project_dir}/02-cleaned/strict_creator_from_consumer.json", 'r', encoding='utf-8') as f:
    strict_creator = json.load(f)

def is_consumer_perspective(ugc):
    text = (ugc['title'] + ' ' + ugc['content']).lower()
    title = ugc['title']
    
    # 用户明确指定的
    if '生理反应' in title or '人眼还能分辨' in title:
        return True
    
    # 明确消费者信号
    consumer_signals = [
        '刷视频', '看视频', '看剧', '追剧', '看电影', '看paper', '学习',
        '翻译', '字幕', '总结', '摘要', '笔记', '推荐', '屏蔽', '过滤',
        '生理反应', '恶心', '不适感', '分辨', '真假', '认知',
        'safari', '浏览器', '隐藏功能', 'app',
        '不白刷', '刷视频乐趣', '刷视频新体验',
        '失业', '社会', '意义', '深度',
        '沙雕', '斗猫', '月老', '禁忌', '陈鸿宇',
        '成人网站', 'molthub',
        '为什么现在 ai 已经没啥热度',
        '感谢google',
        '不要拿',
        'ai会员',
        '王德峰',
    ]
    
    # 创造者信号
    creator_signals = [
        '生成', '剪辑', '制作', '创作', '教程', '教学', '工具',
        '口播', '脚本', '分镜', '成片', '上传', '发布',
        '带货', '变现', '创业', '副业', '赚钱', '流量', '涨粉',
        '直播', '无人直播', '自动直播',
        '即梦', '可灵', '元宝',
        '复刻', '替换', '一键生成', '手把手',
        '视频分析ai工具', 'ai教育', 'ai教学',
        '短剧解说', '推剧助手',
        'ai分身', 'deepseek',
        '橘猫做饭',
        '无人直播带货',
        'ai形象',
        'ai短剧',
        'updream',
        'ai动态漫',
        '漫剧',
    ]
    
    has_consumer = any(s in text for s in consumer_signals)
    has_creator = any(s in text for s in creator_signals)
    
    # 娱乐内容
    if title in ['沙雕4', '斗猫（1）', '月老掉线', '被开启的禁忌之门', '陈鸿宇1', '【MAT】IS〈インフィニット・ストラトス〉ED 小提琴試演']:
        return True
    
    # 信息/思考内容
    if '深度' in title or '意义' in title or '失业' in title:
        return True
    if '王德峰' in title or '慎用AI' in title:
        return True
    if 'AI会员' in title:
        return True
    if '为什么现在 AI 已经没啥热度' in title:
        return True
    
    # 如果包含创造者信号，排除
    if has_creator and not has_consumer:
        return False
    
    # 如果包含消费者信号，保留
    if has_consumer:
        return True
    
    # 默认排除
    return False

# 分类
consumer_from_review = []
creator_from_review = []

for ugc in needs_review:
    if is_consumer_perspective(ugc):
        consumer_from_review.append(ugc)
    else:
        creator_from_review.append(ugc)

print(f"=== 人工审核结果 ===")
print(f"🟢 消费者视角（保留）: {len(consumer_from_review)}条")
print(f"🔴 创造者视角（排除）: {len(creator_from_review)}条")

print(f"\n=== 消费者视角（保留）===")
for i, ugc in enumerate(consumer_from_review):
    print(f"\n{i+1}. [{ugc['platform']}] {ugc['title'][:80]}")
    print(f"   内容: {ugc['content'][:120]}...")

print(f"\n=== 创造者视角（排除，前20条）===")
for i, ugc in enumerate(creator_from_review[:20]):
    print(f"\n{i+1}. [{ugc['platform']}] {ugc['title'][:80]}")
    print(f"   内容: {ugc['content'][:120]}...")

# 合并最终结果
final_consumer = strict_consumer + consumer_from_review
final_creator = strict_creator + creator_from_review

print(f"\n=== 最终统计 ===")
print(f"🟢 总消费者视角: {len(final_consumer)}条")
print(f"🔴 总创造者视角: {len(final_creator)}条")

# 保存
with open(f"{project_dir}/02-cleaned/final_consumer_ugcs.json", 'w', encoding='utf-8') as f:
    json.dump(final_consumer, f, ensure_ascii=False, indent=2)

with open(f"{project_dir}/02-cleaned/final_creator_ugcs.json", 'w', encoding='utf-8') as f:
    json.dump(final_creator, f, ensure_ascii=False, indent=2)

print(f"\n✅ 已保存最终结果")
