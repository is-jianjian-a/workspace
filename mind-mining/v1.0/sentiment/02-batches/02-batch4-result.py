#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch 4 品牌情绪识别脚本
输入: 02-batch4-input.json (25条UGC, 第76-100条)
输出: 02-batch4-result.json
"""

import json
import os

INPUT_PATH = "/Users/zhijian/workspace/mind-mining/v1.0/sentiment/02-batches/02-batch4-input.json"
OUTPUT_PATH = "/Users/zhijian/workspace/mind-mining/v1.0/sentiment/02-batches/02-batch4-result.json"


def analyze_batch4():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        posts = json.load(f)

    results = []
    opinion_counter = 0

    # ========== Post 1: 6944df23000000001f00778e ==========
    post = posts[0]
    results.append({
        "opinion_id": "batch4_1_1",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "苹果用了差不多12年了，换了8部左右",
        "brand_target": "苹果",
        "sentiment_polarity": "中性",
        "sentiment_intensity": "弱",
        "sentiment_reason": "用户陈述自己使用苹果12年、换过8部的事实，无明确情绪倾向，仅为背景说明",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_1_2",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "个人喜好偏向华为，但我怕使用习惯适应不了华为，好纠结",
        "brand_target": "华为",
        "sentiment_polarity": "混合",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户表达'个人喜好偏向华为'（正向倾向），但又'怕使用习惯适应不了华为'（负向担忧），整体处于纠结状态，情绪混合",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })

    # ========== Post 2: 69e3491b00000000230239a3 ==========
    post = posts[1]
    results.append({
        "opinion_id": "batch4_2_1",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "个人认为对比pocket4的画质确实提升很多",
        "brand_target": "其他",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户认为Pocket4画质'确实提升很多'，对大疆产品有明确正向评价，但本任务品牌范围不含大疆，brand_target标记为'其他'",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_2_2",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "之前一直没入3，很大一部分是因为画质的问题，这次4画质问题是真的改善很多，细节都做的很好",
        "brand_target": "其他",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户指出Pocket4画质'改善很多'、'细节都做的很好'，是对大疆产品的正向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })

    # ========== Post 3: 68c111e6000000001c011a2e ==========
    post = posts[2]
    results.append({
        "opinion_id": "batch4_3_1",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "17pro颜色又丑性价比又低",
        "brand_target": "苹果",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户直接评价iPhone17pro'颜色又丑性价比又低'，情绪明确负向",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_3_2",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "17标准版的性价比真的高，颜色还很好看",
        "brand_target": "苹果",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户评价iPhone17标准版'性价比真的高，颜色还很好看'，情绪明确正向",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })

    # ========== Post 4: 674431b5000000000202ada5 ==========
    post = posts[3]
    # 纯疑问句，无明确观点，不提取

    # ========== Post 5: 6995a524000000001a01c960 ==========
    post = posts[4]
    results.append({
        "opinion_id": "batch4_5_1",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "更喜欢16的黑，给要买手机的朋友们一个参考",
        "brand_target": "苹果",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "弱",
        "sentiment_reason": "用户表达更喜欢iPhone16的黑色，对iPhone16外观有轻微正向偏好",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })

    # ========== Post 6: 6947fd4f000000001d03d2a8 ==========
    post = posts[5]
    results.append({
        "opinion_id": "batch4_6_1",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "苹果用腻了",
        "brand_target": "苹果",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "弱",
        "sentiment_reason": "用户说'苹果用腻了'，表达对苹果的厌倦情绪，轻微负向",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_6_2",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "网上很多人说好，我觉得款式也蛮好看的",
        "brand_target": "华为",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "弱",
        "sentiment_intensity": "弱",
        "sentiment_reason": "用户认为华为'款式也蛮好看的'，对华为外观有轻微正向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_6_3",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "又怕买了华为会卡",
        "brand_target": "华为",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户担心'买了华为会卡'，对华为流畅性有明确负向担忧",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": True
    })

    # ========== Post 7: 6a0c6850000000000602186e ==========
    post = posts[6]
    results.append({
        "opinion_id": "batch4_7_1",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "转华为后，可玩性比苹果高了不止一个Level",
        "brand_target": "华为",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "强",
        "sentiment_reason": "用户明确表示转华为后'可玩性比苹果高了不止一个Level'，对华为可玩性有强烈正向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_7_2",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "质感很好，到手像第一次用iPhone5s和iPhoneX一样惊喜，爱不释手",
        "brand_target": "华为",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "强",
        "sentiment_reason": "用户评价华为'质感很好'，'爱不释手'，情绪强烈正向",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_7_3",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "鸿蒙流畅度很惊喜，跟苹果不相上下",
        "brand_target": "华为",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "强",
        "sentiment_reason": "用户认为鸿蒙'流畅度很惊喜，跟苹果不相上下'，对华为系统流畅度高度认可",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": True
    })
    results.append({
        "opinion_id": "batch4_7_4",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "就创新而言，确实遥遥领先了",
        "brand_target": "华为",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "强",
        "sentiment_reason": "用户认为华为'创新而言，确实遥遥领先'，对华为创新有强烈正向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })

    # ========== Post 8: 66b8963900000000050238e4 ==========
    post = posts[7]
    results.append({
        "opinion_id": "batch4_8_1",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "每年iPhone最难用的时候一定是夏天，三十多度的天气稍微玩玩就发烫降亮度",
        "brand_target": "苹果",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户指出iPhone夏天'发烫降亮度'，对苹果发热问题有明确负向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": True
    })
    results.append({
        "opinion_id": "batch4_8_2",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "鸿蒙的动画和跟手性绝对是体验最好的，从iOS换到鸿蒙也不会有什么不适应",
        "brand_target": "华为",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "强",
        "sentiment_reason": "用户认为鸿蒙'动画和跟手性绝对是体验最好的'，对华为系统流畅度和跟手性高度认可",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": True
    })
    results.append({
        "opinion_id": "batch4_8_3",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "在功能性和实用性方面安卓本身就是完爆苹果的，像是比较实用的分屏、长截图、NFC门禁卡、骚扰拦截这些软件功能一直都有苹果用户吐槽，但苹果也从来没有加上",
        "brand_target": "苹果",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户指出苹果在分屏、长截图、NFC等功能上'从来没有加上'，对苹果功能性缺失有明确负向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_8_4",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "如果iOS的目标群体是全球用户，那么华为一定更懂中国人。尤其是移动支付方面，华为的智慧感知简直太方便了",
        "brand_target": "华为",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "强",
        "sentiment_reason": "用户认为'华为一定更懂中国人'，智慧感知'简直太方便了'，对华为本地化体验高度认可",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_8_5",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "今年iPad Pro的发布让我彻底想退坑了，除了OLED屏幕确实没什么升级，价格倒是贵了不少",
        "brand_target": "苹果",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户认为iPad Pro'除了OLED屏幕确实没什么升级，价格倒是贵了不少'，对苹果产品升级诚意负向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_8_6",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "体验了一下刚发布的MatePad Pro12.2柔光版，丝滑的想让我想换掉我的20款iPad Pro了，华为手机和平板之间的联动也非常好用",
        "brand_target": "华为",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "强",
        "sentiment_reason": "用户认为MatePad Pro'丝滑的想让我想换掉iPad Pro'，华为联动'非常好用'，强烈正向",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": True
    })
    results.append({
        "opinion_id": "batch4_8_7",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "华为WatchGT系列主流的功能一个没少，续航却比Apple Watch好太多，从一天一充换成一周一充的体验简直不要太好",
        "brand_target": "华为",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "强",
        "sentiment_reason": "用户认为华为手表'续航却比Apple Watch好太多'，体验'简直不要太好'，强烈正向",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_8_8",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "如果你现在用的是iPhone的标准版或者准备入手16的标准版，不妨尝试换到同样价位的华为Pura或者Mate系列，一定会感觉到巨大的变化",
        "brand_target": "华为",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "强",
        "sentiment_reason": "用户推荐从iPhone标准版换到华为Pura/Mate系列，认为'一定会感觉到巨大的变化'，强烈正向推荐",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })

    # ========== Post 9: 67bbf3ad000000000901773d ==========
    post = posts[8]
    # 纯疑问句，无明确观点，不提取

    # ========== Post 10: 69ec072d0000000035025be7 ==========
    post = posts[9]
    # 纯疑问句，无明确观点，不提取

    # ========== Post 11: 694f6805000000001e0099c6 ==========
    post = posts[10]
    results.append({
        "opinion_id": "batch4_11_1",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "感觉系统流畅度还是苹果最好",
        "brand_target": "苹果",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户认为'系统流畅度还是苹果最好'，对苹果流畅度有明确正向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": True
    })
    results.append({
        "opinion_id": "batch4_11_2",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "安卓和鸿蒙流畅度差不多",
        "brand_target": "华为",
        "sentiment_polarity": "中性",
        "sentiment_intensity": "弱",
        "sentiment_reason": "用户认为安卓和鸿蒙'流畅度差不多'，无明显情绪倾向，为中性比较",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": True
    })
    results.append({
        "opinion_id": "batch4_11_3",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "vivo的屏幕感官比华为强一些，感觉华为的屏幕冷白冷白的",
        "brand_target": "华为",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "弱",
        "sentiment_reason": "用户认为华为屏幕'冷白冷白的'，相比vivo屏幕感官弱，对华为屏幕有轻微负向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_11_4",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "vivo的屏幕感官比华为强一些",
        "brand_target": "vivo",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "弱",
        "sentiment_reason": "用户认为vivo屏幕感官比华为强，对vivo屏幕有轻微正向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })

    # ========== Post 12: 6a051d3500000000080315a1 ==========
    post = posts[11]
    # 纯疑问句，不提取

    # ========== Post 13: 6804f2a3000000001c02866e ==========
    post = posts[12]
    results.append({
        "opinion_id": "batch4_13_1",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "安卓看起来动画什么的，也挺流畅的，动效也好看，但是用起来就是轻飘飘的手感，不踏实",
        "brand_target": "安卓",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户认为安卓'用起来就是轻飘飘的手感，不踏实'，虽然承认动画流畅，但整体体验负向",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": True
    })
    results.append({
        "opinion_id": "batch4_13_2",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "苹果的iOS用起来就是很成熟稳重的流畅，体验起来差别挺大的",
        "brand_target": "苹果",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户认为苹果iOS'很成熟稳重的流畅'，与安卓形成对比，对苹果流畅度正向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": True
    })

    # ========== Post 14: 686de7f8000000000b02dfb4 ==========
    post = posts[13]
    results.append({
        "opinion_id": "batch4_14_1",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "华为新的鸿蒙系统有些功能和苹果类似，音乐锁屏一样可以放大，有可以调节参数的滤镜",
        "brand_target": "华为",
        "sentiment_polarity": "中性",
        "sentiment_intensity": "弱",
        "sentiment_reason": "用户指出华为鸿蒙有些功能和苹果类似，为功能描述，无明显情绪倾向",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_14_2",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "我觉得挺好用的，一英寸拍照好、系统也流畅，还挺省电的",
        "brand_target": "华为",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户认为华为Pura80 Pro+'拍照好、系统也流畅，还挺省电'，多个维度正向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": True
    })

    # ========== Post 15: 696b8020000000000a03304a ==========
    post = posts[14]
    results.append({
        "opinion_id": "batch4_15_1",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "苹果很卡，华为就很快，真的有这么大的差异吗？iPhone下载只有1.7m，华为300多",
        "brand_target": "苹果",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "强",
        "sentiment_reason": "用户实测iPhone下载速度'只有1.7m'且'很卡'，与华为300多形成强烈对比，对苹果WiFi性能强烈负向",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": True
    })
    results.append({
        "opinion_id": "batch4_15_2",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "华为就很快",
        "brand_target": "华为",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "强",
        "sentiment_reason": "用户实测华为WiFi速度'300多'且'很快'，对华为网络性能强烈正向",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": True
    })

    # ========== Post 16: 68613fd40000000012023b16 ==========
    post = posts[15]
    results.append({
        "opinion_id": "batch4_16_1",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "mate70PRO更宽反而握着更舒服，16PROMAX有点硌手，不好单手操作",
        "brand_target": "华为",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户认为mate70PRO'握着更舒服'，相比16PROMAX'硌手'，对华为握持感正向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_16_2",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "16PROMAX有点硌手，不好单手操作",
        "brand_target": "苹果",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户认为16PROMAX'有点硌手，不好单手操作'，对苹果握持感负向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_16_3",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "华为相机好、信号好、充电快",
        "brand_target": "华为",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户明确评价华为'相机好、信号好、充电快'，多维度正向",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_16_4",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "苹果屏幕更细腻、信号差、充电慢",
        "brand_target": "苹果",
        "sentiment_polarity": "混合",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户评价苹果'屏幕更细腻'（正向）但'信号差、充电慢'（负向），情绪混合",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_16_5",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "实测苹果的待机时间更久",
        "brand_target": "苹果",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户实测'苹果的待机时间更久'，对苹果续航有正向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })

    # ========== Post 17: 669772070000000005004ad5 ==========
    post = posts[16]
    results.append({
        "opinion_id": "batch4_17_1",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "最大的感受就是信号，华为真的不是强的一点半点…在地下室、电梯、大的室内剧院等地方，苹果信号必差！但是华为刷短视频、下载、游戏啥的真的无压力",
        "brand_target": "华为",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "强",
        "sentiment_reason": "用户认为华为信号'不是强的一点半点'，在地下室、电梯等场景'无压力'，强烈正向",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_17_2",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "苹果信号必差",
        "brand_target": "苹果",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "强",
        "sentiment_reason": "用户明确指出在地下室、电梯等场景'苹果信号必差'，对苹果信号强烈负向",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_17_3",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "返回功能：这点苹果做的也是很差，而且很不好用，华为（等一众安卓手机）的返回功能就特别好用",
        "brand_target": "苹果",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户认为苹果返回功能'做的也是很差，而且很不好用'，对苹果交互负向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_17_4",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "华为（等一众安卓手机）的返回功能就特别好用",
        "brand_target": "华为",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户认为华为返回功能'特别好用'，对华为交互正向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_17_5",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "震动反馈：这一项上华为扣大分，体验和苹果比差的不是一点半点。华为这震动马达我真的想把它彻底关掉，有的时候真的是噪音，毫无体验感可言",
        "brand_target": "华为",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "强",
        "sentiment_reason": "用户认为华为震动'扣大分'、'差的不是一点半点'、'毫无体验感可言'，强烈负向",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_17_6",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "操作系统：都很流畅",
        "brand_target": "华为",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "弱",
        "sentiment_reason": "用户认为华为和苹果'都很流畅'，对华为系统流畅度轻微正向",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": True
    })
    results.append({
        "opinion_id": "batch4_17_7",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "和iOS比，在很多细节上还是有差距的，我一十几年的苹果老用户肯定是更站队苹果",
        "brand_target": "苹果",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户认为iOS'在很多细节上还是有差距的'（优于鸿蒙），'更站队苹果'，对苹果系统正向",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_17_8",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "网上测评都说华为手机不适合游戏，应该还是处理器的原因",
        "brand_target": "华为",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户指出'华为手机不适合游戏'、'处理器的原因'，对华为游戏性能负向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": True
    })
    results.append({
        "opinion_id": "batch4_17_9",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "苹果最大的缺点就是信号差，除了这点，其它没有什么硬伤",
        "brand_target": "苹果",
        "sentiment_polarity": "混合",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户指出苹果'最大的缺点就是信号差'（负向），但'其它没有什么硬伤'（正向），情绪混合",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })

    # ========== Post 18: 69b3cce6000000002200ced6 ==========
    post = posts[17]
    results.append({
        "opinion_id": "batch4_18_1",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "华为Mate 80 pro真用不习惯",
        "brand_target": "华为",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "强",
        "sentiment_reason": "用户明确表示'华为Mate 80 pro真用不习惯'，情绪强烈负向",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_18_2",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "用鸿蒙系统的感觉不好用！太难用了",
        "brand_target": "华为",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "强",
        "sentiment_reason": "用户认为鸿蒙'不好用！太难用了'，情绪强烈负向",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_18_3",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "有些APP软件真的不完善",
        "brand_target": "华为",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户指出华为'有些APP软件真的不完善'，对鸿蒙生态负向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_18_4",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "希望华为能顶起来",
        "brand_target": "华为",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "弱",
        "sentiment_reason": "用户表达'希望华为能顶起来'，虽整体吐槽但含期待情绪，轻微正向",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })

    # ========== Post 19: 6852730f000000001203da93 ==========
    post = posts[18]
    results.append({
        "opinion_id": "batch4_19_1",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "整体的环境光华为和OPPO还原的比较好",
        "brand_target": "华为",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户认为华为'环境光还原的比较好'，对华为拍照有正向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_19_2",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "这组整体来说华为拍的最接近实际观感",
        "brand_target": "华为",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户认为华为'拍的最接近实际观感'，对华为拍照色彩还原正向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_19_3",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "苹果拍的整体有些发黄",
        "brand_target": "苹果",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户认为苹果'拍的整体有些发黄'，对苹果拍照色彩负向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_19_4",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "华为对于建筑颜色还原的比较好，但是天空有些过于蓝了",
        "brand_target": "华为",
        "sentiment_polarity": "混合",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户认为华为'建筑颜色还原的比较好'（正向），但'天空有些过于蓝了'（负向），情绪混合",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_19_5",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "OPPO相对还原",
        "brand_target": "OPPO",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "弱",
        "sentiment_reason": "用户认为OPPO拍照'相对还原'，对OPPO拍照轻微正向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })

    # ========== Post 20: 68e75b37000000000300d635 ==========
    post = posts[19]
    results.append({
        "opinion_id": "batch4_20_1",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "大屏换小屏的体验感太好了",
        "brand_target": "苹果",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户认为从16promax换到17pro'体验感太好了'，对苹果17pro正向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_20_2",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "实测电池可以跟16promax平起平坐",
        "brand_target": "苹果",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户实测17pro电池'可以跟16promax平起平坐'，对17pro续航正向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_20_3",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "发热问题改善了很多，这一代真的没必要用max了",
        "brand_target": "苹果",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户认为17pro'发热问题改善了很多'，对苹果发热控制正向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": True
    })

    # ========== Post 21: 68eb629f0000000004000ed1 ==========
    post = posts[20]
    results.append({
        "opinion_id": "batch4_21_1",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "手感好，轻薄不硌手，没有头重脚轻的感觉",
        "brand_target": "苹果",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户认为iPhone Air'手感好，轻薄不硌手'，对苹果手感正向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_21_2",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "发热控制比较好，虽然不及17pro系列，在户外30度高亮度4G环境，依旧感觉不到烫手",
        "brand_target": "苹果",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户认为iPhone Air'发热控制比较好'，户外使用'感觉不到烫手'，对苹果发热控制正向",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": True
    })
    results.append({
        "opinion_id": "batch4_21_3",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "单扬声器，这个纯主观感受",
        "brand_target": "苹果",
        "sentiment_polarity": "中性",
        "sentiment_intensity": "弱",
        "sentiment_reason": "用户指出单扬声器为'纯主观感受'，未明确表达好坏倾向，为中性描述",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_21_4",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "扬声器播放特定音频会滋啦滋啦响，或者50%音量以上也会出现",
        "brand_target": "苹果",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户指出扬声器'滋啦滋啦响'，属于17pro及air通病，对苹果扬声器负向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })

    # ========== Post 22: 699d48dd000000002800b6bc ==========
    post = posts[21]
    results.append({
        "opinion_id": "batch4_22_1",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "信号确实比苹果好很多，之前苹果在家里信号1格也是醉了，现在基本4-5格",
        "brand_target": "华为",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "强",
        "sentiment_reason": "用户认为华为信号'比苹果好很多'，从苹果1格到华为4-5格，强烈正向",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_22_2",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "之前苹果在家里信号1格也是醉了",
        "brand_target": "苹果",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户指出苹果在家'信号1格也是醉了'，对苹果信号负向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_22_3",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "电池确实缓解了我的焦虑，之前苹果半天充一次，现在最多可以2天充一次",
        "brand_target": "华为",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "强",
        "sentiment_reason": "用户认为华为电池'缓解了我的焦虑'，从苹果半天一充到华为最多2天一充，强烈正向",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_22_4",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "音乐播放音质一般，特别是连接车载蓝牙时",
        "brand_target": "华为",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户认为华为'音乐播放音质一般'，对华为音质负向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_22_5",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "输入法响应的速度比苹果慢",
        "brand_target": "华为",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户认为华为'输入法响应的速度比苹果慢'，对华为输入法负向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": True
    })
    results.append({
        "opinion_id": "batch4_22_6",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "已经适配鸿蒙系统的APP基本都是阉割版本",
        "brand_target": "华为",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户指出鸿蒙APP'基本都是阉割版本'，对鸿蒙生态负向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_22_7",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "手机太大，单手操作确实麻烦",
        "brand_target": "华为",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "弱",
        "sentiment_reason": "用户认为华为手机'太大，单手操作确实麻烦'，对华为尺寸轻微负向",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })

    # ========== Post 23: 69e72789000000001b020544 ==========
    post = posts[22]
    results.append({
        "opinion_id": "batch4_23_1",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "设计的丑就算了，没了Xmage也算了，卖的贵4699也可以忍一忍给你算了",
        "brand_target": "华为",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户指出Pura90'设计的丑'、'没了Xmage'、'卖的贵'，多维度负向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_23_2",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "你跟nova15 Ultra一样一样的啊？不知道的以为你nova16呢",
        "brand_target": "华为",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "强",
        "sentiment_reason": "用户认为Pura90与nova15 Ultra'一样一样'，甚至像nova16，对产品定位强烈负向嘲讽",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_23_3",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "甚至摄像头设计的还没nova15Ultra好看",
        "brand_target": "华为",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户认为Pura90摄像头'还没nova15Ultra好看'，对华为设计负向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_23_4",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "Pura系列出了这么个玩意儿，简直就是'扶不起的阿斗'",
        "brand_target": "华为",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "强",
        "sentiment_reason": "用户称Pura90为'扶不起的阿斗'，情绪强烈负向，对产品极度失望",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })

    # ========== Post 24: 6947d773000000001e02a5e7 ==========
    post = posts[23]
    results.append({
        "opinion_id": "batch4_24_1",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "作为影像旗舰和mate影像拉不开差距",
        "brand_target": "华为",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户指出Pura作为影像旗舰和mate'拉不开差距'，对Pura影像定位负向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_24_2",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "Pura系列卖点不足，机型阉割离谱",
        "brand_target": "华为",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "强",
        "sentiment_reason": "用户认为Pura'卖点不足，机型阉割离谱'，情绪强烈负向",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_24_3",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "p80延续了p70的做法，但大家已经不买账了",
        "brand_target": "华为",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户指出P80延续P70做法但'大家已经不买账了'，对市场接受度负向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_24_4",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "丢失了p系列精髓，售价不合理",
        "brand_target": "华为",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "强",
        "sentiment_reason": "用户认为Pura'丢失了p系列精髓，售价不合理'，对产品定位和定价强烈负向",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_24_5",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "p80是第一次没有大改外观，辨识度很难和p70区分开，全系很重很厚，超大杯p80u的deco只是简单放大，丢失了美学与轻薄",
        "brand_target": "华为",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户指出P80'辨识度很难和p70区分开'、'全系很重很厚'、'丢失了美学与轻薄'，多维度负向",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_24_6",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "mate70、mate80不断降价的同时，p70、p80价格却纹丝不动，大家是难以接受的",
        "brand_target": "华为",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户认为P系列价格'纹丝不动'而mate降价，消费者'难以接受'，对华为定价策略负向",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })

    # ========== Post 25: 67ee9931000000001d019e2b ==========
    post = posts[24]
    results.append({
        "opinion_id": "batch4_25_1",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "丝滑流畅：鸿蒙Next的系统动画支棱起来了，不管是上滑回桌面打断动画，还是第三方APP内的动画，非常接近iOS，流畅到像德芙广告",
        "brand_target": "华为",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "强",
        "sentiment_reason": "用户认为鸿蒙Next'流畅到像德芙广告'、'非常接近iOS'，对鸿蒙动画流畅度高度认可",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": True
    })
    results.append({
        "opinion_id": "batch4_25_2",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "美学设计：鸿蒙Next的颜值终于不拖后腿了，几乎每个系统界面都重新设计，毛玻璃模糊很不错",
        "brand_target": "华为",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户认为鸿蒙Next'颜值终于不拖后腿'、'毛玻璃模糊很不错'，对鸿蒙设计正向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_25_3",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "小艺AI：长按图片拖给小艺，一键添加日程/生成Excel表格/查剧查片/识图搜索，系统图库还可以消除路人，Siri遇到这些会说'我好像不明白'",
        "brand_target": "华为",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户认为小艺AI功能丰富，对比Siri'我好像不明白'，对华为AI能力正向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_25_4",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "系统输入法：小艺语音转文字准确率比iOS好不少，苹果自带输入法还在把'鸿蒙'识别成'红焖'",
        "brand_target": "华为",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户认为小艺语音转文字'准确率比iOS好不少'，对华为输入法正向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_25_5",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "鸿蒙生态阵痛期：鸿蒙Next部分小众APP还没上架商店，已上架的部分应用存在功能缺失，能用但还不够好用",
        "brand_target": "华为",
        "sentiment_polarity": "负向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户指出鸿蒙Next'部分小众APP还没上架'、'功能缺失'、'还不够好用'，对生态负向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_25_6",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "精致感略逊一筹：在控制中心，天气APP等界面设计和过渡动画还是没iOS细腻自然，苹果的审美依旧在线",
        "brand_target": "苹果",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户认为iOS'细腻自然'、'苹果的审美依旧在线'，对苹果设计精致度正向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })
    results.append({
        "opinion_id": "batch4_25_7",
        "note_id": post["note_id"],
        "title": post["title"],
        "source_keyword": post["source_keyword"],
        "liked_count": post["liked_count"],
        "comment_count": post["comment_count"],
        "opinion_text": "软件适配差距：iOS锁屏小组件种类丰富，鸿蒙目前只有基础样式，iOS实时活动适配也更全面",
        "brand_target": "苹果",
        "sentiment_polarity": "正向",
        "sentiment_intensity": "中",
        "sentiment_reason": "用户认为iOS'锁屏小组件种类丰富'、'实时活动适配也更全面'，对苹果软件生态正向评价",
        "confidence": "高",
        "full_title": post["title"],
        "full_content": post["content"],
        "is_fluency_related": False
    })

    # 写输出
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"分析完成！共处理 {len(posts)} 条UGC，提取 {len(results)} 条观点")
    print(f"输出文件: {OUTPUT_PATH}")

    # 统计
    brand_counts = {}
    sentiment_counts = {}
    fluency_count = 0
    for r in results:
        brand_counts[r["brand_target"]] = brand_counts.get(r["brand_target"], 0) + 1
        sentiment_counts[r["sentiment_polarity"]] = sentiment_counts.get(r["sentiment_polarity"], 0) + 1
        if r["is_fluency_related"]:
            fluency_count += 1
    print(f"\n品牌分布: {brand_counts}")
    print(f"情绪分布: {sentiment_counts}")
    print(f"流畅相关: {fluency_count} 条")


if __name__ == "__main__":
    analyze_batch4()
