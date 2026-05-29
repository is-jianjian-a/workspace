#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch 1 品牌情绪识别 - 25条UGC (第1-25条)
基于语义理解提取观点、品牌、情绪
"""

import json
from pathlib import Path

# 读取输入
input_path = Path('/Users/zhijian/workspace/mind-mining/v1.0/sentiment/02-batches/02-batch1-input.json')
with open(input_path, 'r', encoding='utf-8') as f:
    posts = json.load(f)

opinions = []

# ========== Post 1 ==========
# 多年苹果老用户，24年初被华为的一通推销入了华为mate 60pro...结果真的是让我大失所望
p = posts[0]
opinions.append({
    "opinion_id": "batch1_01_1",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "用了才一年多就卡到炸裂，进一个程序要等好几秒才能反应过来，拍的照片要等几秒钟相册才显示，甚至会诡异的不见。而且发热发到感觉要炸掉的程度。",
    "brand_target": "华为",
    "sentiment_polarity": "负向",
    "sentiment_intensity": "强",
    "sentiment_reason": "\"用了才一年多就卡到炸裂\"\"发热发到感觉要炸掉的程度\"——用户明确表达极度不满",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": True
})
opinions.append({
    "opinion_id": "batch1_01_2",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "掉电还掉的贼快，而且除了原装线，我用其他线充不进去电，才用了一年电池健康度就86%。",
    "brand_target": "华为",
    "sentiment_polarity": "负向",
    "sentiment_intensity": "强",
    "sentiment_reason": "\"掉电还掉的贼快\"\"才用了一年电池健康度就86%\"——明确批评续航和电池衰减",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": False
})
opinions.append({
    "opinion_id": "batch1_01_3",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "像素根本没有吹的那么好，一开始显色度还行，用到现在颜色已经特别失真，拍照特别特别模糊。",
    "brand_target": "华为",
    "sentiment_polarity": "负向",
    "sentiment_intensity": "强",
    "sentiment_reason": "\"像素根本没有吹的那么好\"\"拍照特别特别模糊\"——对拍照效果强烈不满",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": False
})
opinions.append({
    "opinion_id": "batch1_01_4",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "华为手机的信号是真的好，这个不黑。",
    "brand_target": "华为",
    "sentiment_polarity": "正向",
    "sentiment_intensity": "中",
    "sentiment_reason": "\"信号是真的好\"——明确肯定信号表现",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": False
})
opinions.append({
    "opinion_id": "batch1_01_5",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "忍了一年实在受不了了，最终决定还是换回苹果，入了新款17pro，本来真的对华为有很高期待的，用完真的拉黑。",
    "brand_target": "华为",
    "sentiment_polarity": "负向",
    "sentiment_intensity": "强",
    "sentiment_reason": "\"用完真的拉黑\"——极端负面态度",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": False
})

# ========== Post 2 ==========
# 纯对比展示，无明确观点，跳过

# ========== Post 3 ==========
p = posts[2]
opinions.append({
    "opinion_id": "batch1_03_1",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "信号是真的好，苹果进电梯就无信号，华为从5G变4G但不影响使用。",
    "brand_target": "华为",
    "sentiment_polarity": "正向",
    "sentiment_intensity": "中",
    "sentiment_reason": "\"信号是真的好\"——明确肯定华为信号",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": False
})
opinions.append({
    "opinion_id": "batch1_03_2",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "苹果进电梯就无信号。",
    "brand_target": "苹果",
    "sentiment_polarity": "负向",
    "sentiment_intensity": "中",
    "sentiment_reason": "\"进电梯就无信号\"——批评苹果信号差",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": False
})
opinions.append({
    "opinion_id": "batch1_03_3",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "屏幕视觉精细感可以对标苹果，在握感、操作流畅度等方面体验优于其他厂商。",
    "brand_target": "华为",
    "sentiment_polarity": "正向",
    "sentiment_intensity": "中",
    "sentiment_reason": "\"体验优于其他厂商\"——肯定华为屏幕和流畅度",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": True
})
opinions.append({
    "opinion_id": "batch1_03_4",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "广告变少，各app在iOS端也开始大量放广告，打开部分app就各种跳转，目前鸿蒙暂无此问题。",
    "brand_target": "华为",
    "sentiment_polarity": "正向",
    "sentiment_intensity": "弱",
    "sentiment_reason": "\"广告变少\"\"鸿蒙暂无此问题\"——肯定鸿蒙广告控制",
    "confidence": "中",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": False
})
opinions.append({
    "opinion_id": "batch1_03_5",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "卡片/组件能真正发挥用处，能不花钱就看到天气变化情况和云图变化趋势，日历待办也方便很多。",
    "brand_target": "华为",
    "sentiment_polarity": "正向",
    "sentiment_intensity": "中",
    "sentiment_reason": "\"能真正发挥用处\"\"方便很多\"——肯定组件功能",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": False
})
opinions.append({
    "opinion_id": "batch1_03_6",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "长焦能把远处拉近还不糊。",
    "brand_target": "华为",
    "sentiment_polarity": "正向",
    "sentiment_intensity": "中",
    "sentiment_reason": "\"能把远处拉近还不糊\"——肯定长焦拍照",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": False
})
opinions.append({
    "opinion_id": "batch1_03_7",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "鸿蒙系统下各app还是不能适配，但我觉得这不是系统的问题，而是各app开发商的问题。",
    "brand_target": "华为",
    "sentiment_polarity": "负向",
    "sentiment_intensity": "弱",
    "sentiment_reason": "\"各app还是不能适配\"——指出应用适配问题，但用户认为不是华为责任",
    "confidence": "中",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": False
})
opinions.append({
    "opinion_id": "batch1_03_8",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "重。。。和17pro不相上下。",
    "brand_target": "华为",
    "sentiment_polarity": "负向",
    "sentiment_intensity": "弱",
    "sentiment_reason": "\"重\"——批评重量",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": False
})

# ========== Post 4 ==========
p = posts[3]
opinions.append({
    "opinion_id": "batch1_04_1",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "逆光：华为mate60pro＞iPhone15pro。",
    "brand_target": "华为",
    "sentiment_polarity": "正向",
    "sentiment_intensity": "中",
    "sentiment_reason": "\"逆光：华为mate60pro＞iPhone15pro\"——逆光拍照华为更好",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": False
})
opinions.append({
    "opinion_id": "batch1_04_2",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "顺光：iPhone15pro＞华为mate60pro。",
    "brand_target": "苹果",
    "sentiment_polarity": "正向",
    "sentiment_intensity": "中",
    "sentiment_reason": "\"顺光：iPhone15pro＞华为mate60pro\"——顺光拍照苹果更好",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": False
})
opinions.append({
    "opinion_id": "batch1_04_3",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "苹果什么都好，就是逆光拍照不能兼顾人像和背景的白平衡，导致人物在背景强光线上发灰。",
    "brand_target": "苹果",
    "sentiment_polarity": "负向",
    "sentiment_intensity": "中",
    "sentiment_reason": "\"逆光拍照不能兼顾人像和背景的白平衡\"\"人物发灰\"——批评苹果逆光拍照",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": False
})
opinions.append({
    "opinion_id": "batch1_04_4",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "逆光选华为，在极强的光线下华为不仅人物拍的很清晰，背景也很有氛围感。整体色调很和谐，最主要是不发灰没有色偏。",
    "brand_target": "华为",
    "sentiment_polarity": "正向",
    "sentiment_intensity": "中",
    "sentiment_reason": "\"人物拍的很清晰\"\"背景也很有氛围感\"\"不发灰没有色偏\"——肯定华为逆光拍照",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": False
})

# ========== Post 5 ==========
# 主要是索尼vs苹果对比，华为未提及，跳过

# ========== Post 6 ==========
p = posts[5]
opinions.append({
    "opinion_id": "batch1_06_1",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "初上手感觉鸿蒙6很丝滑啊，发热和续航比4.2好太多了，感觉流畅度和稳定性已经超越了iOS，特别是iOS26那一坨。",
    "brand_target": "华为",
    "sentiment_polarity": "正向",
    "sentiment_intensity": "强",
    "sentiment_reason": "\"很丝滑啊\"\"流畅度和稳定性已经超越了iOS\"——强烈肯定鸿蒙流畅度",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": True
})
opinions.append({
    "opinion_id": "batch1_06_2",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "鸿蒙真的是越升级越流畅，流畅度真遥遥领先。",
    "brand_target": "华为",
    "sentiment_polarity": "正向",
    "sentiment_intensity": "强",
    "sentiment_reason": "\"越升级越流畅\"\"遥遥领先\"——高度肯定",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": True
})

# ========== Post 7 ==========
p = posts[6]
opinions.append({
    "opinion_id": "batch1_07_1",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "这俩手机现在都不卡，日常用不管是UI动画丝滑程度还是跟手度，都跟刚买时候无异。",
    "brand_target": "华为",
    "sentiment_polarity": "正向",
    "sentiment_intensity": "中",
    "sentiment_reason": "\"都不卡\"\"UI动画丝滑程度还是跟手度，都跟刚买时候无异\"——肯定华为流畅度",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": True
})
opinions.append({
    "opinion_id": "batch1_07_2",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "这俩手机现在都不卡，日常用不管是UI动画丝滑程度还是跟手度，都跟刚买时候无异。",
    "brand_target": "苹果",
    "sentiment_polarity": "正向",
    "sentiment_intensity": "中",
    "sentiment_reason": "\"都不卡\"\"UI动画丝滑程度还是跟手度，都跟刚买时候无异\"——肯定苹果流畅度",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": True
})
opinions.append({
    "opinion_id": "batch1_07_3",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "iPhone15Pro芯片性能很强悍＋系统本身就做得好。哪怕过了两年，游戏方面表现依旧很不错。但是网络信号不咋好，用流量玩王者之类，常常460。",
    "brand_target": "苹果",
    "sentiment_polarity": "混合",
    "sentiment_intensity": "中",
    "sentiment_reason": "\"芯片性能很强悍\"\"游戏方面表现依旧很不错\"（正） vs \"网络信号不咋好\"\"常常460\"（负）",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": True
})
opinions.append({
    "opinion_id": "batch1_07_4",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "Mate60Pro麒麟芯片的代差导致性能不好，夏天时候玩王者温度一上去，60帧都不咋稳得住。",
    "brand_target": "华为",
    "sentiment_polarity": "负向",
    "sentiment_intensity": "中",
    "sentiment_reason": "\"性能不好\"\"60帧都不咋稳得住\"——批评华为游戏性能",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": True
})
opinions.append({
    "opinion_id": "batch1_07_5",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "iPhone15Pro电池健康还有91%，日常用续航跟尿尿似的。Mate60Pro电池健康还有86%，日常用续航尿尿似的。掉电都很快。",
    "brand_target": "苹果",
    "sentiment_polarity": "负向",
    "sentiment_intensity": "中",
    "sentiment_reason": "\"续航跟尿尿似的\"\"掉电都很快\"——批评苹果续航",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": True
})
opinions.append({
    "opinion_id": "batch1_07_6",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "Mate60Pro电池健康还有86%，日常用续航尿尿似的。受快充影响＋夏天十分烫，华为电池健康下降很快。",
    "brand_target": "华为",
    "sentiment_polarity": "负向",
    "sentiment_intensity": "中",
    "sentiment_reason": "\"续航尿尿似的\"\"电池健康下降很快\"——批评华为续航和电池衰减",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": True
})

# ========== Post 8 ==========
p = posts[7]
opinions.append({
    "opinion_id": "batch1_08_1",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "两部手机都非常流畅，完全感觉不到卡的地方。",
    "brand_target": "华为",
    "sentiment_polarity": "正向",
    "sentiment_intensity": "中",
    "sentiment_reason": "\"非常流畅\"\"完全感觉不到卡\"——肯定华为流畅度",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": True
})
opinions.append({
    "opinion_id": "batch1_08_2",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "两部手机都非常流畅，完全感觉不到卡的地方。",
    "brand_target": "苹果",
    "sentiment_polarity": "正向",
    "sentiment_intensity": "中",
    "sentiment_reason": "\"非常流畅\"\"完全感觉不到卡\"——肯定苹果流畅度",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": True
})
opinions.append({
    "opinion_id": "batch1_08_3",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "信号无论在什么地方都比苹果好太多太了，用苹果的时候在停车场开不了导航，华为就完全不会有这个问题。",
    "brand_target": "华为",
    "sentiment_polarity": "正向",
    "sentiment_intensity": "强",
    "sentiment_reason": "\"比苹果好太多太了\"——强烈肯定华为信号",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": False
})
opinions.append({
    "opinion_id": "batch1_08_4",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "用苹果的时候在停车场开不了导航。",
    "brand_target": "苹果",
    "sentiment_polarity": "负向",
    "sentiment_intensity": "中",
    "sentiment_reason": "\"在停车场开不了导航\"——批评苹果信号",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": False
})
opinions.append({
    "opinion_id": "batch1_08_5",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "华为基本没有杀后台的问题，苹果经常打游戏的时候切出去回条消息就重新加载了。",
    "brand_target": "华为",
    "sentiment_polarity": "正向",
    "sentiment_intensity": "中",
    "sentiment_reason": "\"基本没有杀后台的问题\"——肯定华为后台留存",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": True
})
opinions.append({
    "opinion_id": "batch1_08_6",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "苹果经常打游戏的时候切出去回条消息就重新加载了。",
    "brand_target": "苹果",
    "sentiment_polarity": "负向",
    "sentiment_intensity": "中",
    "sentiment_reason": "\"切出去回条消息就重新加载了\"——批评苹果杀后台",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": True
})
opinions.append({
    "opinion_id": "batch1_08_7",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "侧滑返回、分屏、单手操作、88w快充真的太爽了谁用谁知道。圆弧边框的手感比苹果好了不止一点。",
    "brand_target": "华为",
    "sentiment_polarity": "正向",
    "sentiment_intensity": "强",
    "sentiment_reason": "\"真的太爽了\"\"手感比苹果好了不止一点\"——强烈肯定华为操作体验",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": False
})
opinions.append({
    "opinion_id": "batch1_08_8",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "华为在信号切换的时候比苹果顺畅很多，比如从家里出门，从WiFi环境切换到5G，苹果会卡一段时间，华为很丝滑。",
    "brand_target": "华为",
    "sentiment_polarity": "正向",
    "sentiment_intensity": "中",
    "sentiment_reason": "\"比苹果顺畅很多\"\"华为很丝滑\"——肯定华为信号切换流畅度",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": True
})
opinions.append({
    "opinion_id": "batch1_08_9",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "从家里出门，从WiFi环境切换到5G，苹果会卡一段时间。",
    "brand_target": "苹果",
    "sentiment_polarity": "负向",
    "sentiment_intensity": "弱",
    "sentiment_reason": "\"苹果会卡一段时间\"——批评苹果信号切换",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": True
})
opinions.append({
    "opinion_id": "batch1_08_10",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "华为震动马达太太太廉价了，质感很差。",
    "brand_target": "华为",
    "sentiment_polarity": "负向",
    "sentiment_intensity": "强",
    "sentiment_reason": "\"太太太廉价了\"\"质感很差\"——强烈批评华为马达",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": False
})
opinions.append({
    "opinion_id": "batch1_08_11",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "华为在外放音量比较大的时候手机会震。",
    "brand_target": "华为",
    "sentiment_polarity": "负向",
    "sentiment_intensity": "弱",
    "sentiment_reason": "\"手机会震\"——批评外放震动",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": False
})
opinions.append({
    "opinion_id": "batch1_08_12",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "华为耳机不如AirPods，所以现在我还是在用airpods，连接的时候要在蓝牙那边点一下。",
    "brand_target": "华为",
    "sentiment_polarity": "负向",
    "sentiment_intensity": "中",
    "sentiment_reason": "\"华为耳机不如AirPods\"——批评华为耳机",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": False
})
opinions.append({
    "opinion_id": "batch1_08_13",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "华为有很多广告要花十几分钟设置关掉。",
    "brand_target": "华为",
    "sentiment_polarity": "负向",
    "sentiment_intensity": "中",
    "sentiment_reason": "\"有很多广告\"——批评广告多",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": False
})
opinions.append({
    "opinion_id": "batch1_08_14",
    "note_id": p["note_id"],
    "title": p["title"],
    "source_keyword": p["source_keyword"],
    "liked_count": p["liked_count"],
    "comment_count": p["comment_count"],
    "opinion_text": "华为看b站视频快进的时候声音会一卡一卡的，b站党崩溃。",
    "brand_target": "华为",
    "sentiment_polarity": "负向",
    "sentiment_intensity": "中",
    "sentiment_reason": "\"声音会一卡一卡的\"\"b站党崩溃\"——批评视频播放卡顿",
    "confidence": "高",
    "full_title": p["title"],
    "full_content": p["content"],
    "is_fluency_related": True
})

# 保存结果
output_path = Path('/Users/zhijian/workspace/mind-mining/v1.0/sentiment/02-batches/02-batch1-result.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(opinions, f, ensure_ascii=False, indent=2)

print(f"Batch 1完成: {len(opinions)}条观点")
