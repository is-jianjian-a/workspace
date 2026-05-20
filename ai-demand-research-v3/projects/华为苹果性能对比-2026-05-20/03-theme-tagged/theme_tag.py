#!/usr/bin/env python3
"""
华为苹果性能对比UGC主题段落打标脚本
主题：流畅丝滑、卡顿问题、稳定性
"""

import json
import os
import re

# 定义主题关键词模式
THEME_PATTERNS = {
    "流畅丝滑": {
        "keywords": [
            "丝滑", "流畅", "顺滑", "跟手", "动画顺滑", "动画丝滑", "操作丝滑", "操作流畅",
            "系统丝滑", "系统流畅", "很丝滑", "很流畅", "非常丝滑", "非常流畅", "无比丝滑",
            "无比流畅", "极致丝滑", "极致流畅", "丝滑流畅", "流畅丝滑", "丝滑得一比",
            "丝滑到", "流畅到", "丝滑感", "流畅感", "行云流水", "如丝般顺滑", "德芙",
            "响应快", "反应快", "不卡顿", "不卡", "零卡顿", "秒开", "秒响应",
            "全局120", "高刷", "120Hz", "120hz", "高刷新率", "ProMotion",
            "动画效果", "动画质感", "过渡动画", "打断动画", "动画流畅",
            "滑动丝滑", "滑动流畅", "切换丝滑", "切换流畅", "转场丝滑",
            "稳帧", "稳定帧率", "满帧", "不掉帧",
        ],
        "exclude_keywords": ["不丝滑", "不流畅", "卡顿", "掉帧", "卡死", "反应慢", "延迟", "卡卡的", "卡的要死"],
    },
    "卡顿问题": {
        "keywords": [
            "卡顿", "卡死", "卡爆", "卡的要死", "卡卡的", "很卡", "非常卡", "太卡了",
            "掉帧", "掉帧严重", "严重掉帧", "画面掉帧", "视频掉帧", "拍摄掉帧",
            "反应慢", "反应迟钝", "响应慢", "加载慢", "打开慢", "转圈圈", "一直转",
            "延迟", "有延迟", "明显延迟", "加载延迟", "消息延迟", "微信延迟",
            "闪退", "崩溃", "死机", "重启", "bug", "BUG", "卡顿问题", "卡顿现象",
            "卡住", "卡了", "卡住了", "卡一下", "卡一下", "一顿一顿", "一卡一卡",
            "不流畅", "不丝滑", "不跟手", "操作卡顿", "界面卡顿", "动画卡顿",
            "发热卡顿", "发烫卡顿", "过热降频", "降频", "性能下降",
            "杀后台", "后台被杀", "内存不足",
            "打开app要等很久", "点击任何链接都要等很久", "app之间跳转也巨巨巨巨卡",
            "页面卡了", "卡的页面不动", "卡成PPT", "卡成ppt",
            "加载不出来", "显示不出来", "拉进度条", "进度条",
        ],
        "exclude_keywords": ["不卡顿", "不卡", "零卡顿", "不会卡", "没有卡顿"],
    },
    "稳定性": {
        "keywords": [
            "稳定", "不稳定", "系统稳定", "系统不稳定", "很稳定", "非常稳定", "稳定性",
            "闪退", "崩溃", "死机", "重启", "自动重启", "频繁重启", "突然重启",
            "bug", "BUG", "有bug", "有BUG", "各种bug", "莫名bug", "莫名其妙",
            "异常", "显示异常", "界面异常", "功能异常", "系统异常",
            "失灵", "触控失灵", "屏幕失灵", "按键失灵", "识别不上",
            "无响应", "未响应", "程序无响应", "应用无响应",
            "黑屏", "白屏", "花屏", "蓝屏", "冻屏",
            "出错", "报错", "错误", "故障", "问题",
            "适配问题", "软件适配", "应用适配", "兼容性问题", "不兼容",
            "系统问题", "系统bug", "系统崩溃", "系统闪退",
            "发热严重", "发烫严重", "过热", "温度高", "烫手",
            "续航崩", "续航崩了", "电量焦虑", "掉电快", "耗电快",
            "信号差", "信号不好", "没信号", "断流", "网络卡顿", "网络差",
            "识别不了", "无法识别", "识别失败", "支付失败",
        ],
        "exclude_keywords": ["稳定选", "稳定性好", "很稳定", "非常稳定", "系统稳定", "长期稳定"],
    }
}


