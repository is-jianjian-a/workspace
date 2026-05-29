#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch 2 品牌情绪识别 - 25条UGC (第26-50条)
基于语义理解提取观点、品牌、情绪
"""

import json
from pathlib import Path

# 读取输入
input_path = Path('/Users/zhijian/workspace/mind-mining/v1.0/sentiment/02-batches/02-batch2-input.json')
with open(input_path, 'r', encoding='utf-8') as f:
    posts = json.load(f)

opinions = []

# ========== Post 1 (idx 0) ==========
p = posts[0]
# 华为 Mate 60pro 拜拜，用了两年手机越来越烫，电池一天充三四次，拍照发灰，微信没有实况，卡顿闪退
opinions.append({
    "opinion_id": "batch2_01_1", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "用了两年的华为Mate60pro手机越来越烫，电池一天充三四次，拍照发灰，微信没有实况，卡顿闪退。",
    "brand_target": "华为", "sentiment_polarity": "负向", "sentiment_intensity": "强",
    "sentiment_reason": "\"手机越来越烫\"\"电池一天充三四次\"\"卡顿闪退\"——多项严重问题",
    "confidence": "高", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": True
})
# 换苹果原因
opinions.append({
    "opinion_id": "batch2_01_2", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "苹果17pm颜值在线越看越顺眼，拍照也很不错双摄超喜欢，终于可以看朋友圈的实况图了。",
    "brand_target": "苹果", "sentiment_polarity": "正向", "sentiment_intensity": "中",
    "sentiment_reason": "\"颜值在线\"\"拍照也很不错\"——肯定苹果外观和拍照",
    "confidence": "高", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": False
})
# 苹果使用感受优点
opinions.append({
    "opinion_id": "batch2_01_3", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "苹果17pm电池耐用，从中午十二点满电到现在还有27的电量，相机调色盘太懂爱拍照人士了，还是一如既往的苹果流畅感。",
    "brand_target": "苹果", "sentiment_polarity": "正向", "sentiment_intensity": "中",
    "sentiment_reason": "\"电池耐用\"\"流畅感\"——肯定续航和流畅度",
    "confidence": "高", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": True
})
# 苹果缺点
opinions.append({
    "opinion_id": "batch2_01_4", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "苹果信号确实比不了华为，在电梯里电话都接不到。",
    "brand_target": "苹果", "sentiment_polarity": "负向", "sentiment_intensity": "中",
    "sentiment_reason": "\"信号确实比不了\"\"电梯里电话都接不到\"——批评信号",
    "confidence": "高", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": False
})
# 苹果缺点2
opinions.append({
    "opinion_id": "batch2_01_5", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "苹果花里胡哨的功能少了很多，比如图片的一键消除、中转站等。",
    "brand_target": "苹果", "sentiment_polarity": "负向", "sentiment_intensity": "弱",
    "sentiment_reason": "\"功能少了很多\"——批评功能缺失",
    "confidence": "高", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": False
})

# ========== Post 2 (idx 1) ==========
p = posts[1]
# 关于华为Pura X Max
opinions.append({
    "opinion_id": "batch2_02_1", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "Pura X Max游戏是能玩了，但是改善的不是很大，玩儿着有点点卡，已经默认开了极致。",
    "brand_target": "华为", "sentiment_polarity": "负向", "sentiment_intensity": "弱",
    "sentiment_reason": "\"玩儿着有点点卡\"——轻微批评游戏流畅度",
    "confidence": "中", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": True
})
# 屏幕/拍照
opinions.append({
    "opinion_id": "batch2_02_2", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "屏保的动态壁纸对比1代可玩儿性强了，这点非常喜欢。阔折叠今天出去随手拍的几张照片，我觉得已经很不错了。",
    "brand_target": "华为", "sentiment_polarity": "正向", "sentiment_intensity": "中",
    "sentiment_reason": "\"非常喜欢\"\"已经很不错了\"——肯定动态壁纸和拍照",
    "confidence": "高", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": False
})
# iPad mini7 电池
opinions.append({
    "opinion_id": "batch2_02_3", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "iPad mini7电池健康就已经91了，真的没有很经常用，这个烂烂的电池让我很焦虑。",
    "brand_target": "苹果", "sentiment_polarity": "负向", "sentiment_intensity": "中",
    "sentiment_reason": "\"烂烂的电池让我很焦虑\"——批评电池衰减",
    "confidence": "高", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": True
})

# ========== Post 3 (idx 2) ==========
p = posts[2]
# 上至苹果最新款，下到华为旗舰机，没有一个是会卡的
opinions.append({
    "opinion_id": "batch2_03_1", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "上至苹果最新款，下到华为旗舰机，没有一个是会卡的。",
    "brand_target": "华为", "sentiment_polarity": "正向", "sentiment_intensity": "中",
    "sentiment_reason": "\"没有一个是会卡的\"——肯定华为流畅度",
    "confidence": "高", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": True
})
opinions.append({
    "opinion_id": "batch2_03_2", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "上至苹果最新款，下到华为旗舰机，没有一个是会卡的。",
    "brand_target": "苹果", "sentiment_polarity": "正向", "sentiment_intensity": "中",
    "sentiment_reason": "\"没有一个是会卡的\"——肯定苹果流畅度",
    "confidence": "高", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": True
})

# ========== Post 4 (idx 3) ==========
# 多品牌拍照对比，纯客观描述，无明确情绪，跳过

# ========== Post 5 (idx 4) ==========
p = posts[4]
# 华为微距强
opinions.append({
    "opinion_id": "batch2_05_1", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "微距模式的华为简直强的可怕，苹果手机确实比不了，细看华为拍的清晰度也更高一些，就连小螃蟹的腿毛和花纹都很清晰，手掌的皮肤纹理也是，细节处理的都很好。",
    "brand_target": "华为", "sentiment_polarity": "正向", "sentiment_intensity": "强",
    "sentiment_reason": "\"简直强的可怕\"\"苹果手机确实比不了\"——强烈肯定华为微距",
    "confidence": "高", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": False
})
# 苹果微距
opinions.append({
    "opinion_id": "batch2_05_2", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "色调的话，华为偏白偏亮，苹果有些发黄。",
    "brand_target": "苹果", "sentiment_polarity": "负向", "sentiment_intensity": "弱",
    "sentiment_reason": "\"有些发黄\"——轻微批评色调",
    "confidence": "高", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": False
})

# ========== Post 6 (idx 5) ==========
# 内容只有标题，无实质内容，跳过

# ========== Post 7 (idx 6) ==========
p = posts[6]
# 华为Mate70 Pro+
opinions.append({
    "opinion_id": "batch2_07_1", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "华为Mate 70 Pro+除了性能和手感之外，非常棒的旗舰手机。影像系统、屏幕都有进步，3D人脸也特别好用，鸿蒙系统流畅度非常好。",
    "brand_target": "华为", "sentiment_polarity": "正向", "sentiment_intensity": "中",
    "sentiment_reason": "\"非常棒的旗舰手机\"\"流畅度非常好\"——肯定华为综合表现",
    "confidence": "高", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": True
})
# 华为性能不足
opinions.append({
    "opinion_id": "batch2_07_2", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "麒麟9020芯片的性能的确比不过同价位或者其它性能旗舰手机，只是靠着华为的系统优化保证日常使用很丝滑流畅。手机有点宽，再窄一些就更好了。",
    "brand_target": "华为", "sentiment_polarity": "负向", "sentiment_intensity": "中",
    "sentiment_reason": "\"性能的确比不过\"\"手机有点宽\"——批评性能和手感",
    "confidence": "高", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": True
})
# iPhone 16 Pro Max
opinions.append({
    "opinion_id": "batch2_07_3", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "iPhone 16 Pro Max A18 Pro的性能和iOS系统的闭环生态，依旧是行业一流水平。拍视频比安卓强很多，屏幕边框很窄，也是卖得最好的旗舰手机。",
    "brand_target": "苹果", "sentiment_polarity": "正向", "sentiment_intensity": "强",
    "sentiment_reason": "\"行业一流水平\"\"拍视频比安卓强很多\"——高度肯定苹果性能和视频",
    "confidence": "高", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": False
})
# iPhone缺点
opinions.append({
    "opinion_id": "batch2_07_4", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "iPhone 16 Pro Max的确有些创新不足，有些方面不如国产做得好。",
    "brand_target": "苹果", "sentiment_polarity": "负向", "sentiment_intensity": "弱",
    "sentiment_reason": "\"创新不足\"\"不如国产做得好\"——轻微批评创新",
    "confidence": "高", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": False
})

# ========== Post 8 (idx 7) ==========
# 纯拍照对比展示，无明确观点，跳过

# ========== Post 9 (idx 8) ==========
p = posts[8]
# 色彩还原对比
opinions.append({
    "opinion_id": "batch2_09_1", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "就色彩还原来说，苹果华为是不相上下的，华为拍红色的还原效果确实很不错，但绿叶就有些偏鲜艳了。",
    "brand_target": "华为", "sentiment_polarity": "混合", "sentiment_intensity": "弱",
    "sentiment_reason": "\"还原效果确实很不错\"（正）vs \"绿叶就有些偏鲜艳了\"（负）",
    "confidence": "中", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": False
})
opinions.append({
    "opinion_id": "batch2_09_2", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "就色彩还原来说，苹果华为是不相上下的，反而是苹果的表现更出色些。",
    "brand_target": "苹果", "sentiment_polarity": "正向", "sentiment_intensity": "弱",
    "sentiment_reason": "\"苹果的表现更出色些\"——轻微肯定苹果色彩还原",
    "confidence": "中", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": False
})

# ========== Post 10 (idx 9) ==========
# 纯分享照片，无明确观点，跳过

# ========== Post 11 (idx 10) ==========
p = posts[10]
# 睡眠监测对比
opinions.append({
    "opinion_id": "batch2_11_1", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "华为测出来的睡眠总时长要更长，比苹果长了半个小时。华为的算法更关注入睡的时间，主打一个早睡早起身体好的感觉。",
    "brand_target": "华为", "sentiment_polarity": "中性", "sentiment_intensity": "弱",
    "sentiment_reason": "客观描述差异，无明确褒贬",
    "confidence": "中", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": False
})
opinions.append({
    "opinion_id": "batch2_11_2", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "苹果在手表端可以看到详细的睡眠数据。苹果的睡眠打分会高很多，几乎每晚的睡眠都能给我九十以上甚至满分。",
    "brand_target": "苹果", "sentiment_polarity": "正向", "sentiment_intensity": "弱",
    "sentiment_reason": "\"可以看到详细的睡眠数据\"\"打分会高很多\"——肯定苹果数据详细",
    "confidence": "高", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": False
})

# ========== Post 12 (idx 11) ==========
# 纯梗图，无实质内容，跳过

# ========== Post 13 (idx 12) ==========
p = posts[12]
# 睡眠监测深度对比
opinions.append({
    "opinion_id": "batch2_13_1", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "苹果手表更贴近我个人的睡眠状态，尤其是对清醒时间和深度睡眠的记录更符合实际情况。",
    "brand_target": "苹果", "sentiment_polarity": "正向", "sentiment_intensity": "中",
    "sentiment_reason": "\"更符合实际情况\"——肯定苹果睡眠监测准确性",
    "confidence": "高", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": False
})
opinions.append({
    "opinion_id": "batch2_13_2", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "华为手表的数据会让人自我感觉良好，提供了情绪价值。华为不开启24小时血压监控的话可以几天一充，苹果续航一直是短板，每天一充。",
    "brand_target": "华为", "sentiment_polarity": "混合", "sentiment_intensity": "弱",
    "sentiment_reason": "\"提供了情绪价值\"\"几天一充\"（正）vs 数据不够准确（隐含负）",
    "confidence": "中", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": True
})
# 苹果续航
opinions.append({
    "opinion_id": "batch2_13_3", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "苹果续航一直是短板，每天一充。",
    "brand_target": "苹果", "sentiment_polarity": "负向", "sentiment_intensity": "中",
    "sentiment_reason": "\"续航一直是短板\"——批评续航",
    "confidence": "高", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": True
})

# ========== Post 14 (idx 13) ==========
# 多品牌人像对比，纯客观描述+个人喜好，无强烈情绪，跳过主要品牌观点
# 但有一些对苹果和华为的具体评价
p = posts[13]
opinions.append({
    "opinion_id": "batch2_14_1", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "华为的效果是四个中整体最亮的一个，皮肤显得很白皙，皮肤也很细腻，看不出什么瑕疵。",
    "brand_target": "华为", "sentiment_polarity": "正向", "sentiment_intensity": "中",
    "sentiment_reason": "\"皮肤显得很白皙\"\"看不出什么瑕疵\"——肯定华为人像",
    "confidence": "高", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": False
})
opinions.append({
    "opinion_id": "batch2_14_2", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "苹果人像发挥依旧是老样子，果粉喜欢的真实感，室内光线下拍出的皮肤很柔和，稍稍能看到皮肤上的瑕疵，整体有些发黄发暗。",
    "brand_target": "苹果", "sentiment_polarity": "混合", "sentiment_intensity": "弱",
    "sentiment_reason": "\"真实感\"\"很柔和\"（正）vs \"发黄发暗\"（负）",
    "confidence": "高", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": False
})

# ========== Post 15 (idx 14) ==========
# 配置对比，纯信息，无明确情绪，跳过

# ========== Post 16 (idx 15) ==========
# 纯提问，无观点，跳过

# ========== Post 17 (idx 16) ==========
# 专业评测，较客观，提取关键观点
p = posts[16]
opinions.append({
    "opinion_id": "batch2_17_1", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "Mate80Pro和ProMax能支持到最高的极致+120帧，画面更流畅。Mate80Pro和ProMax的优势就展现出来了。",
    "brand_target": "华为", "sentiment_polarity": "正向", "sentiment_intensity": "中",
    "sentiment_reason": "\"画面更流畅\"\"优势就展现出来了\"——肯定性能和流畅度",
    "confidence": "高", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": True
})

# ========== Post 18 (idx 17) ==========
p = posts[17]
# 华为fit 5 pro bug
opinions.append({
    "opinion_id": "batch2_18_1", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "华为watch fit 5 pro手表居然配的线是type-a，找遍了全家，找不出一个像样的a口充电器。很奇怪的设计，很奇怪的逻辑。不好理解。",
    "brand_target": "华为", "sentiment_polarity": "负向", "sentiment_intensity": "中",
    "sentiment_reason": "\"很奇怪的设计\"\"不好理解\"——批评充电接口设计",
    "confidence": "高", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": False
})

# ========== Post 19 (idx 18) ==========
p = posts[18]
# 白送选哪个
opinions.append({
    "opinion_id": "batch2_19_1", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "华为Mate80Pro和iPhone17Pro都是好手机，日用都是很流畅，华为的优势是信号和拍照，苹果则是系统生态成熟和录像牛。",
    "brand_target": "华为", "sentiment_polarity": "正向", "sentiment_intensity": "弱",
    "sentiment_reason": "\"优势是信号和拍照\"——肯定华为信号和拍照",
    "confidence": "高", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": False
})
opinions.append({
    "opinion_id": "batch2_19_2", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "华为Mate80Pro和iPhone17Pro都是好手机，日用都是很流畅，苹果则是系统生态成熟和录像牛。",
    "brand_target": "苹果", "sentiment_polarity": "正向", "sentiment_intensity": "弱",
    "sentiment_reason": "\"系统生态成熟和录像牛\"——肯定苹果生态和视频",
    "confidence": "高", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": False
})

# ========== Post 20 (idx 19) ==========
# 荣耀价格对比，无华为/苹果直接观点，跳过

# ========== Post 21 (idx 20) ==========
# 纯提问，无观点，跳过

# ========== Post 22 (idx 21) ==========
p = posts[21]
# 苹果→华为体验
opinions.append({
    "opinion_id": "batch2_22_1", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "华为可以分屏，用苹果时很羡慕的分屏。",
    "brand_target": "华为", "sentiment_polarity": "正向", "sentiment_intensity": "中",
    "sentiment_reason": "\"很羡慕的分屏\"——肯定华为分屏功能",
    "confidence": "高", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": False
})
opinions.append({
    "opinion_id": "batch2_22_2", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "华为拍照也有实况，拍出的照片清晰度确实很高，有相机出片的感觉，可以放大的倍数更高。",
    "brand_target": "华为", "sentiment_polarity": "正向", "sentiment_intensity": "中",
    "sentiment_reason": "\"清晰度确实很高\"\"有相机出片的感觉\"——肯定华为拍照",
    "confidence": "高", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": False
})
opinions.append({
    "opinion_id": "batch2_22_3", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "苹果拍照的真实感也确实会好点。",
    "brand_target": "苹果", "sentiment_polarity": "正向", "sentiment_intensity": "弱",
    "sentiment_reason": "\"真实感也确实会好点\"——轻微肯定苹果拍照真实感",
    "confidence": "高", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": False
})
opinions.append({
    "opinion_id": "batch2_22_4", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "华为充电速度更快，洗漱回来居然充满了，这确实给我惊喜到了。",
    "brand_target": "华为", "sentiment_polarity": "正向", "sentiment_intensity": "强",
    "sentiment_reason": "\"居然充满了\"\"给我惊喜到了\"——强烈肯定充电速度",
    "confidence": "高", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": True
})
opinions.append({
    "opinion_id": "batch2_22_5", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "华为信号会好很多会更稳定一些。",
    "brand_target": "华为", "sentiment_polarity": "正向", "sentiment_intensity": "中",
    "sentiment_reason": "\"会好很多会更稳定\"——肯定信号",
    "confidence": "高", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": False
})

# ========== Post 23 (idx 22) ==========
p = posts[22]
# 后悔买华为
opinions.append({
    "opinion_id": "batch2_23_1", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "刚买完华为手机就后悔了，一直用的都是苹果，感觉好不习惯。",
    "brand_target": "华为", "sentiment_polarity": "负向", "sentiment_intensity": "中",
    "sentiment_reason": "\"就后悔了\"\"好不习惯\"——后悔换华为",
    "confidence": "高", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": False
})

# ========== Post 24 (idx 23) ==========
p = posts[23]
# 感觉华为比苹果好太多了
opinions.append({
    "opinion_id": "batch2_24_1", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "感觉华为比苹果好太多了。",
    "brand_target": "华为", "sentiment_polarity": "正向", "sentiment_intensity": "强",
    "sentiment_reason": "\"好太多了\"——强烈偏好华为",
    "confidence": "高", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": False
})
opinions.append({
    "opinion_id": "batch2_24_2", "note_id": p["note_id"], "title": p["title"],
    "source_keyword": p["source_keyword"], "liked_count": p["liked_count"], "comment_count": p["comment_count"],
    "opinion_text": "感觉华为比苹果好太多了。",
    "brand_target": "苹果", "sentiment_polarity": "负向", "sentiment_intensity": "强",
    "sentiment_reason": "\"比苹果好太多了\"（隐含苹果不够好）——负面暗示",
    "confidence": "中", "full_title": p["title"], "full_content": p["content"], "is_fluency_related": False
})

# ========== Post 25 (idx 24) ==========
# 纯提问，无观点，跳过

# 保存结果
output_path = Path('/Users/zhijian/workspace/mind-mining/v1.0/sentiment/02-batches/02-batch2-result.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(opinions, f, ensure_ascii=False, indent=2)

print(f"Batch 2完成: {len(opinions)}条观点")
