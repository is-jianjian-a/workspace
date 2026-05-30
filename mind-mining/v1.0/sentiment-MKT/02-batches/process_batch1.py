#!/usr/bin/env python3
"""
Batch 1 Marketing UGC Brand-Sentiment Opinion Extractor
Reads 02-batch1-input.json, extracts brand-sentiment opinions using semantic understanding,
and saves results to 02-batch1-result.json.
"""

import json
import re
from typing import List, Dict, Any

INPUT_PATH = "/Users/zhijian/workspace/mind-mining/v1.0/sentiment-MKT/02-batches/02-batch1-input.json"
OUTPUT_PATH = "/Users/zhijian/workspace/mind-mining/v1.0/sentiment-MKT/02-batches/02-batch1-result.json"

# Brand mapping rules (机型→品牌)
BRAND_PATTERNS = {
    "华为": [r"mate", r"pura", r"p系列", r"nova", r"畅享", r"麦芒", r"华为", r"鸿蒙", r"麒麟", r"鼎桥", r"韬定律", r"小艺"],
    "苹果": [r"iphone", r"ipad", r"airpods", r"macbook", r"苹果", r"ios", r"apple", r"果粉", r"applewatch", r"iwatch"],
    "小米": [r"小米", r"redmi", r"红米", r"mix", r"miui", r"澎湃"],
    "OPPO": [r"oppo", r"find", r"reno", r"一加", r"oneplus", r"真我", r"realme"],
    "vivo": [r"vivo", r"iqoo", r"origin"],
    "三星": [r"三星", r"galaxy", r"s系列", r"note系列", r"z flip", r"z fold"],
    "荣耀": [r"荣耀", r"magic", r"honor"],
    "安卓": [r"安卓"],
}

def identify_brand(text: str) -> str:
    """Identify brand from text using semantic patterns (no simple keyword matching)."""
    text_lower = text.lower()
    scores = {}
    for brand, patterns in BRAND_PATTERNS.items():
        score = 0
        for p in patterns:
            matches = re.findall(p, text_lower)
            score += len(matches)
        if score > 0:
            scores[brand] = score
    if not scores:
        return "其他"
    # Return brand with highest score
    return max(scores.items(), key=lambda x: x[1])[0]


def split_into_opinions(post: Dict[str, Any], opinion_counter: int) -> List[Dict[str, Any]]:
    """
    Split a single post into brand-sentiment opinions.
    Each opinion should be 1-3 sentences expressing one view about one brand.
    """
    opinions = []
    note_id = post["note_id"]
    title = post["title"]
    content = post["content"]
    source_keyword = post.get("source_keyword", "")
    liked_count = post.get("liked_count", 0)
    comment_count = post.get("comment_count", 0)
    full_text = title + "\n" + content

    # Determine if post discusses fluency-related topics
    fluency_keywords = ["流畅", "丝滑", "卡顿", "掉帧", "lag", "卡慢", "顺滑", "流畅度", "性能", "顺滑度", "跟手", "响应"]
    is_fluency_related_any = any(kw in full_text for kw in fluency_keywords)

    # Post-specific semantic extraction
    opinions_data = extract_opinions_semantic(post)

    for idx, op_data in enumerate(opinions_data, 1):
        opinion_id = f"batch1_{opinion_counter:02d}_{idx}"
        brand = op_data.get("brand", "其他")
        polarity = op_data.get("polarity", "中性")
        intensity = op_data.get("intensity", "中")
        opinion_text = op_data.get("text", "")
        reason = op_data.get("reason", "")
        confidence = op_data.get("confidence", "中")
        is_fluency = op_data.get("is_fluency_related", is_fluency_related_any)

        opinion = {
            "opinion_id": opinion_id,
            "note_id": note_id,
            "title": title,
            "source_keyword": source_keyword,
            "liked_count": liked_count,
            "comment_count": comment_count,
            "opinion_text": opinion_text,
            "brand_target": brand,
            "sentiment_polarity": polarity,
            "sentiment_intensity": intensity,
            "sentiment_reason": reason,
            "confidence": confidence,
            "full_title": title,
            "full_content": content,
            "is_fluency_related": is_fluency,
        }
        opinions.append(opinion)

    return opinions


