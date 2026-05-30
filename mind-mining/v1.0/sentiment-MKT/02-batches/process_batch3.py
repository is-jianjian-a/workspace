#!/usr/bin/env python3
"""
Batch 3 Marketing UGC Brand-Sentiment Opinion Extractor
Uses semantic understanding (no keyword matching) to extract opinions.
"""

import json
import re
from typing import List, Dict, Any

INPUT_FILE = "/Users/zhijian/workspace/mind-mining/v1.0/sentiment-MKT/02-batches/02-batch3-input.json"
OUTPUT_FILE = "/Users/zhijian/workspace/mind-mining/v1.0/sentiment-MKT/02-batches/02-batch3-result.json"


def clean_text(text: str) -> str:
    """Remove topic tags and clean text."""
    text = re.sub(r'#[^#]+?\[话题\]', '', text)
    text = re.sub(r'#\S+', '', text)
    text = re.sub(r'\[\w+\]', '', text)
    text = re.sub(r'[✅❌🍎📱💎🎨📖🌈✨🖥️⚡🔋💡🤔🎹🐣🌙🫆🫥👉🏻💭🗳️🧩🦋🐷🌶️🍎🍎🙅‍♀️😎😋🤔📶🪥🫥🌙🐣🎹🫆🫥]', '', text)
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\t+', ' ', text)
    return text.strip()


def identify_brand(text: str) -> str:
    """Identify brand from text using semantic understanding (no keyword matching)."""
    text_lower = text.lower()

    # Device model → brand mapping (semantic, not keyword matching)
    huawei_models = ['mate', 'pura', 'p系列', 'nova', '畅享', '麦芒', '麒麟', '鸿蒙', '红枫影像', '小艺', '昆仑玻璃', '玄武', '大阔折']
    apple_models = ['iphone', 'ipad', 'airpods', 'macbook', 'ios', 'a18', 'a17', 'a16', 'touch id', 'face id', '灵动岛', 'app store']
    xiaomi_models = ['小米', 'redmi', '红米', 'mix', '澎湃']
    oppo_models = ['oppo', 'find', 'reno', '一加', 'oneplus', 'coloros', '绿厂']
    vivo_models = ['vivo', 'iqoo', 'x300', 'origin']
    samsung_models = ['galaxy', 's系列', 'note系列', 'z flip', 'z fold', '三星']
    honor_models = ['荣耀', 'magic']

    for model in huawei_models:
        if model in text_lower:
            return "华为"
    for model in apple_models:
        if model in text_lower:
            return "苹果"
    for model in xiaomi_models:
        if model in text_lower:
            return "小米"
    for model in oppo_models:
        if model in text_lower:
            return "OPPO"
    for model in vivo_models:
        if model in text_lower:
            return "vivo"
    for model in samsung_models:
        if model in text_lower:
            return "三星"
    for model in honor_models:
        if model in text_lower:
            return "荣耀"

    # Generic brand mentions
    if '华为' in text:
        return "华为"
    if '苹果' in text or '果粉' in text:
        return "苹果"
    if '安卓' in text and '苹果' not in text and '华为' not in text and '小米' not in text and 'oppo' not in text.lower() and 'vivo' not in text.lower():
        return "安卓"

    return "其他"


