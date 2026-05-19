#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
复查并修正 all_classified_merged.json 的分类
"""
import json

INPUT_FILE = "/Users/zhijian/workspace/ai-demand-research-v3/projects/宝爸宝妈-2026-05-19/02-classified/all_classified_merged.json"
OUTPUT_FILE = "/Users/zhijian/workspace/ai-demand-research-v3/projects/宝爸宝妈-2026-05-19/02-classified/all_classified_reviewed.json"

# 读取JSON
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"总条数: {len(data)}")

# 统计原始分类
counts = {}
for item in data:
    c = item.get('classification', '未知')
    counts[c] = counts.get(c, 0) + 1
print(f"原始分类统计: {counts}")

# 需要修正的条目: note_id -> 新分类, 原因, 置信度
# 基于内容分析，对25条batch_06的"待复查"条目进行分类

changes = {
    # 1. 早教课有用么？ - 一家三口体验早教课，宝妈育儿类
    "69d34fcf0000000023024ff6": {
        "classification": "宝妈育儿类",
        "reason": "一家三口体验早教课并分享感受，询问其他宝妈早教课效果，属于早教消费决策类育儿内容",
        "confidence": "高"
    },
    # 2. 警惕幼儿邪典视频 - 陪娃看儿歌发现邪典视频
    "67e2ab1c000000001c007cc4": {
        "classification": "宝妈育儿类",
        "reason": "宝妈陪娃看SSS儿歌时发现并警惕幼儿邪典视频，属于儿童安全/早教内容筛选话题",
        "confidence": "高"
    },
    # 3. 儿子两岁，我禁止家人夸他聪明 - 育儿理念分享
    "668b5ddd00000000050051ed": {
        "classification": "宝妈育儿类",
        "reason": "两岁宝妈分享科学育儿理念（如何正确夸赞孩子），属于早教/育儿方法分享",
        "confidence": "高"
    },
    # 4. 2岁，早教已经花了10个W - 早教消费分享
    "68a57b94000000001b0375d5": {
        "classification": "宝妈育儿类",
        "reason": "宝妈详细分享2岁宝宝早教花费和各类早教课程体验，属于早教消费/经验分享",
        "confidence": "高"
    },
    # 5. 新手引导桌游 - 从内容看是早教老师视角
    "697c68f9000000001a01c137": {
        "classification": "宝妈育儿类",
        "reason": "关于儿童桌游/早教游戏引导技巧分享，面向早教工作者和家长，属于早教方法类内容",
        "confidence": "中"
    },
    # 6. 19月龄首次英语早教剧 - 宝妈分享早教体验
    "6a06a06c000000000603637e": {
        "classification": "宝妈育儿类",
        "reason": "宝妈分享19月龄宝宝首次体验英语早教剧的经历和感受，属于早教体验分享",
        "confidence": "高"
    },
    # 7. 果然只有评论区才有英语启蒙大实话 - 英语启蒙求助
    "694a1c41000000001e039906": {
        "classification": "宝妈育儿类",
        "reason": "宝妈分享英语启蒙困惑并求助其他宝妈经验，属于早教/英语启蒙话题",
        "confidence": "高"
    },
    # 8. 曾经人均标配的金宝贝和美吉姆 - 早教行业讨论
    "665dc6aa0000000005007654": {
        "classification": "宝妈育儿类",
        "reason": "宝妈讨论早教行业变化（金宝贝美吉姆关闭），询问现在小月龄宝宝早教去处，属于早教话题",
        "confidence": "高"
    },
    # 9. 0-3岁不踩雷早教绘本合集 - 早教绘本推荐
    "6a09c880000000003501d776": {
        "classification": "宝妈育儿类",
        "reason": "宝妈整理0-3岁早教绘本推荐清单，属于早教资源/绘本推荐类育儿内容",
        "confidence": "高"
    },
    # 10. 干了一个月儿童陪伴师，我跑路了！ - 职业经历，非宝妈视角
    "697f5366000000000a03c227": {
        "classification": "无关类",
        "reason": "内容是儿童陪伴师的职业工作经历吐槽，属于职场/职业话题，非宝妈主动分享的育儿经验",
        "confidence": "高"
    },
    # 11. 亲测体验✨一对一入户早教真香！ - 入户早教体验
    "6a07f0270000000035032728": {
        "classification": "宝妈育儿类",
        "reason": "宝妈分享23月龄宝宝一对一入户早教体验，属于早教服务体验分享",
        "confidence": "高"
    },
    # 12. 上海免费早教-普陀区公益早教 - 早教信息分享
    "69f004ff000000003603046c": {
        "classification": "宝妈育儿类",
        "reason": "分享上海普陀区公益早教预约信息，属于早教资源/福利信息分享",
        "confidence": "高"
    },
    # 13. 当我问DeepSeek有没有必要报早教班 - 早教决策讨论
    "67a4a6d3000000002802908a": {
        "classification": "宝妈育儿类",
        "reason": "讨论是否有必要报早教班，属于早教消费决策类育儿内容",
        "confidence": "高"
    },
    # 14. 送托育的孩子真的很可怜吗 - 托育经验分享
    "681e2115000000002001fc60": {
        "classification": "宝妈育儿类",
        "reason": "宝妈分享孩子上托育的真实经历和进步，反驳托育焦虑，属于托育/早教经验分享",
        "confidence": "高"
    },
    # 15. 我真的好费解 - 蒙氏早教求助
    "68f3a16d000000000500183f": {
        "classification": "宝妈育儿类",
        "reason": "宝妈询问蒙氏早教是什么并求助购买建议，属于早教知识求助",
        "confidence": "高"
    },
    # 16. 宝宝绘本都这样了？ - 绘本内容吐槽
    "6816d3350000000009038997": {
        "classification": "宝妈育儿类",
        "reason": "宝妈吐槽某绘本设计不合理（影子和实物反差大），属于早教绘本/阅读话题",
        "confidence": "高"
    },
    # 17. 真的没人质疑用SSS做英语启蒙的有效性嘛？ - 英语启蒙讨论
    "68c18082000000001c032d9e": {
        "classification": "宝妈育儿类",
        "reason": "宝妈质疑SSS儿歌英语启蒙的有效性并寻求建议，属于早教/英语启蒙方法讨论",
        "confidence": "高"
    },
    # 18. 孩子上了早教和没上有区别吗？ - 内容仅为标题重复，无实质内容
    "69b0240a00000000230387f7": {
        "classification": "信息缺失类",
        "reason": "标题和正文完全重复同一句话，没有任何实质内容或讨论展开",
        "confidence": "高"
    },
    # 19. 当孩子开始说脏话，你的第—反应很重要 - 育儿方法分享
    "67f78137000000001d003e85": {
        "classification": "宝妈育儿类",
        "reason": "宝妈分享3-5岁孩子说脏话的应对方法，属于早教/育儿行为引导内容",
        "confidence": "高"
    },
    # 20. 最近切切乐玩儿的有点疯魔 - 早教玩具分享
    "66d1ccf1000000001f01e610": {
        "classification": "宝妈育儿类",
        "reason": "宝妈分享宝宝玩切切乐玩具的探索过程，属于早教玩具/精细动作发展话题",
        "confidence": "高"
    },
    # 21. 接触蒙氏后惊觉 所有带娃难题都是自找的 - 蒙氏育儿分享
    "68749556000000002201e103": {
        "classification": "宝妈育儿类",
        "reason": "宝妈分享蒙台梭利育儿理念及常见育儿误区分析，属于早教/育儿方法干货",
        "confidence": "高"
    },
    # 22. 原来伊能静早教过悲观感性的女生怎么择偶! - 明星情感内容，非育儿
    "69423845000000000d03e3be": {
        "classification": "无关类",
        "reason": "内容是关于伊能静和秦昊的婚恋关系分析，属于明星情感/亲密关系话题，标题虽有'早教'但实为谐音梗，与儿童早教完全无关",
        "confidence": "高"
    },
    # 23. 早教制造焦虑 - 早教体验吐槽
    "688620670000000010027454": {
        "classification": "宝妈育儿类",
        "reason": "宝妈分享转机构后早教课体验不佳并吐槽制造焦虑，属于早教消费/体验分享",
        "confidence": "高"
    },
    # 24. 我是早教老师，请攻击我最薄弱的地方 - 职场/职业内容
    "67ecc87e000000001d002b89": {
        "classification": "无关类",
        "reason": "早教老师发布的职场互动帖（求批评），属于职业/职场话题，非宝妈育儿经验分享",
        "confidence": "高"
    },
    # 25. 聊一聊国内托育为什么不太流行 - 托育行业讨论
    "69afe78a0000000009023655": {
        "classification": "宝妈育儿类",
        "reason": "讨论国内托育不流行的原因，涉及教育理念、老人带娃等育儿相关话题，属于早教/托育话题",
        "confidence": "高"
    },
}

# 应用修正
changed_count = 0
for item in data:
    note_id = item.get('note_id')
    if note_id in changes:
        old_classification = item.get('classification')
        new_info = changes[note_id]
        item['classification'] = new_info['classification']
        item['reason'] = new_info['reason']
        item['confidence'] = new_info['confidence']
        item['review_changed'] = True
        changed_count += 1
        print(f"修正: {note_id} | {old_classification} -> {new_info['classification']}")

print(f"\n共修正 {changed_count} 条")

# 统计新分类
new_counts = {}
for item in data:
    c = item.get('classification', '未知')
    new_counts[c] = new_counts.get(c, 0) + 1
print(f"\n修正后分类统计: {new_counts}")

# 保存
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n已保存到: {OUTPUT_FILE}")
