#!/usr/bin/env python3
"""对消费者视角UGC进行严格的二次视角分析"""

import json
from collections import Counter

project_dir = "/Users/zhijian/workspace/ai-demand-research-v3/projects/看视频时想要的AI功能-2026-05-18"

with open(f"{project_dir}/02-cleaned/ugc_full_text_with_tags.json", 'r', encoding='utf-8') as f:
    ugc_list = json.load(f)

with open(f"{project_dir}/02-cleaned/consumer_view_ugcs.json", 'r', encoding='utf-8') as f:
    consumer_ugcs = json.load(f)

with open(f"{project_dir}/02-cleaned/mixed_view_ugcs.json", 'r', encoding='utf-8') as f:
    mixed_ugcs = json.load(f)

with open(f"{project_dir}/02-cleaned/creator_view_ugcs.json", 'r', encoding='utf-8') as f:
    creator_ugcs = json.load(f)

# 找到两条知乎UGC
target_ids = []
for ugc in ugc_list:
    if ugc['platform'] == 'zhihu':
        if '生理反应' in ugc['title'] or '人眼还能分辨' in ugc['title']:
            target_ids.append(ugc['id'])

# 重新构建消费者列表
final_consumer_ids = set()
for ugc in consumer_ugcs:
    final_consumer_ids.add(ugc['id'])
for uid in target_ids:
    final_consumer_ids.add(uid)

# 混合视角全部归为创造者
mixed_ids = {u['id'] for u in mixed_ugcs}
creator_ids = {u['id'] for u in creator_ugcs}
final_creator_ids = creator_ids | mixed_ids
for uid in target_ids:
    final_creator_ids.discard(uid)
    final_consumer_ids.add(uid)

id_to_ugc = {u['id']: u for u in ugc_list}
final_consumer_ugcs = [id_to_ugc[uid] for uid in final_consumer_ids if uid in id_to_ugc]

# 严格消费者视角关键词
strict_consumer_keywords = [
    '看视频', '观看', '播放', '看剧', '追剧', '看电影', '看番', '看片',
    '看视频时', '看视频的时候', '看视频想要', '看视频希望',
    '学习', '记笔记', '知识点', '复习', '课程', '网课', '教程',
    '摘要', '总结', '提炼', '要点', '精华', '省流', '省流助手',
    '搜索', '找', '定位', '跳转到', '时间戳', '跳到',
    '推荐', '个性化', '过滤', '屏蔽', '不感兴趣', '同质化', '信息茧房',
    '字幕', '翻译', '听不懂', '外语', '英文', '日文', '中文', '双语',
    '倍速', '快进', '跳过', '广告', '片头', '片尾', '进度条',
    '画质', '高清', '4k', '模糊', '清晰', '修复', '增强',
    '投屏', '同步', '跨设备', '手机看', '电视', '平板',
    '氛围', '助眠', '解压', '放松', '沉浸式', '白噪音',
    '问视频', '解释', '什么意思', '为什么', '怎么做', '不懂',
    '自动', '智能', 'ai帮我', 'ai功能', '想要', '希望', '需要',
    '方便', '省事', '省力', '效率', '节省时间',
]

# 严格创造者视角关键词
strict_creator_keywords = [
    '生成视频', '文生视频', '图生视频', '一键成片', 'ai生成', '生成短片',
    '数字人', '虚拟主播', '换脸', 'deepfake', 'ai特效',
    '自动剪辑', '智能剪辑', '一键剪辑', '自动剪', 'ai剪辑',
    '高光', '精彩片段', '自动截取', '自动切片', '切片',
    '二创', '混剪', '合拍', '模板', '素材', '视频模板',
    '视频制作', '做视频', '剪视频', '拍视频', '录视频',
    '视频编辑', '剪辑软件', 'pr', '剪映', 'final cut',
    '后期制作', '调色', '配音', '配字幕',
    'up主', '博主', '创作者', '内容创作', '视频创作',
    '流量', '涨粉', '爆款', '视频号', '自媒体', '运营',
    '口播', '脚本', '分镜', '故事板', '成片',
    '发布', '上传', '分发', '平台', '算法推荐',
]

# 二次分析
strict_consumer = []
strict_creator = []
needs_review = []

for ugc in final_consumer_ugcs:
    text = (ugc['title'] + ' ' + ugc['content']).lower()
    
    has_consumer = any(kw in text for kw in strict_consumer_keywords)
    has_creator = any(kw in text for kw in strict_creator_keywords)
    
    if has_creator and not has_consumer:
        strict_creator.append(ugc)
    elif has_consumer and not has_creator:
        strict_consumer.append(ugc)
    elif has_creator and has_consumer:
        needs_review.append(ugc)
    else:
        consumer_layer2 = {'智能摘要', '知识提取', '学习管理', '实时翻译', 
                          '画质增强', '自动字幕', '内容过滤', '个性化推荐',
                          '跨设备同步', '氛围音效', '智能问答', '跳过广告'}
        creator_layer2 = {'ai生成视频', '自动剪辑', '二创工具'}
        
        if any(tag in consumer_layer2 for tag in ugc['layer2']):
            strict_consumer.append(ugc)
        elif any(tag in creator_layer2 for tag in ugc['layer2']):
            strict_creator.append(ugc)
        else:
            needs_review.append(ugc)

print(f"=== 严格二次分析结果 ===")
print(f"🟢 严格消费者视角: {len(strict_consumer)}条")
print(f"🔴 严格创造者视角: {len(strict_creator)}条")
print(f"🟡 需人工审核: {len(needs_review)}条")

print(f"\n=== 严格创造者视角（从消费者中移除）===")
for i, ugc in enumerate(strict_creator[:10]):
    print(f"\n{i+1}. [{ugc['platform']}] {ugc['title'][:80]}")
    print(f"   内容: {ugc['content'][:120]}...")
    print(f"   二层: {ugc['layer2']}")

print(f"\n=== 需人工审核（前15条）===")
for i, ugc in enumerate(needs_review[:15]):
    print(f"\n{i+1}. [{ugc['platform']}] {ugc['title'][:80]}")
    print(f"   内容: {ugc['content'][:150]}...")
    print(f"   二层: {ugc['layer2']}")

# 保存结果
with open(f"{project_dir}/02-cleaned/strict_consumer_ugcs.json", 'w', encoding='utf-8') as f:
    json.dump(strict_consumer, f, ensure_ascii=False, indent=2)

with open(f"{project_dir}/02-cleaned/strict_creator_from_consumer.json", 'w', encoding='utf-8') as f:
    json.dump(strict_creator, f, ensure_ascii=False, indent=2)

with open(f"{project_dir}/02-cleaned/needs_review_ugcs.json", 'w', encoding='utf-8') as f:
    json.dump(needs_review, f, ensure_ascii=False, indent=2)

print(f"\n✅ 已保存严格分析结果")