def extract_sentences(text):
    """将文本按句子分割"""
    # 按换行、句号、感叹号、问号分割
    sentences = re.split(r'[\n。！？\t]+', text)
    return [s.strip() for s in sentences if s.strip() and len(s.strip()) >= 5]


def match_theme(sentence, theme):
    """判断句子是否匹配某个主题"""
    patterns = THEME_PATTERNS[theme]
    keywords = patterns["keywords"]
    exclude_keywords = patterns.get("exclude_keywords", [])

    # 先检查排除词
    for excl in exclude_keywords:
        if excl in sentence:
            return False

    # 检查关键词
    for kw in keywords:
        if kw in sentence:
            return True

    return False


def detect_brand_model(sentence, title, tags):
    """从段落中检测品牌和机型"""
    sentence_lower = sentence.lower()
    title_lower = title.lower()

    # 华为机型匹配
    huawei_models = [
        ("华为Mate60Pro", ["mate60pro", "mate 60 pro", "mate60 pro"]),
        ("华为Mate60", ["mate60", "mate 60"]),
        ("华为Mate70Pro", ["mate70pro", "mate 70 pro", "mate70 pro"]),
        ("华为Mate70", ["mate70", "mate 70"]),
        ("华为Mate80Pro", ["mate80pro", "mate 80 pro", "mate80 pro"]),
        ("华为Mate80", ["mate80", "mate 80"]),
        ("华为Pura70", ["pura70", "pura 70"]),
        ("华为Pura80", ["pura80", "pura 80"]),
        ("华为Pura90", ["pura90", "pura 90"]),
        ("华为P70", ["p70", "p 70"]),
        ("华为P40", ["p40", "p 40"]),
        ("华为P30", ["p30", "p 30"]),
        ("华为P20", ["p20", "p 20"]),
        ("华为Mate40Pro", ["mate40pro", "mate 40 pro", "mate40 pro"]),
        ("华为Mate40", ["mate40", "mate 40"]),
        ("华为Pura X Max", ["pura x max", "puraxmax", "pura x"]),
        ("华为Mate X7", ["mate x7", "matex7"]),
        ("华为Mate X5", ["mate x5", "matex5"]),
        ("华为MatebookGT14", ["matebook gt 14", "matebookgt14"]),
        ("华为Mate60RS", ["mate60rs", "mate 60 rs"]),
        ("华为Mate80RS", ["mate80rs", "mate 80 rs"]),
        ("华为nova15ultra", ["nova 15 ultra", "nova15ultra"]),
    ]

    # 苹果机型匹配
    apple_models = [
        ("iPhone15ProMax", ["iphone15promax", "iphone 15 pro max", "15promax", "15 pro max"]),
        ("iPhone15Pro", ["iphone15pro", "iphone 15 pro", "15pro", "15 pro", "苹果15pro"]),
        ("iPhone15", ["iphone15", "iphone 15", "苹果15", "15"]),
        ("iPhone16ProMax", ["iphone16promax", "iphone 16 pro max", "16promax", "16 pro max"]),
        ("iPhone16Pro", ["iphone16pro", "iphone 16 pro", "16pro", "16 pro", "苹果16pro"]),
        ("iPhone16", ["iphone16", "iphone 16", "苹果16", "16"]),
        ("iPhone17ProMax", ["iphone17promax", "iphone 17 pro max", "17promax", "17 pro max"]),
        ("iPhone17Pro", ["iphone17pro", "iphone 17 pro", "17pro", "17 pro", "苹果17pro"]),
        ("iPhone17", ["iphone17", "iphone 17", "苹果17", "17"]),
        ("iPhone18", ["iphone18", "iphone 18", "苹果18", "18"]),
        ("iPhone14Pro", ["iphone14pro", "iphone 14 pro", "14pro", "14 pro"]),
        ("iPhone14", ["iphone14", "iphone 14", "苹果14", "14"]),
        ("iPhone13", ["iphone13", "iphone 13", "苹果13", "13"]),
        ("iPhone11ProMax", ["iphone11promax", "iphone 11 pro max", "11promax"]),
        ("iPhone4S", ["iphone4s", "iphone 4s", "4s"]),
        ("iPhone6S", ["iphone6s", "iphone 6s", "6s"]),
        ("iPadAir5", ["ipad air 5", "ipadair5"]),
        ("iPad11", ["ipad 11", "ipad11"]),
        ("iPadPro", ["ipad pro", "ipadpro"]),
        ("iPadMini", ["ipad mini", "ipadmini"]),
        ("MacBookPro", ["macbook pro", "macbookpro"]),
        ("AirPodsPro", ["airpods pro", "airpodspro"]),
        ("AppleWatch", ["apple watch", "applewatch"]),
    ]

    found_huawei = []
    found_apple = []

    # 在句子中查找
    for model_name, keywords in huawei_models:
        for kw in keywords:
            if kw in sentence_lower:
                found_huawei.append(model_name)
                break

    for model_name, keywords in apple_models:
        for kw in keywords:
            if kw in sentence_lower:
                found_apple.append(model_name)
                break

    # 如果句子中没有，在title中查找
    if not found_huawei and not found_apple:
        for model_name, keywords in huawei_models:
            for kw in keywords:
                if kw in title_lower:
                    found_huawei.append(model_name)
                    break
        for model_name, keywords in apple_models:
            for kw in keywords:
                if kw in title_lower:
                    found_apple.append(model_name)
                    break

    # 判断品牌
    has_huawei_keyword = any(k in sentence_lower for k in ["华为", "鸿蒙", "huawei", "麒麟", "mate", "pura", "pura x", "p70", "p80", "p90"])
    has_apple_keyword = any(k in sentence_lower for k in ["苹果", "iphone", "ios", "ipad", "mac", "airpods", "a19", "a18", "a17", "a16", "a20", "🍎"])

    if not has_huawei_keyword:
        has_huawei_keyword = any(k in title_lower for k in ["华为", "鸿蒙", "huawei", "麒麟", "mate", "pura", "pura x"])
    if not has_apple_keyword:
        has_apple_keyword = any(k in title_lower for k in ["苹果", "iphone", "ios", "ipad", "mac", "🍎"])

    # 组合结果
    results = []
    if found_huawei:
        results.extend(found_huawei)
    elif has_huawei_keyword:
        results.append("华为")

    if found_apple:
        results.extend(found_apple)
    elif has_apple_keyword:
        results.append("苹果")

    if results:
        return "/".join(sorted(set(results)))

    # 检查tags
    for tag in tags:
        tag_lower = tag.lower()
        if any(k in tag_lower for k in ["华为", "鸿蒙", "huawei", "mate", "pura"]):
            return "华为"
        if any(k in tag_lower for k in ["苹果", "iphone", "ios", "ipad"]):
            return "苹果"

    return "不明确"


