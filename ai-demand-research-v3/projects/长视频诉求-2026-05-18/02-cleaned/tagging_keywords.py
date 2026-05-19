#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
标签提取脚本 - 长视频诉求调研
生成: 2026-05-18
用途: 对清洗后的数据进行一层主题、二层主题、情绪、场景标签提取
"""

import json
import pandas as pd
from collections import defaultdict

# 加载关键词词典
with open("tagging_keywords.json", "r", encoding="utf-8") as f:
    KEYWORDS = json.load(f)

# ========== 一层主题 ==========
L1_TOPICS = {c["name"]: c["keywords"] for c in KEYWORDS["一层主题"]["categories"]}

# ========== 二层主题 ==========
L2_TOPICS = {c["name"]: c["keywords"] for c in KEYWORDS["二层主题"]["categories"]}
L2_PARENT = {c["name"]: c["parent"] for c in KEYWORDS["二层主题"]["categories"]}

# ========== 情绪标签 ==========
EMOTIONS = {c["name"]: c["keywords"] for c in KEYWORDS["情绪标签"]["categories"]}

# ========== 场景标签 ==========
SCENES = {c["name"]: c["keywords"] for c in KEYWORDS["场景标签"]["categories"]}


def match_labels(text, keyword_dict):
    """匹配文本中的标签关键词"""
    text_lower = text.lower()
    matched = []
    for label, keywords in keyword_dict.items():
        for kw in keywords:
            if kw.lower() in text_lower:
                matched.append(label)
                break
    return matched


def classify_text(text):
    """
    对单条文本进行分类标签提取
    返回: {
        "l1_topics": [...],
        "l2_topics": [...],
        "emotions": [...],
        "scenes": [...]
    }
    """
    return {
        "l1_topics": match_labels(text, L1_TOPICS),
        "l2_topics": match_labels(text, L2_TOPICS),
        "emotions": match_labels(text, EMOTIONS),
        "scenes": match_labels(text, SCENES),
    }


def tag_dataframe(df, text_col="text"):
    """
    对DataFrame进行批量标签提取
    新增列: l1_topics, l2_topics, emotions, scenes
    """
    results = df[text_col].apply(classify_text)
    df["l1_topics"] = results.apply(lambda x: x["l1_topics"])
    df["l2_topics"] = results.apply(lambda x: x["l2_topics"])
    df["emotions"] = results.apply(lambda x: x["emotions"])
    df["scenes"] = results.apply(lambda x: x["scenes"])
    
    # 添加主标签（取第一个匹配）
    df["l1_main"] = df["l1_topics"].apply(lambda x: x[0] if x else "未分类")
    df["l2_main"] = df["l2_topics"].apply(lambda x: x[0] if x else "未分类")
    df["emotion_main"] = df["emotions"].apply(lambda x: x[0] if x else "未分类")
    df["scene_main"] = df["scenes"].apply(lambda x: x[0] if x else "未分类")
    
    return df


def get_topic_stats(df):
    """获取主题分布统计"""
    stats = {
        "l1_distribution": df["l1_main"].value_counts().to_dict(),
        "l2_distribution": df["l2_main"].value_counts().to_dict(),
        "emotion_distribution": df["emotion_main"].value_counts().to_dict(),
        "scene_distribution": df["scene_main"].value_counts().to_dict(),
    }
    return stats


if __name__ == "__main__":
    # 示例用法
    import sys
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        df = pd.read_json(input_file)
        df = tag_dataframe(df)
        df.to_json("labeled_data.json", orient="records", force_ascii=False, indent=2)
        print(f"标签提取完成，结果保存到 labeled_data.json")
        print(f"共处理 {len(df)} 条数据")
    else:
        print("用法: python tagging_keywords.py <input_json_file>")
