#!/usr/bin/env python3
"""
classify_batch_032.py
读取 batch_032.json，对每条UGC进行8类分类（layer1主题 + layer2主题 + 情绪 + 场景 + UGC/营销/混合/中性），
输出 result_batch_032.json
"""
import json
from pathlib import Path

# 路径
INPUT_PATH = Path("/Users/zhijian/workspace/ai-demand-research-v3/projects/看视频时想要的AI功能-2026-05-18/02-cleaned/batches/batch_032.json")
OUTPUT_PATH = Path("/Users/zhijian/workspace/result_batch_032.json")

# ========== 8类分类词典 ==========

# 1. Layer1 主题（12个）
LAYER1 = {
    "视频摘要/总结": ["摘要", "总结", "概括", "提炼", "要点", "精华", "省流", "省时间", "没时间看", "太长", "快速了解"],
    "语音/字幕相关": ["字幕", "翻译", "同声传译", "外语", "英文", "日文", "听不懂", "口音", "语音识别", "语音转文字"],
    "内容搜索/定位": ["搜索", "找片段", "定位", "跳转到", "哪里提到", "关键词", "时间戳", "某个部分"],
    "智能推荐/过滤": ["推荐", "个性化", "猜我喜欢", "过滤", "屏蔽", "不感兴趣", "减少", "别推", "同质化", "重复"],
    "互动/问答": ["问视频", "聊天", "对话", "提问", "解答", "解释", "什么意思", "为什么", "怎么看"],
    "视频生成/编辑": ["生成", "剪辑", "自动剪辑", "高光", "精彩片段", "二创", "混剪", "AI生成", "换脸"],
    "学习/笔记": ["记笔记", "做笔记", "学习", "知识点", "重点", "复习", "收藏", "整理", "脑图", "思维导图"],
    "情感/氛围": ["氛围", "情绪", "配音乐", "BGM", "音效", "沉浸式", "助眠", "解压", "放松"],
    "效率/倍速": ["倍速", "快进", "跳过", "广告", "片头", "片尾", "注水", "拖沓", "节奏"],
    "画质/修复": ["画质", "修复", "高清", "4K", "模糊", "老视频", "上色", "补帧", "清晰"],
    "跨设备/同步": ["投屏", "同步", "跨设备", "手机看", "电脑看", "平板", "电视", "无缝", "续播"],
    "社交/分享": ["分享", "转发", "发给朋友", "一起看", "弹幕", "评论", "讨论", "Reaction"],
}

