#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parenting UGC Data Analysis - Baseline (No Skill)
Analyzes Xiaohongshu parenting data for scene analysis, user journey, and keyword decomposition.
"""

import json
import os
from collections import Counter, defaultdict
from datetime import datetime

# Load data
DATA_PATH = "/Users/zhijian/workspace/ai-demand-research-v3/projects/宝爸宝妈育儿收集需求-2026-05-18-v2/03-cleaned/output/labeled_data.json"
OUTPUT_DIR = "/Users/zhijian/workspace/UGC-research-v2-workspace/iteration-1/parenting-demand-research/without_skill/outputs/"

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total records: {len(data)}")

# ========== BASIC STATISTICS ==========
# Layer1 distribution
layer1_all = []
layer2_all = []
emotions_all = []
scenes_all = []
signals_all = []
keywords_all = []
quality_all = []

# Engagement metrics
engagement_by_layer1 = defaultdict(lambda: {'likes': 0, 'collects': 0, 'comments': 0, 'shares': 0, 'count': 0})

for item in data:
    layer1_all.extend(item.get('layer1', []))
    layer2_all.extend(item.get('layer2', []))
    emotions_all.extend(item.get('emotions', []))
    scenes_all.extend(item.get('scenes', []))
    signals_all.extend(item.get('signals', []))
    keywords_all.append(item.get('source_keyword', ''))
    quality_all.append(item.get('quality', ''))
    
    for l1 in item.get('layer1', []):
        engagement_by_layer1[l1]['likes'] += item.get('liked_count', 0)
        engagement_by_layer1[l1]['collects'] += item.get('collected_count', 0)
        engagement_by_layer1[l1]['comments'] += item.get('comment_count', 0)
        engagement_by_layer1[l1]['shares'] += item.get('share_count', 0)
        engagement_by_layer1[l1]['count'] += 1

layer1_counts = Counter(layer1_all)
layer2_counts = Counter(layer2_all)
emotions_counts = Counter(emotions_all)
scenes_counts = Counter(scenes_all)
signals_counts = Counter(signals_all)
keywords_counts = Counter(keywords_all)
quality_counts = Counter(quality_all)

print("\n=== LAYER1 DISTRIBUTION ===")
for k, v in layer1_counts.most_common():
    print(f"  {k}: {v}")

print("\n=== LAYER2 TOP 20 ===")
for k, v in layer2_counts.most_common(20):
    print(f"  {k}: {v}")

print("\n=== EMOTIONS ===")
for k, v in emotions_counts.most_common():
    print(f"  {k}: {v}")

print("\n=== SCENES ===")
for k, v in scenes_counts.most_common():
    print(f"  {k}: {v}")

print("\n=== SIGNALS ===")
for k, v in signals_counts.most_common():
    print(f"  {k}: {v}")

print("\n=== SOURCE KEYWORDS ===")
for k, v in keywords_counts.most_common():
    print(f"  {k}: {v}")

print("\n=== QUALITY ===")
for k, v in quality_counts.most_common():
    print(f"  {k}: {v}")

# ========== SCENE ANALYSIS ==========
# Co-occurrence: scenes x layer1
scene_layer1 = defaultdict(lambda: Counter())
scene_layer2 = defaultdict(lambda: Counter())
scene_emotions = defaultdict(lambda: Counter())
scene_signals = defaultdict(lambda: Counter())

for item in data:
    scenes = item.get('scenes', [])
    for scene in scenes:
        for l1 in item.get('layer1', []):
            scene_layer1[scene][l1] += 1
        for l2 in item.get('layer2', []):
            scene_layer2[scene][l2] += 1
        for emo in item.get('emotions', []):
            scene_emotions[scene][emo] += 1
        for sig in item.get('signals', []):
            scene_signals[scene][sig] += 1

print("\n=== SCENE x LAYER1 CO-OCCURRENCE ===")
for scene in sorted(scene_layer1.keys()):
    print(f"\n  Scene: {scene}")
    for l1, cnt in scene_layer1[scene].most_common():
        print(f"    {l1}: {cnt}")

# ========== USER JOURNEY ANALYSIS ==========
# Analyze by keyword (represents different stages/topics)
keyword_layer1 = defaultdict(lambda: Counter())
keyword_layer2 = defaultdict(lambda: Counter())
keyword_emotions = defaultdict(lambda: Counter())
keyword_scenes = defaultdict(lambda: Counter())

for item in data:
    kw = item.get('source_keyword', 'unknown')
    for l1 in item.get('layer1', []):
        keyword_layer1[kw][l1] += 1
    for l2 in item.get('layer2', []):
        keyword_layer2[kw][l2] += 1
    for emo in item.get('emotions', []):
        keyword_emotions[kw][emo] += 1
    for scene in item.get('scenes', []):
        keyword_scenes[kw][scene] += 1

print("\n=== KEYWORD x LAYER1 ===")
for kw in sorted(keyword_layer1.keys()):
    print(f"\n  Keyword: {kw}")
    for l1, cnt in keyword_layer1[kw].most_common():
        print(f"    {l1}: {cnt}")

# ========== ENGAGEMENT ANALYSIS ==========
print("\n=== ENGAGEMENT BY LAYER1 ===")
for l1, stats in sorted(engagement_by_layer1.items()):
    avg_likes = stats['likes'] / stats['count'] if stats['count'] > 0 else 0
    avg_collects = stats['collects'] / stats['count'] if stats['count'] > 0 else 0
    print(f"  {l1}: count={stats['count']}, avg_likes={avg_likes:.1f}, avg_collects={avg_collects:.1f}")

# High engagement posts
engagement_list = []
for item in data:
    engagement = item.get('liked_count', 0) + item.get('collected_count', 0) * 2 + item.get('comment_count', 0) * 3 + item.get('share_count', 0) * 2
    engagement_list.append({
        'note_id': item.get('note_id', ''),
        'title': item.get('title', '')[:50],
        'keyword': item.get('source_keyword', ''),
        'layer1': item.get('layer1', []),
        'layer2': item.get('layer2', []),
        'emotions': item.get('emotions', []),
        'scenes': item.get('scenes', []),
        'engagement': engagement,
        'likes': item.get('liked_count', 0),
        'collects': item.get('collected_count', 0),
        'comments': item.get('comment_count', 0),
        'shares': item.get('share_count', 0),
    })

engagement_list.sort(key=lambda x: x['engagement'], reverse=True)

print("\n=== TOP 20 HIGH ENGAGEMENT POSTS ===")
for i, item in enumerate(engagement_list[:20]):
    print(f"  {i+1}. [{item['keyword']}] {item['title']}... | E={item['engagement']} (L:{item['likes']} C:{item['collects']} M:{item['comments']} S:{item['shares']})")
    print(f"      layer1={item['layer1']}, emotions={item['emotions']}, scenes={item['scenes']}")

# ========== SAVE ANALYSIS RESULTS ==========
results = {
    'total_records': len(data),
    'layer1_distribution': dict(layer1_counts),
    'layer2_distribution': dict(layer2_counts.most_common(50)),
    'emotions_distribution': dict(emotions_counts),
    'scenes_distribution': dict(scenes_counts),
    'signals_distribution': dict(signals_counts),
    'keywords_distribution': dict(keywords_counts),
    'quality_distribution': dict(quality_counts),
    'engagement_by_layer1': {k: dict(v) for k, v in engagement_by_layer1.items()},
    'scene_layer1': {k: dict(v) for k, v in scene_layer1.items()},
    'scene_layer2': {k: dict(v.most_common(20)) for k, v in scene_layer2.items()},
    'scene_emotions': {k: dict(v) for k, v in scene_emotions.items()},
    'scene_signals': {k: dict(v) for k, v in scene_signals.items()},
    'keyword_layer1': {k: dict(v) for k, v in keyword_layer1.items()},
    'keyword_layer2': {k: dict(v.most_common(30)) for k, v in keyword_layer2.items()},
    'keyword_emotions': {k: dict(v) for k, v in keyword_emotions.items()},
    'keyword_scenes': {k: dict(v) for k, v in keyword_scenes.items()},
    'top_engagement_posts': engagement_list[:30],
}

with open(os.path.join(OUTPUT_DIR, 'analysis_results.json'), 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n✅ Analysis results saved to {OUTPUT_DIR}analysis_results.json")
