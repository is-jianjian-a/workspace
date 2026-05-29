#!/usr/bin/env python3
"""
UGC帖子语义分类脚本 - batch_015
读取 batch_015.json，输出 result_015.json
分类结果基于LLM语义理解硬编码
"""

import json

INPUT_PATH = "/Users/zhijian/workspace/mind-mining/v1.0/classification/02-batches/batch_015.json"
OUTPUT_PATH = "/Users/zhijian/workspace/mind-mining/v1.0/classification/02-batches/result_015.json"

# 基于LLM语义理解的分类结果（硬编码）
CLASSIFICATION_RESULTS = [
    {
        "note_id": "6a0b0594000000003502123d",
        "category": "real_ugc",
        "reason": "第一人称真实使用体验，用户反馈华为mate80pm实况图卡顿问题，有具体机型和具体问题"
    },
    {
        "note_id": "6800ee53000000001c034e12",
        "category": "real_ugc",
        "reason": "第一人称换机心路历程，从苹果13pro换到华为mate70pro，详细描述了信号、充电、拍照、系统操作等真实使用感受，有具体数据和个人适应过程"
    },
    {
        "note_id": "6991bebf000000001a02ec29",
        "category": "real_ugc",
        "reason": "第一人称真实换机失败经历，十几年果粉转华为用了一个多月又换回苹果，有个人心路历程和真实感受"
    },
    {
        "note_id": "676e1c37000000000b023a87",
        "category": "real_ugc",
        "reason": "第一人称真实使用吐槽，mate60pro发热严重、掉帧，虽然短但有具体问题和机型"
    },
    {
        "note_id": "68b2da40000000001b02086f",
        "category": "real_ugc",
        "reason": "第一人称拍照对比体验，详细对比了iPhone16Pro和华为Pura80Pro+的色彩还原和细节表现，最后表达了个人偏好"
    },
    {
        "note_id": "6a0b1774000000003700cad3",
        "category": "real_ugc",
        "reason": "第一人称有明确主题的提问讨论，用户mate40pro用了4年准备换机，列出了具体预算、需求和品牌纠结，寻求建议"
    },
    {
        "note_id": "664ea3960000000015011f6a",
        "category": "news",
        "reason": "客观行业信息汇总，列举各品牌手机耐用性，无个人使用体验，属于一般性资讯内容"
    },
    {
        "note_id": "6863ab950000000023006ba6",
        "category": "real_ugc",
        "reason": "第一人称真实拍照对比体验，晚上同时用苹果16promax和华为pura70Ultra拍摄，详细对比了色彩还原度、清晰度和AI算法效果"
    },
    {
        "note_id": "6a093174000000000803eb6b",
        "category": "info_missing",
        "reason": "内容过短，仅有标题和两个话题标签，无实质观点或可判断意图的内容"
    },
    {
        "note_id": "6853a089000000001d00ce4b",
        "category": "news",
        "reason": "转述第三方测评内容（小白测评），引用他人评测数据对比华为Pura80Ultra和iPhone16ProMax视频拍摄，无个人使用体验"
    },
    {
        "note_id": "60cf5fc2000000000102734e",
        "category": "real_ugc",
        "reason": "第一人称主观观点，用户表达鸿蒙、安卓、苹果三大系统UI越来越像的个人感受，有明确主观判断"
    },
    {
        "note_id": "6502a9bf000000001e03c48a",
        "category": "real_ugc",
        "reason": "第一人称真实使用体验，描述了mate60pro的手感、外观和拍照效果，并与iPhone14promax对比，有个人真实感受"
    },
    {
        "note_id": "65295485000000001e02c42b",
        "category": "real_ugc",
        "reason": "第一人称真实自拍对比体验，用华为mate60pro和苹果iPhone14pro在阴天傍晚车内拍摄，详细对比了不同模式效果并表达个人审美偏好"
    },
    {
        "note_id": "649941ec0000000013011738",
        "category": "real_ugc",
        "reason": "第一人称真实售后体验对比，详细描述了苹果售后和华为售后的服务差异，有具体地点、具体事件和个人感受"
    },
    {
        "note_id": "60f3c8dd000000000102decc",
        "category": "real_ugc",
        "reason": "第一人称真实观察和提问，用户发现同样的小红书APP在华为手机上占用内存比苹果多3G，有具体数据和真实困惑"
    },
    {
        "note_id": "63ae5f33000000001f020eda",
        "category": "spec_comparison",
        "reason": "以产品参数为核心的客观对比，重点对比华为1440Hz和苹果480Hz的PWM调光频率参数，属于硬件规格对比"
    },
    {
        "note_id": "66f0ec1e000000002c014837",
        "category": "real_ugc",
        "reason": "第一人称真实到店体验对比，用户亲自到门店测试苹果、小米、华为、vivo多款手机拍照效果，有具体机型和详细观察"
    },
    {
        "note_id": "6875ee32000000000d01a302",
        "category": "news",
        "reason": "明星资讯类内容，主要报道明星龚俊使用华为pura80Pro，核心是 celebrity news，手机只是附属信息"
    },
    {
        "note_id": "6864efb9000000001c03470a",
        "category": "real_ugc",
        "reason": "第一人称双持使用体验，详细分享了mate70RS和iPhone16pro在不同场景（商务、影像、游戏、社交）下的使用感受，有个人真实体验"
    },
    {
        "note_id": "66eea845000000002603ce4d",
        "category": "marketing",
        "reason": "格式整齐、模板化的购机推荐，一句一品牌的通用推荐语，无具体数据、无个人使用体验，属于推广类内容"
    },
    {
        "note_id": "68c62a39000000001c0113bc",
        "category": "marketing",
        "reason": "简短的产品推荐内容，带有店铺话题标签（买家电到苏宁易购），无个人使用体验，属于销售推广"
    },
    {
        "note_id": "66267cd3000000001c0059bd",
        "category": "real_ugc",
        "reason": "第一人称真实使用体验，描述了爬山和地铁场景下华为与苹果的信号差异，有具体场景和个人多次经历"
    },
    {
        "note_id": "68bf9e06000000001c035951",
        "category": "spec_comparison",
        "reason": "以产品拆机内部结构和散热设计为核心的客观对比，展示6款旗舰手机的工业设计，属于参数/规格对比"
    },
    {
        "note_id": "69294ffb000000001e0353f1",
        "category": "spec_comparison",
        "reason": "以各品牌灵动岛/通知岛功能为核心的客观对比，列举各厂商技术实现，属于功能规格对比"
    },
    {
        "note_id": "67277dc8000000001b02fbeb",
        "category": "news",
        "reason": "行业分析类内容，引用鸿蒙设备数量、应用数量等市场数据，无个人使用体验，属于行业资讯"
    }
]


def main():
    # 读取输入文件（验证存在性）
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        batch_data = json.load(f)

    print(f"读取到 {len(batch_data)} 条帖子")
    print(f"分类结果数量: {len(CLASSIFICATION_RESULTS)}")

    # 验证所有note_id匹配
    input_ids = {item["note_id"] for item in batch_data}
    result_ids = {item["note_id"] for item in CLASSIFICATION_RESULTS}

    if input_ids != result_ids:
        missing = input_ids - result_ids
        extra = result_ids - input_ids
        if missing:
            print(f"警告: 缺少分类的note_id: {missing}")
        if extra:
            print(f"警告: 多余的note_id: {extra}")
    else:
        print("所有note_id匹配正确")

    # 写入结果文件
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(CLASSIFICATION_RESULTS, f, ensure_ascii=False, indent=2)

    print(f"结果已保存到: {OUTPUT_PATH}")

    # 统计分类分布
    from collections import Counter
    categories = Counter(item["category"] for item in CLASSIFICATION_RESULTS)
    print("\n分类分布:")
    for cat, count in categories.most_common():
        print(f"  {cat}: {count}")


if __name__ == "__main__":
    main()
