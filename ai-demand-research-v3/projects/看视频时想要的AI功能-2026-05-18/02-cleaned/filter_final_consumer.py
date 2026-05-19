#!/usr/bin/env python3
"""从消费者列表中移除明显的创造者视角UGC"""

import json

project_dir = "/Users/zhijian/workspace/ai-demand-research-v3/projects/看视频时想要的AI功能-2026-05-18"

with open(f"{project_dir}/02-cleaned/final_consumer_ugcs.json", 'r', encoding='utf-8') as f:
    final_consumer = json.load(f)

creator_ids_to_remove = set()

for ugc in final_consumer:
    text = (ugc['title'] + ' ' + ugc['content']).lower()
    title = ugc['title']
    
    # 明确创造者视角
    if '教程' in title and ('AI漫剧' in title or 'AI视频生成' in title or 'ComfyUI' in title):
        creator_ids_to_remove.add(ugc['id'])
    elif 'updream保姆级教程' in title:
        creator_ids_to_remove.add(ugc['id'])
    elif '0基础小白保姆级教程' in title:
        creator_ids_to_remove.add(ugc['id'])
    elif '豆包手机版使用教程' in title:
        creator_ids_to_remove.add(ugc['id'])
    elif 'AI跳舞保姆级教程' in title:
        creator_ids_to_remove.add(ugc['id'])
    elif '接单变现' in text:
        creator_ids_to_remove.add(ugc['id'])
    elif '短视频带货' in text and '智能开播' in text:
        creator_ids_to_remove.add(ugc['id'])
    elif '用ai制作零食视频带货' in text:
        creator_ids_to_remove.add(ugc['id'])
    elif '一键生成短剧详细制作流程' in text:
        creator_ids_to_remove.add(ugc['id'])
    elif 'AI短剧制作' in text:
        creator_ids_to_remove.add(ugc['id'])
    elif 'deepseek生成50条原创视频' in text:
        creator_ids_to_remove.add(ugc['id'])
    elif '一键去除不想要的人和物' in text and '剪辑教程' in text:
        creator_ids_to_remove.add(ugc['id'])
    elif '快影剪辑教程' in text:
        creator_ids_to_remove.add(ugc['id'])
    elif 'ai制作' in text and '没有使用真人肖像权' in text:
        creator_ids_to_remove.add(ugc['id'])
    elif '去掉廉价感，AI直出4K超清视频' in title:
        creator_ids_to_remove.add(ugc['id'])
    elif '一句话，让你的🦞可以全网抓信息' in title:
        creator_ids_to_remove.add(ugc['id'])
    elif 'AI视频工具推荐' in title and 'comfyui' in text:
        creator_ids_to_remove.add(ugc['id'])
    elif 'AI视频总结工具合集' in title and '30选3' in title:
        creator_ids_to_remove.add(ugc['id'])

print(f"需要移除的创造者视角UGC: {len(creator_ids_to_remove)}条")

# 过滤
filtered_consumer = [u for u in final_consumer if u['id'] not in creator_ids_to_remove]

print(f"\n过滤前消费者UGC: {len(final_consumer)}条")
print(f"过滤后消费者UGC: {len(filtered_consumer)}条")

# 保存
with open(f"{project_dir}/02-cleaned/final_consumer_ugcs_v2.json", 'w', encoding='utf-8') as f:
    json.dump(filtered_consumer, f, ensure_ascii=False, indent=2)

print(f"\n✅ 已保存最终消费者视角UGC: {len(filtered_consumer)}条")

# 统计
from collections import Counter
platform_dist = Counter(u['platform'] for u in filtered_consumer)
print(f"\n=== 最终消费者视角平台分布 ===")
for p, c in platform_dist.most_common():
    print(f"  {p}: {c}条")
