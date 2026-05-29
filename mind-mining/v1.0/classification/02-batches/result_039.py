#!/usr/bin/env python3
"""
UGC帖子语义分类脚本 - batch_039
分类结果硬编码，基于LLM语义理解
"""

import json

INPUT_PATH = "/Users/zhijian/workspace/mind-mining/v1.0/classification/02-batches/batch_039.json"
OUTPUT_PATH = "/Users/zhijian/workspace/mind-mining/v1.0/classification/02-batches/result_039.json"

# 硬编码分类结果（基于语义理解）
CLASSIFICATIONS = [
    {
        "note_id": "67e6900f000000001c02b546",
        "category": "real_ugc",
        "reason": "第一人称真实提问，询问华为手机投屏卡顿问题，有明确主题和使用场景"
    },
    {
        "note_id": "67766de7000000000902c922",
        "category": "tutorial",
        "reason": "提供了具体的操作步骤（关闭高级视觉效果）解决卡顿问题，属于教程/攻略"
    },
    {
        "note_id": "6971f763000000000b0102ce",
        "category": "real_ugc",
        "reason": "第一人称真实吐槽，表达mate60卡顿到'社死'的真实情感体验"
    },
    {
        "note_id": "6895a5a400000000230224d1",
        "category": "real_ugc",
        "reason": "第一人称真实抱怨，描述更新系统后卡成ppt的具体问题和愤怒情绪"
    },
    {
        "note_id": "69423eb6000000001f0042ff",
        "category": "real_ugc",
        "reason": "第一人称详细描述mate40 pro突然卡顿的经历，包含具体使用细节和排查过程"
    },
    {
        "note_id": "67dd343e000000001c001536",
        "category": "real_ugc",
        "reason": "第一人称长篇换机心路历程，从p9到mate60 pro的使用体验，包含具体机型、内存数据、销售对话等真实细节"
    },
    {
        "note_id": "69e49dfc000000001a0339d0",
        "category": "real_ugc",
        "reason": "第一人称真实吐槽，描述pura80pro新买的就白屏、卡顿的具体问题，有真实情感"
    },
    {
        "note_id": "685e9a10000000000d024b4c",
        "category": "real_ugc",
        "reason": "第一人称真实使用体验，matex5用了一年卡顿，询问解决办法和替代产品"
    },
    {
        "note_id": "697484140000000022033bc5",
        "category": "tutorial",
        "reason": "明确的教程攻略，列出7步解决卡顿的方法，有操作步骤和指导性质"
    },
    {
        "note_id": "692027bb000000001e038ae4",
        "category": "real_ugc",
        "reason": "第一人称真实提问，询问p80pro纯血鸿蒙卡顿问题，寻求同款用户共鸣"
    },
    {
        "note_id": "683038520000000012001aa2",
        "category": "real_ugc",
        "reason": "第一人称真实经历，描述m40pro莫名其妙卡顿，去过两家官方维修店的具体经历"
    },
    {
        "note_id": "69723205000000001a036143",
        "category": "tutorial",
        "reason": "分享了具体的拯救卡顿方法（备份+恢复出厂设置），包含详细步骤和结果，属于教程"
    },
    {
        "note_id": "69f1902b000000002003a8f8",
        "category": "real_ugc",
        "reason": "第一人称真实吐槽，mate80pro信号问题导致网络卡顿，表达崩溃情绪"
    },
    {
        "note_id": "69e06c1f000000001e00c2d6",
        "category": "info_missing",
        "reason": "标题仅'华为mate40Pro卡顿'，内容为空，无实质信息可判断"
    },
    {
        "note_id": "68baebaa000000001d008cbb",
        "category": "real_ugc",
        "reason": "第一人称真实提问，P80用20多天越来越卡，询问其他用户情况"
    },
    {
        "note_id": "69ba5cef000000002300445c",
        "category": "real_ugc",
        "reason": "第一人称真实体验，描述刷多个app出现卡顿，询问是鸿蒙还是安卓问题"
    },
    {
        "note_id": "69b8deb300000000210101f2",
        "category": "real_ugc",
        "reason": "第一人称真实问题描述，P70Pro开机卡在HUAWEI界面，有具体故障场景"
    },
    {
        "note_id": "69ce8da4000000001a02eb33",
        "category": "real_ugc",
        "reason": "第一人称真实吐槽，mate80第6天刷抖音死机，表达不满情绪"
    },
    {
        "note_id": "6941015d000000001e020459",
        "category": "real_ugc",
        "reason": "第一人称真实提问，询问mate80屏幕卡顿掉帧问题，寻求其他用户反馈"
    },
    {
        "note_id": "69cfdc44000000001b001ddc",
        "category": "real_ugc",
        "reason": "第一人称真实吐槽，mate80看抖音视频加载不出来，表达愤怒情绪"
    },
    {
        "note_id": "69be5377000000002301d686",
        "category": "real_ugc",
        "reason": "第一人称真实抱怨，mate70pro用2个多月频繁卡顿闪退死机"
    },
    {
        "note_id": "6846def10000000020029177",
        "category": "real_ugc",
        "reason": "第一人称详细测评体验，包含颜值、手感、性能、系统、拍照、生态6个维度的真实使用感受，有具体对比（15 PM）和量化描述"
    },
    {
        "note_id": "68c97d01000000001302a1b8",
        "category": "real_ugc",
        "reason": "第一人称真实提问，p40Pro卡顿询问换机建议，有具体机型和存储信息"
    },
    {
        "note_id": "69feb247000000003601eb66",
        "category": "info_missing",
        "reason": "标题情绪化但无实质内容，内容仅为话题标签，无任何具体问题或体验描述"
    },
    {
        "note_id": "6a0eac460000000006035d7d",
        "category": "real_ugc",
        "reason": "第一人称真实吐槽，买了三个月出现卡顿、发热等问题，包含具体使用细节和多个痛点"
    }
]


def main():
    # 读取输入文件验证note_id
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        posts = json.load(f)
    
    # 验证所有帖子都有分类
    input_ids = {p["note_id"] for p in posts}
    output_ids = {c["note_id"] for c in CLASSIFICATIONS}
    
    missing = input_ids - output_ids
    extra = output_ids - input_ids
    
    if missing:
        print(f"警告: 缺少 {len(missing)} 条帖子的分类: {missing}")
    if extra:
        print(f"警告: 有 {len(extra)} 条多余的分类: {extra}")
    
    # 写入结果
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(CLASSIFICATIONS, f, ensure_ascii=False, indent=2)
    
    print(f"分类完成: {len(CLASSIFICATIONS)} 条帖子")
    print(f"输出文件: {OUTPUT_PATH}")
    
    # 统计
    from collections import Counter
    stats = Counter(c["category"] for c in CLASSIFICATIONS)
    print("\n分类统计:")
    for cat, count in stats.most_common():
        print(f"  {cat}: {count}")


if __name__ == "__main__":
    main()
