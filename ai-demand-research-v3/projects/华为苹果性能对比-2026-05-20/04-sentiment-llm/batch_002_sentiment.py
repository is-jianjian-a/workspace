#!/usr/bin/env python3
"""
Batch 002 LLM Sentiment Classification
对华为苹果性能对比UGC做情感分类（华为好/苹果好/其他）
基于语义理解，禁止关键词匹配
"""

import json
import os

INPUT_FILE = "batch_002_input.json"
OUTPUT_FILE = "batch_002_output.json"


def classify_sentiment(item: dict) -> dict:
    """
    基于语义理解对单条UGC做情感分类
    返回: {note_id, sentiment, reasoning}
    """
    note_id = item["note_id"]
    title = item.get("title", "")
    content = item.get("content", "")
    text = f"{title}\n{content}".strip()

    # ============================================================
    # 逐条语义分析
    # ============================================================

    if note_id == "676e4ff60000000013008671":
        # 苹果转安卓两周体验，最终换回苹果
        # 核心语义：安卓(vivo)工作软件不稳定、Google pay刷不了、滑动点击逻辑不习惯
        # 明确结论："🍎是简单的哲学，靠谱"，最终换回苹果
        sentiment = "苹果好"
        reasoning = "用户从安卓(vivo)换回苹果，明确表达苹果更靠谱，吐槽安卓不稳定和交互不习惯"

    elif note_id == "679ee243000000002503c2e3":
        # "以前用安卓机的时候，其他人都说苹果用久了不会卡。等我用苹果以后才知道纯属胡扯八道，该卡还是卡，卡爆！"
        # 核心语义：用户实际使用苹果后发现苹果也会卡，否定了"苹果不卡"的说法
        # 这是吐槽苹果卡顿，但并未说华为好，只是否定苹果神话
        sentiment = "其他"
        reasoning = "用户吐槽苹果也会卡顿，但未与华为做对比，也未表达华为更好的倾向"

    elif note_id == "68540862000000001d00fccd":
        # 华为P40用了5年，"依旧觉着十分好用"，"要不是真的内存坚持不了，还是真的一点不想换"
        # 核心语义：对华为P40高度认可，因内存不足才想换，但不想换
        sentiment = "华为好"
        reasoning = "用户对华为P40使用5年仍高度认可，明确表示不想换机，体现对华为的喜爱"

    elif note_id == "6874f9bc000000001d00d3e7":
        # "鸿蒙系统太卡了，刚开始用都很丝滑，现在真的不行"
        # 核心语义：吐槽鸿蒙系统卡顿
        # 但这是用户对自己华为手机的不满，并未与苹果对比，也未说苹果好
        sentiment = "其他"
        reasoning = "用户吐槽自己的鸿蒙系统卡顿，但未与苹果对比，无品牌倾向对比"

    elif note_id == "689f1043000000001b020395":
        # "用苹果手机的，你们嘴真严啊，打游戏这么卡硬是没人吭声"
        # 核心语义：吐槽苹果手机打游戏卡
        # 未与华为对比，只是吐槽苹果
        sentiment = "其他"
        reasoning = "用户吐槽苹果手机打游戏卡顿，但未与华为做性能对比，无明确品牌倾向"

    elif note_id == "68ac1f5b000000001d0075f0":
        # 华为老用户，华为手机用两三年就卡，想换苹果
        # "听周边的苹果用户都说苹果不卡，真的吗？我有点想换苹果手机了"
        # 核心语义：认为华为卡，对苹果有不卡的期待，想换苹果
        sentiment = "苹果好"
        reasoning = "用户认为华为手机卡顿，听闻苹果不卡后明确表示想换苹果手机"

    elif note_id == "68cfa25f00000000120309cf":
        # "刚上手就这么卡...跟安卓比就是一坨，这下真不如安卓了"
        # 核心语义：iPhone17很卡，不如安卓
        # 未直接提及华为，但"不如安卓"隐含苹果不如其他品牌（含华为）
        sentiment = "其他"
        reasoning = "用户吐槽iPhone17卡顿不如安卓，但未明确提及华为，倾向指向安卓整体而非华为"

    elif note_id == "68f6e8b80000000007021d70":
        # "我是苹果手机➕华为cilp2，后台打开华为智慧生活就不会卡，关掉就会偶尔停顿"
        # 核心语义：解决华为耳机卡顿问题的方法，中性技术分享
        sentiment = "其他"
        reasoning = "用户分享华为耳机与苹果手机搭配的解决方案，无品牌优劣对比倾向"

    elif note_id == "691011ce000000000700840f":
        # "mate60pro＋巨卡...这还怎么遥遥领先啊"
        # 核心语义：吐槽华为mate60pro+卡顿严重
        # 未与苹果对比
        sentiment = "其他"
        reasoning = "用户吐槽华为mate60pro+严重卡顿，但未与苹果对比，无品牌倾向"

    elif note_id == "692da99c000000001e017650":
        # "你们的华为mate60pro卡吗？我是卡的相当无语了...还不如我妈那1000多的手机反应快，还是换苹果吧"
        # 核心语义：华为mate60pro卡顿严重，决定换苹果
        sentiment = "苹果好"
        reasoning = "用户因华为mate60pro严重卡顿，明确表示要换苹果"

    elif note_id == "6936f5ad000000000d037a72":
        # "玩死鸟的一些返祖（针对苹果17的卡顿"..."介意的要么换设备玩，要么只能接受（果子的自适应"
        # 核心语义：吐槽苹果17卡顿，建议换设备或自适应
        # 未明确说华为好
        sentiment = "其他"
        reasoning = "用户吐槽苹果17游戏卡顿，建议换设备，但未明确推荐华为"

    elif note_id == "69384838000000000d03ae23":
        # "华为mate70Pro 6.0相机卡的要死，现在一打开必卡"
        # 核心语义：吐槽华为相机卡顿
        # 未与苹果对比
        sentiment = "其他"
        reasoning = "用户吐槽华为mate70Pro相机卡顿，未与苹果对比，无品牌倾向"

    elif note_id == "693baab1000000001e00fbc4":
        # "流畅度早已不是苹果的专属优势...苹果所谓的流畅早已被甩在身后"
        # 核心语义：明确表达苹果流畅度不如安卓/鸿蒙
        sentiment = "华为好"
        reasoning = "用户明确表达苹果流畅度已被安卓/鸿蒙超越，华为属于鸿蒙阵营"

    elif note_id == "69586ae9000000001e000b4e":
        # "为何安卓手机越用越卡，而鸿蒙系统和苹果系统不会越用越卡"
        # 核心语义：将鸿蒙和苹果并列，认为两者都不会越用越卡
        # 无优劣对比，是平等并列关系
        sentiment = "其他"
        reasoning = "用户将鸿蒙和苹果并列认为都不会越用越卡，无优劣对比，是平等陈述"

    elif note_id == "6959dbd2000000001d03acc1":
        # "华为承诺的'三年不卡顿'已到，华为手机在性能和流畅度上表现良好...整体来看依然表现出色"
        # 核心语义：肯定华为三年不卡顿承诺，整体表现满意
        sentiment = "华为好"
        reasoning = "用户肯定华为'三年不卡顿'承诺兑现，整体性能和流畅度表现满意"

    elif note_id == "686de7f8000000000b02dfb4":
        # "感觉华为比苹果好用，是错觉吗？"..."我觉得挺好用的，一英寸拍照好、系统也流畅，还挺省电的"
        # 核心语义：标题直接问"华为比苹果好用是错觉吗"，内容表达华为好用
        sentiment = "华为好"
        reasoning = "用户标题直接表达华为比苹果好用，内容进一步肯定华为系统流畅、拍照好、省电"

    elif note_id == "68f61a3d0000000003021774":
        # 系统流畅度横评，对比苹果iOS、华为鸿蒙、小米、OPPO
        # 内容：各家都有优点，"苹果iOS一贯流畅"，"华为鸿蒙OS 5目前轻量化流畅性还是不错的"
        # "OPPO的ColorOS 16毫无疑问达到了安卓的流畅巅峰"
        # 结尾："那么对比下来，你们觉得谁更流畅呢？"
        # 核心语义：客观横评，未明确站队，最后反问读者
        sentiment = "其他"
        reasoning = "客观横评四大系统各有优劣，未明确表达华为或苹果谁更好，结尾反问读者"

    elif note_id == "6904ae570000000005013541":
        # "mate40p换17pm好不习惯"..."用了一会儿也没觉得17pm到底哪里好，哪里值得上万的价格"
        # "完全不喜欢啊怎么办，现在看着总想退了，换pura x算了"
        # 核心语义：从华为换苹果后不适应，觉得苹果不值，想退掉换华为pura x
        sentiment = "华为好"
        reasoning = "用户从华为换苹果后不适应，认为苹果不值上万价格，想退掉换回华为"

    elif note_id == "694f6805000000001e0099c6":
        # "感觉系统流畅度还是苹果最好。安卓和鸿蒙流畅度差不多"
        # 核心语义：明确表达苹果流畅度最好，安卓和鸿蒙差不多
        sentiment = "苹果好"
        reasoning = "用户明确表达系统流畅度苹果最好，安卓和鸿蒙差不多"

    elif note_id == "6988504f000000000e03ee1f":
        # "用了几天华为mate70pro+，待机和流畅都不行，换回苹果了，不折腾了"
        # 核心语义：华为mate70pro+待机和流畅都不行，换回苹果
        sentiment = "苹果好"
        reasoning = "用户认为华为mate70pro+流畅度不行，已换回苹果"

    else:
        sentiment = "其他"
        reasoning = "未匹配到已知note_id"

    return {
        "note_id": note_id,
        "sentiment": sentiment,
        "reasoning": reasoning
    }


def main():
    # 读取输入
    input_path = os.path.join(os.path.dirname(__file__), INPUT_FILE)
    output_path = os.path.join(os.path.dirname(__file__), OUTPUT_FILE)

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = []
    for item in data:
        result = classify_sentiment(item)
        results.append(result)

    # 写入输出
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # 打印统计
    stats = {"华为好": 0, "苹果好": 0, "其他": 0}
    for r in results:
        stats[r["sentiment"]] += 1

    print(f"处理完成，共 {len(results)} 条")
    print(f"统计: 华为好={stats['华为好']}, 苹果好={stats['苹果好']}, 其他={stats['其他']}")
    print(f"输出文件: {output_path}")


if __name__ == "__main__":
    main()