def detect_sentiment(sentence, theme):
    """判断情感倾向"""
    sentence_lower = sentence.lower()

    # 明确负面表达（优先级最高）
    explicit_negative = [
        "卡顿", "卡死", "卡爆", "卡的要死", "卡卡的", "很卡", "非常卡", "太卡了", "太卡",
        "掉帧", "反应慢", "反应迟钝", "有延迟", "明显延迟",
        "闪退", "崩溃", "死机", "重启", "自动重启", "频繁重启",
        "不稳定", "系统不稳定", "发热严重", "发烫严重",
        "续航崩", "掉电快", "耗电快", "信号差", "没信号",
        "难用", "垃圾", "失望", "后悔", "无语", "恶心", "恼火",
        "越用越卡", "越来越卡", "用久了卡", "负优化",
        "卡成PPT", "卡的页面不动", "打开app要等很久",
        "不流畅", "不丝滑", "根本不了", "无法", "不能",
        "难用无比", "难用的要命", "bug", "各种问题",
    ]

    # 明确正面表达
    explicit_positive = [
        "很丝滑", "非常丝滑", "无比丝滑", "极致丝滑", "太丝滑了", "丝滑流畅", "丝滑到",
        "很流畅", "非常流畅", "无比流畅", "极致流畅", "太流畅了", "流畅度拉满",
        "不卡顿", "零卡顿", "没有卡顿", "不会卡", "不卡", "一点也不卡",
        "好用", "好用啊", "真的好用", "非常好用", "太好用",
        "稳定", "很稳定", "非常稳定", "系统稳定", "稳定性好", "长期稳定",
        "值得肯定", "爱了", "真香", "满意", "惊喜", "舒服",
    ]

    # 先检查明确负面表达（优先级最高）
    for en in explicit_negative:
        if en in sentence:
            return "负面"

    # 再检查明确正面表达
    for ep in explicit_positive:
        if ep in sentence:
            return "正面"

    # 根据主题判断
    if theme == "流畅丝滑":
        # 如果包含负面词如"卡"、"延迟"等，且没有明确正面词
        if any(w in sentence for w in ["卡", "延迟", "掉帧", "不流畅", "慢"]):
            return "负面"
        if "丝滑" in sentence or "流畅" in sentence or "顺滑" in sentence:
            return "正面"
        return "中性"

    elif theme == "卡顿问题":
        # 卡顿问题主题默认负面
        if any(w in sentence for w in ["不卡", "零卡顿", "没有卡顿", "流畅"]):
            return "正面"
        return "负面"

    elif theme == "稳定性":
        # 稳定性主题
        if "不稳定" in sentence or any(w in sentence for w in ["闪退", "崩溃", "死机", "bug", "失灵", "异常"]):
            return "负面"
        if "稳定" in sentence and "不" not in sentence:
            return "正面"
        if "稳定" in sentence and "不" in sentence:
            return "负面"
        return "中性"

    return "中性"


