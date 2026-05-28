#!/usr/bin/env python3
"""
UGC Classification Script for batch_036.json
8-class classification based on content analysis.
"""

import json
import re

INPUT_PATH = "/Users/zhijian/workspace/mind-mining/v1.0/batches/batch_036.json"
OUTPUT_PATH = "/Users/zhijian/workspace/result_batch_036.json"

# 8 UGC categories
CATEGORIES = [
    "功能体验/使用感受",
    "购买决策/对比选择",
    "吐槽/抱怨/负面反馈",
    "技巧/攻略/教程",
    "产品推荐/种草",
    "资讯/新闻/行业动态",
    "情感/态度/观点表达",
    "其他"
]

def classify_item(item):
    """
    Classify a single UGC item into one of 8 categories.
    Uses title + content for classification.
    """
    title = item.get("title", "")
    content = item.get("content", "")
    text = (title + " " + content).lower()
    
    # 1. 技巧/攻略/教程 - how-to, tips, guides
    tutorial_keywords = ["怎么", "如何", "教程", "攻略", "技巧", "方法", "设置", "关闭", "打开", "调整", "步骤", "指南", "教你怎么", "一分钟", "快速"]
    if any(kw in text for kw in tutorial_keywords):
        # But check if it's more of a complaint
        if not any(kw in text for kw in ["吐槽", "垃圾", "恶心", "后悔", "崩溃", "失望", "反感", "晕", "想吐", "太差", "极差", "心碎", "罪过", "缺点"]):
            return "技巧/攻略/教程"
    
    # 2. 产品推荐/种草 - explicit recommendations
    recommend_keywords = ["推荐", "闭眼冲", "必买", "种草", "好价", "值得买", "入手", "安利", "首选", "最佳选择", "闭眼入"]
    if any(kw in text for kw in recommend_keywords):
        return "产品推荐/种草"
    
    # 3. 资讯/新闻/行业动态 - news, reports, industry info
    news_keywords = ["财报", "年报", "发布", "营收", "销量", "市场份额", "行业", "资讯", "新闻", "动态", "报道"]
    if any(kw in text for kw in news_keywords):
        return "资讯/新闻/行业动态"
    
    # Check for product review / experience sharing (positive or neutral)
    # These are not complaints but sharing of usage experience
    if "用了" in text and ("发现" in text or "觉得" in text or "感觉" in text):
        # Check it's not a complaint
        if not any(kw in text for kw in ["吐槽", "垃圾", "恶心", "后悔", "崩溃", "失望", "反感", "晕", "想吐", "太差", "极差", "心碎", "罪过", "缺点", "毛病", "烦", "难用", "卡顿", "卡死", "发热", "发烫", "不流畅", "费电", "耗电"]):
            return "功能体验/使用感受"
    
    # 4. 吐槽/抱怨/负面反馈 - complaints, negative experiences
    complaint_keywords = ["吐槽", "垃圾", "恶心", "后悔", "崩溃", "失望", "反感", "晕", "想吐", "太差", "极差", "罪过", "缺点", "毛病", "问题", "烦", "难用", "卡顿", "卡死", "发热", "发烫", "不流畅", "费电", "耗电", "心碎", "无助", "罪过"]
    complaint_phrases = ["远离", "转投", "不如", "比不上", "很烦", "很卡", "太丑", "太崩溃了"]
    if any(kw in text for kw in complaint_keywords) or any(ph in text for ph in complaint_phrases):
        return "吐槽/抱怨/负面反馈"
    
    # 5. 购买决策/对比选择 - purchase decisions, comparisons
    purchase_keywords = ["买", "选", "纠结", "二选一", "换", "有必要", "值得", "对比", "vs", "还是", "哪个", "怎么选", "选谁"]
    if any(kw in text for kw in purchase_keywords):
        # Check if it's a complaint about already purchased
        if "买了" not in text and "后悔" not in text and "吐槽" not in text:
            return "购买决策/对比选择"
    
    # 6. 功能体验/使用感受 - usage experience, features
    experience_keywords = ["体验", "感受", "流畅", "丝滑", "好用", "舒服", "爽", "不错", "满意", "喜欢", "爱用", "习惯", "用了", "使用", "发现", "感觉", "质量", "屏幕", "续航", "充电", "信号", "拍照", "音质", "扬声器", "马达", "震动"]
    if any(kw in text for kw in experience_keywords):
        return "功能体验/使用感受"
    
    # 7. 情感/态度/观点表达 - opinions, attitudes, emotional expressions
    attitude_keywords = ["认为", "觉得", "观点", "看法", "态度", "站", "支持", "反对", "自豪", "舒坦", "祛魅", "拥有", "想", "应该", "为什么", "到底"]
    if any(kw in text for kw in attitude_keywords):
        return "情感/态度/观点表达"
    
    # 8. 其他 - update/announcement type posts
    update_keywords = ["更新", "升级", "修复", "版本", "直接更新", "速度更新"]
    if any(kw in text for kw in update_keywords):
        return "资讯/新闻/行业动态"
    
    # Default
    return "其他"


def main():
    # Load input
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    results = []
    category_counts = {cat: 0 for cat in CATEGORIES}
    
    for item in data:
        category = classify_item(item)
        category_counts[category] += 1
        
        result_item = {
            "id": item.get("id"),
            "note_id": item.get("note_id"),
            "nickname": item.get("nickname"),
            "title": item.get("title"),
            "content": item.get("content"),
            "liked_count": item.get("liked_count"),
            "comment_count": item.get("comment_count"),
            "share_count": item.get("share_count"),
            "source_keyword": item.get("source_keyword"),
            "category": category
        }
        results.append(result_item)
    
    # Save output
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # Print summary
    print(f"Total records: {len(results)}")
    print(f"Output saved to: {OUTPUT_PATH}")
    print("\nCategory distribution:")
    for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        if count > 0:
            print(f"  {cat}: {count}")


if __name__ == "__main__":
    main()
