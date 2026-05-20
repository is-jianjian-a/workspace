#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对华为苹果性能对比UGC进行精确主题段落打标（Batch 001-005）
主题：流畅丝滑、卡顿问题、稳定性
"""

import json
import os


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# 主题关键词映射
THEME_KEYWORDS = {
    "流畅丝滑": [
        "丝滑", "流畅", "顺滑", "丝滑流畅", "非常流畅", "很流畅", "很丝滑",
        "流畅丝滑", "丝滑流畅", "跟手", "动画丝滑", "操作丝滑", "丝滑得一比",
        "丝滑到飞起", "丝滑跟手", "全局120", "120帧", "高刷", "刷新率",
        "不卡", "不卡顿", "零卡顿", "无卡顿", "响应快", "启动快",
        "iOS系统很流畅", "鸿蒙系统很流畅", "鸿蒙真的很流畅", "系统流畅",
        "流畅度", "流畅体验", "流畅度拉满", "久用不卡顿", "越用越顺",
        "傻快", "全局高刷", "稳帧", "稳帧率", "动画流畅", "过渡动画",
        "如丝般顺滑", "德芙", "机圈德芙", "T0级别", "T0选手"
    ],
    "卡顿问题": [
        "卡", "卡顿", "很卡", "非常卡", "卡的要死", "卡死了", "卡爆", "卡哭了",
        "掉帧", "掉帧严重", "掉帧卡顿", "严重掉帧", "锁帧", "锁60帧", "不能保持全局高刷",
        "反应慢", "反应迟钝", "打开慢", "加载慢", "转圈圈", "一直转圈圈",
        "闪退", "频繁闪退", "app闪退", "软件闪退", "页面卡", "页面卡顿",
        "视频卡", "视频卡成PPT", "卡成PPT", "刷视频卡", "刷抖音卡",
        "游戏卡", "打游戏卡", "发热卡顿", "发烫卡顿", "发热掉帧", "发烫掉帧",
        "网络卡顿", "信号卡顿", "延迟高", "有延迟", "微信延迟",
        "打开app要等很久", "点击任何链接都要等很久", "app之间跳转也巨卡",
        "杀后台", "杀后台严重", "内存不够", "内存不足", "存储满了",
        "越用越卡", "用久了卡", "用两年就卡", "三年就卡", "卡顿问题",
        "不流畅", "不丝滑", "卡卡的", "有点卡", "偶尔卡顿", "经常卡顿",
        "莫名卡顿", "莫名其妙卡顿", "卡顿现象", "卡顿严重", "严重卡顿",
        "过渡动画也改成史了", "过度动画", "动画不流畅", "滑动不流畅",
        "点击不灵敏", "反应不灵敏", "触摸不灵敏", "操作不跟手",
        "负优化", "系统卡顿", "鸿蒙卡", "iOS卡", "苹果卡", "华为卡"
    ],
    "稳定性": [
        "稳定", "稳定性", "系统稳定", "极度稳定", "非常稳定", "很稳定",
        "不稳定", "系统崩溃", "死机", "重启", "自动重启", "频繁重启",
        "bug", "有bug", "莫名其妙bug", "莫名bug", "各种bug", "bug多",
        "系统bug", "软件bug", "应用bug", "兼容性问题", "不兼容",
        "适配问题", "软件适配", "应用适配", "app适配", "功能缺失",
        "功能不全", "缺胳膊短腿", "功能无法使用", "无法使用", "不能用",
        "闪退", "频繁闪退", "崩溃", "应用崩溃", "系统崩溃",
        "断流", "信号断流", "网络断流", "断连", "连接不稳定",
        "发热严重", "发烫严重", "过热", "温度过高", "发热降频",
        "电池老化", "电池健康", "续航崩", "续航焦虑", "电量焦虑",
        "系统更新后卡顿", "升级后卡顿", "更新后出问题", "越更新越卡",
        "长期使用", "用三五年", "用三年", "用四年", "用五年", "用六年",
        "耐用", "耐摔", "省心", "靠谱", "不出问题", "零维修",
        "久用不卡", "长期使用流畅", "长期稳定性", "持久流畅",
        "系统干净", "无广告", "纯净模式", "广告多", "弹窗多",
        "值得信赖", "可靠", "值得信赖的品牌", "质量可靠"
    ]
}


def detect_themes(text):
    """检测文本中涉及的主题"""
    themes = set()
    for theme, keywords in THEME_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                themes.add(theme)
                break
    return themes


def extract_quote(text, theme, max_sentences=3):
    """从文本中提取与主题直接相关的1-3句话原文"""
    import re
    # 按句号、感叹号、问号、换行分割成句子
    sentences = re.split(r'[。！？\n]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    keywords = THEME_KEYWORDS.get(theme, [])
    matched = []

    for s in sentences:
        for kw in keywords:
            if kw in s and s not in matched:
                matched.append(s)
                break
        if len(matched) >= max_sentences:
            break

    if not matched:
        return None

    return "，".join(matched) + "。"


def infer_brand_model(quote, title, content, tags):
    """从quote中推断品牌型号"""
    text = quote + " " + title + " " + content
    brand_models = []

    # 华为型号
    huawei_patterns = [
        ("华为", "Mate 60 Pro"), ("华为", "Mate60Pro"), ("华为", "Mate 60"),
        ("华为", "Mate 70"), ("华为", "Mate70"), ("华为", "Mate 80"),
        ("华为", "Mate80"), ("华为", "Mate 90"), ("华为", "Mate90"),
        ("华为", "Pura 70"), ("华为", "Pura70"), ("华为", "Pura 80"),
        ("华为", "Pura80"), ("华为", "Pura 90"), ("华为", "Pura90"),
        ("华为", "P40"), ("华为", "P30"), ("华为", "P20"),
        ("华为", "Mate X5"), ("华为", "Mate X7"), ("华为", "Pura X"),
        ("华为", "PuraX"), ("华为", "Mate 40"), ("华为", "Mate40"),
        ("华为", "nova"), ("华为", "畅享"),
        ("华为", "MateBook"), ("华为", "Matebook"),
        ("华为", "鸿蒙"), ("华为", "HarmonyOS"),
    ]

    # 苹果型号
    apple_patterns = [
        ("苹果", "iPhone 15"), ("苹果", "iPhone15"), ("苹果", "iPhone 16"),
        ("苹果", "iPhone16"), ("苹果", "iPhone 17"), ("苹果", "iPhone17"),
        ("苹果", "iPhone 18"), ("苹果", "iPhone18"),
        ("苹果", "iPhone 14"), ("苹果", "iPhone14"),
        ("苹果", "iPhone 13"), ("苹果", "iPhone13"),
        ("苹果", "iPhone 11"), ("苹果", "iPhone11"),
        ("苹果", "iPhone 4"), ("苹果", "iPhone4"), ("苹果", "iPhone 6"),
        ("苹果", "iPhone6"), ("苹果", "iPhone 4S"), ("苹果", "iPhone4S"),
        ("苹果", "iPad"), ("苹果", "MacBook"), ("苹果", "Macbook"),
        ("苹果", "iOS"), ("苹果", "A17"), ("苹果", "A18"), ("苹果", "A19"),
        ("苹果", "A20"), ("苹果", "A16"),
    ]

    # 通用品牌
    general_patterns = [
        ("华为", "华为"), ("苹果", "苹果"), ("苹果", "iPhone"), ("苹果", "🍎"),
        ("荣耀", "荣耀"), ("荣耀", "Magic"), ("小米", "小米"), ("小米", "红米"),
        ("OPPO", "OPPO"), ("OPPO", "oppo"), ("vivo", "vivo"),
        ("三星", "三星"), ("三星", "Samsung"),
    ]

    found_huawei = False
    found_apple = False
    found_other = False
    other_brand = None

    for brand, pattern in huawei_patterns:
        if pattern in text:
            found_huawei = True
            break

    for brand, pattern in apple_patterns:
        if pattern in text:
            found_apple = True
            break

    for brand, pattern in general_patterns:
        if pattern in text:
            if brand == "华为":
                found_huawei = True
            elif brand == "苹果":
                found_apple = True
            else:
                found_other = True
                other_brand = brand

    if found_huawei and found_apple:
        return "华为/苹果"
    elif found_huawei:
        return "华为"
    elif found_apple:
        return "苹果"
    elif found_other:
        return other_brand
    else:
        # 从tags推断
        for tag in tags:
            tag_lower = tag.lower()
            if "华为" in tag or "huawei" in tag_lower or "鸿蒙" in tag or "mate" in tag_lower or "pura" in tag_lower:
                return "华为"
            if "苹果" in tag or "iphone" in tag_lower or "ios" in tag_lower or "ipad" in tag_lower:
                return "苹果"
        return "未知"


def infer_sentiment(quote, theme):
    """基于quote本身判断情感倾向"""
    negative_words = [
        "卡", "卡顿", "掉帧", "闪退", "崩溃", "死机", "bug", "不流畅",
        "不丝滑", "不跟手", "反应慢", "加载慢", "转圈圈", "卡死",
        "卡爆", "卡哭", "严重", "垃圾", "差", "烂", "恶心", "无语",
        "失望", "后悔", "难用", "烦", "抓狂", "恼火", "痛苦",
        "不如", "比不上", "落后", "退步", "降级", "负优化",
        "缺胳膊短腿", "功能缺失", "不兼容", "适配问题",
        "发热严重", "发烫严重", "过热", "温度过高", "续航崩",
        "不稳定", "出问题", "有问题", "毛病", "缺陷",
        "越用越卡", "用久了卡", "三年就卡", "卡顿问题",
        "锁帧", "不能保持", "不灵敏", "误触", "延迟",
        "莫名其妙", "莫名", "诡异", "奇怪", "异常"
    ]

    positive_words = [
        "丝滑", "流畅", "顺滑", "跟手", "稳定", "省心", "靠谱",
        "好用", "舒服", "爽", "惊喜", "满意", "不错", "优秀",
        "出色", "棒", "强", "厉害", "牛", "赞", "好评",
        "不卡", "无卡顿", "零卡顿", "无广告", "干净",
        "久用不卡", "耐用", "耐摔", "持久", "长期流畅",
        "响应快", "启动快", "加载快", "反应快",
        "全局高刷", "120帧", "稳帧", "T0", "顶级",
        "越来越好", "提升", "改善", "优化", "升级",
        "值得", "推荐", "闭眼入", "首选", "完美"
    ]

    # 主题特殊判断
    if theme == "卡顿问题":
        # 卡顿问题主题默认负面，除非明确说"不卡"
        if "不卡" in quote or "无卡顿" in quote or "零卡顿" in quote:
            return "正面"
        return "负面"

    if theme == "流畅丝滑":
        # 流畅丝滑主题默认正面，除非有否定词
        negation = ["不丝滑", "不流畅", "不够丝滑", "不够流畅", "没有", "不如", "不像", "不是"]
        for neg in negation:
            if neg in quote:
                return "负面"
        return "正面"

    if theme == "稳定性":
        # 稳定性主题
        if "不稳定" in quote or "出问题" in quote or "bug" in quote or "崩溃" in quote or "死机" in quote:
            return "负面"
        if "稳定" in quote or "省心" in quote or "靠谱" in quote or "耐用" in quote:
            return "正面"

    # 通用判断
    neg_count = sum(1 for w in negative_words if w in quote)
    pos_count = sum(1 for w in positive_words if w in quote)

    if neg_count > pos_count:
        return "负面"
    elif pos_count > neg_count:
        return "正面"
    else:
        return "中性"


def process_ugc(ugc):
    """处理单条UGC，生成主题标签"""
    text = ugc.get("title", "") + "\n" + ugc.get("content", "")
    themes = detect_themes(text)

    labels = []
    for theme in themes:
        quote = extract_quote(text, theme)
        if quote:
            brand_model = infer_brand_model(quote, ugc.get("title", ""), ugc.get("content", ""), ugc.get("tags", []))
            sentiment = infer_sentiment(quote, theme)
            labels.append({
                "theme": theme,
                "quote": quote,
                "brand_model": brand_model,
                "sentiment": sentiment
            })

    return {
        "note_id": ugc.get("note_id"),
        "title": ugc.get("title"),
        "content": ugc.get("content"),
        "liked_count": ugc.get("liked_count"),
        "comment_count": ugc.get("comment_count"),
        "share_count": ugc.get("share_count"),
        "collected_count": ugc.get("collected_count"),
        "source_keyword": ugc.get("source_keyword"),
        "tags": ugc.get("tags"),
        "labels": labels
    }


def main():
    base_dir = "/Users/zhijian/workspace/ai-demand-research-v3/projects/华为苹果性能对比-2026-05-20/03-theme-tagged-v2"

    for i in range(1, 6):
        input_file = os.path.join(base_dir, f"batch_{i:03d}_input.json")
        output_file = os.path.join(base_dir, f"batch_{i:03d}_output.json")

        print(f"Processing {input_file}...")
        data = load_json(input_file)
        results = [process_ugc(ugc) for ugc in data]
        save_json(output_file, results)
        print(f"Saved to {output_file}, total {len(results)} UGCs, labeled {sum(len(r['labels']) for r in results)} themes")


if __name__ == "__main__":
    main()
