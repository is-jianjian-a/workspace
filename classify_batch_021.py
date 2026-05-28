#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UGC 8类分类脚本 - batch_021.json
分类定义：
1. real_ugc - 真实UGC：消费者真实声音，有第一人称视角、具体使用细节、真实情感
2. tutorial - 教程/攻略：教用户怎么做，有操作步骤
3. news - 新闻/行业：客观报道、行业分析
4. spec_comparison - 参数对比：以产品参数为核心的客观对比
5. marketing - 营销/推广：以推广销售为目的，模板化
6. info_missing - 信息不全：仅有标题/标签，正文为空或极少
7. invalid - 无效帖：内容极短无实质观点，或纯表情
8. career - 求职/工作：面试、offer、离职、职场
"""

import json
import re

# ============ 分类规则引擎 ============

def classify_post(post):
    """对单条帖子进行分类，返回 (category, confidence, reason)"""
    title = post.get("title", "") or ""
    content = post.get("content", "") or ""
    nickname = post.get("nickname", "") or ""
    tag_list = post.get("tag_list", "") or ""
    full_text = (title + "\n" + content).strip()
    text_lower = full_text.lower()

    # --- 前置快速判断 ---

    # 1. 无效帖检测 (invalid)
    if is_invalid(content, title):
        return "invalid", 0.95, "内容极短无实质观点或纯表情/符号"

    # 2. 信息不全检测 (info_missing)
    if is_info_missing(content, title):
        return "info_missing", 0.9, "正文为空或极少，仅有标题/标签"

    # 3. 求职/工作检测 (career)
    if is_career(full_text):
        return "career", 0.9, "内容涉及求职、面试、offer、离职、职场"

    # 5. 新闻/行业检测 (news)
    if is_news(full_text, nickname):
        return "news", 0.85, "客观报道、行业分析、市场数据"

    # 6. 参数对比检测 (spec_comparison)
    if is_spec_comparison(full_text):
        return "spec_comparison", 0.85, "以产品参数、硬件规格为核心的对比"

    # 7. 营销/推广检测 (marketing)
    if is_marketing(full_text, nickname):
        return "marketing", 0.85, "推广销售目的，模板化文案，参数罗列"

    # 4. 教程/攻略检测 (tutorial) - 在营销之后，避免教程被误判为营销
    if is_tutorial(full_text):
        return "tutorial", 0.85, "包含操作步骤、教程、攻略、设置方法"

    # 8. 真实UGC检测 (real_ugc)
    if is_real_ugc(full_text, nickname):
        return "real_ugc", 0.85, "消费者真实声音，第一人称视角，具体使用细节，真实情感"

    # 默认 fallback - 根据内容特征智能判断
    return smart_fallback(full_text, nickname)


def smart_fallback(text, nickname):
    """智能 fallback：根据内容特征判断最可能的类别"""
    # 强营销号特征昵称
    strong_marketing_accounts = ["评测", "导购", "精选", "好物", "情报员", "宝贝亚古兽"]
    # 一般营销号特征
    marketing_accounts = ["数码", "科技", "手机", "推荐", "研究所"]
    is_strong_marketing = any(acc in nickname for acc in strong_marketing_accounts)
    is_marketing_account = any(acc in nickname for acc in marketing_accounts)

    # 有第一人称 + 具体体验
    first_person = ["我", "本人", "自己", "我的"]
    has_first_person = any(fp in text for fp in first_person)

    # 主观感受词
    feeling_words = ["感觉", "觉得", "体验", "喜欢", "不喜欢", "满意", "失望", "好用", "难用"]
    has_feeling = any(w in text for w in feeling_words)

    # 客观参数词
    spec_words = ["像素", "处理器", "芯片", "分辨率", "电池", "屏幕", "摄像头", "hz", "mah"]
    spec_count = sum(1 for w in spec_words if w in text.lower())

    # 对比词
    compare_words = ["对比", "vs", "pk", "区别", "差距", "相比", "比较"]
    has_compare = any(w in text.lower() for w in compare_words)

    # 真实情感/细节词（UGC特征）
    ugc_detail_words = ["用了", "一周", "一个月", "平时", "日常", "续航", "信号", "拍照", "卡顿", "流畅", "发热", "充电", "问题", "缺点"]
    ugc_detail_count = sum(1 for w in ugc_detail_words if w in text)

    # 真实情感词
    emotion_words = ["哈哈", "😂", "😭", "😅", "真的", "确实", "居然", "没想到", "吐槽", "抱怨", "惊喜", "失望", "纠结", "终于", "受不了", "爱了"]
    has_emotion = any(w in text for w in emotion_words)

    if is_strong_marketing:
        if has_first_person and (ugc_detail_count >= 2 or has_emotion):
            return "real_ugc", 0.6, "强营销号但有真实UGC特征"
        elif has_compare and spec_count >= 2:
            return "spec_comparison", 0.6, "强营销号+对比+参数，倾向参数对比"
        else:
            return "marketing", 0.6, "强营销号特征，倾向营销"
    elif is_marketing_account:
        if has_first_person and (ugc_detail_count >= 2 or has_emotion):
            return "real_ugc", 0.6, "营销号但有真实UGC特征"
        elif has_compare and spec_count >= 2:
            return "spec_comparison", 0.6, "营销号+对比+参数，倾向参数对比"
        elif spec_count >= 2:
            return "marketing", 0.6, "营销号+参数罗列，倾向营销"
        else:
            return "real_ugc", 0.55, "营销号但无强营销特征，倾向UGC"
    elif has_first_person and (has_feeling or ugc_detail_count >= 2 or has_emotion):
        return "real_ugc", 0.6, "有第一人称+主观感受/细节，倾向真实UGC"
    elif has_compare and spec_count >= 2:
        return "spec_comparison", 0.6, "有对比+参数，倾向参数对比"
    else:
        return "real_ugc", 0.5, "默认分类为真实UGC"


# ============ 各类别判断函数 ============

def is_invalid(content, title):
    """无效帖：内容极短无实质观点，或纯表情/符号"""
    if not content or len(content.strip()) < 5:
        return True
    # 纯表情/符号判断：去除常见标点后几乎为空
    cleaned = re.sub(r'[\u4e00-\u9fff\w]', '', content)
    if len(cleaned) > len(content) * 0.8 and len(content) < 30:
        return True
    return False


def is_info_missing(content, title):
    """信息不全：正文为空或极少，仅有标题/标签"""
    if not content or len(content.strip()) < 10:
        return True
    # 正文极少（少于15个字符）且主要是标签
    if len(content.strip()) < 15 and "#" in content:
        return True
    return False


def is_career(text):
    """求职/工作：面试、offer、离职、职场"""
    career_keywords = [
        "面试", "offer", "离职", "辞职", "跳槽", "简历", "hr", "招聘",
        "求职", "找工作", "入职", "转正", "裁员", "职场", "工作",
        "工资", "薪资", "年终奖", "绩效", "加班", "996", "背调",
        "二面", "三面", "终面", "笔试", "群面", "面经"
    ]
    count = sum(1 for kw in career_keywords if kw in text)
    return count >= 2 or (count >= 1 and any(kw in text for kw in ["面试", "offer", "离职", "求职"]))


def is_tutorial(text):
    """教程/攻略：教用户怎么做，有操作步骤"""
    tutorial_patterns = [
        r"步骤\d", r"第[一二三四五六七八九十\d]步", r"首先.*然后",
        r"打开.*设置", r"点击.*选择", r"进入.*找到",
        r"教程", r"攻略", r"手把手", r"教你", r"怎么设置",
        r"如何开启", r"操作方法", r"设置方法", r"使用技巧",
        r"保姆级", r"一看就会", r"新手必看", r"小白教程"
    ]
    count = sum(1 for p in tutorial_patterns if re.search(p, text))
    return count >= 2


def is_news(text, nickname):
    """新闻/行业：客观报道、行业分析"""
    news_keywords = [
        "据报道", "消息称", "据悉", "业内人士", "分析师",
        "市场份额", "出货量", "销量数据", "行业", "产业链",
        "供应链", "财报", "营收", "同比增长", "季度",
        "发布会", "官宣", "定档", "即将发布", "爆料"
    ]
    # 新闻号特征
    news_accounts = ["情报", "爆料", "快讯", "资讯", "新闻", "科技", "数码报"]
    is_news_account = any(acc in nickname for acc in news_accounts)

    # 导购/推荐类排除（不是新闻）
    exclude_guide = ["怎么选", "如何选择", "推荐", "选购", "预算", "建议"]
    has_guide = any(e in text for e in exclude_guide)

    count = sum(1 for kw in news_keywords if kw in text)
    return (count >= 2 or (is_news_account and count >= 1)) and not has_guide


def is_spec_comparison(text):
    """参数对比：以产品参数为核心的客观对比"""
    spec_keywords = [
        "像素", "光圈", "处理器", "芯片", "cpu", "gpu", "ram", "rom",
        "分辨率", "刷新率", "hz", "mah", "电池容量", "充电功率",
        "跑分", "安兔兔", "geekbench", "帧率", "fps",
        "主摄", "超广角", "长焦", "传感器", "cmos",
        "重量", "厚度", "mm", "克", "g", "英寸"
    ]
    # 对比标记
    comparison_markers = ["对比", "vs", "versus", "pk", "差距", "相较", "相比", "优于", "不如"]
    # 排除个人体验对比（如睡眠监测、拍照效果主观对比）
    exclude_experience = ["睡眠", "监测", "体验", "感受", "手感", "习惯", "喜欢", "觉得"]

    has_comparison = any(m in text.lower() for m in comparison_markers)
    has_exclusion = any(e in text for e in exclude_experience)

    spec_count = sum(1 for kw in spec_keywords if kw in text.lower())
    return has_comparison and spec_count >= 3 and not has_exclusion


def is_marketing(text, nickname):
    """营销/推广：以推广销售为目的，模板化"""
    # 强营销号特征昵称（更严格）
    strong_marketing_accounts = ["评测", "导购", "精选", "好物", "情报员", "宝贝亚古兽"]
    # 一般营销号特征
    marketing_accounts = ["数码", "科技", "手机", "推荐", "研究所"]
    is_strong_marketing = any(acc in nickname for acc in strong_marketing_accounts)
    is_marketing_account = any(acc in nickname for acc in marketing_accounts)

    # 模板化特征 - 强模板化标记
    template_patterns = [
        r"^[\d一二三四五六七八九十]+[\.、]",  # 1. 2. 3. 或 1、2、3、 在行首
        r"✅|❌|‼️|🔥|✨|💫|⭐|🥳|❤️|💬|👉🏻|👇🏻|🌈|🎉",
        r"闭眼入|真香.*种草|安利.*入手|入手不亏|冲了",
        r"售价.*元|价格.*起|国补.*到手",
        r"参数.*：.*\d+|配置.*：.*\d+",
        r"梯队榜|排名.*榜单|上榜.*机皇|封神|顶流",
        r"快来.*看看|评论区.*说说|戳中你心巴|必看",
        r"选哪款.*一句话建议|一句话总结|选购指南",
        r"亮点功能|主打.*适合.*用户",
    ]
    template_count = sum(1 for p in template_patterns if re.search(p, text))

    # 纯参数罗列（大量数字+单位）
    spec_heavy = len(re.findall(r'\d+\.?\d*\s*[英寸mm克gHzhzWwMP]+', text)) >= 5

    # 强推广语气
    promo_words = ["必买", "闭眼入", "真香", "种草", "安利", "抢购", "预售", "冲了", "入手不亏", "必看"]
    promo_count = sum(1 for w in promo_words if w in text)

    # 梯队榜/榜单类营销
    ranking_words = ["梯队", "榜单", "排名", "上榜", "机皇", "封神", "顶流", "销量排行榜"]
    has_ranking = any(w in text for w in ranking_words)

    # 纯标题党/无实质内容
    title_only = len(text.strip()) < 30 and ("？" in text or "?" in text or "！" in text)

    score = 0
    if is_strong_marketing:
        score += 2
    elif is_marketing_account:
        score += 1
    if template_count >= 3:
        score += 2
    elif template_count >= 2:
        score += 1
    if spec_heavy:
        score += 1
    if promo_count >= 2:
        score += 2
    elif promo_count >= 1:
        score += 1
    if has_ranking:
        score += 2
    if title_only:
        score += 1

    # 排除有强UGC特征的内容
    ugc_detail_words = ["用了", "一周", "一个月", "平时", "日常", "续航", "信号", "拍照", "卡顿", "流畅", "发热", "充电", "问题", "缺点", "睡眠", "深度睡眠"]
    ugc_detail_count = sum(1 for w in ugc_detail_words if w in text)
    first_person = ["我", "本人", "自己", "我的"]
    has_first_person = any(fp in text for fp in first_person)
    emotion_words = ["哈哈", "😂", "😭", "😅", "真的", "确实", "居然", "没想到", "吐槽", "抱怨", "惊喜", "失望", "纠结", "终于", "受不了", "爱了"]
    has_emotion = any(w in text for w in emotion_words)

    # 有UGC特征时降低营销判定
    if has_first_person and (ugc_detail_count >= 2 or has_emotion):
        score -= 2
    # 有第一人称但UGC特征不够强时，适当降低
    elif has_first_person and ugc_detail_count >= 1:
        score -= 1

    # 无第一人称但有强模板化特征时，增加营销判定
    if not has_first_person and template_count >= 2:
        score += 1

    return score >= 4


def is_real_ugc(text, nickname):
    """真实UGC：消费者真实声音，第一人称视角、具体使用细节、真实情感"""
    # 第一人称标记
    first_person = ["我", "本人", "自己", "我的"]
    has_first_person = any(fp in text for fp in first_person)

    # 真实使用细节
    detail_markers = [
        "用了", "使用", "体验", "感觉", "觉得", "发现", "遇到", "问题",
        "一天", "一周", "一个月", "平时", "日常", "经常", "有时候",
        "续航", "信号", "拍照", "卡顿", "流畅", "发热", "充电",
        "优点", "缺点", "满意", "失望", "后悔", "值得", "不值"
    ]
    detail_count = sum(1 for m in detail_markers if m in text)

    # 真实情感表达
    emotion_markers = [
        "哈哈", "😂", "😭", "😅", "真的", "确实", "居然", "没想到",
        "吐槽", "抱怨", "惊喜", "失望", "纠结", "犹豫", "终于",
        "受不了", "习惯了", "爱了", "劝退", "种草", "拔草"
    ]
    has_emotion = any(e in text for e in emotion_markers)

    # 排除强营销号（降低权重，不直接排除）
    marketing_accounts = ["数码", "科技", "推荐", "导购", "精选", "好物", "研究所", "情报员", "爆料"]
    is_marketing_account = any(acc in nickname for acc in marketing_accounts)

    score = 0
    if has_first_person:
        score += 2
    if detail_count >= 3:
        score += 2
    if has_emotion:
        score += 1
    if not is_marketing_account:
        score += 1
    else:
        # 营销号但有强UGC特征也可通过
        if has_first_person and detail_count >= 2:
            score += 1

    return score >= 4


# ============ 主程序 ============

def main():
    input_path = "/Users/zhijian/workspace/mind-mining/v1.0/batches/batch_021.json"
    output_path = "/Users/zhijian/workspace/result_batch_021.json"

    # 读取输入
    with open(input_path, "r", encoding="utf-8") as f:
        posts = json.load(f)

    results = []
    category_counts = {}

    for post in posts:
        category, confidence, reason = classify_post(post)

        result = {
            "id": post.get("id"),
            "note_id": post.get("note_id"),
            "nickname": post.get("nickname"),
            "title": post.get("title"),
            "category": category,
            "confidence": confidence,
            "reason": reason,
            # 保留原始字段
            "content": post.get("content"),
            "liked_count": post.get("liked_count"),
            "collected_count": post.get("collected_count"),
            "comment_count": post.get("comment_count"),
            "share_count": post.get("share_count"),
            "tag_list": post.get("tag_list"),
            "source_keyword": post.get("source_keyword"),
            "note_url": post.get("note_url"),
            "time": post.get("time"),
        }
        results.append(result)
        category_counts[category] = category_counts.get(category, 0) + 1

    # 写入输出
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # 打印统计
    print(f"✅ 分类完成！共处理 {len(results)} 条帖子")
    print(f"📁 结果已保存至: {output_path}")
    print("\n📊 分类统计:")
    for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"   {cat}: {count} 条")


if __name__ == "__main__":
    main()
