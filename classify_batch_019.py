#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UGC分类脚本 - batch_019.json
8类分类体系：
1. real_ugc    - 真实UGC
2. tutorial    - 教程/攻略
3. news        - 新闻/行业
4. spec_comparison - 参数对比
5. marketing   - 营销/推广
6. info_missing - 信息不全
7. invalid     - 无效帖
8. career      - 求职/工作
"""

import json
import os

# 分类定义映射
CATEGORY_MAP = {
    "real_ugc": "真实UGC",
    "tutorial": "教程/攻略",
    "news": "新闻/行业",
    "spec_comparison": "参数对比",
    "marketing": "营销/推广",
    "info_missing": "信息不全",
    "invalid": "无效帖",
    "career": "求职/工作",
}


def classify_item(item):
    """
    基于内容语义对单条UGC进行分类
    返回 (category, category_name, reason)
    """
    title = item.get("title", "")
    content = item.get("content", "")
    text = (title + " " + content).lower()
    nickname = item.get("nickname", "")

    # 1. invalid 最优先 - 与手机完全无关或极短无实质内容
    if len(content.strip()) < 10 and len(title.strip()) < 5:
        return "invalid", CATEGORY_MAP["invalid"], "内容过短，无实质观点"

    # 2. career - 求职/工作相关
    career_keywords = ["面试", "求职", "招聘", "离职", "工作", "入职", "薪资", "offer", "hr", "简历", "跳槽"]
    if any(kw in text for kw in career_keywords):
        if any(kw in text for kw in ["华为公司", "苹果公司", "苹果面试", "华为面试", "入职华为", "入职苹果"]):
            return "career", CATEGORY_MAP["career"], "涉及求职/工作相关内容"

    # 判断是否有个人体验/主观观点
    personal_experience_markers = [
        "我觉得", "我认为", "我感觉", "我用", "我的", "我自己", "体验", "感受", "吐槽",
        "喜欢", "不喜欢", "满意", "不满意", "后悔", "值得", "不值", "推荐", "不推荐",
        "入手", "买了", "换了", "使用", "用了", "试了一下", "亲测", "实测", "个人觉得",
        "个人感受", "心得", "体会", "发现", "注意到", "观察到"
    ]
    has_personal = any(kw in text for kw in personal_experience_markers)

    # 检查是否有具体数据（量化信息）
    has_specific_data = any(char.isdigit() for char in content) and any(
        kw in text for kw in ["万", "像素", "mah", "w", "hz", "gb", "英寸", "mm", "g", "元", "nit", "倍", "mp"]
    )

    # 检查结构化格式（参数罗列常见）
    structured_format = any(kw in text for kw in ["📌", "✅", "❌", "•", "·", "【", "】", "→", "▶", "◆", "📊", "📱", "📷"])
    bullet_points = content.count("\n•") + content.count("\n-") + content.count("\n·") + content.count("\n📌")

    # 3. tutorial - 教程/攻略（真正的操作指导）
    tutorial_indicators = [
        "怎么设置", "如何设置", "设置教程", "设置方法", "设置步骤", "配置方法", "配置教程",
        "使用教程", "使用技巧", "操作步骤", "操作方法", "调节方法", "调节教程",
        "必学", "教你", "手把手", "一步步", "傻瓜式", "零基础"
    ]
    is_tutorial = any(ind in text for ind in tutorial_indicators)
    has_steps = any(kw in text for kw in ["第一步", "第二步", "第三步", "step", "步骤", "1.", "2.", "3.", "①", "②", "③"])
    if is_tutorial and has_steps:
        return "tutorial", CATEGORY_MAP["tutorial"], "包含明确的操作步骤或设置方法指导"

    # 4. spec_comparison - 参数对比（以参数为核心的客观对比）
    spec_indicators = [
        "参数", "配置", "规格", "对比表", "一图看懂", "一表看懂", "参数对比",
        "处理器", "芯片", "屏幕", "电池", "像素", "hz", "mah", "gb", "ram", "rom",
        "主摄", "长焦", "超广角", "光圈", "分辨率", "刷新率", "ppi", "nit",
        "mm", "g", "重量", "厚度", "尺寸", "pro", "max", "ultra"
    ]
    spec_count = sum(1 for ind in spec_indicators if ind in text)
    is_spec_heavy = spec_count >= 6

    comparison_markers = ["对比", "vs", "🆚", "区别", "差异", "升级"]
    is_comparison = any(m in title.lower() or m in content.lower() for m in comparison_markers)

    # 参数对比：大量参数+结构化格式+对比意图，且无个人体验
    if is_spec_heavy and is_comparison:
        if bullet_points >= 3 or structured_format:
            if not has_personal:
                return "spec_comparison", CATEGORY_MAP["spec_comparison"], "以产品参数和规格为核心的客观对比"

    # 参数对比兜底：标题明确+参数密度极高+无个人体验
    if "参数对比" in title and not has_personal:
        if spec_count >= 5:
            return "spec_comparison", CATEGORY_MAP["spec_comparison"], "标题明确为参数对比，且内容以参数规格为主"

    # 参数对比兜底2：参数密度极高+无个人体验+对比意图
    if is_spec_heavy and not has_personal and is_comparison:
        return "spec_comparison", CATEGORY_MAP["spec_comparison"], "参数密度高且以对比为主，无个人体验"

    # 5. news - 新闻/行业报道（客观报道，无个人体验）
    news_indicators = [
        "发布", "发布会", "宣布", "推出", "上市", "定价", "售价", "价格公布",
        "行业", "市场", "销量", "份额", "财报", "营收", " reportedly"
    ]
    news_title_patterns = ["来了", "发布", "上市", "推出", "官宣", "定档", "预售", "开售", "正式发布"]
    is_news_title = any(pat in title for pat in news_title_patterns)

    if is_news_title and not has_personal:
        if any(kw in text for kw in news_indicators):
            return "news", CATEGORY_MAP["news"], "客观报道产品发布/上市/行业信息，无个人体验"

    # 6. marketing - 营销/推广（推广销售目的，模板化夸赞，无具体数据/个人体验）
    marketing_indicators = [
        "千万别买", "不然你会后悔", "让你心动", "太绝", "必入", "闭眼入", "冲",
        "绝绝子", "yyds", "神仙", "宝藏", "绝了", "惊艳", "真香",
        "入手不亏", "相信我", "必须分享", "强烈推荐", "强烈推荐",
        "不买后悔", "错过", "限量", "抢购", "秒杀", "福利"
    ]
    marketing_count = sum(1 for ind in marketing_indicators if ind in text)
    is_marketing_style = marketing_count >= 2

    # 营销风格 + 无个人体验 + 无具体数据
    if is_marketing_style and not has_personal and not has_specific_data:
        return "marketing", CATEGORY_MAP["marketing"], "营销推广风格，模板化夸赞，无具体数据支撑"

    # 7. info_missing - 信息不全（内容过短或空疑问句）
    if len(content.strip()) < 15:
        if "?" in title or "？" in title or ("怎么" in title and len(content.strip()) < 30):
            return "info_missing", CATEGORY_MAP["info_missing"], "内容过短或为标题党式空疑问句，无法判断意图"

    # ===== 兜底分类 =====

    # 有具体数据+对比结构+无个人体验 → spec_comparison（如果参数密度高）
    if is_spec_heavy and structured_format and not has_personal:
        return "spec_comparison", CATEGORY_MAP["spec_comparison"], "以参数规格为核心的结构化内容"

    # 营销风格+具体数据 → real_ugc（有数据即使营销风格也归UGC）
    # 有营销风格但无个人体验无数据 → marketing
    if is_marketing_style and not has_personal and not has_specific_data:
        return "marketing", CATEGORY_MAP["marketing"], "营销推广风格内容"

    # real_ugc 兜底 - 有具体数据、个人体验、真实观点
    return "real_ugc", CATEGORY_MAP["real_ugc"], "有具体使用细节、真实观点或量化数据"


def main():
    input_path = "/Users/zhijian/workspace/mind-mining/v1.0/batches/batch_019.json"
    output_path = "/Users/zhijian/workspace/result_batch_019.json"

    # 读取输入
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = []
    for item in data:
        category, category_name, reason = classify_item(item)
        result = {
            "id": item["id"],
            "note_id": item["note_id"],
            "title": item["title"],
            "category": category,
            "category_name": category_name,
            "source_keyword": item.get("source_keyword", ""),
            "liked_count": item.get("liked_count", 0),
            "comment_count": item.get("comment_count", 0),
            "reason": reason,
        }
        results.append(result)

    # 写入输出
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # 统计
    stats = {}
    for r in results:
        cat = r["category"]
        stats[cat] = stats.get(cat, 0) + 1

    print(f"✅ 分类完成！共处理 {len(results)} 条数据")
    print(f"📁 输出文件: {output_path}")
    print("\n📊 分类统计:")
    for cat, count in sorted(stats.items(), key=lambda x: -x[1]):
        name = CATEGORY_MAP.get(cat, cat)
        print(f"  {cat:20s} ({name:8s}): {count:3d} 条")


if __name__ == "__main__":
    main()