def generate_reason(sentence, theme, sentiment):
    """生成标注理由"""
    if theme == "流畅丝滑":
        if "丝滑" in sentence and "流畅" in sentence:
            return "用户同时提到丝滑和流畅，表达正面体验"
        elif "丝滑" in sentence:
            return "用户明确提到丝滑体验"
        elif "流畅" in sentence:
            return "用户明确提到流畅体验"
        elif "高刷" in sentence or "120" in sentence:
            return "用户提到高刷新率带来的流畅体验"
        elif "动画" in sentence:
            return "用户提到动画效果流畅"
        elif "跟手" in sentence:
            return "用户提到操作跟手"
        elif "不卡" in sentence or "不卡顿" in sentence:
            return "用户表达不卡顿的正面体验"
        elif "全局" in sentence and "帧" in sentence:
            return "用户提到全局稳帧的流畅体验"
        else:
            return "用户表达流畅/丝滑相关体验"

    elif theme == "卡顿问题":
        if "卡顿" in sentence:
            return "用户明确提到卡顿问题"
        elif "卡死" in sentence:
            return "用户提到卡死问题"
        elif "掉帧" in sentence:
            return "用户提到掉帧问题"
        elif "反应慢" in sentence or "反应迟钝" in sentence:
            return "用户提到反应慢/迟钝问题"
        elif "延迟" in sentence:
            return "用户提到延迟问题"
        elif "加载" in sentence and ("慢" in sentence or "不出来" in sentence):
            return "用户提到加载慢/加载失败问题"
        elif "闪退" in sentence:
            return "用户提到应用闪退"
        elif "发热" in sentence and "卡" in sentence:
            return "用户提到发热导致的卡顿"
        elif "杀后台" in sentence:
            return "用户提到杀后台问题"
        elif "卡成PPT" in sentence or "ppt" in sentence.lower():
            return "用户形容卡顿严重如PPT"
        elif "越用越卡" in sentence or "越来越卡" in sentence:
            return "用户反馈手机越用越卡"
        else:
            return "用户表达卡顿/不流畅相关体验"

    elif theme == "稳定性":
        if "闪退" in sentence:
            return "用户提到应用闪退问题"
        elif "崩溃" in sentence:
            return "用户提到系统/应用崩溃"
        elif "死机" in sentence:
            return "用户提到死机问题"
        elif "重启" in sentence:
            return "用户提到自动/频繁重启"
        elif "bug" in sentence.lower():
            return "用户提到系统/应用bug"
        elif "不稳定" in sentence:
            return "用户提到系统不稳定"
        elif "发热" in sentence or "发烫" in sentence:
            return "用户提到发热/发烫问题"
        elif "信号差" in sentence or "没信号" in sentence or "断流" in sentence:
            return "用户提到信号/网络不稳定"
        elif "续航崩" in sentence or "掉电快" in sentence:
            return "用户提到续航/电池不稳定"
        elif "失灵" in sentence:
            return "用户提到功能失灵"
        elif "适配" in sentence and "问题" in sentence:
            return "用户提到软件适配问题"
        elif "异常" in sentence:
            return "用户提到系统/功能异常"
        elif "稳定" in sentence and "不" not in sentence:
            return "用户表达系统稳定的正面评价"
        else:
            return "用户表达稳定性相关体验"

    return f"用户表达{theme}相关体验"