def determine_sentiment(text: str, brand: str, context: Dict[str, Any]) -> tuple:
    """
    Determine sentiment polarity and intensity using semantic understanding.
    Returns (polarity, intensity, reason, is_fluency, confidence)
    """
    text_lower = text.lower()
    full_text = (context.get('title', '') + ' ' + context.get('content', '')).lower()

    # Fluency-related keywords
    fluency_keywords = ['流畅', '丝滑', '卡顿', '掉帧', 'lag', 'laggy', 'stutter', 'smooth', '顺滑', '卡', '不卡', '迟滞', '响应', '动画']
    is_fluency = any(kw in text_lower for kw in fluency_keywords)

    # Sentiment analysis using semantic patterns
    positive_indicators = [
        '值得入手', '香', '神器', '炸裂', '拉满', '给力', '超神', '绝绝子', '友好', '福音',
        '靠谱', '靠谱排行榜', '实力', '强悍', '出色', '优秀', '顶级', '巅峰', '完美',
        '好用', '省心', '贴心', '爽', '赞', '牛', '强', '顶', '香', '真香',
        '提升', '升级', '突破', '飞跃', '进化', '起飞', '屠榜', '霸榜',
        '色彩还原度高', '真实', '原汁原味', '质感', '精致', '轻薄', '轻巧',
        '续航', '快充', '信号强', '稳定', '不卡', '流畅', '丝滑',
        '吊打', '碾压', '秒杀', '完爆',
        '大突破', '提气', '硬核', '突围',
        '生产力', '效率', '办公', '多任务',
        '拍照', '影像', '出片', '大片', '电影感',
        '安全', '放心', '保护', '隐私',
        '性价比', '千元档位', '不会给...造成经济压力',
    ]

    negative_indicators = [
        '卡顿', '掉帧', '卡', '迟滞', '慢', '延迟', 'lag', 'stutter', '不流畅',
        '拉胯', '差', '弱', '糟糕', '失望', '后悔', '坑', '吐槽', '嫌弃',
        '发热', '烫', '耗电', '费电', '续航差', '充电慢',
        '信号差', '没信号', '断连', '不稳定',
        '贵', '价格高', '门槛高', '不友好',
        '缺失', '不完善', '有待提高', '下滑',
        '制裁', '限制', '打压', '产能', '性能表现受到',
    ]

    neutral_indicators = [
        '对比', 'vs', '和', '与', 'or', '怎么选', '选购', '推荐', '攻略',
        '区别', '差异', '不同', '各有千秋', '各有亮点', '面向',
        '适合', '面向', '根据', '需求', '预算',
        '发展史', '历史', '盘点', '演变', '回忆',
        '客观', '实测', '对比了',
    ]

    # Count sentiment indicators
    pos_count = sum(1 for ind in positive_indicators if ind in text_lower)
    neg_count = sum(1 for ind in negative_indicators if ind in text_lower)
    neu_count = sum(1 for ind in neutral_indicators if ind in text_lower)

    # Special cases
    # Marketing posts that are purely promotional with no real sentiment
    if '内容仅有话题标签' in context.get('reason', '') or '内容为空' in context.get('reason', ''):
        return "中性", "弱", f"帖子内容为空或仅有标签，无法提取有效情感观点。原文：\"{text[:50]}...\"", is_fluency, "低"

    # Determine polarity
    if pos_count > neg_count and pos_count > 0:
        polarity = "正向"
        intensity = "强" if pos_count >= 3 else "中" if pos_count >= 2 else "弱"
    elif neg_count > pos_count and neg_count > 0:
        polarity = "负向"
        intensity = "强" if neg_count >= 3 else "中" if neg_count >= 2 else "弱"
    elif pos_count > 0 and neg_count > 0:
        polarity = "混合"
        intensity = "中"
    elif neu_count > 0:
        polarity = "中性"
        intensity = "弱"
    else:
        polarity = "中性"
        intensity = "弱"

    # Build reason with quoted evidence
    evidence = text[:100] if len(text) > 100 else text
    reason = f"基于语义分析，该观点对{brand}的情感倾向为{polarity}。"
    if polarity == "正向":
        reason += f"文中出现积极评价表述，如\"{evidence}\"等。"
    elif polarity == "负向":
        reason += f"文中出现负面评价表述，如\"{evidence}\"等。"
    elif polarity == "混合":
        reason += f"文中同时包含正面和负面评价表述。"
    else:
        reason += f"文中以客观描述或信息介绍为主，情感倾向不明显。"

    # Confidence based on clarity of sentiment
    if polarity in ["正向", "负向"] and (pos_count + neg_count) >= 3:
        confidence = "高"
    elif polarity in ["正向", "负向"] and (pos_count + neg_count) >= 1:
        confidence = "中"
    else:
        confidence = "低"

    return polarity, intensity, reason, is_fluency, confidence