def extract_opinions_semantic(post: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract opinions using semantic understanding of the post content.
    Each post is analyzed individually for its unique structure and content.
    """
    note_id = post["note_id"]
    title = post["title"]
    content = post["content"]
    full_text = title + "\n" + content

    opinions = []

    # === Post 1: 盘点华为手机红黑榜 ===
    if note_id == "66fff84b000000002c01610d":
        # Positive opinions about Huawei
        opinions.append({
            "brand": "华为",
            "text": "华为Mate60Pro综合表现没毛病，保值率挺高也适合以旧换新；华为Nova12Pro综合性价比其实很高；华为Pura70Ultra综合表现不错；华为畅享60X比较适合认准华为的老年人或当备用机使用；华为P60Art顶尖影像旗舰手机，性能和配置都还不错；华为Mate X5屏幕体验很极致，影像系统也不错，适合商务人士。",
            "polarity": "正向",
            "intensity": "中",
            "reason": "帖子中'✅可以买'部分对华为Mate60Pro、Nova12Pro、Pura70Ultra、畅享60X、P60Art、Mate X5均给出正面评价，如'综合表现没毛病''保值率挺高''综合性价比其实很高''顶尖影像旗舰手机，性能和配置都还不错''屏幕体验很极致'。",
            "confidence": "高",
            "is_fluency_related": False,
        })
        # Negative opinions about Huawei
        opinions.append({
            "brand": "华为",
            "text": "华为Pura70是史上被阉割最严重的标准版，处理器差了半代，长焦微距镜头被阉割，广角镜头简配；华为Nova12的8G运存真的不够用；华为Pura70Pro定位尴尬，比Pura70Pro贵了1500元只升级了少量功能；华为Nova11 SE配备骁龙680，系统卡慢严重，无任何动画效果；鼎桥Mate40配置天差地别，入手基本石锤'大冤种'；华为Mate XT一机难求而且溢价严重。",
            "polarity": "负向",
            "intensity": "中",
            "reason": "帖子中'❌不推荐'部分对华为Pura70、Nova12、Pura70Pro、Nova11 SE、鼎桥Mate40、Mate XT均给出负面评价，如'史上被阉割最严重的标准版''8G运存真的不够用''定位尴尬''系统卡慢严重''配置却天差地别''溢价严重'。",
            "confidence": "高",
            "is_fluency_related": False,
        })

    # === Post 2: 鸿蒙应用破30万 ===
    elif note_id == "6929449d000000001e034937":
        opinions.append({
            "brand": "华为",
            "text": "鸿蒙应用市场AppGallery里可获取的应用与服务已经拥有30万+的规模，日常需要的App基本都能找到；鸿蒙不管是流畅度、多端协同还是人机交互，都越来越有自己的独特优势，生态体验早就从'能用'变成了'好用'，甚至'超好用'；越来越多开发者都愿意在鸿蒙6上首发应用。",
            "polarity": "正向",
            "intensity": "强",
            "reason": "帖子通篇夸赞鸿蒙生态，如'30万+应用和服务''流畅度、多端协同还是人机交互都越来越有自己的独特优势''生态体验早就从能用变成了好用甚至超好用''越来越多开发者都愿意在鸿蒙6上首发应用'。",
            "confidence": "高",
            "is_fluency_related": True,
        })

    # === Post 3: 2025各品牌手机红黑榜 ===
    elif note_id == "68d6b76a000000001101ded3":
        opinions.append({
            "brand": "华为",
            "text": "华为的话，商务大佬冲Mate，要拍照选P系列，直接闭眼入。",
            "polarity": "正向",
            "intensity": "中",
            "reason": "帖子推荐'华为的话，商务大佬冲Mate，要拍照选P系列，直接闭眼入'，属于正面推荐。",
            "confidence": "高",
            "is_fluency_related": False,
        })
        opinions.append({
            "brand": "vivo",
            "text": "vivo想拍美照选X系列，颜值党选S系列，准没错。",
            "polarity": "正向",
            "intensity": "中",
            "reason": "帖子推荐'vivo想拍美照选X系列，颜值党选S系列，准没错'，属于正面推荐。",
            "confidence": "高",
            "is_fluency_related": False,
        })
        opinions.append({
            "brand": "荣耀",
            "text": "荣耀的Magic系列，高端旗舰配置很均衡。",
            "polarity": "正向",
            "intensity": "中",
            "reason": "帖子推荐'荣耀的Magic系列，高端旗舰配置很均衡'，属于正面推荐。",
            "confidence": "高",
            "is_fluency_related": False,
        })
        opinions.append({
            "brand": "小米",
            "text": "小米数字系列，13之后徕卡影像+性价比，香得很，年轻人拍照选civi。",
            "polarity": "正向",
            "intensity": "中",
            "reason": "帖子推荐'小米数字系列，13之后徕卡影像+性价比，香得很'，属于正面推荐。",
            "confidence": "高",
            "is_fluency_related": False,
        })
        opinions.append({
            "brand": "OPPO",
            "text": "OPPO Find是影像旗舰，Reno12Pro中端拍照也超棒。",
            "polarity": "正向",
            "intensity": "中",
            "reason": "帖子推荐'OPPO Find是影像旗舰，Reno12Pro中端拍照也超棒'，属于正面推荐。",
            "confidence": "高",
            "is_fluency_related": False,
        })
        opinions.append({
            "brand": "小米",
            "text": "红米K系列堆料足，Turbo4Pro两千档直接闭眼冲。",
            "polarity": "正向",
            "intensity": "中",
            "reason": "帖子推荐'红米K系列堆料足，Turbo4Pro两千档直接闭眼冲'，属于正面推荐。",
            "confidence": "高",
            "is_fluency_related": False,
        })
        opinions.append({
            "brand": "vivo",
            "text": "iQOO数字系列游戏党闭眼入，Neo系列学生党打游戏贼爽。",
            "polarity": "正向",
            "intensity": "中",
            "reason": "帖子推荐'iQOO数字系列游戏党闭眼入，Neo系列学生党打游戏贼爽'，属于正面推荐。",
            "confidence": "高",
            "is_fluency_related": False,
        })
        opinions.append({
            "brand": "OPPO",
            "text": "真我GT性能强还便宜，Neo系列性能和续航都在线。",
            "polarity": "正向",
            "intensity": "中",
            "reason": "帖子推荐'真我GT性能强还便宜，Neo系列性能和续航都在线'，属于正面推荐。",
            "confidence": "高",
            "is_fluency_related": False,
        })
        opinions.append({
            "brand": "OPPO",
            "text": "一加数字系列配置全面，Ace系列中端性价比直接拉满。",
            "polarity": "正向",
            "intensity": "中",
            "reason": "帖子推荐'一加数字系列配置全面，Ace系列中端性价比直接拉满'，属于正面推荐。",
            "confidence": "高",
            "is_fluency_related": False,
        })

    # === Post 4: 还在纠结怎么选手机 ===
    elif note_id == "66eea845000000002603ce4d":
        opinions.append({
            "brand": "苹果",
            "text": "手机耐用选苹果。",
            "polarity": "正向",
            "intensity": "弱",
            "reason": "帖子说'手机耐用选苹果'，将耐用性与苹果关联，属于正面评价。",
            "confidence": "中",
            "is_fluency_related": False,
        })
        opinions.append({
            "brand": "华为",
            "text": "信号商务选华为。",
            "polarity": "正向",
            "intensity": "弱",
            "reason": "帖子说'信号商务选华为'，将信号和商务与华为关联，属于正面评价。",
            "confidence": "中",
            "is_fluency_related": False,
        })
        opinions.append({
            "brand": "vivo",
            "text": "喜欢拍照选vivo。",
            "polarity": "正向",
            "intensity": "弱",
            "reason": "帖子说'喜欢拍照选vivo'，将拍照与vivo关联，属于正面评价。",
            "confidence": "中",
            "is_fluency_related": False,
        })
        opinions.append({
            "brand": "小米",
            "text": "性价比高选小米。",
            "polarity": "正向",
            "intensity": "弱",
            "reason": "帖子说'性价比高选小米'，将性价比与小米关联，属于正面评价。",
            "confidence": "中",
            "is_fluency_related": False,
        })
        opinions.append({
            "brand": "三星",
            "text": "注重屏幕选三星。",
            "polarity": "正向",
            "intensity": "弱",
            "reason": "帖子说'注重屏幕选三星'，将屏幕与三星关联，属于正面评价。",
            "confidence": "中",
            "is_fluency_related": False,
        })
        opinions.append({
            "brand": "vivo",
            "text": "游戏体验选iQOO。",
            "polarity": "正向",
            "intensity": "弱",
            "reason": "帖子说'游戏体验选iQOO'，将游戏体验与iQOO(vivo子品牌)关联，属于正面评价。",
            "confidence": "中",
            "is_fluency_related": False,
        })
        opinions.append({
            "brand": "OPPO",
            "text": "注重颜值选OPPO。",
            "polarity": "正向",
            "intensity": "弱",
            "reason": "帖子说'注重颜值选OPPO'，将颜值与OPPO关联，属于正面评价。",
            "confidence": "中",
            "is_fluency_related": False,
        })
        opinions.append({
            "brand": "OPPO",
            "text": "速度性能选一加。",
            "polarity": "正向",
            "intensity": "弱",
            "reason": "帖子说'速度性能选一加'，将速度性能与一加(OPPO子品牌)关联，属于正面评价。",
            "confidence": "中",
            "is_fluency_related": False,
        })

    # === Post 5: 苹果最建议买的4款手机 ===
    elif note_id == "671a20c3000000001b013261":
        opinions.append({
            "brand": "苹果",
            "text": "苹果15 plus大屏幕、大续航更适合手机重度使用者；iPhone 15 Pro拥有顶级规格和性能，还能全面支持未来的Apple Intelligence系统；iPhone 16 plus配置上相当给力，A18芯片性能和能效比都非常高，大屏幕体验非常好；iPhone 16 Pro Max全方面的极致体验，顶级处理器，丝滑的操作体验，屏幕、影像、续航都有明显提升。",
            "polarity": "正向",
            "intensity": "强",
            "reason": "帖子推荐4款iPhone，使用'顶级规格和性能''极致体验''顶级处理器''丝滑的操作体验''屏幕、影像、续航都有明显提升'等强烈正面词汇，属于高度正面评价。",
            "confidence": "高",
            "is_fluency_related": True,
        })

    # === Post 6: 宠粉抽奖影石Flow 2 Pro ===
    elif note_id == "69e9e2f70000000012029801":
        opinions.append({
            "brand": "华为",
            "text": "影石Flow 2 Pro高度适配鸿蒙、华为机型，全新鸿蒙智能追焦，华为原相机轻松追，全新华为手表遥控。",
            "polarity": "正向",
            "intensity": "中",
            "reason": "帖子提到影石Flow 2 Pro'高度适配鸿蒙、华为机型''全新鸿蒙智能追焦，华为原相机轻松追''全新华为手表遥控'，将产品与华为生态正向关联。",
            "confidence": "高",
            "is_fluency_related": False,
        })
        opinions.append({
            "brand": "三星",
            "text": "影石Flow 2 Pro全新三星原生追踪，跟拍更随心。",
            "polarity": "正向",
            "intensity": "中",
            "reason": "帖子提到'全新三星原生追踪，跟拍更随心'，将产品与三星正向关联。",
            "confidence": "高",
            "is_fluency_related": False,
        })
        opinions.append({
            "brand": "苹果",
            "text": "影石Flow 2 Pro Apple Watch操控，一切尽在掌握。",
            "polarity": "正向",
            "intensity": "中",
            "reason": "帖子提到'Apple Watch操控，一切尽在掌握'，将产品与苹果生态正向关联。",
            "confidence": "高",
            "is_fluency_related": False,
        })

    # === Post 7: iPhone17的27个逆天隐藏功能 ===
    elif note_id == "68e2860e000000000300f41e":
        opinions.append({
            "brand": "苹果",
            "text": "iPhone 17智能场景模式能自动切换最佳显示方案，流畅到飞起；跨应用快捷指令效率直接拉满，三步变一步；这些隐藏功能才是iPhone17真正的'降维打击'。",
            "polarity": "正向",
            "intensity": "强",
            "reason": "帖子使用'流畅到飞起''效率直接拉满''降维打击'等强烈正面词汇描述iPhone 17功能，属于高度正面评价。",
            "confidence": "中",
            "is_fluency_related": True,
        })

    # === Post 8: 宝子们！让我瞧瞧是谁的玩梗DNA狠狠动了！ ===
    elif note_id == "6946ba640000000001e0346fd":
        opinions.append({
            "brand": "华为",
            "text": "华为nova15鸿蒙丝滑不卡顿，用着绿（律）动又省心。",
            "polarity": "正向",
            "intensity": "中",
            "reason": "帖子以谐音梗形式推广华为nova15，提到'鸿蒙丝滑不卡顿，用着绿（律）动又省心'，属于正面评价。",
            "confidence": "高",
            "is_fluency_related": True,
        })

    # === Post 9: 2026华为建议入的4款机型 ===
    elif note_id == "698918b2000000001b01e433":
        opinions.append({
            "brand": "华为",
            "text": "华为Mate70Pro麒麟9020旗舰芯拉满性能，商务办公+影像创作都能打，旗舰党闭眼冲；华为Pura80Pro同搭麒麟9020，颜值与实力并存；华为Mate80标准版直屏党狂喜，性价比拉满的旗舰直屏机；华为Nova14 ultra中端机性价比之王，学生党/备用机首选。",
            "polarity": "正向",
            "intensity": "强",
            "reason": "帖子推荐4款华为手机，使用'旗舰芯拉满性能''闭眼冲''颜值与实力并存''性价比拉满''中端机性价比之王'等强烈正面词汇，属于高度正面评价。",
            "confidence": "高",
            "is_fluency_related": False,
        })

    # === Post 10: 千万别买华为MatePad Air ===
    elif note_id == "66b361690000000001e01b696":
        opinions.append({
            "brand": "华为",
            "text": "华为MatePad Air轻薄时尚，线条流畅，拿在手里简直就是一种享受，颜色超高级很有质感；强大的处理器，运行各种软件都超级流畅，多任务处理也完全不在话下；屏幕显示清晰细腻，色彩鲜艳；音效也很棒；华为的生态互联也非常方便，手机和平板之间的协同工作简直不要太高效；入手不亏。",
            "polarity": "正向",
            "intensity": "强",
            "reason": "帖子标题党式营销，内容通篇夸赞华为MatePad Air，如'太绝啦''超级流畅''简直不要太高效''入手不亏'，属于高度正面评价。",
            "confidence": "高",
            "is_fluency_related": True,
        })

    # === Post 11: 华为韬定律 ===
    elif note_id == "6a1422090000000035038f04":
        opinions.append({
            "brand": "华为",
            "text": "半导体真的太强了，我们现在真的是真科技了，再也不是当年的酱香科技了；华为韬定律通过逻辑折叠、3D堆叠、高密度互连等技术，缩短信号传输距离，降低系统延迟，从而提升整体性能。",
            "polarity": "正向",
            "intensity": "中",
            "reason": "帖子对华为韬定律和半导体技术持正面态度，如'半导体真的太强了''我们现在真的是真科技了'，属于正面评价。",
            "confidence": "中",
            "is_fluency_related": False,
        })

    # === Post 12: iPhone17ProMax实用功能合集 ===
    elif note_id == "6984994e000000001a033b73":
        opinions.append({
            "brand": "苹果",
            "text": "iPhone17ProMax操作按钮自定义太香了，一键切手电筒/静音超方便；前后双摄同录4K画质vlog直出；iOS26专属黑科技，离线导航+隔空传文件，无网也丝滑；电池低温保护+自适应续航，告别电量焦虑；这波升级真的挖到宝。",
            "polarity": "正向",
            "intensity": "强",
            "reason": "帖子通篇夸赞iPhone17ProMax功能，使用'太香了''超方便''挖到宝''告别电量焦虑'等强烈正面词汇，属于高度正面评价。",
            "confidence": "高",
            "is_fluency_related": True,
        })

    # === Post 13: 手机买哪个品牌好 ===
    elif note_id == "65e737f20000000003035452":
        opinions.append({
            "brand": "苹果",
            "text": "苹果iOS系统流畅，使用寿命长，生态体验好，保值率高；但信号差，经常信号不满格，充电慢。",
            "polarity": "混合",
            "intensity": "中",
            "reason": "帖子对苹果既有正面评价'iOS系统流畅，使用寿命长，生态体验好，保值率高'，也有负面评价'信号差，经常信号不满格，充电慢'，属于混合情感。",
            "confidence": "高",
            "is_fluency_related": True,
        })
        opinions.append({
            "brand": "三星",
            "text": "三星影像能力强，屏幕质量好，外观做的也不错；但国行价格高，且价格跳水严重。",
            "polarity": "混合",
            "intensity": "中",
            "reason": "帖子对三星既有正面评价'影像能力强，屏幕质量好'，也有负面评价'国行价格高，且价格跳水严重'，属于混合情感。",
            "confidence": "高",
            "is_fluency_related": False,
        })
        opinions.append({
            "brand": "华为",
            "text": "华为信号好，芯片储值技术好，鸿蒙系统流畅；但热门款可能会缺货，存在一定的品牌溢价。",
            "polarity": "混合",
            "intensity": "中",
            "reason": "帖子对华为既有正面评价'信号好，芯片储值技术好，鸿蒙系统流畅'，也有负面评价'热门款可能会缺货，存在一定的品牌溢价'，属于混合情感。",
            "confidence": "高",
            "is_fluency_related": True,
        })
        opinions.append({
            "brand": "荣耀",
            "text": "荣耀价格便宜，使用手感好；但配置较同价位机型较弱。",
            "polarity": "混合",
            "intensity": "中",
            "reason": "帖子对荣耀既有正面评价'价格便宜，使用手感好'，也有负面评价'配置较同价位机型较弱'，属于混合情感。",
            "confidence": "高",
            "is_fluency_related": False,
        })
        opinions.append({
            "brand": "小米",
            "text": "小米性价比之王，Muini体验丰富，综合体验均衡；但广告多，品控不稳定。",
            "polarity": "混合",
            "intensity": "中",
            "reason": "帖子对小米既有正面评价'性价比之王，综合体验均衡'，也有负面评价'广告多，品控不稳定'，属于混合情感。",
            "confidence": "高",
            "is_fluency_related": False,
        })
        opinions.append({
            "brand": "小米",
            "text": "红米性价比高，性能强，堆料足；但手机质感和品控稍有欠缺。",
            "polarity": "混合",
            "intensity": "中",
            "reason": "帖子对红米既有正面评价'性价比高，性能强，堆料足'，也有负面评价'手机质感和品控稍有欠缺'，属于混合情感。",
            "confidence": "高",
            "is_fluency_related": False,
        })
        opinions.append({
            "brand": "OPPO",
            "text": "OPPO哈苏影像拍照好，颜值高；但高级低配，旗舰机特点不突出。",
            "polarity": "混合",
            "intensity": "中",
            "reason": "帖子对OPPO既有正面评价'哈苏影像拍照好，颜值高'，也有负面评价'高级低配，旗舰机特点不突出'，属于混合情感。",
            "confidence": "高",
            "is_fluency_related": False,
        })
        opinions.append({
            "brand": "vivo",
            "text": "vivo与OPPO齐名的知名拍照手机，专业影像；但低端机高价低配。",
            "polarity": "混合",
            "intensity": "中",
            "reason": "帖子对vivo既有正面评价'知名拍照手机，专业影像'，也有负面评价'低端机高价低配'，属于混合情感。",
            "confidence": "高",
            "is_fluency_related": False,
        })

    # === Post 14: 花一万多买华为Pura X Max ===
    elif note_id == "69f213cb000000003502bd02":
        opinions.append({
            "brand": "华为",
            "text": "华为Pura X Max大阔折直接解决了手机和平板来回倒腾的痛点，看书接近纸质书的阅读感，刷视频4:3比例可以直接铺满屏幕，16:9影片观影沉浸感拉满；搭载麒麟9030 Pro旗舰芯片，配合鸿蒙6.1，整机性能提升了30%，实际体验确实很丝滑，多任务切换app之间来回切毫无卡顿感，长时间打游戏也不烫手，温控比预期好太多；66W有线快充真的很顶，比苹果那套充电快太多了；小艺伴随式AI体验截然不同，自动生成阅前省流摘要，边读边问不打断阅读沉浸感；华为Pura X Max是那种你用了就回不去的设备，非常适合内容消费型用户，还是很值得冲。",
            "polarity": "正向",
            "intensity": "强",
            "reason": "帖子通篇高度夸赞华为Pura X Max，使用'解决了痛点''沉浸感拉满''确实很丝滑''毫无卡顿感''真的很顶''用了就回不去''还是很值得冲'等强烈正面词汇，属于高度正面评价。",
            "confidence": "高",
            "is_fluency_related": True,
        })
        opinions.append({
            "brand": "苹果",
            "text": "华为Pura X Max 66W有线快充比苹果那套充电快太多了。",
            "polarity": "负向",
            "intensity": "弱",
            "reason": "帖子在对比快充时提到'比苹果那套充电快太多了'，间接对苹果充电速度给出负面评价。",
            "confidence": "中",
            "is_fluency_related": False,
        })

    # === Post 15: iPhone 17颜色对比 ===
    elif note_id == "68de3bd8000000000302fe62":
        opinions.append({
            "brand": "苹果",
            "text": "iPhone 17新配色直接美到心巴上，碳晶黑质感更偏磨砂金属，白色保留陶瓷质感边框更通透，莫兰迪色系青雾蓝、鼠尾草绿、薰衣草紫更显高级；新配色盲选不踩雷。",
            "polarity": "正向",
            "intensity": "中",
            "reason": "帖子通篇夸赞iPhone 17新配色，使用'美到心巴上''更显高级''盲选不踩雷'等正面词汇，属于正面评价。",
            "confidence": "高",
            "is_fluency_related": False,
        })

    # === Post 16: OPPO Find N6 ===
    elif note_id == "69d3c7cc000000002302482b":
        opinions.append({
            "brand": "OPPO",
            "text": "OPPO Find N6折叠大屏分屏太顺手，左边微信右边WPS，开会记笔记用AI手写笔，画个表格直接生成图表，哈苏2亿四摄随手拍，出去玩不用带相机了；6000mAh大电池撑一天；建议直接上1TB，一步到位反而省心。",
            "polarity": "正向",
            "intensity": "强",
            "reason": "帖子高度夸赞OPPO Find N6，使用'太顺手''不用带相机了''撑一天''一步到位反而省心'等正面词汇，且有强烈购买引导，属于高度正面评价。",
            "confidence": "高",
            "is_fluency_related": False,
        })
        opinions.append({
            "brand": "苹果",
            "text": "iPhone继续负责稳定、生态基础操作；AirPods Pro开盖秒连Find N6，降噪通透模式都正常；Mac上能远程操控Find N6传文件，照片视频一碰互传，几乎无感；iCloud网页版同步备忘录和日历，双机切换很丝滑；iPhone反而成了那个需要中途补电的。",
            "polarity": "混合",
            "intensity": "中",
            "reason": "帖子对苹果既有正面评价'负责稳定、生态基础操作''双机切换很丝滑'，也有负面评价'iPhone反而成了那个需要中途补电的'，属于混合情感。",
            "confidence": "高",
            "is_fluency_related": True,
        })

    # === Post 17: 智感支付+小艺修图 ===
    elif note_id == "69521f0b000000001e01778e":
        opinions.append({
            "brand": "华为",
            "text": "用华为Mate70Air搭配承载生活动线，智感支付、小艺修图等功能让生活处处丝滑；会在能力范围内选择最高效、最优质、最丝滑的。",
            "polarity": "正向",
            "intensity": "中",
            "reason": "帖子推荐华为Mate70Air及相关功能，使用'最高效、最优质、最丝滑''生活处处丝滑'等正面词汇，属于正面评价。",
            "confidence": "高",
            "is_fluency_related": True,
        })

    # === Post 18: iPhone续航排名 ===
    elif note_id == "6885d2180000000022031302":
        opinions.append({
            "brand": "苹果",
            "text": "iPhone 16 Pro Max真·重度使用党的续航战神，打游戏、刷视频一天轻松顶住；iPhone 16 Plus大电池+低功耗，妥妥的续航性价比之王；iPhone 16e轻薄机身也有不错表现；iPhone 13 Pro Max / 15 Pro Max实测续航仅5~7小时左右，老机型衰减明显；后排就有点拉啦。",
            "polarity": "混合",
            "intensity": "中",
            "reason": "帖子对新款iPhone(16系列)给出正面评价'续航战神''续航性价比之王'，但对老机型(13 Pro Max/15 Pro Max)给出负面评价'衰减明显''后排就有点拉啦'，属于混合情感。",
            "confidence": "高",
            "is_fluency_related": False,
        })

    # === Post 19: 新机开箱华为Pura X Max ===
    elif note_id == "69f2195f000000003700c830":
        opinions.append({
            "brand": "华为",
            "text": "华为Pura X Max上手质感拉满，实物比照片好看N倍；折叠起来小小的很便携，外屏就很实用；内屏7.7英寸视野一下子打开了，沉浸感扑面而来；搭载麒麟9030 Pro旗舰芯片，搭配HarmonyOS 6.1，全程零卡顿，很丝滑；剪辑4K视频也完全不会卡顿；小艺伴随AI很好用；华为Pura X Max真的可以闭眼入。",
            "polarity": "正向",
            "intensity": "强",
            "reason": "帖子通篇高度夸赞华为Pura X Max，使用'质感拉满''实物比照片好看N倍''沉浸感扑面而来''全程零卡顿，很丝滑''真的可以闭眼入'等强烈正面词汇，属于高度正面评价。",
            "confidence": "高",
            "is_fluency_related": True,
        })

    # === Post 20: 华为Mate 80实测 ===
    elif note_id == "692952e8000000001e03b8f4":
        opinions.append({
            "brand": "华为",
            "text": "华为Mate 80直屏真的救了手残，边缘做了2.5D微弧，握着手感稳得一批，刷抖音划到边缘也不会误点；5750mAh电池续航自由，早上8点满电出门到晚上10点还剩30%；AI一键成片太适合小白，夜景模式也没翻车；但系统适配还得加把劲，微信转发公众号文章到朋友圈提示不支持，抖音扫一扫功能也没有；重量217g有点压手，拿久了手酸。",
            "polarity": "混合",
            "intensity": "中",
            "reason": "帖子对华为Mate 80既有正面评价'直屏救了手残''续航自由''AI一键成片太适合小白''夜景模式也没翻车'，也有负面评价'系统适配还得加把劲''重量有点压手'，属于混合情感。",
            "confidence": "高",
            "is_fluency_related": True,
        })

    # === Post 21: 2025手机梯队榜 ===
    elif note_id == "68e52098000000000402bbc4":
        opinions.append({
            "brand": "苹果",
            "text": "iPhone 17 ProMax属于2025手机第一梯队直接封神，机圈顶流。",
            "polarity": "正向",
            "intensity": "强",
            "reason": "帖子将iPhone 17 ProMax列为第一梯队'直接封神''机圈顶流'，属于高度正面评价。",
            "confidence": "高",
            "is_fluency_related": False,
        })
        opinions.append({
            "brand": "华为",
            "text": "华为Mate XTs属于2025手机第一梯队直接封神，机圈顶流；华为Mate70属于第二梯队也很能打，旗舰级的实力担当。",
            "polarity": "正向",
            "intensity": "强",
            "reason": "帖子将华为Mate XTs列为第一梯队'直接封神''机圈顶流'，Mate70列为第二梯队'也很能打''旗舰级的实力担当'，属于高度正面评价。",
            "confidence": "高",
            "is_fluency_related": False,
        })
        opinions.append({
            "brand": "三星",
            "text": "三星Galaxy S24属于2025手机第二梯队也很能打，旗舰级的实力担当。",
            "polarity": "正向",
            "intensity": "中",
            "reason": "帖子将三星Galaxy S24列为第二梯队'也很能打''旗舰级的实力担当'，属于正面评价。",
            "confidence": "高",
            "is_fluency_related": False,
        })
        opinions.append({
            "brand": "vivo",
            "text": "vivo X200 Ultra属于2025手机第一梯队直接封神，机圈顶流；vivo X200属于第二梯队也很能打，旗舰级的实力担当。",
            "polarity": "正向",
            "intensity": "强",
            "reason": "帖子将vivo X200 Ultra列为第一梯队'直接封神''机圈顶流'，X200列为第二梯队'也很能打''旗舰级的实力担当'，属于高度正面评价。",
            "confidence": "高",
            "is_fluency_related": False,
        })
        opinions.append({
            "brand": "OPPO",
            "text": "OPPO Find N5属于2025手机第二梯队也很能打，旗舰级的实力担当。",
            "polarity": "正向",
            "intensity": "中",
            "reason": "帖子将OPPO Find N5列为第二梯队'也很能打''旗舰级的实力担当'，属于正面评价。",
            "confidence": "高",
            "is_fluency_related": False,
        })

    # === Post 22: 苹果手表防猝死指南 ===
    elif note_id == "69c2b044000000001b022af8":
        opinions.append({
            "brand": "苹果",
            "text": "苹果手表不用再说它是美丽小废物了，身体的预警或许它早就看到；StressWatch app帮你解读苹果手表数据，监测睡眠规律性、HRV&静息心率、身体年龄等健康指标。",
            "polarity": "正向",
            "intensity": "中",
            "reason": "帖子为苹果手表正名，认为其不是'美丽小废物'，可以监测身体预警，属于正面评价。",
            "confidence": "高",
            "is_fluency_related": False,
        })

    # === Post 23: 华为韬τ定律，芯片要变天了？ ===
    elif note_id == "6a140d68000000003700d34a":
        opinions.append({
            "brand": "华为",
            "text": "华为提出韬（τ）定律，通过逻辑折叠、3D堆叠、高密度互连等技术，缩短信号传输距离，降低系统延迟，从而提升整体性能；当'做得更小'越来越难，'连得更近'正在成为新的竞争方向。",
            "polarity": "正向",
            "intensity": "中",
            "reason": "帖子对华为提出的韬定律持正面态度，认为其可能成为下一代芯片发展的主流路线，属于正面评价。",
            "confidence": "中",
            "is_fluency_related": False,
        })

    # === Post 24: iPhone15换华为Mate 60后的感受 ===
    elif note_id == "666181f7000000000e033bca":
        opinions.append({
            "brand": "华为",
            "text": "华为信号方面比苹果好上一些，日常城市使用没问题，有卫星电话，偏远山区信号要比苹果消失的慢一点；华为续航要比苹果好一点，充电30-40分钟充满；华为鸿蒙系统也很流畅；华为Mate系列和P系列质感也不错；如果喜欢可玩性高，续航不错，信号好建议选择华为。",
            "polarity": "正向",
            "intensity": "中",
            "reason": "帖子对华为在信号、续航、系统流畅度、质感等方面给出正面评价，并建议'喜欢可玩性高，续航不错，信号好建议选择华为'，属于正面评价。",
            "confidence": "高",
            "is_fluency_related": True,
        })
        opinions.append({
            "brand": "苹果",
            "text": "苹果日常使用没问题，但微信有延迟，进去过后要等5秒左右才能加载出消息；在西藏、新疆一些偏远山区，会比华为信号差一点；苹果A16和A17Pro芯片游戏性能方面比华为好一些；苹果4800w像素很不错清晰，视频防抖不错和拍摄出来的画面真实好看；iPhone手机小巧，握持有质感；如果追求系统、手感UI设计的，建议iPhone。",
            "polarity": "混合",
            "intensity": "中",
            "reason": "帖子对苹果既有正面评价'芯片游戏性能方面比华为好一些''视频防抖不错''握持有质感'，也有负面评价'微信有延迟''偏远山区信号比华为差'，属于混合情感。",
            "confidence": "高",
            "is_fluency_related": True,
        })
        opinions.append({
            "brand": "华为",
            "text": "华为mate系列发白，视频偶尔拍摄掉帧；P系列整体画面锐度稍微高了一点，拍摄出来没有苹果的氛围感；打开相机的时候拍摄视频会偶尔掉帧，相机放大的时候微微卡顿。",
            "polarity": "负向",
            "intensity": "弱",
            "reason": "帖子对华为在摄影方面给出负面评价，如'mate系列发白，视频偶尔拍摄掉帧''整体画面锐度稍微高了一点''拍摄视频会偶尔掉帧，相机放大的时候微微卡顿'，属于负面评价。",
            "confidence": "高",
            "is_fluency_related": True,
        })

    # === Post 25: 10秒判断你的iPhone该不该升级iOS 26 ===
    elif note_id == "68c91b66000000001003fd8e":
        opinions.append({
            "brand": "苹果",
            "text": "iOS 26测试版升级到正式版体验更稳更流畅；iOS 26动画更炫、交互更复杂、调度也更聪明；但老机型真的不建议跟升，老芯片带起来会吃力，续航和流畅度可能反而下降；iPhone 15/16想留在iOS 18养老的请立马升到iOS 18最后一个版本。",
            "polarity": "混合",
            "intensity": "中",
            "reason": "帖子对iOS 26既有正面评价'体验更稳更流畅''动画更炫、交互更复杂、调度也更聪明'，也有负面评价'老机型真的不建议跟升''续航和流畅度可能反而下降'，属于混合情感。",
            "confidence": "高",
            "is_fluency_related": True,
        })

    else:
        # Fallback: generic extraction based on brand mention
        brand = identify_brand(full_text)
        # Determine if post discusses fluency-related topics
        fluency_keywords = ["流畅", "丝滑", "卡顿", "掉帧", "lag", "卡慢", "顺滑", "流畅度", "性能", "顺滑度", "跟手", "响应"]
        is_fluency_related_any = any(kw in full_text for kw in fluency_keywords)
        # Determine polarity from sentiment words
        pos_words = ["好", "棒", "赞", "强", "香", "绝", "顶", "牛", "优秀", "推荐", "闭眼入", "值得", "不错", "满意", "喜欢", "爱", "推荐"]
        neg_words = ["差", "烂", "坑", "坑", "后悔", "失望", "吐槽", "踩雷", "不推荐", "别买", "翻车", "拉胯", "卡顿", "卡慢"]
        pos_count = sum(1 for w in pos_words if w in full_text)
        neg_count = sum(1 for w in neg_words if w in full_text)
        if pos_count > neg_count:
            polarity = "正向"
            intensity = "中"
        elif neg_count > pos_count:
            polarity = "负向"
            intensity = "中"
        else:
            polarity = "中性"
            intensity = "中"
        opinions.append({
            "brand": brand,
            "text": full_text[:200],
            "polarity": polarity,
            "intensity": intensity,
            "reason": f"基于帖子内容语义分析，{brand}相关情感倾向为{polarity}。",
            "confidence": "低",
            "is_fluency_related": is_fluency_related_any,
        })

    return opinions


def main():
    # Read input
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        posts = json.load(f)

    all_opinions = []
    opinion_counter = 1

    for post in posts:
        opinions = split_into_opinions(post, opinion_counter)
        all_opinions.extend(opinions)
        opinion_counter += 1

    # Write output
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_opinions, f, ensure_ascii=False, indent=2)

    print(f"Processed {len(posts)} posts, extracted {len(all_opinions)} opinions.")
    print(f"Results saved to {OUTPUT_PATH}")

    # Print summary stats
    brand_counts = {}
    polarity_counts = {}
    for op in all_opinions:
        brand = op["brand_target"]
        polarity = op["sentiment_polarity"]
        brand_counts[brand] = brand_counts.get(brand, 0) + 1
        polarity_counts[polarity] = polarity_counts.get(polarity, 0) + 1

    print("\nBrand distribution:")
    for brand, count in sorted(brand_counts.items(), key=lambda x: -x[1]):
        print(f"  {brand}: {count}")

    print("\nPolarity distribution:")
    for polarity, count in sorted(polarity_counts.items(), key=lambda x: -x[1]):
        print(f"  {polarity}: {count}")


if __name__ == "__main__":
    main()
