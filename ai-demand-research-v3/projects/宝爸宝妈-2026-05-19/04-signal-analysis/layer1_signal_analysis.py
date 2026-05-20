#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宝妈育儿类UGC 第一层信号识别脚本
分析 layer1_batch_01.json，生成 layer1_batch_01_signal.json
"""

import json

INPUT_FILE = "/Users/zhijian/workspace/ai-demand-research-v3/projects/宝爸宝妈-2026-05-19/04-signal-analysis/layer1_batch_01.json"
OUTPUT_FILE = "/Users/zhijian/workspace/ai-demand-research-v3/projects/宝爸宝妈-2026-05-19/04-signal-analysis/layer1_batch_01_signal.json"


def analyze_signals(data):
    """
    逐条分析UGC内容，识别四分类信号。
    返回包含原始数据和信号分析结果的列表。
    """
    results = []

    for item in data:
        note_id = item.get("note_id", "")
        title = item.get("title", "")
        content = item.get("content", "")
        full_text = (title + " " + content).strip()

        signals = []

        # ========== 1. 需求信号（Demand Signal） ==========
        # 用户明确表达：想要什么、不满什么、希望改进什么、提出具体建议
        has_demand = False
        demand_reason = ""

        # 明确求助/询问
        if "想问下" in full_text or "求助" in full_text or "请问" in full_text:
            has_demand = True
            demand_reason = "用户明确提出求助/询问"
        # 育儿补贴申领问题 - 明确寻求解决方案
        elif "育儿补贴" in full_text and "咋整" in full_text:
            has_demand = True
            demand_reason = "用户明确表达育儿补贴被占用的问题，寻求处理方案"
        # 建议类表达
        elif "我建议" in full_text or "建议这样问" in full_text:
            has_demand = True
            demand_reason = "用户明确提出建议/改进方案"
        # 寻求中介/推荐
        elif "需要中介" in full_text or "私信我" in full_text:
            has_demand = True
            demand_reason = "用户明确提供/寻求服务推荐"
        # 怎么办类问题
        elif "怎么办" in full_text or "怎么处理" in full_text or "咋整" in full_text:
            has_demand = True
            demand_reason = "用户明确表达困惑并寻求解决方案"

        if has_demand:
            signals.append({
                "signal_type": "需求信号",
                "signal_subtype": "明确求助/建议",
                "evidence": demand_reason,
                "confidence": "高"
            })

        # ========== 2. 使用反馈信号（Experience Signal） ==========
        # 用户没有提需求，但表达了：使用感受、困惑、卡点、满意/不满意
        has_experience = False
        experience_reason = ""
        experience_confidence = "中"

        # 育儿嫂负面体验
        if "育儿嫂" in full_text and ("不好" in full_text or "一言难尽" in full_text or "发疯" in full_text):
            has_experience = True
            experience_reason = "用户表达对育儿嫂服务的不满和困扰"
            experience_confidence = "高"
        # 带娃疲惫体验
        elif "带娃" in full_text and ("累" in full_text or "折磨" in full_text or "崩溃" in full_text):
            has_experience = True
            experience_reason = "用户表达带娃过程中的疲惫和情绪压力"
            experience_confidence = "高"
        # 找阿姨的挫折体验
        elif "找阿姨" in full_text or ("阿姨" in full_text and "真心错付" in full_text):
            has_experience = True
            experience_reason = "用户分享找育儿嫂过程中的负面体验和挫败感"
            experience_confidence = "高"
        # 情绪表达强烈的体验
        elif "逆子" in full_text or "天塌了" in full_text:
            has_experience = True
            experience_reason = "用户表达强烈的育儿情绪和挫败感"
            experience_confidence = "高"
        # 代际冲突体验
        elif "冻她" in full_text or "代际" in full_text or ("爸爸" in full_text and "非得说" in full_text):
            has_experience = True
            experience_reason = "用户表达育儿过程中的代际观念冲突体验"
            experience_confidence = "高"
        # 二胎平衡困扰
        elif "二胎" in full_text and ("心疼" in full_text or "矛盾" in full_text):
            has_experience = True
            experience_reason = "用户表达二胎家庭中平衡关爱的困扰"
            experience_confidence = "高"
        # 全职爸爸体验
        elif "全职爸爸" in full_text or ("爸爸" in full_text and "累" in full_text and "情绪" in full_text):
            has_experience = True
            experience_reason = "用户表达全职育儿角色的身心压力和情绪体验"
            experience_confidence = "高"
        # 养育成本体验
        elif "开支" in full_text or ("花" in full_text and "万" in full_text):
            has_experience = True
            experience_reason = "用户分享育儿经济成本带来的压力体验"
            experience_confidence = "中"
        # 育儿方式反思中的体验
        elif "容错率" in full_text and "焦虑" in full_text:
            has_experience = True
            experience_reason = "用户表达对育儿方式影响孩子心理的体验观察"
            experience_confidence = "高"
        # 凝视式育儿体验
        elif "凝视" in full_text or "直升机" in full_text:
            has_experience = True
            experience_reason = "用户表达对过度控制型育儿方式的观察和反思体验"
            experience_confidence = "高"
        # 鸡娃压力体验
        elif "鸡娃" in full_text or "魔怔" in full_text or "窒息" in full_text:
            has_experience = True
            experience_reason = "用户表达对鸡娃教育方式的负面体验和批判"
            experience_confidence = "高"
        # 生育率杀手/日程压力
        elif "生育率杀手" in full_text or "绝杀" in full_text:
            has_experience = True
            experience_reason = "用户通过分享日程表达育儿负担过重的体验"
            experience_confidence = "高"
        # 育儿嫂第一人称吐槽（体验强烈）
        elif "一年10万" in full_text and "不想干" in full_text:
            has_experience = True
            experience_reason = "育儿嫂第一人称表达工作不满和雇主问题"
            experience_confidence = "高"

        if has_experience:
            signals.append({
                "signal_type": "使用反馈信号",
                "signal_subtype": "情绪/体验表达",
                "evidence": experience_reason,
                "confidence": experience_confidence
            })

        # ========== 3. 关注/讨论信号（Attention Signal） ==========
        # 用户在持续讨论：某功能、某内容、某玩法、某趋势
        attention_topics = []
        attention_confidence = "中"

        # 识别持续讨论的话题
        if "育儿嫂" in full_text:
            attention_topics.append("育儿嫂话题")
        if "爸爸" in full_text and ("育儿" in full_text or "带娃" in full_text or "陪伴" in full_text):
            attention_topics.append("父亲参与育儿话题")
        if "凝视式育儿" in full_text or "过度控制" in full_text:
            attention_topics.append("过度控制型育儿方式")
        if "鸡娃" in full_text or "打压式" in full_text or "名校" in full_text:
            attention_topics.append("鸡娃/教育焦虑话题")
        if "二胎" in full_text or "姐弟" in full_text:
            attention_topics.append("二胎家庭关系话题")
        if "育儿知识" in full_text or "育儿观念" in full_text or "常识" in full_text:
            attention_topics.append("育儿知识/观念话题")
        if "养育成本" in full_text or "开支" in full_text or "花多少钱" in full_text:
            attention_topics.append("育儿成本话题")
        if "体罚" in full_text or "打孩子" in full_text:
            attention_topics.append("体罚/管教方式话题")
        if "叫儿子" in full_text or "叫闺女" in full_text or "独立人格" in full_text:
            attention_topics.append("亲子称呼与独立人格话题")
        if "生育率" in full_text or "生小孩" in full_text or "要不要生" in full_text:
            attention_topics.append("生育决策话题")
        if "宠爱" in full_text or "溺爱" in full_text or "边界" in full_text:
            attention_topics.append("宠爱与溺爱边界话题")
        if "多子女" in full_text or "长子" in full_text or "次子" in full_text:
            attention_topics.append("多子女性格差异话题")
        if "容错率" in full_text or "犯错" in full_text:
            attention_topics.append("孩子犯错与容错教育话题")
        if "比较" in full_text and "别人家孩子" in full_text:
            attention_topics.append("孩子比较与竞争焦虑话题")
        if "崔玉涛" in full_text:
            attention_topics.append("专家育儿知识引用话题")
        if "育儿补贴" in full_text:
            attention_topics.append("育儿补贴政策话题")

        if attention_topics:
            signals.append({
                "signal_type": "关注/讨论信号",
                "signal_subtype": "话题讨论",
                "evidence": "用户在持续讨论以下话题：" + "、".join(attention_topics),
                "confidence": attention_confidence
            })

        # ========== 4. 噪声（Noise） ==========
        # 真正低价值内容：纯表情、无意义感叹、与主题完全无关的闲聊
        is_noise = False
        noise_reason = ""

        # 极短内容判断
        if len(full_text) < 30:
            # 检查是否有实质内容
            if full_text.count("！") + full_text.count("？") + full_text.count("。") <= 1:
                is_noise = True
                noise_reason = "内容过短，缺乏实质信息"

        # 纯情绪感叹
        if "卧槽" in full_text and len(full_text) < 50 and "逆子" not in full_text:
            is_noise = True
            noise_reason = "主要为无意义感叹，缺乏实质内容"

        if is_noise:
            signals.append({
                "signal_type": "噪声",
                "signal_subtype": "低价值内容",
                "evidence": noise_reason,
                "confidence": "中"
            })

        # 构建结果项（与已有输出格式保持一致）
        signal_types = [s["signal_type"] for s in signals]
        # 取第一个信号的理由作为主要理由，若多信号则合并
        if len(signals) == 1:
            signal_reason = signals[0]["evidence"]
            confidence = signals[0]["confidence"]
        elif len(signals) > 1:
            signal_reason = "；".join([f"{s['signal_type']}：{s['evidence']}" for s in signals])
            confidence = "高"
        else:
            signal_reason = "未识别到明确信号"
            confidence = "低"

        result = {
            "note_id": note_id,
            "source_keyword": item.get("source_keyword", ""),
            "title": title,
            "content": content,
            "signal_types": signal_types,
            "signal_reason": signal_reason,
            "confidence": confidence
        }
        results.append(result)

    return results


def main():
    # 1. 读取输入JSON
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"读取到 {len(data)} 条数据")

    # 2. 逐条分析
    results = analyze_signals(data)

    # 3. 统计
    total = len(results)
    with_signals = sum(1 for r in results if r["signal_types"])
    without_signals = total - with_signals

    signal_type_counts = {}
    for r in results:
        for st in r["signal_types"]:
            signal_type_counts[st] = signal_type_counts.get(st, 0) + 1

    print(f"\n分析完成:")
    print(f"  总条数: {total}")
    print(f"  识别到信号: {with_signals}")
    print(f"  未识别信号: {without_signals}")
    print(f"  信号类型分布:")
    for st, cnt in sorted(signal_type_counts.items(), key=lambda x: -x[1]):
        print(f"    {st}: {cnt}")

    # 4. 写入输出JSON
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n结果已写入: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
