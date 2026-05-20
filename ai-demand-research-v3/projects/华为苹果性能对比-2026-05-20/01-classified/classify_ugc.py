#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对华为苹果性能对比UGC进行分类（Batch 001-003）
三分类：
1. unrelated - 内容不涉及华为苹果在性能/流畅度/稳定性/卡顿/丝滑任一维度的对比或体验
2. incomplete - 信息明显残缺、不知所云、无法判断主题
3. valid - 明确涉及华为vs苹果在性能/流畅度/稳定性/卡顿/丝滑任一维度的对比、体验、评价、讨论
"""

import json
import os

# 定义分类判断函数
def classify_ugc(item):
    """
    根据标题和内容判断UGC分类
    返回 (classification, reason)
    """
    title = item.get("title_cleaned", "").strip()
    content = item.get("content_cleaned", "").strip()
    note_id = item.get("note_id", "")
    
    # 合并标题和内容用于判断
    full_text = (title + " " + content).lower()
    
    # 关键词定义
    # 性能/流畅度/稳定性/卡顿/丝滑相关关键词
    performance_keywords = [
        "性能", "流畅", "丝滑", "卡顿", "掉帧", "稳帧", "帧率", "高刷", "刷新率",
        "系统", "芯片", "处理器", "a17", "a18", "a19", "麒麟", "9000s", "9020", "9030",
        "鸿蒙", "ios", "动画", "打断动画", "跟手", "延迟", "响应", "速度",
        "打游戏", "游戏", "发热", "温控", "功耗", "调度", "后台",
        "卡", "不卡", "顺滑", "流畅度", "稳定性", "稳定"
    ]
    
    # 华为苹果对比相关关键词
    comparison_keywords = [
        "华为", "苹果", "iphone", "huawei", "mate", "pura", "p70", "p80",
        "mate60", "mate70", "mate80", "pura70", "pura80",
        "苹果换华为", "华为换苹果", "果粉转", "转华为", "转苹果",
        "安卓换苹果", "苹果换安卓", "鸿蒙", "ios"
    ]
    
    # 拍照/摄影/屏幕/续航等无关维度（如果仅涉及这些，则为unrelated）
    unrelated_dimensions = [
        "拍照", "摄影", "人像", "live图", "色调", "色彩", "清晰度", "美颜",
        "屏幕", "显示", "分辨率", "亮度", "通透", "oled",
        "续航", "电池", "充电", "快充", "电量",
        "信号", "wifi", "网络",
        "颜值", "外观", "设计", "质感", "做工",
        "价格", "性价比", "预算",
        "生态", "carplay", "airdrop", "隔空投送"
    ]
    
    # 1. 先判断 incomplete
    # 信息明显残缺、不知所云、无法判断主题
    if not title and not content:
        return "incomplete", "标题和内容均为空，无法判断主题"
    
    if not content and len(title) < 5:
        return "incomplete", "内容为空且标题过短，信息残缺"
    
    # 内容过于简短且没有实质信息
    if len(content) < 10 and len(title) < 10:
        return "incomplete", "标题和内容均过短，信息不完整"
    
    # 内容为空或仅有话题标签
    if not content or content.strip() == "":
        # 如果标题有意义，尝试根据标题判断
        if len(title) >= 10 and any(kw in full_text for kw in comparison_keywords):
            pass  # 标题有意义，继续判断
        else:
            return "incomplete", "内容为空，仅有标题或标签"
    
    # 2. 判断是否同时涉及华为和苹果
    has_huawei = any(kw in full_text for kw in ["华为", "huawei", "mate", "pura", "鸿蒙"])
    has_apple = any(kw in full_text for kw in ["苹果", "iphone", "ios", "果粉"])
    
    # 3. 判断是否涉及性能/流畅度/稳定性/卡顿/丝滑维度
    has_performance = any(kw in full_text for kw in performance_keywords)
    
    # 4. 判断是否仅涉及无关维度
    # 如果内容主要讨论拍照、屏幕、续航、信号、颜值、价格、生态等，则为unrelated
    
    # 特殊处理：明确涉及性能/流畅度/卡顿/丝滑的对比
    performance_indicators = [
        "性能", "流畅", "丝滑", "卡顿", "掉帧", "稳帧", "帧率", "高刷",
        "动画", "打断动画", "跟手", "响应", "速度", "系统",
        "芯片", "处理器", "a17", "a18", "a19", "麒麟",
        "打游戏", "游戏", "发热", "温控", "功耗",
        "卡", "不卡", "顺滑", "流畅度", "稳定性", "稳定"
    ]
    
    # 检查是否有明确的性能维度对比
    explicit_performance_comparison = False
    for kw in performance_indicators:
        if kw in full_text:
            explicit_performance_comparison = True
            break
    
    # 如果同时涉及华为和苹果，且有性能相关讨论
    if (has_huawei or has_apple) and explicit_performance_comparison:
        # 进一步确认是否是对比类内容
        # 如果只是单方面提到性能，但来源是华为苹果对比关键词，也算valid
        return "valid", f"明确涉及{'华为vs苹果' if (has_huawei and has_apple) else '华为/苹果'}在性能/流畅度/稳定性维度的对比或体验"
    
    # 如果同时涉及华为和苹果，但没有性能维度
    if has_huawei and has_apple:
        # 检查是否主要是拍照、屏幕、续航等无关维度
        unrelated_focus = False
        unrelated_keywords = ["拍照", "摄影", "人像", "live图", "色调", "色彩", "屏幕", "显示", "续航", "电池", "充电", "信号", "颜值", "外观", "设计", "生态"]
        for kw in unrelated_keywords:
            if kw in full_text:
                unrelated_focus = True
                break
        
        if unrelated_focus and not explicit_performance_comparison:
            return "unrelated", "内容涉及华为苹果对比，但主要讨论拍照/屏幕/续航/信号/颜值/生态等无关维度，不涉及性能/流畅度/稳定性/卡顿/丝滑"
        
        # 如果是选机建议/求推荐类，看是否提到性能/流畅
        if "选" in title or "推荐" in title or "怎么选" in title:
            if explicit_performance_comparison:
                return "valid", "选机讨论中明确涉及性能/流畅度维度的对比"
            else:
                return "unrelated", "选机建议但未明确涉及性能/流畅度/稳定性/卡顿/丝滑维度的对比"
    
    # 如果只涉及华为或苹果单方面
    if has_huawei or has_apple:
        if explicit_performance_comparison:
            # 检查是否有对比意味（如"比"、"对比"、"换"等）
            comparison_indicators = ["比", "对比", "换", "转", "vs", "versus"]
            has_comparison = any(kw in full_text for kw in comparison_indicators)
            if has_comparison:
                return "valid", "涉及华为/苹果与其他品牌的性能/流畅度对比"
        
        # 单方面讨论华为或苹果的性能
        if explicit_performance_comparison:
            # 如果来源关键词是华为苹果对比，且内容涉及性能，算valid
            source_keyword = item.get("source_keyword", "")
            if "华为和苹果" in source_keyword or "华为苹果" in source_keyword:
                return "valid", "来源为华为苹果对比搜索，内容涉及性能/流畅度体验"
    
    # 5. 检查是否是纯拍照对比、屏幕对比、续航对比等
    if has_huawei and has_apple:
        return "unrelated", "内容涉及华为苹果，但未涉及性能/流畅度/稳定性/卡顿/丝滑维度的对比或体验"
    
    # 6. 完全不相关的内容
    if not has_huawei and not has_apple:
        return "unrelated", "内容不涉及华为或苹果"
    
    # 默认情况
    return "unrelated", "内容不符合有效UGC的分类标准"


def process_batch(input_path, output_path):
    """处理单个batch文件"""
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    results = []
    for item in data:
        classification, reason = classify_ugc(item)
        
        # 截取content_cleaned前200字
        content_cleaned = item.get("content_cleaned", "")
        content_preview = content_cleaned[:200] if len(content_cleaned) > 200 else content_cleaned
        
        result = {
            "note_id": item.get("note_id", ""),
            "title_cleaned": item.get("title_cleaned", ""),
            "content_cleaned": content_preview,
            "classification": classification,
            "reason": reason
        }
        results.append(result)
    
    # 保存结果
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # 统计
    stats = {
        "valid": sum(1 for r in results if r["classification"] == "valid"),
        "unrelated": sum(1 for r in results if r["classification"] == "unrelated"),
        "incomplete": sum(1 for r in results if r["classification"] == "incomplete"),
        "total": len(results)
    }
    
    return stats


def main():
    base_dir = "/Users/zhijian/workspace/ai-demand-research-v3/projects/华为苹果性能对比-2026-05-20/01-classified"
    
    all_stats = {}
    
    for batch_num in [1, 2, 3]:
        input_path = os.path.join(base_dir, f"batch_{batch_num:03d}_input.json")
        output_path = os.path.join(base_dir, f"batch_{batch_num:03d}_output.json")
        
        print(f"\n处理 Batch {batch_num:03d}...")
        stats = process_batch(input_path, output_path)
        all_stats[f"batch_{batch_num:03d}"] = stats
        
        print(f"  总计: {stats['total']}")
        print(f"  valid: {stats['valid']} ({stats['valid']/stats['total']*100:.1f}%)")
        print(f"  unrelated: {stats['unrelated']} ({stats['unrelated']/stats['total']*100:.1f}%)")
        print(f"  incomplete: {stats['incomplete']} ({stats['incomplete']/stats['total']*100:.1f}%)")
        print(f"  已保存: {output_path}")
    
    # 汇总统计
    total_all = sum(s['total'] for s in all_stats.values())
    valid_all = sum(s['valid'] for s in all_stats.values())
    unrelated_all = sum(s['unrelated'] for s in all_stats.values())
    incomplete_all = sum(s['incomplete'] for s in all_stats.values())
    
    print(f"\n{'='*50}")
    print("汇总统计:")
    print(f"  总计: {total_all}")
    print(f"  valid: {valid_all} ({valid_all/total_all*100:.1f}%)")
    print(f"  unrelated: {unrelated_all} ({unrelated_all/total_all*100:.1f}%)")
    print(f"  incomplete: {incomplete_all} ({incomplete_all/total_all*100:.1f}%)")


if __name__ == "__main__":
    main()
