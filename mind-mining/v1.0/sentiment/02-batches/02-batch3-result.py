#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch 3 品牌情绪识别脚本
基于语义理解的UGC品牌情绪分析（非关键词匹配）
"""

import json
import os

INPUT_PATH = "/Users/zhijian/workspace/mind-mining/v1.0/sentiment/02-batches/02-batch3-input.json"
OUTPUT_PATH = "/Users/zhijian/workspace/mind-mining/v1.0/sentiment/02-batches/02-batch3-result.json"

BRANDS = ["华为", "苹果", "三星", "小米", "OPPO", "vivo", "安卓"]


def analyze_post(post: dict, post_idx: int) -> list:
    """
    对单条UGC进行语义级观点拆分和品牌情绪识别。
    返回该帖子产生的所有观点列表。
    """
    opinions = []
    note_id = post.get("note_id", "")
    title = post.get("title", "")
    content = post.get("content", "")
    source_keyword = post.get("source_keyword", "")
    liked_count = post.get("liked_count", 0) or 0
    comment_count = post.get("comment_count", 0) or 0
    full_text = f"{title}\n{content}"

    # 根据语义逐条分析
    if note_id == "69e6409f0000000023011db4":
        # 帖子3011：第一部手机在苹果和华为中纠结
        # 纯疑问求助，无明确观点，不提取
        pass

    elif note_id == "69c3835e0000000023015ddb":
        # 帖子3012：发起外观设计讨论，纯提问
        pass

    elif note_id == "67d79445000000000603f492":
        # 帖子3013：到底选华为还是苹果啊
        pass

    elif note_id == "692816a9000000001d038d05":
        # 帖子3014：Mate70RS对比Mate80RS质感
        opinions.append({
            "opinion_text": "陶瓷的手感确实很温润舒服，新的昆仑玻璃后盖也感觉不错，有阻尼感还能摸到纹路，手感上不那么滑。",
            "brand_target": "华为",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "中",
            "sentiment_reason": "原文'陶瓷的手感确实很温润舒服'、'新的昆仑玻璃后盖也感觉不错'，对华为Mate系列后盖材质手感给予正面评价。",
            "confidence": "高",
            "is_fluency_related": False
        })
        opinions.append({
            "opinion_text": "边框是变成直角边框但同样是亮面钛金属，感觉也没有硌手感。",
            "brand_target": "华为",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "弱",
            "sentiment_reason": "原文'感觉也没有硌手感'，对华为直角边框设计表示接受，无负面感受。",
            "confidence": "中",
            "is_fluency_related": False
        })
        opinions.append({
            "opinion_text": "拍照色彩上第二代红枫确实更准色彩还原度更好。",
            "brand_target": "华为",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "中",
            "sentiment_reason": "原文'第二代红枫确实更准色彩还原度更好'，对华为拍照色彩表现给予明确肯定。",
            "confidence": "高",
            "is_fluency_related": False
        })
        opinions.append({
            "opinion_text": "整体没有大家网上说的质感下降啥的我感觉，喜欢的还是会喜欢，依旧是全方面顶级的旗舰。",
            "brand_target": "华为",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "强",
            "sentiment_reason": "原文'依旧是全方面顶级的旗舰'，对华为旗舰整体质感给予高度肯定，反驳网上负面说法。",
            "confidence": "高",
            "is_fluency_related": False
        })

    elif note_id == "69bce520000000001a023a03":
        # 帖子3015：华为Mate80风驰版镜头变化
        # 纯观察描述，无明确情绪观点
        pass

    elif note_id == "69e8348b0000000021004069":
        # 帖子3016：Pura90标准版真机体验
        opinions.append({
            "opinion_text": "直至线下见到了真机：'这不是还挺美的！'",
            "brand_target": "华为",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "中",
            "sentiment_reason": "原文'这不是还挺美的！'，用户亲眼见到华为Pura90真机后表示惊喜和认可。",
            "confidence": "高",
            "is_fluency_related": False
        })
        opinions.append({
            "opinion_text": "Ta其实很高级也很耐看，视觉重心高度聚焦于左上角，三角形依然先锋，不循规蹈矩。",
            "brand_target": "华为",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "强",
            "sentiment_reason": "原文'很高级也很耐看'、'三角形依然先锋，不循规蹈矩'，对华为Pura90设计语言给予高度审美肯定。",
            "confidence": "高",
            "is_fluency_related": False
        })
        opinions.append({
            "opinion_text": "磨砂玻璃背板没有冗余的元素，在哑光质感下呈现出柔和的陶瓷般光泽，搭配金属中框，清冷、纯净且克制，整体调性相当利落。",
            "brand_target": "华为",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "强",
            "sentiment_reason": "原文'清冷、纯净且克制，整体调性相当利落'，对华为Pura90背板质感和整体调性高度赞赏。",
            "confidence": "高",
            "is_fluency_related": False
        })
        opinions.append({
            "opinion_text": "最舒服的是裸机轻薄手感，偏爱极简主义的朋友应该会很喜欢。",
            "brand_target": "华为",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "中",
            "sentiment_reason": "原文'最舒服的是裸机轻薄手感'，对华为Pura90手感体验给予正面评价。",
            "confidence": "高",
            "is_fluency_related": False
        })
        opinions.append({
            "opinion_text": "我很看好Ta。",
            "brand_target": "华为",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "强",
            "sentiment_reason": "原文'我很看好Ta'，明确表达对华为Pura90标准版前景的看好和支持。",
            "confidence": "高",
            "is_fluency_related": False
        })

    elif note_id == "6953a4f3000000001e0249d5":
        # 帖子3017：荣耀Power2设计和配色眼熟
        # 涉及荣耀和iPhone，荣耀不在目标品牌中，iPhone提及为调侃
        opinions.append({
            "opinion_text": "据说明年iPhone18 Pro系列也要取消拼色设计了，荣耀Power2也算是iPhone 18Pro版本前瞻了。",
            "brand_target": "苹果",
            "sentiment_polarity": "中性",
            "sentiment_intensity": "弱",
            "sentiment_reason": "原文提及iPhone18 Pro可能取消拼色设计，属于信息引用和调侃，无明确褒贬。",
            "confidence": "低",
            "is_fluency_related": False
        })

    elif note_id == "69538241000000002202102b":
        # 帖子3018：荣耀Power2真机实拍
        # 纯展示，无明确观点
        pass

    elif note_id == "6a0731050000000035029491":
        # 帖子3019：华为和苹果选哪一个
        opinions.append({
            "opinion_text": "因为我其他的产品都是华为，所以觉得再换华为会更方便。",
            "brand_target": "华为",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "弱",
            "sentiment_reason": "原文'觉得再换华为会更方便'，因生态一致性对华为换机持正面倾向。",
            "confidence": "中",
            "is_fluency_related": False
        })
        opinions.append({
            "opinion_text": "但是我看好多说纯血鸿蒙系统有些功能不太适配。",
            "brand_target": "华为",
            "sentiment_polarity": "负向",
            "sentiment_intensity": "中",
            "sentiment_reason": "原文'纯血鸿蒙系统有些功能不太适配'，引用他人对华为鸿蒙系统适配问题的担忧。",
            "confidence": "中",
            "is_fluency_related": True
        })
        opinions.append({
            "opinion_text": "而苹果确实拍照比较好看。",
            "brand_target": "苹果",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "中",
            "sentiment_reason": "原文'苹果确实拍照比较好看'，明确肯定苹果拍照优势。",
            "confidence": "高",
            "is_fluency_related": False
        })
        opinions.append({
            "opinion_text": "听说苹果手机比较省内存。",
            "brand_target": "苹果",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "弱",
            "sentiment_reason": "原文'苹果手机比较省内存'，对苹果内存管理持正面印象。",
            "confidence": "中",
            "is_fluency_related": True
        })

    elif note_id == "6837cd670000000012001ee6":
        # 帖子3020：华为mate70Pro vs iPhone16Promax拍照对比
        opinions.append({
            "opinion_text": "安卓和鸿蒙拍照有时候会优化过度，显得很假。",
            "brand_target": "安卓",
            "sentiment_polarity": "负向",
            "sentiment_intensity": "中",
            "sentiment_reason": "原文'安卓和鸿蒙拍照有时候会优化过度，显得很假'，对安卓/鸿蒙拍照算法持负面评价。",
            "confidence": "高",
            "is_fluency_related": False
        })
        opinions.append({
            "opinion_text": "华为mate70拍出的效果竟然会这么好，不会像pura70那样发灰或者色彩过于浓郁，又保留了华为原本就有的优点（细节丰富，清晰度高）。",
            "brand_target": "华为",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "强",
            "sentiment_reason": "原文'效果竟然会这么好'、'细节丰富，清晰度高'，对华为mate70拍照效果高度肯定，超出预期。",
            "confidence": "高",
            "is_fluency_related": False
        })
        opinions.append({
            "opinion_text": "华为mate70的色彩跟苹果差距很小了，都属于比较自然的，色彩还原度也比较高。",
            "brand_target": "华为",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "中",
            "sentiment_reason": "原文'色彩跟苹果差距很小了'、'比较自然的，色彩还原度也比较高'，肯定华为mate70色彩表现接近苹果。",
            "confidence": "高",
            "is_fluency_related": False
        })
        opinions.append({
            "opinion_text": "华为存在的问题就是发挥不稳定，前后拍了五六张照片，会存在有的暗有的亮的情况。",
            "brand_target": "华为",
            "sentiment_polarity": "负向",
            "sentiment_intensity": "中",
            "sentiment_reason": "原文'发挥不稳定'、'会存在有的暗有的亮的情况'，指出华为拍照一致性问题。",
            "confidence": "高",
            "is_fluency_related": False
        })
        opinions.append({
            "opinion_text": "苹果拍出的清晰度其实也不错，只是花蕊部分的细节没有华为那么清晰。",
            "brand_target": "苹果",
            "sentiment_polarity": "混合",
            "sentiment_intensity": "中",
            "sentiment_reason": "原文'清晰度其实也不错'为正向，但'花蕊部分的细节没有华为那么清晰'为负向，整体为混合评价。",
            "confidence": "高",
            "is_fluency_related": False
        })
        opinions.append({
            "opinion_text": "华为近距离拍摄的清晰度确实很绝，就连右边花瓣上沾着的绒毛都丝丝分明。",
            "brand_target": "华为",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "强",
            "sentiment_reason": "原文'清晰度确实很绝'、'绒毛都丝丝分明'，对华为微距拍摄清晰度高度赞赏。",
            "confidence": "高",
            "is_fluency_related": False
        })

    elif note_id == "68d4bb9c000000001101ce2f":
        # 帖子3021：iPhone钛金属边框讨论
        # 纯提问，无明确观点
        pass

    elif note_id == "6a0a9164000000003502adc8":
        # 帖子3022：请～大家帮忙选手机！
        opinions.append({
            "opinion_text": "一直都用的华为，感觉除了拍照不太行，系统和性能都很丝滑方便。",
            "brand_target": "华为",
            "sentiment_polarity": "混合",
            "sentiment_intensity": "中",
            "sentiment_reason": "原文'系统和性能都很丝滑方便'为正向，但'拍照不太行'为负向，整体为混合评价。",
            "confidence": "高",
            "is_fluency_related": True
        })
        opinions.append({
            "opinion_text": "但是现在的新机都是鸿蒙系统担心app不适配。",
            "brand_target": "华为",
            "sentiment_polarity": "负向",
            "sentiment_intensity": "中",
            "sentiment_reason": "原文'担心app不适配'，对华为鸿蒙系统生态适配表示担忧。",
            "confidence": "高",
            "is_fluency_related": True
        })
        opinions.append({
            "opinion_text": "周围的朋友都劝换苹果，但是担心信号和电池问题。",
            "brand_target": "苹果",
            "sentiment_polarity": "负向",
            "sentiment_intensity": "中",
            "sentiment_reason": "原文'担心信号和电池问题'，对苹果手机信号和电池续航持负面预期。",
            "confidence": "高",
            "is_fluency_related": True
        })

    elif note_id == "65ed958a0000000013026c63":
        # 帖子3023：十年果粉换华为深度对比
        # 华为体验升级
        opinions.append({
            "opinion_text": "信号：信号无论在什么地方都比苹果好太多太多了（比如用苹果的时候在停车场开不了导航，华为就完全不会有这个问题）。",
            "brand_target": "华为",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "强",
            "sentiment_reason": "原文'比苹果好太多太多了'、'华为就完全不会有这个问题'，对华为信号表现给予极高评价，对比苹果优势明显。",
            "confidence": "高",
            "is_fluency_related": True
        })
        opinions.append({
            "opinion_text": "后台留存：华为基本没有杀后台的问题，苹果经常打游戏的时候切出去回条消息就重新加载了。",
            "brand_target": "华为",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "强",
            "sentiment_reason": "原文'基本没有杀后台的问题'，对华为后台留存能力高度肯定，对比苹果优势明显。",
            "confidence": "高",
            "is_fluency_related": True
        })
        opinions.append({
            "opinion_text": "华为在信号切换的时候比苹果顺畅很多，比如从家里出门，从WiFi环境切换到5G，苹果会卡一段时间，华为很丝滑。",
            "brand_target": "华为",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "强",
            "sentiment_reason": "原文'比苹果顺畅很多'、'华为很丝滑'，对华为网络切换流畅度高度肯定。",
            "confidence": "高",
            "is_fluency_related": True
        })
        opinions.append({
            "opinion_text": "圆弧边框的手感比苹果好了不止一点。",
            "brand_target": "华为",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "中",
            "sentiment_reason": "原文'比苹果好了不止一点'，对华为圆弧边框手感明显优于苹果。",
            "confidence": "高",
            "is_fluency_related": False
        })
        opinions.append({
            "opinion_text": "88w快充真的太爽了谁用谁知道。",
            "brand_target": "华为",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "强",
            "sentiment_reason": "原文'真的太爽了谁用谁知道'，对华为快充体验高度赞赏。",
            "confidence": "高",
            "is_fluency_related": True
        })
        opinions.append({
            "opinion_text": "华为震动马达太太太廉价了，质感很差。",
            "brand_target": "华为",
            "sentiment_polarity": "负向",
            "sentiment_intensity": "强",
            "sentiment_reason": "原文'太太太廉价了，质感很差'，对华为震动马达强烈不满。",
            "confidence": "高",
            "is_fluency_related": False
        })
        opinions.append({
            "opinion_text": "华为在外放音量比较大的时候手机会震。",
            "brand_target": "华为",
            "sentiment_polarity": "负向",
            "sentiment_intensity": "中",
            "sentiment_reason": "原文'外放音量比较大的时候手机会震'，指出华为外放震手问题。",
            "confidence": "高",
            "is_fluency_related": False
        })
        opinions.append({
            "opinion_text": "华为耳机不如AirPods，所以现在我还是在用airpods，连接的时候要在蓝牙那边点一下。",
            "brand_target": "华为",
            "sentiment_polarity": "负向",
            "sentiment_intensity": "中",
            "sentiment_reason": "原文'华为耳机不如AirPods'，对华为耳机体验明确表示不如苹果。",
            "confidence": "高",
            "is_fluency_related": False
        })
        opinions.append({
            "opinion_text": "华为有很多广告要花十几分钟设置关掉。",
            "brand_target": "华为",
            "sentiment_polarity": "负向",
            "sentiment_intensity": "中",
            "sentiment_reason": "原文'有很多广告要花十几分钟设置关掉'，对华为系统广告多表示不满。",
            "confidence": "高",
            "is_fluency_related": True
        })
        opinions.append({
            "opinion_text": "华为看b站视频快进的时候声音会一卡一卡的，b站党崩溃。",
            "brand_target": "华为",
            "sentiment_polarity": "负向",
            "sentiment_intensity": "强",
            "sentiment_reason": "原文'声音会一卡一卡的，b站党崩溃'，对华为B站视频播放卡顿强烈不满。",
            "confidence": "高",
            "is_fluency_related": True
        })
        # 苹果相关
        opinions.append({
            "opinion_text": "苹果经常打游戏的时候切出去回条消息就重新加载了。",
            "brand_target": "苹果",
            "sentiment_polarity": "负向",
            "sentiment_intensity": "中",
            "sentiment_reason": "原文'苹果经常打游戏的时候切出去回条消息就重新加载了'，对苹果杀后台问题不满。",
            "confidence": "高",
            "is_fluency_related": True
        })
        opinions.append({
            "opinion_text": "用苹果的时候在停车场开不了导航。",
            "brand_target": "苹果",
            "sentiment_polarity": "负向",
            "sentiment_intensity": "中",
            "sentiment_reason": "原文'用苹果的时候在停车场开不了导航'，指出苹果信号差导致导航失效。",
            "confidence": "高",
            "is_fluency_related": True
        })
        opinions.append({
            "opinion_text": "苹果会卡一段时间。",
            "brand_target": "苹果",
            "sentiment_polarity": "负向",
            "sentiment_intensity": "中",
            "sentiment_reason": "原文'苹果会卡一段时间'，对苹果WiFi切换5G时的卡顿不满。",
            "confidence": "高",
            "is_fluency_related": True
        })

    elif note_id == "68eeee8c0000000004010015":
        # 帖子3024：从苹果用户换到华为感受
        opinions.append({
            "opinion_text": "苹果电池不耐用。",
            "brand_target": "苹果",
            "sentiment_polarity": "负向",
            "sentiment_intensity": "中",
            "sentiment_reason": "原文'苹果电池不耐用'，对苹果电池续航表示不满。",
            "confidence": "高",
            "is_fluency_related": True
        })
        opinions.append({
            "opinion_text": "到手第一天发现系统用不习惯，而且很多不更新我就了解了一下是在完善，开始好难受，好想退货。",
            "brand_target": "华为",
            "sentiment_polarity": "负向",
            "sentiment_intensity": "强",
            "sentiment_reason": "原文'开始好难受，好想退货'，对华为P80初期系统体验强烈不满。",
            "confidence": "高",
            "is_fluency_related": True
        })
        opinions.append({
            "opinion_text": "但是用了几天下来，发现鸿蒙系统完善很快，很多功能很强大，是苹果很多没有的功能。",
            "brand_target": "华为",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "强",
            "sentiment_reason": "原文'完善很快，很多功能很强大，是苹果很多没有的功能'，对华为鸿蒙系统功能丰富性高度肯定。",
            "confidence": "高",
            "is_fluency_related": True
        })
        opinions.append({
            "opinion_text": "支持华为，支持国产，越用越香，真的挺不错的，期待鸿蒙系统更加好。",
            "brand_target": "华为",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "强",
            "sentiment_reason": "原文'越用越香，真的挺不错的'，对华为整体体验高度认可并表达支持。",
            "confidence": "高",
            "is_fluency_related": False
        })

    elif note_id == "69f710cc0000000035026b15":
        # 帖子3025：Pura90标准版耐看
        opinions.append({
            "opinion_text": "结果看完真机越看越顺眼，属于耐看型越看越上头。",
            "brand_target": "华为",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "中",
            "sentiment_reason": "原文'越看越顺眼'、'越看越上头'，对华为Pura90外观耐看性给予正面评价。",
            "confidence": "高",
            "is_fluency_related": False
        })

    elif note_id == "69e602be000000002301d025":
        # 帖子3026：华为沉浸光感表现
        opinions.append({
            "opinion_text": "感觉华为这个沉浸光感还挺好看，华为的性能居然也能支撑得起来，而且还很流畅，这就是自研系统的好处吗？",
            "brand_target": "华为",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "强",
            "sentiment_reason": "原文'还挺好看'、'性能居然也能支撑得起来，而且还很流畅'，对华为沉浸光感视觉效果和性能支撑高度肯定。",
            "confidence": "高",
            "is_fluency_related": True
        })

    elif note_id == "681a0258000000001200456f":
        # 帖子3027：想问下大家在华为和苹果手机之间选了哪个
        pass

    elif note_id == "68698cb20000000024009cb7":
        # 帖子3028：苹果跟华为那个好
        pass

    elif note_id == "678bea44000000001901ee1c":
        # 帖子3029：苹果用户千万不要尝试换华为
        opinions.append({
            "opinion_text": "信号好，流畅度高，操作方便，续航好，充电快。",
            "brand_target": "华为",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "强",
            "sentiment_reason": "原文'信号好，流畅度高，操作方便，续航好，充电快'，对华为多项体验给予高度肯定。",
            "confidence": "高",
            "is_fluency_related": True
        })
        opinions.append({
            "opinion_text": "拍照哒咩（原相机发灰，录制视频不行，前置不如后置）。",
            "brand_target": "华为",
            "sentiment_polarity": "负向",
            "sentiment_intensity": "强",
            "sentiment_reason": "原文'拍照哒咩'、'原相机发灰，录制视频不行，前置不如后置'，对华为P70 Pro拍照能力强烈不满。",
            "confidence": "高",
            "is_fluency_related": False
        })
        opinions.append({
            "opinion_text": "想换回苹果。",
            "brand_target": "苹果",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "中",
            "sentiment_reason": "原文'想换回苹果'，因华为拍照不满而倾向回归苹果。",
            "confidence": "中",
            "is_fluency_related": False
        })

    elif note_id == "68311df6000000002203690a":
        # 帖子3030：到底是买华为还是苹果
        pass

    elif note_id == "67d3db2200000000090396e9":
        # 帖子3031：14pro想换mate70pro+
        opinions.append({
            "opinion_text": "苹果用了两年多了，感觉各方面的性能变慢了一点，系统方面也没有很流畅了。",
            "brand_target": "苹果",
            "sentiment_polarity": "负向",
            "sentiment_intensity": "中",
            "sentiment_reason": "原文'各方面的性能变慢了一点，系统方面也没有很流畅了'，对苹果14pro长期使用后性能下降和流畅度降低不满。",
            "confidence": "高",
            "is_fluency_related": True
        })
        opinions.append({
            "opinion_text": "但是看到华为mate系列才上新感觉还不错，正在考虑要不要换一个mate系列的高配。",
            "brand_target": "华为",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "弱",
            "sentiment_reason": "原文'感觉还不错'、'正在考虑要不要换一个mate系列的高配'，对华为mate系列新品持正面兴趣。",
            "confidence": "中",
            "is_fluency_related": False
        })

    elif note_id == "684ee05c000000002202eb23":
        # 帖子3032：选啥Pura80啊，现在买Mate70才真香
        opinions.append({
            "opinion_text": "现在Mate70降价，同配置比Pura80普遍便宜500-600。",
            "brand_target": "华为",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "中",
            "sentiment_reason": "原文指出Mate70降价后性价比高于Pura80，对Mate70购买价值持正面评价。",
            "confidence": "高",
            "is_fluency_related": False
        })
        opinions.append({
            "opinion_text": "9999都可以买Mate70Rs了，哪个男人能拒绝八边形Deco的诱惑？",
            "brand_target": "华为",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "强",
            "sentiment_reason": "原文'哪个男人能拒绝八边形Deco的诱惑'，对华为Mate70RS外观设计高度赞赏。",
            "confidence": "高",
            "is_fluency_related": False
        })
        opinions.append({
            "opinion_text": "买Pura80的等等，这一代降价空间也不小，水分不小。",
            "brand_target": "华为",
            "sentiment_polarity": "负向",
            "sentiment_intensity": "中",
            "sentiment_reason": "原文'水分不小'，暗示华为Pura80定价偏高，存在降价空间。",
            "confidence": "高",
            "is_fluency_related": False
        })

    elif note_id == "68a6f79b000000001b01d45e":
        # 帖子3033：同价位选华为还是苹果
        pass

    elif note_id == "68d7c7dc000000001201d4e3":
        # 帖子3034：17promax感觉银色最好看
        opinions.append({
            "opinion_text": "纠结橙色和银色，最后还是选了银色比较适合我吧。",
            "brand_target": "苹果",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "弱",
            "sentiment_reason": "原文'选了银色比较适合我吧'，对苹果17promax银色配色表示满意。",
            "confidence": "中",
            "is_fluency_related": False
        })

    elif note_id == "692d9cd8000000001d03e1da":
        # 帖子3035：华为80Pro使用体验
        opinions.append({
            "opinion_text": "但是我觉得还是够用，屏幕观感还行。",
            "brand_target": "华为",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "弱",
            "sentiment_reason": "原文'还是够用，屏幕观感还行'，对华为80Pro基本使用体验给予平淡肯定。",
            "confidence": "中",
            "is_fluency_related": False
        })
        opinions.append({
            "opinion_text": "就是这个自然色温怎么啥环境都偏冷呢？跟旁边的苹果形成鲜明对比感觉没啥用。",
            "brand_target": "华为",
            "sentiment_polarity": "负向",
            "sentiment_intensity": "中",
            "sentiment_reason": "原文'啥环境都偏冷'、'感觉没啥用'，对华为80Pro自然色温功能不满，认为不如苹果。",
            "confidence": "高",
            "is_fluency_related": False
        })
        opinions.append({
            "opinion_text": "外观质感相较于前几代我觉得是倒退，星环好评，直角高亮边框差评。",
            "brand_target": "华为",
            "sentiment_polarity": "混合",
            "sentiment_intensity": "中",
            "sentiment_reason": "原文'星环好评'为正向，'外观质感相较于前几代我觉得是倒退'、'直角高亮边框差评'为负向，整体混合评价。",
            "confidence": "高",
            "is_fluency_related": False
        })
        opinions.append({
            "opinion_text": "总评如果对华为有好感这代还是值得买的。",
            "brand_target": "华为",
            "sentiment_polarity": "正向",
            "sentiment_intensity": "弱",
            "sentiment_reason": "原文'对华为有好感这代还是值得买的'，对华为80Pro持条件性推荐态度。",
            "confidence": "中",
            "is_fluency_related": False
        })

    # 组装输出
    results = []
    for opinion_idx, op in enumerate(opinions, start=1):
        results.append({
            "opinion_id": f"batch3_{post_idx}_{opinion_idx}",
            "note_id": note_id,
            "title": title,
            "source_keyword": source_keyword,
            "liked_count": liked_count,
            "comment_count": comment_count,
            "opinion_text": op["opinion_text"],
            "brand_target": op["brand_target"],
            "sentiment_polarity": op["sentiment_polarity"],
            "sentiment_intensity": op["sentiment_intensity"],
            "sentiment_reason": op["sentiment_reason"],
            "confidence": op["confidence"],
            "full_title": title,
            "full_content": content,
            "is_fluency_related": op["is_fluency_related"]
        })

    return results


def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        posts = json.load(f)

    all_opinions = []
    for post_idx, post in enumerate(posts, start=1):
        opinions = analyze_post(post, post_idx)
        all_opinions.extend(opinions)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_opinions, f, ensure_ascii=False, indent=2)

    print(f"分析完成！共处理 {len(posts)} 条UGC，提取 {len(all_opinions)} 个观点。")
    print(f"结果已保存至: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
