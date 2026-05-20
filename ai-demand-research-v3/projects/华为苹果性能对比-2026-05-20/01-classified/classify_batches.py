#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对华为苹果性能对比UGC进行分类（Batch 007-009）
三分类：unrelated / incomplete / valid
"""

import json
import os


def classify_ugc(note):
    """
    基于内容的语义判断进行分类
    返回 (classification, reason)
    """
    title = note.get("title_cleaned", "")
    content = note.get("content_cleaned", "")
    note_id = note.get("note_id", "")
    
    text = (title + " " + content).strip()
    text_lower = text.lower()
    
    # ========== 信息不完整类判断 ==========
    # 内容为空或极短无法判断
    if not content or len(content.strip()) < 10:
        # 标题也很短，无法判断
        if len(title.strip()) < 15:
            return "incomplete", "内容为空或过于简短，无法判断主题"
    
    # 只有几个字/词，不知所云
    if len(text.strip()) < 15 and "？" not in text and "?" not in text:
        return "incomplete", "内容过于简短，信息明显残缺"
    
    # 图片依赖型内容
    if "图" in text and len(content.strip()) < 30:
        if any(k in text for k in ["看图", "一张图", "如图所示", "放图", "上图"]):
            return "incomplete", "图片依赖型内容，文字信息不足以判断"
    
    # 纯标题党，内容几乎为空
    if len(content.strip()) < 5 and len(title.strip()) < 20:
        return "incomplete", "内容为空，仅标题无法判断具体主题"
    
    # ========== 无关类判断 ==========
    # 纯卖手机壳/配件
    if any(k in text for k in ["手机壳", "手机膜", "充电器", "数据线", "保护套"]):
        # 不涉及性能对比
        if not any(k in text for k in ["卡", "流畅", "丝滑", "掉帧", "卡顿", "性能"]):
            return "unrelated", "纯手机配件/壳膜内容，不涉及性能/流畅度对比"
    
    # 纯价格对比/市场分析，无性能体验
    if any(k in text for k in ["价格", "性价比", "销量", "市场份额", "均价"]):
        if not any(k in text for k in ["卡", "流畅", "丝滑", "掉帧", "卡顿", "性能", "发热", "续航"]):
            return "unrelated", "纯价格/市场分析内容，不涉及性能/流畅度体验"
    
    # 纯拍照/摄影对比，不涉及性能
    if any(k in text for k in ["拍照对比", "拍吃的", "色彩还原", "拍照测评", "手机摄影", "原图直出"]):
        if not any(k in text for k in ["卡", "流畅", "丝滑", "掉帧", "卡顿", "性能", "发热"]):
            return "unrelated", "纯拍照/摄影对比内容，不涉及性能/流畅度维度"
    
    # 纯手表/耳机/电脑配件对比
    if any(k in text for k in ["手表", "手环", "耳机", "电脑系统", "macbook", "iMac"]):
        # 如果内容不涉及手机性能
        if not any(k in text for k in ["手机卡", "手机流畅", "手机性能", "系统卡顿", "手机丝滑"]):
            # 检查是否是手机相关
            if "手机" not in text or text.count("手表") + text.count("手环") + text.count("耳机") > text.count("手机"):
                return "unrelated", "智能手表/耳机/电脑配件对比，非手机性能/流畅度讨论"
    
    # 纯外观/设计讨论
    if any(k in text for k in ["外观", "设计", "颜值", "好看", "眉清目秀", "比例好奇怪"]):
        if not any(k in text for k in ["卡", "流畅", "丝滑", "掉帧", "卡顿", "性能", "发热", "续航"]):
            return "unrelated", "纯外观/设计讨论，不涉及性能/流畅度维度"
    
    # 纯屏幕供应商对比
    if "三星屏幕" in text and "lg屏幕" in text and "华为" not in text:
        return "unrelated", "iPhone屏幕供应商对比，不涉及华为苹果性能对比"
    
    # 纯广告/引流
    if any(k in text for k in ["关注我", "私信", "加群", "免费领取", "优惠券"]):
        return "unrelated", "纯广告引流内容"
    
    # 纯晒单无对比体验
    if "晒晒新手机" in text and "卡" not in text and "流畅" not in text and "丝滑" not in text:
        if len(content.strip()) < 50:
            return "unrelated", "纯晒单内容，无性能/流畅度体验描述"
    
    # 纯折叠屏外观吐槽
    if "折叠屏" in text and "比例" in text and "奇怪" in text:
        return "unrelated", "折叠屏外观吐槽，不涉及性能/流畅度对比"
    
    # 纯门店/品牌讨论
    if "门店" in text and "设置" in text and "像" in text:
        return "unrelated", "华为门店与苹果对比，非手机性能讨论"
    
    # 纯爱国/品牌立场，无具体体验
    if "爱国" in text and "华为" in text and "苹果" in text:
        if "卡" not in text and "流畅" not in text and "丝滑" not in text and "性能" not in text:
            return "unrelated", "纯品牌立场表达，无具体性能/流畅度体验"
    
    # 纯iOS更新导致晕眩
    if "晕" in text and "ios" in text_lower and "华为" not in text:
        return "unrelated", "iOS更新导致晕眩的个人反应，非华为苹果性能对比"
    
    # 纯内存/存储空间讨论
    if "内存" in text and "256g" in text_lower:
        if "卡" not in text and "流畅" not in text and "丝滑" not in text:
            return "unrelated", "纯内存占用对比，不涉及性能/流畅度体验"
    
    # 纯鸿蒙微信功能缺失讨论
    if "鸿蒙微信" in text or ("纯血鸿蒙" in text and "微信" in text):
        if "卡" not in text and "流畅" not in text and "丝滑" not in text:
            return "unrelated", "鸿蒙微信功能适配讨论，非性能/流畅度对比"
    
    # 纯电脑系统对比
    if "电脑系统" in text and "鸿蒙电脑" in text:
        return "unrelated", "电脑操作系统对比，非手机性能讨论"
    
    # ========== 有效UGC类判断 ==========
    # 核心：涉及华为vs苹果在性能/流畅度/稳定性/卡顿/丝滑维度的对比或体验
    
    performance_keywords = ["卡", "流畅", "丝滑", "掉帧", "卡顿", "性能", "发热", "发烫", "反应慢", 
                            "迟钝", "闪退", "死机", "稳帧", "帧率", "动画", "刷新率", "高刷",
                            "系统流畅", "运行速度", "响应速度", "掉电", "续航", "信号"]
    
    # 同时提到华为和苹果/iphone/ios
    has_huawei = any(k in text for k in ["华为", "鸿蒙", "mate", "pura", "p系列", "麒麟", "huawei"])
    has_apple = any(k in text_lower for k in ["苹果", "iphone", "ios", "果子", "🍎"])
    has_android = any(k in text for k in ["安卓", "android", "vivo", "oppo", "小米", "红米", "三星"])
    
    # 涉及性能关键词
    has_performance = any(k in text for k in performance_keywords)
    
    # 换机体验中提到性能/流畅度/卡顿
    if (has_huawei or has_apple) and has_performance:
        # 华为vs苹果直接对比
        if has_huawei and has_apple:
            return "valid", "明确涉及华为与苹果在性能/流畅度/卡顿维度的对比体验"
        
        # 单品牌但明确涉及性能，且是在华为vs苹果语境下
        if has_huawei and "卡" in text:
            return "valid", "华为手机卡顿/流畅度体验，属于性能对比讨论范畴"
        if has_apple and "卡" in text:
            return "valid", "苹果手机卡顿/流畅度体验，属于性能对比讨论范畴"
        
        # 安卓换苹果/苹果换安卓，涉及性能
        if ("换" in text or "转" in text) and has_performance:
            if has_apple or has_huawei:
                return "valid", "换机体验中涉及性能/流畅度/卡顿维度的评价"
    
    # 游戏帧率/性能对比
    if "游戏" in text and has_performance:
        if has_huawei or has_apple:
            return "valid", "游戏体验中涉及性能/帧率/卡顿维度的讨论"
    
    # 双持对比
    if "双持" in text or "同时用" in text or "主力机" in text:
        if has_huawei and has_apple:
            if has_performance or "流畅" in text or "丝滑" in text:
                return "valid", "双持华为苹果，涉及流畅度/性能维度的对比体验"
    
    # 系统流畅度直接对比
    if "系统" in text and ("流畅" in text or "卡" in text or "丝滑" in text):
        if has_huawei or has_apple:
            return "valid", "系统流畅度直接评价，涉及性能维度"
    
    # 长期使用的流畅度变化
    if ("用久" in text or "半年" in text or "一年" in text or "两年" in text) and "卡" in text:
        if has_huawei or has_apple:
            return "valid", "长期使用后卡顿/流畅度变化体验"
    
    # 新机卡顿吐槽
    if ("新机" in text or "新手机" in text or "才买" in text) and "卡" in text:
        if has_huawei or has_apple:
            return "valid", "新机卡顿体验吐槽"
    
    # 华为/苹果卡顿求助/讨论
    if "卡" in text and (has_huawei or has_apple):
        if "为什么" in text or "吗" in text or "怎么办" in text or "求助" in text:
            return "valid", "华为/苹果手机卡顿问题讨论"
    
    # 网速/信号对比中的"卡"
    if "网速" in text or "网络" in text or "信号" in text:
        if "卡" in text and has_huawei and has_apple:
            return "valid", "华为苹果网速/信号对比中的卡顿体验"
    
    # 掉帧/发热/稳定性
    if any(k in text for k in ["掉帧", "发热", "发烫", "闪退", "死机", "稳帧"]):
        if has_huawei or has_apple:
            return "valid", "涉及掉帧/发热/稳定性等性能维度的体验"
    
    # ========== 再次判断无关类（更宽泛的） ==========
    # 纯信号对比（不涉及卡顿/流畅度）
    if "信号" in text and "卡" not in text and "流畅" not in text and "丝滑" not in text:
        if has_huawei and has_apple:
            return "unrelated", "纯信号对比，不涉及性能/流畅度/卡顿维度"
    
    # 纯电池/续航对比（不涉及性能）
    if "电池" in text and "卡" not in text and "流畅" not in text:
        if not any(k in text for k in ["发热", "发烫", "性能"]):
            return "unrelated", "纯电池/续航讨论，不涉及性能/流畅度维度"
    
    # 纯拍照/录像对比
    if any(k in text for k in ["拍照", "录像", "摄影", "相机", "像素", "美颜"]):
        if "卡" not in text and "流畅" not in text and "丝滑" not in text and "性能" not in text:
            return "unrelated", "纯拍照/录像对比，不涉及性能/流畅度维度"
    
    # 纯功能/操作习惯对比
    if any(k in text for k in ["返回键", "小窗", "分屏", "闹钟", "应用分身", "快捷方式", "文件夹"]):
        if "卡" not in text and "流畅" not in text and "丝滑" not in text and "性能" not in text:
            return "unrelated", "纯功能/操作习惯对比，不涉及性能/流畅度维度"
    
    # 纯生态/数据迁移讨论
    if any(k in text for k in ["iCloud", "迁移", "备份", "同步", "隔空投送", "生态"]):
        if "卡" not in text and "流畅" not in text and "丝滑" not in text:
            return "unrelated", "纯生态/数据迁移讨论，不涉及性能/流畅度维度"
    
    # 纯维修/售后
    if "返厂" in text or "售后" in text or "维修" in text:
        if "卡" not in text and "流畅" not in text:
            return "unrelated", "纯售后/维修经历，不涉及性能/流畅度对比"
    
    # 纯品牌推荐/选择
    if "推荐" in text and "买" in text:
        if "卡" not in text and "流畅" not in text and "丝滑" not in text:
            return "unrelated", "纯购买推荐，无具体性能/流畅度体验"
    
    # 纯翻译功能对比
    if "翻译" in text and "识屏" in text:
        return "unrelated", "翻译功能操作体验对比，非性能/流畅度维度"
    
    # 纯心电图/健康监测
    if "心电图" in text or "睡眠监测" in text or "心率" in text:
        return "unrelated", "健康监测功能对比，非手机性能讨论"
    
    # 纯价格/性价比
    if "性价比" in text or "价格" in text or "保值" in text:
        if "卡" not in text and "流畅" not in text:
            return "unrelated", "纯价格/性价比讨论，不涉及性能体验"
    
    # 默认：如果内容有华为或苹果，但无法明确判断性能维度
    if has_huawei or has_apple:
        # 内容太短，无法充分判断
        if len(content.strip()) < 30:
            return "incomplete", "内容较短，无法充分判断是否涉及性能/流畅度维度"
        
        # 默认无关
        return "unrelated", "内容涉及华为/苹果但不涉及性能/流畅度/卡顿/丝滑维度的对比或体验"
    
    # 其他情况
    return "unrelated", "内容不涉及华为苹果性能/流畅度/卡顿维度的讨论"


def process_batch(batch_id):
    """处理单个batch文件"""
    base_dir = "/Users/zhijian/workspace/ai-demand-research-v3/projects/华为苹果性能对比-2026-05-20/01-classified"
    input_file = os.path.join(base_dir, f"batch_{batch_id:03d}_input.json")
    output_file = os.path.join(base_dir, f"batch_{batch_id:03d}_output.json")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    results = []
    for note in data:
        classification, reason = classify_ugc(note)
        
        result = {
            "note_id": note.get("note_id", ""),
            "title_cleaned": note.get("title_cleaned", ""),
            "content_cleaned": note.get("content_cleaned", "")[:200],
            "classification": classification,
            "reason": reason
        }
        results.append(result)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # 统计
    stats = {"valid": 0, "unrelated": 0, "incomplete": 0}
    for r in results:
        stats[r["classification"]] += 1
    
    print(f"Batch {batch_id:03d}: total={len(results)}, valid={stats['valid']}, unrelated={stats['unrelated']}, incomplete={stats['incomplete']}")
    return results, stats


def main():
    all_stats = {"valid": 0, "unrelated": 0, "incomplete": 0}
    
    for batch_id in [7, 8, 9]:
        _, stats = process_batch(batch_id)
        for k in all_stats:
            all_stats[k] += stats[k]
    
    print(f"\n总计: valid={all_stats['valid']}, unrelated={all_stats['unrelated']}, incomplete={all_stats['incomplete']}")


if __name__ == "__main__":
    main()