# 2. Layer2 主题（34个）
LAYER2 = {
    "长视频压缩": ["省流", "省时间", "没时间看", "太长", "快速了解", "速读", "brief", "梗概"],
    "智能摘要": ["摘要", "总结", "概括", "提炼", "要点", "精华", "一句话"],
    "章节拆分": ["章节", "分段", "目录", "时间节点", "结构化"],
    "实时翻译": ["翻译", "同声传译", "双语", "外语", "英文", "日文", "实时"],
    "字幕生成": ["字幕", "语音识别", "语音转文字", "自动生成字幕", "实时字幕"],
    "口音处理": ["口音", "方言", "听不懂", "语速", "发音"],
    "语义搜索": ["语义", "意思", "内容搜索", "搜视频"],
    "片段定位": ["找片段", "定位", "跳转到", "时间戳", "某个部分"],
    "关键词高亮": ["关键词", "高亮", "标记", "标注"],
    "兴趣推荐": ["猜我喜欢", "个性化", "推荐", "兴趣", "喜好"],
    "去重过滤": ["同质化", "重复", "相似", "去重", "过滤"],
    "负面屏蔽": ["屏蔽", "不感兴趣", "减少", "别推", "拉黑"],
    "视频问答": ["问视频", "视频问答", "提问", "解答", "什么意思"],
    "AI对话": ["聊天", "对话", "AI助手", "智能问答", "交互"],
    "知识解释": ["解释", "为什么", "怎么看", "原理", "科普"],
    "AI生成视频": ["AI生成", "生成视频", "文生视频", "图生视频", "一键成片"],
    "自动剪辑": ["自动剪辑", "高光", "精彩片段", "剪辑", "智能剪辑"],
    "二创工具": ["二创", "混剪", "换脸", "数字人", "虚拟主播", "模板", "合拍"],
    "笔记工具": ["记笔记", "做笔记", "学习笔记", "整理", "收藏"],
    "知识提取": ["知识点", "重点", "提取", "脑图", "思维导图"],
    "学习管理": ["复习", "学习", "课程", "知识管理", "进度"],
    "氛围音效": ["氛围", "配音乐", "BGM", "音效", "沉浸式"],
    "助眠解压": ["助眠", "解压", "放松", "ASMR", "白噪音"],
    "情绪适配": ["情绪", "情绪识别", "心情", "适配"],
    "智能倍速": ["倍速", "智能倍速", "语速", "节奏"],
    "跳过广告": ["跳过", "广告", "片头", "片尾"],
    "内容精简": ["注水", "拖沓", "精简", "智能跳过", "快进"],
    "画质增强": ["画质", "高清", "4K", "清晰", "超分", "画质增强"],
    "老片修复": ["修复", "老视频", "上色", "补帧", "去噪", "复古"],
    "多端同步": ["同步", "跨设备", "云端同步", "无缝", "续播"],
    "投屏控制": ["投屏", "电视", "平板", "多屏"],
    "一起看": ["一起看", "同框", "合拍", "同步看"],
    "分享转发": ["分享", "转发", "发给朋友"],
    "弹幕评论": ["弹幕", "评论", "讨论", "Reaction"],
}

# 3. 情绪标签（6个）
EMOTIONS = {
    "frustration": ["烦", "讨厌", "受不了", "恶心", "垃圾", "难用", "失望", "无语", "崩溃", "抓狂", "气死", "火大"],
    "焦虑/急迫": ["急", "赶时间", "没时间", "来不及", "太慢", "等不及", "焦虑", "着急", "紧迫"],
    "困惑/迷茫": ["不懂", "不明白", "不知道", "迷茫", "困惑", "看不懂", "什么意思", "疑惑"],
    "疲惫/厌倦": ["累", "疲惫", "厌倦", "无聊", "重复", "同质化", "看腻了", "审美疲劳"],
    "期待/渴望": ["希望", "期待", "想要", "如果能", "要是", "建议", "最好", "强烈", "迫切需要", "急需"],
    "惊喜/兴奋": ["惊艳", "绝了", "牛", "厉害", "神奇", "方便", "爽", "爱了", "哇塞", "震撼"],
}

# 4. 场景标签（6个）
SCENES = {
    "通勤/路上": ["通勤", "地铁", "公交", "路上", "开车", "骑车", "走路", "出行", "旅途"],
    "工作/学习": ["上班", "工作", "学习", "上课", "自习", "办公室", "备考", "考研", "职场", "学生"],
    "睡前/休息": ["睡前", "睡觉", "躺床上", "休息", "放松", "助眠", "失眠", "熬夜", "躺平"],
    "吃饭/碎片": ["吃饭", "外卖", "等餐", "排队", "课间", "午休", "碎片", "摸鱼", "间隙"],
    "运动/健身": ["运动", "健身", "跑步", "瑜伽", "锻炼", "健身房"],
    "家庭/陪伴": ["家人", "孩子", "陪", "一起看", "客厅", "电视", "家庭", "亲子"],
}

# 5. UGC/营销/混合/中性 分类信号
MARKETING_SIGNALS = ["广告", "推广", "合作", "赞助", "品牌", "优惠", "折扣", "限时", "抢购", "链接", "购买", "下单", "私信", "咨询", "关注我", "戳链接", "点击", "领取", "同款", "对接", "扣1", "邀请码", "教程", "保姆级", "快速上手", "官方地址", "使用手册"]
UGC_SIGNALS = ["我", "我的", "我家", "我们", "亲身经历", "亲测", "实测", "感觉", "觉得", "认为", "体验", "感受"]


