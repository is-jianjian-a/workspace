#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Theme tagging script for batches 006-010
Themes: 流畅丝滑, 卡顿问题, 稳定性
"""

import json
import os
import re

INPUT_DIR = "/Users/zhijian/workspace/ai-demand-research-v3/projects/华为苹果性能对比-2026-05-20/03-theme-tagged-v2"
OUTPUT_DIR = INPUT_DIR


def detect_brand(text, title=""):
    """Detect brand and model from text and title"""
    combined = (title + " " + text).lower()
    text_lower = text.lower()
    title_lower = title.lower()
    
    # Huawei models - more specific first
    if "mate80" in combined or "mate 80" in combined:
        return "华为 Mate80"
    if "mate70" in combined or "mate 70" in combined:
        return "华为 Mate70"
    if "mate60" in combined or "mate 60" in combined:
        return "华为 Mate60"
    if "pura90" in combined or "pura 90" in combined or "p90" in combined:
        return "华为 Pura90"
    if "pura80" in combined or "pura 80" in combined or "p80" in combined:
        return "华为 Pura80"
    if "pura70" in combined or "pura 70" in combined or "p70" in combined:
        return "华为 Pura70"
    if "p60" in combined or "p60" in combined:
        return "华为 P60"
    if "matepadmini" in combined:
        return "华为 MatePad Mini"
    if "华为" in text or "鸿蒙" in text or "麒麟" in text or "华为" in title:
        return "华为"
    
    # Apple models - more specific first
    if "17promax" in combined or "17 pro max" in combined or "17pm" in combined:
        return "苹果 iPhone 17 Pro Max"
    if "17pro" in combined or "17 pro" in combined:
        return "苹果 iPhone 17 Pro"
    if "17air" in combined or "17 air" in combined:
        return "苹果 iPhone 17 Air"
    if "iphone17" in combined or ("17" in combined and "iphone" in combined):
        return "苹果 iPhone 17"
    if "16promax" in combined or "16 pro max" in combined:
        return "苹果 iPhone 16 Pro Max"
    if "16pro" in combined or "16 pro" in combined:
        return "苹果 iPhone 16 Pro"
    if "iphone16" in combined:
        return "苹果 iPhone 16"
    if "15promax" in combined or "15 pro max" in combined or "15pm" in combined:
        return "苹果 iPhone 15 Pro Max"
    if "15pro" in combined or "15 pro" in combined:
        return "苹果 iPhone 15 Pro"
    if "iphone15" in combined:
        return "苹果 iPhone 15"
    if "14pro" in combined or "14 pro" in combined:
        return "苹果 iPhone 14 Pro"
    if "iphone14" in combined:
        return "苹果 iPhone 14"
    if "13pro" in combined or "13 pro" in combined:
        return "苹果 iPhone 13 Pro"
    if "iphone13" in combined:
        return "苹果 iPhone 13"
    if "iphone12" in combined or ("12" in combined and "iphone" in combined):
        return "苹果 iPhone 12"
    if "iphone" in combined or "ios" in combined:
        return "苹果"
    
    # Other brands
    if "小米" in text or "xiaomi" in text_lower:
        return "小米"
    if "vivo" in text_lower:
        return "vivo"
    if "oppo" in text_lower:
        return "OPPO"
    if "荣耀" in text or "honor" in text_lower:
        return "荣耀"
    if "三星" in text or "samsung" in text_lower:
        return "三星"
    
    return "未知"


def has_any(text, keywords):
    """Check if text contains any of the keywords"""
    return any(kw in text for kw in keywords)


def get_best_quote(lines, keywords, exclude_keywords=None, max_chars=150):
    """Get the best matching quote from lines"""
    if exclude_keywords is None:
        exclude_keywords = []
    
    candidates = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if has_any(line, keywords) and not has_any(line, exclude_keywords):
            # Score based on relevance
            score = sum(1 for kw in keywords if kw in line)
            # Prefer shorter, more focused quotes
            length_penalty = len(line) / 100
            candidates.append((line, score - length_penalty))
    
    if candidates:
        # Sort by score descending
        candidates.sort(key=lambda x: x[1], reverse=True)
        best = candidates[0][0]
        # Truncate if too long, but try to keep complete sentences
        if len(best) > max_chars:
            # Try to find a sentence boundary
            truncated = best[:max_chars]
            last_punct = max(truncated.rfind("。"), truncated.rfind("！"), truncated.rfind("？"), truncated.rfind("."), truncated.rfind("!"))
            if last_punct > max_chars * 0.5:
                best = truncated[:last_punct+1]
            else:
                best = truncated + "..."
        return best
    return None


def tag_ugc(note):
    """Tag a single UGC with themes"""
    title = note.get("title", "")
    content = note.get("content", "")
    full_text = title + "\n" + content
    
    tags = []
    lines = [l.strip() for l in full_text.split("\n") if l.strip()]
    
    # === Theme 1: 流畅丝滑 ===
    smooth_keywords = ["流畅", "丝滑", "顺滑", "跟手", "不卡", "德芙", "动画", "打断动画", "系统动画", "响应快", "反应快", "迅速", "快", "绵密", "内外都很丝滑"]
    smooth_exclude = ["卡顿", "卡死", "掉帧", "卡到", "不流畅", "卡成", "卡爆", "卡得", "很卡", "太卡"]
    
    quote = get_best_quote(lines, smooth_keywords, smooth_exclude)
    if quote:
        brand = detect_brand(quote, title)
        
        neg_words = ["不如", "差", "不丝滑", "不流畅", "卡顿", "卡死", "差劲", "糟糕", "略逊", "差距"]
        pos_words = ["丝滑", "流畅", "顺滑", "德芙", "非常好", "很棒", "优秀", "超越", "领先", "不输", "媲美", "抗衡", "很好", "不错", "真正意义上", "抗衡", "快"]
        
        if has_any(quote, neg_words):
            sentiment = "负面"
        elif has_any(quote, pos_words):
            sentiment = "正面"
        else:
            sentiment = "中性"
        
        tags.append({
            "theme": "流畅丝滑",
            "quote": quote,
            "brand_model": brand,
            "sentiment": sentiment
        })
    
    # === Theme 2: 卡顿问题 ===
    lag_keywords = ["卡顿", "卡死", "卡到", "掉帧", "反应慢", "慢半拍", "闪退", "死机", "卡成", "卡爆", "卡得", "很卡", "太卡", "卡卡卡", "卡住了", "加载慢", "重新加载", "杀后台", "卡住不动", "卡到起飞", "卡到爆炸", "卡得像", "卡顿了", "变卡", "开始卡了", "卡的刷不了"]
    
    quote = get_best_quote(lines, lag_keywords)
    if quote:
        brand = detect_brand(quote, title)
        sentiment = "负面"
        
        tags.append({
            "theme": "卡顿问题",
            "quote": quote,
            "brand_model": brand,
            "sentiment": sentiment
        })
    
    # === Theme 3: 稳定性 ===
    stability_keywords = ["稳定", "不稳", "闪退", "死机", "重启", "崩溃", "bug", "发热", "发烫", "掉电快", "续航", "电池", "信号", "断网", "断流", "失联", "无信号", "系统更新", "版本", "烫手", "温度高", "烧", "断触", "罚站", "定位卡顿"]
    
    quote = get_best_quote(lines, stability_keywords)
    if quote:
        brand = detect_brand(quote, title)
        
        neg_words = ["不稳", "闪退", "死机", "崩溃", "bug", "发热", "发烫", "掉电快", "断网", "断流", "失联", "无信号", "差", "严重", "拉胯", "糟糕", "烫手", "烧", "罚站", "定位卡顿", "卡顿"]
        pos_words = ["稳定", "可靠", "好", "强", "优秀", "出色", "给力", "扎实", "省心", "稳", "不错", "碾压", "薄纱"]
        
        if has_any(quote, neg_words):
            sentiment = "负面"
        elif has_any(quote, pos_words):
            sentiment = "正面"
        else:
            sentiment = "中性"
        
        tags.append({
            "theme": "稳定性",
            "quote": quote,
            "brand_model": brand,
            "sentiment": sentiment
        })
    
    return tags


def process_batch(batch_num):
    """Process a single batch file"""
    input_file = os.path.join(INPUT_DIR, f"batch_{batch_num:03d}_input.json")
    output_file = os.path.join(OUTPUT_DIR, f"batch_{batch_num:03d}_output.json")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    results = []
    for note in data:
        tags = tag_ugc(note)
        if tags:
            results.append({
                "note_id": note.get("note_id", ""),
                "title": note.get("title", ""),
                "content": note.get("content", ""),
                "tags": tags
            })
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"Batch {batch_num:03d}: Processed {len(data)} UGCs, tagged {len(results)} with themes")
    return len(data), len(results)


def main():
    total_ugcs = 0
    total_tagged = 0
    
    for batch_num in range(6, 11):
        n, t = process_batch(batch_num)
        total_ugcs += n
        total_tagged += t
    
    print(f"\nTotal: {total_ugcs} UGCs processed, {total_tagged} tagged with themes")


if __name__ == "__main__":
    main()
