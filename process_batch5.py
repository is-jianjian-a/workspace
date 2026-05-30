#!/usr/bin/env python3
"""
Process remaining-batch5: Extract brand-sentiment opinions from 10 xiaohongshu posts.
Uses semantic understanding, not keyword matching.
"""

import json

# Read input
with open("/Users/zhijian/workspace/mind-mining/v1.0/sentiment/02-batches/remaining-batch5-input.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

opinions = []
opinion_counter = 0

for idx, post in enumerate(posts):
    note_id = post["note_id"]
    title = post["title"]
    content = post["content"]
    full_text = title + "\n" + content
    source_keyword = post["source_keyword"]
    liked_count = post["liked_count"]
    comment_count = post["comment_count"]
    
    # Helper to create opinion
    def add_opinion(op_text, brand, polarity, intensity, reason, confidence, is_fluency):
        global opinion_counter
        opinion_counter += 1
        opinions.append({
            "opinion_id": f"rb5_{idx}_{opinion_counter}",
            "note_id": note_id,
            "title": title,
            "source_keyword": source_keyword,
            "liked_count": liked_count,
            "comment_count": comment_count,
            "opinion_text": op_text,
            "brand_target": brand,
            "sentiment_polarity": polarity,
            "sentiment_intensity": intensity,
            "sentiment_reason": reason,
            "confidence": confidence,
            "full_title": title,
            "full_content": content,
            "is_fluency_related": is_fluency
        })

    # ========== POST 115: iPhone14Pro换iPhoneAir ==========
    if idx == 0:
        # Opinion about 苹果 (iPhone Air) - positive on design/thermal, negative on speaker
        add_opinion(
            "iPhoneAir手感好轻薄不硌手，发热控制好，户外30度高亮度4G环境不烫手，芯片有提升",
            "苹果",
            "正向",
            "中",
            "原文：'手感好，轻薄不硌手，没有头重脚轻的感觉'、'发热控制比较好，虽然不及17pro系列，在户外30度高亮度4G环境，依旧感觉不到烫手'、'芯片提升'",
            "高",
            False
        )
        add_opinion(
            "iPhoneAir单扬声器最大音量比17系列小，横屏声音位置别扭；扬声器播放特定音频会滋啦滋啦响，50%音量以上也会出现，属于通病设计问题",
            "苹果",
            "负向",
            "中",
            "原文：'单扬声器，最大音量会比17系列要小'、'扬声器播放特定音频会滋啦滋啦响，或者50%音量以上也会出现'、'这个属于17pro以及air的通病设计问题好像说是因为共振导致的'",
            "高",
            False
        )
        # Mention of 华为 as comparison
        add_opinion(
            "iPhoneAir手感很接近华为mate30或40",
            "华为",
            "中性",
            "弱",
            "原文：'手感很\"接近\"华为mate30或40，个人感觉哈'——仅为手感类比，无明确褒贬",
            "中",
            False
        )

    # ========== POST 116: 15年苹果转华为 ==========
    elif idx == 1:
        # 华为 positive
        add_opinion(
            "华为Mate80ProMax信号比苹果好很多，家里从1格变4-5格；电池续航强，最多2天充一次",
            "华为",
            "正向",
            "强",
            "原文：'信号确实比苹果好很多，之前苹果在家里信号1格也是醉了，现在基本4-5格'、'电池确实缓解了我的焦虑...现在最多可以2天充一次'",
            "高",
            False
        )
        # 华为 negative issues
        add_opinion(
            "华为Mate80ProMax输入法响应速度比苹果慢；已适配鸿蒙的APP是阉割版本；手机太大单手操作麻烦",
            "华为",
            "负向",
            "中",
            "原文：'输入法响应的速度比苹果慢'、'已经适配鸿蒙系统的APP基本都是阉割版本'、'手机太大，单手操作确实麻烦'",
            "高",
            True
        )
        # 苹果 negative (reason for switching)
        add_opinion(
            "苹果15Pro信号差家里只有1格，电池健康度2年降到80%掉电快半天充一次",
            "苹果",
            "负向",
            "中",
            "原文：'之前苹果在家里信号1格也是醉了'、'15Pro用了2年电池健康度只有80%，掉电也快'",
            "高",
            False
        )

    # ========== POST 117: 华为Pura90被开除 ==========
    elif idx == 2:
        add_opinion(
            "华为Pura90标准版设计丑、没了Xmage、售价4699贵、与nova15 Ultra几乎一样，摄像头设计还不如nova15Ultra好看，是扶不起的阿斗",
            "华为",
            "负向",
            "强",
            "原文：'设计的丑就算了，没了Xmage也算了，卖的贵4699也可以忍一忍给你算了'、'你跟nova15 Ultra一样一样的啊'、'甚至摄像头设计的还没nova15Ultra好看'、'简直就是\"扶不起的阿斗\"'",
            "高",
            False
        )
        # Also mentions nova15Ultra (华为子品牌)
        add_opinion(
            "华为nova15 Ultra比Pura90设计更好看，被用来作为对比基准",
            "华为",
            "正向",
            "弱",
            "原文：'甚至摄像头设计的还没nova15Ultra好看'——通过对比间接肯定nova15U设计",
            "中",
            False
        )

    # ========== POST 118: 华为P系列何去何从 ==========
    elif idx == 3:
        # This is a critical analysis of 华为 P series
        add_opinion(
            "华为Pura系列影像能力和mate拉不开差距，mate70p+影像全面超越p70u，mate80pm主摄录像也超越p80u，Pura作为影像旗舰已等于甚至弱于同年mate",
            "华为",
            "负向",
            "强",
            "原文：'作为影像旗舰和mate影像拉不开差距'、'mate70p+影像表现全面超越p70u、mate80pm主摄、录像也超越p80u'",
            "高",
            False
        )
        add_opinion(
            "华为Pura系列卖点不足，机型阉割离谱，p70改名提价后标准版挤牙膏、芯片阉割、pro/pro+纯换皮、ultra定价万元；p80延续此做法大家已不买账",
            "华为",
            "负向",
            "强",
            "原文：'Pura系列卖点不足，机型阉割离谱'、'标准版配置挤牙膏还开创了芯片阉割，pro/pro+纯换皮，ultra定价拉到万元档'、'p80延续了p70的做法，但大家已经不买账了'",
            "高",
            False
        )
        add_opinion(
            "华为Pura系列丢失了美学、影像、轻薄的精髓，p80外观辨识度低、全系很重很厚，售价不合理比mate还贵",
            "华为",
            "负向",
            "中",
            "原文：'丢失了p系列精髓，售价不合理'、'p80是第一次没有大改外观，辨识度很难和p70区分开，全系很重很厚'、'mate70、mate80不断降价的同时，p70、p80价格却纹丝不动'",
            "高",
            False
        )
        # mate series is portrayed positively by comparison
        add_opinion(
            "华为mate系列影像技术首发多（可变光圈、xmage、红枫影像等），降价增配供不应求，表现优于Pura系列",
            "华为",
            "正向",
            "中",
            "原文：'mate80系列降价增配供不应求'、'华为近几年重要的影像技术全部在mate上面首发'——通过对比体现mate系列更受认可",
            "中",
            False
        )

    # ========== POST 119: 鸿蒙Next和iOS18差距 ==========
    elif idx == 4:
        # 华为/鸿蒙 positive
        add_opinion(
            "鸿蒙Next系统动画流畅非常接近iOS，第三方APP适配高斯模糊，隐私保护锁死第三方安装、安全访问相册相机",
            "华为",
            "正向",
            "强",
            "原文：'丝滑流畅：鸿蒙Next的系统动画支棱起来了...非常接近iOS，流畅到像德芙广告'、'第三方APP（比如微信、淘宝、京东）也适配了高斯模糊'、'鸿蒙Next和iOS都锁死了第三方安装...流氓APP窃取隐私是不存在的'",
            "高",
            True
        )
        add_opinion(
            "鸿蒙Next小艺AI功能强于Siri，传送能力（碰一碰、隔空投送）领先iOS，有悬浮窗/应用分身/分屏等iOS没有的功能，系统输入法语音转文字准确率比iOS好",
            "华为",
            "正向",
            "强",
            "原文：'小艺AI：长按图片拖给小艺...Siri遇到这些会说「我好像不明白」'、'两台鸿蒙手机碰一下就可以秒传...iOS的隔空投送还是先提升基础稳定性吧'、'边刷剧边回微信（悬浮窗）、双开工作号（应用分身）...这些iOS至今没有的功能'、'小艺语音转文字准确率比iOS好不少'",
            "高",
            True
        )
        # 苹果 positive
        add_opinion(
            "iOS生态完备无功能缺失，界面设计和过渡动画更细腻自然，审美在线；锁屏小组件种类丰富，实时活动适配更全面",
            "苹果",
            "正向",
            "中",
            "原文：'iOS先发优势生态已经十分完备'、'在控制中心，天气APP等界面设计和过渡动画还是没iOS细腻自然，苹果的审美依旧在线'、'iOS锁屏小组件种类丰富...iOS实时活动适配也更全面'",
            "高",
            True
        )
        # 华为 negative (ecosystem pain)
        add_opinion(
            "鸿蒙Next部分小众APP还没上架，已上架应用存在功能缺失，能用但还不够好用，处于生态阵痛期",
            "华为",
            "负向",
            "中",
            "原文：'鸿蒙Next部分小众APP还没上架商店，已上架的部分应用存在功能缺失，能用但还不够好用'",
            "高",
            False
        )

    # ========== POST 120: 鸿蒙真的好流畅 ==========
    elif idx == 5:
        add_opinion(
            "鸿蒙系统非常流畅方便，元服务好用不用下载软件看新闻没广告，网速和处理速度快",
            "华为",
            "正向",
            "强",
            "原文：'鸿蒙系统真的好方便，显得苹果好笨。鸿蒙的元服务也真的好用！不用下载软件，看新闻没广告可太好了！网速和处理速度也好快！'",
            "高",
            True
        )
        add_opinion(
            "苹果显得笨，从苹果换华为X7后感叹以前过的都是苦日子",
            "苹果",
            "负向",
            "中",
            "原文：'苹果已换华为X7，我以前过的都是什么苦日子啊😦鸿蒙系统真的好方便，显得苹果好笨'",
            "高",
            True
        )
        add_opinion(
            "华为X7微信适配一般，有个小程序蓝牙没法用",
            "华为",
            "负向",
            "弱",
            "原文：'就是微信的适配好像一般，有个小程序的蓝牙没法用'",
            "高",
            False
        )

    # ========== POST 121: 华为VS苹果 ==========
    elif idx == 6:
        # 苹果 positive
        add_opinion(
            "苹果手感好，app图标设计好看有质感，拍电子屏幕从不花屏很稳，无边记好用",
            "苹果",
            "正向",
            "中",
            "原文：'苹果最大优点：手感好，app图标设计好看，有质感，拍电子屏幕从不花屏，很稳，无边记很好用'",
            "高",
            False
        )
        # 苹果 negative
        add_opinion(
            "苹果不能通话录音，信号有时候不好，充电慢；使用时间长外壳升温，耗电快续航一般",
            "苹果",
            "负向",
            "中",
            "原文：'苹果最大缺点：不能通话录音，信号有时候不好，充电慢'、'两者共同缺点：使用时间长了外壳都会升温，耗电都挺快，续航能力都一般'",
            "高",
            False
        )
        # 华为 positive
        add_opinion(
            "华为可自动通话录音、截长图、自动屏蔽骚扰电话短信，充电非常快，拍远景方便清晰",
            "华为",
            "正向",
            "中",
            "原文：'华为最大优点：可自动通话录音，可截长图，可自动屏蔽骚扰电话和短信，充电非常快，拍远景很方便很清晰'",
            "高",
            False
        )
        # 华为 negative
        add_opinion(
            "华为拍电子屏幕会花屏，声音开大手机有震感；使用时间长外壳升温，耗电快续航一般",
            "华为",
            "负向",
            "弱",
            "原文：'华为最大缺点：拍电子屏幕会花屏，声音开大点手机会有震感'、'两者共同缺点：使用时间长了外壳都会升温，耗电都挺快，续航能力都一般'",
            "高",
            False
        )

    # ========== POST 122: 华为mate70pro+待机和流畅不行 ==========
    elif idx == 7:
        add_opinion(
            "华为mate70pro+待机和流畅都不行，用户用了几天后换回苹果",
            "华为",
            "负向",
            "强",
            "原文：'用了几天华为mate70pro+，待机和流畅都不行，换回苹果了，不折腾了'",
            "高",
            True
        )
        # Implicit positive for 苹果 (user switched back)
        add_opinion(
            "用户因华为体验不佳而换回苹果，暗示苹果在待机和流畅度方面更满意",
            "苹果",
            "正向",
            "中",
            "原文：'用了几天华为mate70pro+，待机和流畅都不行，换回苹果了'——通过换机决策间接表达对苹果的认可",
            "中",
            True
        )

    # ========== POST 123: mate80pro与iPhone17pro对比 ==========
    elif idx == 8:
        # 华为 positive
        add_opinion(
            "华为mate80pro白色好看，拍照颜色鲜艳比iPhone17好看，鸿蒙6.0卓易通兼容安卓app，功能性完爆iPhone17，英雄联盟流畅不发热，不杀后台，电量超级耐用",
            "华为",
            "正向",
            "强",
            "原文：'白色的80越看越好看'、'同是标准模式下随手拍了几张，看起来80的更好看，颜色更鲜艳'、'鸿蒙6.0的卓易通很好用，安卓app都可以兼容'、'功能性上完爆17'、'英雄联盟非常流畅，不会发热'、'80没感觉到杀后台'、'超级耐用，完爆苹果'",
            "高",
            True
        )
        # 华为 negative / mixed
        add_opinion(
            "华为mate80pro灵动岛设计不如iPhone17，音量键连在一起偏硬且和锁屏键同侧容易按错，后面板不支持磁吸，系统手感个人还是喜欢iOS",
            "华为",
            "负向",
            "中",
            "原文：'80的灵动岛设计暂时不如17'、'80的音量键是连在一起的，按起来偏硬，而且和锁屏键在一侧，容易按错'、'后面板不支持磁吸'、'系统层面，鸿蒙6.0非常流畅，不卡，但手感上个人还是喜欢iOS'",
            "高",
            True
        )
        # 苹果 negative
        add_opinion(
            "iPhone17背面拼接板丑，拍照泛白颜色柔和，iOS15p杀后台严重",
            "苹果",
            "负向",
            "中",
            "原文：'17只能说是看久了，偶尔还是会被背面那块拼接板丑到'、'17好像有点泛白，颜色更柔和点'、'我的15p杀后台严重'",
            "高",
            True
        )
        # 苹果 positive
        add_opinion(
            "iPhone17灵动岛设计更好，人脸识别图标和应用状态与挖孔融合更好，iOS系统手感更习惯，界面设计和过渡动画更细腻",
            "苹果",
            "正向",
            "中",
            "原文：'80的灵动岛设计暂时不如17，人脸识别图标、应用状态没有跟挖孔很好的融合'、'但手感上个人还是喜欢iOS'——通过对比体现iOS在交互细节上的优势",
            "中",
            True
        )
        # Update edit shows strong positive for 华为
        add_opinion(
            "深度体验后华为mate80非常好用没有短板，已经记不得iPhone好在哪里了",
            "华为",
            "正向",
            "强",
            "原文（编辑更新）：'80深度体验到现在，非常好用，没有短板，已经记不得ip好在哪里了'",
            "高",
            True
        )

    # ========== POST 124: 鸿蒙vs安卓coloros流畅度 ==========
    elif idx == 9:
        # This is a question post, no explicit sentiment
        add_opinion(
            "用户提问鸿蒙系统和安卓最流畅的coloros在流畅度上谁更好，寻求理性讨论，无明确褒贬立场",
            "华为",
            "中性",
            "弱",
            "原文：'鸿蒙系统和安卓最流畅coloros流畅度谁更好'——纯提问，无个人 sentiment",
            "高",
            True
        )
        add_opinion(
            "用户提问中提及安卓coloros作为对比对象，无明确褒贬立场",
            "安卓",
            "中性",
            "弱",
            "原文：'鸿蒙系统和安卓最流畅coloros流畅度谁更好'——被提及作为对比对象，无个人 sentiment",
            "高",
            True
        )

# Reset counter and re-assign proper opinion_ids
temp_opinions = opinions
opinions = []

# Group by post idx
from collections import defaultdict
by_post = defaultdict(list)
for op in temp_opinions:
    # Extract post idx from opinion_id
    parts = op["opinion_id"].split("_")
    post_idx = int(parts[1])
    by_post[post_idx].append(op)

for post_idx in sorted(by_post.keys()):
    ops = by_post[post_idx]
    for op_idx, op in enumerate(ops):
        op["opinion_id"] = f"rb5_{post_idx}_{op_idx}"
        opinions.append(op)

# Write output
with open("/Users/zhijian/workspace/mind-mining/v1.0/sentiment/02-batches/remaining-batch5-result.json", "w", encoding="utf-8") as f:
    json.dump(opinions, f, ensure_ascii=False, indent=2)

print(f"Processed {len(posts)} posts, extracted {len(opinions)} opinions.")
print(f"Output saved to remaining-batch5-result.json")
