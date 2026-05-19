#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import shutil

INPUT_FILE = "/Users/zhijian/workspace/ai-demand-research-v3/projects/宝爸宝妈-2026-05-19/02-classified/all_classified_merged.json"
OUTPUT_FILE = "/Users/zhijian/workspace/ai-demand-research-v3/projects/宝爸宝妈-2026-05-19/02-classified/all_classified_reviewed.json"

# 读取并验证JSON
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"总条数: {len(data)}")

# 统计分类
counts = {}
changed = 0
for item in data:
    c = item.get('classification', '未知')
    counts[c] = counts.get(c, 0) + 1
    if item.get('review_changed'):
        changed += 1

print(f"分类统计: {counts}")
print(f"修正条数: {changed}")

# 复制为reviewed文件
shutil.copy2(INPUT_FILE, OUTPUT_FILE)
print(f"已保存到: {OUTPUT_FILE}")
