#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
华为苹果性能对比UGC情感分类 - batch_001 (20条)
基于语义理解，禁止关键词匹配
"""

import json
import os

# 读取输入
INPUT_PATH = "/Users/zhijian/workspace/ai-demand-research-v3/projects/华为苹果性能对比-2026-05-20/04-sentiment-llm/batch_001_input.json"
OUTPUT_PATH = "/Users/zhijian/workspace/ai-demand-research-v3/projects/华为苹果性能对比-2026-05-20/04-sentiment-llm/batch_001_output.json"

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# 基于语义理解的情感分类结果
results = []

# 逐条分析（基于语义理解，非关键词匹配）
for item in data:
    note_id = item["note_id"]
    title = item.get("title", "")
    content = item.get("content", "")
    full_text = f"{title}\n{content}".strip()

    # 基于语义理解的分类判断
    sentiment = "其他"
    reasoning = ""

    # === 华为好 ===
    if note_id == "67062187000000001b021353":
        # "现在的安卓功能真的比苹果好太多了" "方便程度还是安卓的好" "用了三四年依然很顺滑"
        # 明确表达安卓优于苹果，且推荐安卓
        sentiment = "华为好"
        reasoning = "用户明确表达安卓在功能、便捷性、重量、流畅度等方面优于苹果，且长期用安卓后认为安卓更好"

    elif note_id == "68975a6300000000250176f0":
        # "华为mate40 pro...到现在还在用一点也不卡" "鸿蒙5系统，丝滑流畅"
        # 强调华为手机五年不卡，且新换的pura80也很流畅
        sentiment = "华为好"
        reasoning = "用户通过自身体验证明华为手机长期使用不卡顿，且新机鸿蒙系统丝滑流畅，隐含华为性能/稳定性优秀"

    elif note_id == "698448bc000000000a029496":
        # "鸿蒙6比苹果丝滑" "帧率不抽不卡，太稳定了" "没想到这么好用"
        # 直接对比并明确认为鸿蒙比苹果丝滑稳定
        sentiment = "华为好"
        reasoning = "用户明确表达鸿蒙6比苹果更丝滑、更稳定，且整体使用体验超出预期，强烈推荐"

    elif note_id == "69e6d39100000000210395f1":
        # "比苹果iOS分屏更灵活" "比苹果AirDrop更便捷" "比苹果iOS动画更自然"
        # 多处明确对比并认为鸿蒙优于苹果
        sentiment = "华为好"
        reasoning = "内容多处明确对比，认为鸿蒙在分屏灵活性、跨设备协同便捷性、动画自然度等方面优于苹果iOS"

    elif note_id == "69ec731f00000000350254fe":
        # "影像质感和系统流畅度都提升很明显" "单手拿没负担"
        # 苹果用户转华为，明确认可华为流畅度和影像提升
        sentiment = "华为好"
        reasoning = "资深苹果用户转华为后，明确认可华为系统流畅度和影像质感有明显提升，且重量更轻"

    elif note_id == "69edc524000000003703586a":
        # "鸿蒙真的很流畅...感觉特别流畅跟手" 但前面也说了缺点
        # 虽有缺点，但明确表达鸿蒙流畅度优于iPhone
        sentiment = "华为好"
        reasoning = "用户作为iPhone 17用户，上手华为P90后明确感觉鸿蒙系统特别流畅跟手，优于日常使用的iPhone"

    elif note_id == "69b6cbb60000000021039283":
        # "很多用华为手机...都说用起来很丝滑，就像苹果iOS一样" "三年前的mate60Pro用起来也是流畅的"
        # 强调华为高端机型流畅，与iOS相当
        sentiment = "华为好"
        reasoning = "用户强调华为手机（mate/pura系列）使用体验丝滑流畅，与iOS相当，且旧机型依然流畅"

    # === 苹果好 ===
    elif note_id == "668e6cf40000000003025462":
        # "苹果手感不错，非常流畅" 但主要抱怨屏幕伤眼
        # 虽有正面评价，但核心体验是负面的，且最终卖掉苹果
        sentiment = "其他"
        reasoning = "用户认可苹果手感好、流畅，但核心诉求是屏幕伤眼导致无法使用，最终卖掉苹果，无明确品牌偏好倾向"

    elif note_id == "67865ea0000000000b00f949":
        # "苹果就是比安卓流畅，不服来辩"
        # 明确表达苹果优于安卓
        sentiment = "苹果好"
        reasoning = "用户明确断言苹果比安卓流畅，语气强烈，属于明确站队苹果"

    elif note_id == "68bdad93000000001d019c97":
        # "感觉苹果打游戏比安卓丝滑，是我的错觉吗"
        # 虽是疑问句，但表达的是个人感觉苹果更丝滑
        sentiment = "苹果好"
        reasoning = "用户表达个人感觉苹果打游戏比安卓更丝滑，属于明确倾向苹果的对比判断"

    elif note_id == "6a0b15b7000000003701ea45":
        # "真是不如苹果丝滑方便" "影响工作丝滑度" "心疼自己就买苹果"
        # 多处明确表达苹果在办公场景更丝滑方便
        sentiment = "苹果好"
        reasoning = "用户明确表达华为在办公场景（微信WPS联动、文件解压预览等）不如苹果丝滑方便，且引用'心疼自己就买苹果'"

    elif note_id == "6a0c6e82000000003700dedb":
        # "感受到的丝滑程度华为不可比拟" "系统还是一样优秀丝滑"
        # 明确认为苹果丝滑程度华为无法比拟
        sentiment = "苹果好"
        reasoning = "用户从华为换回苹果后，明确表达苹果的丝滑程度华为不可比拟，系统优秀丝滑"

    # === 其他 ===
    elif note_id == "66f62b08000000002a0308e2":
        # iPhone 15 Pro换iPhone 16的个人体验分享
        # 纯苹果内部对比，无华为相关
        sentiment = "其他"
        reasoning = "内容为iPhone 15 Pro换iPhone 16的个人使用体验，纯苹果产品内部对比，未涉及华为"

    elif note_id == "68ef265300000000050116f9":
        # 四大系统对比，但主要推崇ColorOS，提到iOS和鸿蒙
        # "iOS26说实话用过ColorOS16后，感觉也就那么回事了"
        # 贬低iOS，但主要是推崇OPPO，非华为vs苹果
        sentiment = "其他"
        reasoning = "内容主要推崇ColorOS 16，虽提到iOS和鸿蒙，但核心倾向是OPPO，非华为vs苹果的明确对比"

    elif note_id == "6932b88d000000001e0054b5":
        # "三大系统丝滑程度都是T0级别" "实际差距很小"
        # 中性对比，认为三家都很强，差距小
        sentiment = "其他"
        reasoning = "用户认为iOS、鸿蒙、ColorOS三大系统流畅度都是T0级别，实际差距很小，属于中性客观对比"

    elif note_id == "6937ee45000000001f00c76b":
        # 华为、iPhone、小米人像拍照对比
        # 各有优劣，纯描述差异
        sentiment = "其他"
        reasoning = "内容为华为、iPhone、小米三款手机人像拍照的客观对比，各有优劣，无明确站队"

    elif note_id == "69896b9a000000001a01cba4":
        # "鸿蒙6...更加丝滑" "改得很像iPhone的iOS界面"
        # 描述鸿蒙新版本特性，提到像iOS，无优劣判断
        sentiment = "其他"
        reasoning = "内容描述鸿蒙新版本更丝滑且界面改得像iOS，属于客观描述更新内容，无明确品牌优劣倾向"

    elif note_id == "69a4e37900000000220301ae":
        # "你们的华为mate80pm卡顿么？"
        # 纯提问，无明确倾向
        sentiment = "其他"
        reasoning = "用户纯提问询问华为mate80pm是否卡顿，无明确情感倾向"

    elif note_id == "6628da47000000000401b4c3":
        # "华为mate60pro卡顿问题" 求助帖
        # 抱怨卡顿但不想换，求助解决
        sentiment = "其他"
        reasoning = "用户抱怨华为mate60pro卡顿并求助解决方案，虽有负面情绪但无与苹果的对比，且表示不想换品牌"

    elif note_id == "66bf6e480000000025031352":
        # 华为手机卡顿原因分享，最终解决
        # 分享经验，无苹果对比
        sentiment = "其他"
        reasoning = "用户分享华为手机卡顿原因及解决方法，属于经验分享，未涉及苹果对比"

    results.append({
        "note_id": note_id,
        "sentiment": sentiment,
        "reasoning": reasoning
    })

# 写入输出
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# 统计
huawei = sum(1 for r in results if r["sentiment"] == "华为好")
apple = sum(1 for r in results if r["sentiment"] == "苹果好")
other = sum(1 for r in results if r["sentiment"] == "其他")

print(f"处理完成！共 {len(results)} 条")
print(f"华为好: {huawei} 条")
print(f"苹果好: {apple} 条")
print(f"其他: {other} 条")
print(f"输出文件: {OUTPUT_PATH}")