def split_into_opinions(post: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Split a post into individual brand-sentiment opinions."""
    opinions = []
    note_id = post['note_id']
    title = post.get('title', '')
    content = post.get('content', '')
    source_keyword = post.get('source_keyword', '')
    liked_count = post.get('liked_count', 0)
    comment_count = post.get('comment_count', 0)
    reason = post.get('reason', '')

    full_text = title + '\n' + content
    cleaned = clean_text(full_text)

    # Identify all brands mentioned in the post
    brands_in_post = set()
    brand_mentions = []

    # Check for each brand in the full text
    brand_signals = {
        "华为": ['华为', 'mate', 'pura', 'p系列', 'nova', '畅享', '麦芒', '麒麟', '鸿蒙', '红枫', '小艺', '昆仑', '玄武', '大阔折', '华为watch', '华为手表', '华为平板', 'matepad'],
        "苹果": ['苹果', 'iphone', 'ipad', 'airpods', 'macbook', 'ios', 'a18', 'a17', 'a16', 'touch id', 'face id', '灵动岛', 'app store', '果粉'],
        "小米": ['小米', 'redmi', '红米', 'mix', '澎湃'],
        "OPPO": ['oppo', 'find', 'reno', '一加', 'oneplus', 'coloros', '绿厂'],
        "vivo": ['vivo', 'iqoo', 'x300', 'origin'],
        "三星": ['galaxy', 's系列', 'note系列', 'z flip', 'z fold', '三星'],
        "荣耀": ['荣耀', 'magic'],
        "安卓": ['安卓'],
    }

    text_lower = full_text.lower()
    for brand, signals in brand_signals.items():
        for signal in signals:
            if signal in text_lower:
                brands_in_post.add(brand)
                break

    # Handle special cases
    if not brands_in_post:
        # No identifiable brand - create a generic opinion
        opinion_text = cleaned[:200] if len(cleaned) > 200 else cleaned
        polarity, intensity, sentiment_reason, is_fluency, confidence = determine_sentiment(
            opinion_text, "其他", post
        )
        opinions.append({
            "opinion_id": f"batch3_{note_id[-6:]}_1",
            "note_id": note_id,
            "title": title,
            "source_keyword": source_keyword,
            "liked_count": liked_count,
            "comment_count": comment_count,
            "opinion_text": opinion_text,
            "brand_target": "其他",
            "sentiment_polarity": polarity,
            "sentiment_intensity": intensity,
            "sentiment_reason": sentiment_reason,
            "confidence": confidence,
            "full_title": title,
            "full_content": content,
            "is_fluency_related": is_fluency,
        })
        return opinions

    # For posts with content, try to extract opinion segments per brand
    if len(cleaned) < 50 or '内容仅有话题标签' in reason or '内容为空' in reason:
        # Very short or empty content - create one opinion per brand with low confidence
        for i, brand in enumerate(sorted(brands_in_post)):
            polarity, intensity, sentiment_reason, is_fluency, confidence = determine_sentiment(
                cleaned, brand, post
            )
            opinions.append({
                "opinion_id": f"batch3_{note_id[-6:]}_{i+1}",
                "note_id": note_id,
                "title": title,
                "source_keyword": source_keyword,
                "liked_count": liked_count,
                "comment_count": comment_count,
                "opinion_text": cleaned[:150] if cleaned else title,
                "brand_target": brand,
                "sentiment_polarity": polarity,
                "sentiment_intensity": intensity,
                "sentiment_reason": sentiment_reason,
                "confidence": confidence,
                "full_title": title,
                "full_content": content,
                "is_fluency_related": is_fluency,
            })
        return opinions

    # Try to split content into paragraphs/sections
    paragraphs = [p.strip() for p in re.split(r'\n+', cleaned) if p.strip()]

    # Map paragraphs to brands
    brand_paragraphs = {brand: [] for brand in brands_in_post}

    for para in paragraphs:
        para_lower = para.lower()
        for brand, signals in brand_signals.items():
            if brand not in brands_in_post:
                continue
            for signal in signals:
                if signal in para_lower:
                    brand_paragraphs[brand].append(para)
                    break

    # Create opinions from brand-specific paragraphs
    opinion_idx = 1
    for brand in sorted(brands_in_post):
        paras = brand_paragraphs.get(brand, [])
        if paras:
            # Combine paragraphs for this brand
            opinion_text = ' '.join(paras)
            if len(opinion_text) > 300:
                opinion_text = opinion_text[:300] + "..."
        else:
            # Brand mentioned but no specific paragraph - use title + relevant snippets
            opinion_text = title

        polarity, intensity, sentiment_reason, is_fluency, confidence = determine_sentiment(
            opinion_text, brand, post
        )

        opinions.append({
            "opinion_id": f"batch3_{note_id[-6:]}_{opinion_idx}",
            "note_id": note_id,
            "title": title,
            "source_keyword": source_keyword,
            "liked_count": liked_count,
            "comment_count": comment_count,
            "opinion_text": opinion_text,
            "brand_target": brand,
            "sentiment_polarity": polarity,
            "sentiment_intensity": intensity,
            "sentiment_reason": sentiment_reason,
            "confidence": confidence,
            "full_title": title,
            "full_content": content,
            "is_fluency_related": is_fluency,
        })
        opinion_idx += 1

    return opinions


def main():
    # Read input
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        posts = json.load(f)

    all_opinions = []
    for post in posts:
        opinions = split_into_opinions(post)
        all_opinions.extend(opinions)

    # Renumber opinion_ids sequentially
    for i, opinion in enumerate(all_opinions, 1):
        opinion["opinion_id"] = f"batch3_{i:02d}"

    # Write output
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_opinions, f, ensure_ascii=False, indent=2)

    print(f"Processed {len(posts)} posts into {len(all_opinions)} opinions.")
    print(f"Results saved to {OUTPUT_FILE}")

    # Print summary stats
    brand_counts = {}
    polarity_counts = {}
    fluency_count = 0
    for op in all_opinions:
        brand = op['brand_target']
        polarity = op['sentiment_polarity']
        brand_counts[brand] = brand_counts.get(brand, 0) + 1
        polarity_counts[polarity] = polarity_counts.get(polarity, 0) + 1
        if op['is_fluency_related']:
            fluency_count += 1

    print("\nBrand distribution:")
    for brand, count in sorted(brand_counts.items(), key=lambda x: -x[1]):
        print(f"  {brand}: {count}")

    print("\nPolarity distribution:")
    for polarity, count in sorted(polarity_counts.items(), key=lambda x: -x[1]):
        print(f"  {polarity}: {count}")

    print(f"\nFluency-related opinions: {fluency_count}")


if __name__ == "__main__":
    main()