def parse_count(val):
    """解析互动量字符串为整数"""
    if val is None:
        return 0
    val = str(val).strip()
    if not val or val == '':
        return 0
    val = val.replace(',', '').replace('，', '')
    if '万' in val:
        val = val.replace('万', '')
        try:
            return int(float(val) * 10000)
        except:
            return 0
    try:
        return int(float(val))
    except:
        return 0


def extract_tags(text, dictionary):
    """从文本中提取标签，首次命中即归入"""
    if not text:
        return []
    text = str(text)
    tags = []
    for tag, keywords in dictionary.items():
        for kw in keywords:
            if kw in text:
                tags.append(tag)
                break
    return tags


def classify_content_type(text):
    """分类内容类型：UGC/营销/混合/中性"""
    if not text:
        return "中性"
    text = str(text)
    marketing_score = sum(1 for s in MARKETING_SIGNALS if s in text)
    ugc_score = sum(1 for s in UGC_SIGNALS if s in text)

    has_marketing = marketing_score >= 2
    has_ugc = ugc_score >= 1

    if has_marketing and not has_ugc:
        return "营销"
    elif has_ugc and not has_marketing:
        return "UGC"
    elif has_marketing and has_ugc:
        return "混合"
    else:
        return "中性"


def classify_ugc(ugc):
    """对单条UGC进行分类"""
    text = f"{ugc.get('title', '')}\n{ugc.get('content', '')}\n{ugc.get('full_text', '')}"

    layer1 = extract_tags(text, LAYER1)
    layer2 = extract_tags(text, LAYER2)
    emotions = extract_tags(text, EMOTIONS)
    scenes = extract_tags(text, SCENES)
    content_type = classify_content_type(text)

    return {
        "id": ugc.get("id"),
        "platform": ugc.get("platform"),
        "title": ugc.get("title"),
        "content": ugc.get("content"),
        "liked_count": parse_count(ugc.get("liked_count")),
        "source_keyword": ugc.get("source_keyword"),
        "layer1": layer1,
        "layer2": layer2,
        "emotions": emotions,
        "scenes": scenes,
        "content_type": content_type,
    }


def main():
    # 读取输入
    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    ugcs = data.get("ugcs", [])

    # 分类
    classified = [classify_ugc(ugc) for ugc in ugcs]

    # 统计
    stats = {
        "total": len(classified),
        "content_type": {},
        "layer1": {},
        "layer2": {},
        "emotions": {},
        "scenes": {},
    }
    for item in classified:
        # content_type
        ct = item["content_type"]
        stats["content_type"][ct] = stats["content_type"].get(ct, 0) + 1
        # layer1
        for tag in item["layer1"]:
            stats["layer1"][tag] = stats["layer1"].get(tag, 0) + 1
        # layer2
        for tag in item["layer2"]:
            stats["layer2"][tag] = stats["layer2"].get(tag, 0) + 1
        # emotions
        for tag in item["emotions"]:
            stats["emotions"][tag] = stats["emotions"].get(tag, 0) + 1
        # scenes
        for tag in item["scenes"]:
            stats["scenes"][tag] = stats["scenes"].get(tag, 0) + 1

    # 输出结果
    result = {
        "batch_id": data.get("batch_id"),
        "start_idx": data.get("start_idx"),
        "end_idx": data.get("end_idx"),
        "total_batches": data.get("total_batches"),
        "stats": stats,
        "classified_ugcs": classified,
    }

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"✅ 分类完成，共 {len(classified)} 条UGC")
    print(f"📊 内容类型分布: {stats['content_type']}")
    print(f"📁 结果已保存至: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