def process_ugc(ugc):
    """处理单条UGC，返回主题标注结果"""
    results = []
    note_id = ugc["note_id"]
    title = ugc.get("title", "")
    content = ugc.get("content", "")
    tags = ugc.get("tags", [])

    # 合并标题和内容进行分析
    full_text = title + "\n" + content if title else content
    sentences = extract_sentences(full_text)

    # 对每个主题，找到匹配的句子
    for theme in ["流畅丝滑", "卡顿问题", "稳定性"]:
        matched_sentences = []
        for sentence in sentences:
            if match_theme(sentence, theme):
                matched_sentences.append(sentence)

        # 合并相邻的匹配句子
        if matched_sentences:
            # 去重并合并
            unique_sentences = []
            for s in matched_sentences:
                if s not in unique_sentences:
                    unique_sentences.append(s)

            # 如果有多句，尝试合并成段落
            if len(unique_sentences) == 1:
                quote = unique_sentences[0]
            else:
                # 合并为一段
                quote = "；".join(unique_sentences[:3])  # 最多取3句

            # 限制quote长度
            if len(quote) > 300:
                quote = quote[:300] + "..."

            brand_model = detect_brand_model(quote, title, tags)
            sentiment = detect_sentiment(quote, theme)
            reason = generate_reason(quote, theme, sentiment)

            results.append({
                "note_id": note_id,
                "title": title,
                "theme": theme,
                "quote": quote,
                "brand_model": brand_model,
                "sentiment": sentiment,
                "reason": reason
            })

    return results


def process_batch(input_file, output_file):
    """处理单个batch文件"""
    with open(input_file, 'r', encoding='utf-8') as f:
        ugcs = json.load(f)

    all_results = []
    for ugc in ugcs:
        results = process_ugc(ugc)
        all_results.extend(results)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print(f"处理完成: {input_file} -> {output_file}")
    print(f"  输入UGC数量: {len(ugcs)}")
    print(f"  输出标注数量: {len(all_results)}")

    # 统计各主题数量
    theme_counts = {}
    for r in all_results:
        theme = r["theme"]
        theme_counts[theme] = theme_counts.get(theme, 0) + 1
    for theme, count in theme_counts.items():
        print(f"  - {theme}: {count}")

    return all_results


def main():
    base_dir = "/Users/zhijian/workspace/ai-demand-research-v3/projects/华为苹果性能对比-2026-05-20/03-theme-tagged"

    for i in range(1, 5):
        input_file = os.path.join(base_dir, f"batch_{i:03d}_input.json")
        output_file = os.path.join(base_dir, f"batch_{i:03d}_output.json")

        if os.path.exists(input_file):
            process_batch(input_file, output_file)
        else:
            print(f"文件不存在: {input_file}")


if __name__ == "__main__":
    main()
