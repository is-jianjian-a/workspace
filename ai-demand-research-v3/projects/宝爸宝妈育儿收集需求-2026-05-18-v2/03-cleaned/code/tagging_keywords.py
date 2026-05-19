#!/usr/bin/env python3
"""
标签提取脚本 - 关键词匹配方案（降级备用）
项目：宝爸宝妈育儿收集需求 v2
"""
import json
import re
from pathlib import Path

# 加载关键词词典
KEYWORDS_PATH = Path(__file__).parent / "tagging_keywords.json"
with open(KEYWORDS_PATH, 'r', encoding='utf-8') as f:
    KEYWORDS = json.load(f)


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


def extract_tags(text):
    """从文本中提取标签"""
    if not text:
        return {
            'layer1': [],
            'layer2': [],
            'emotions': [],
            'scenes': [],
            'signals': []
        }
    
    text = str(text)
    result = {
        'layer1': [],
        'layer2': [],
        'emotions': [],
        'scenes': [],
        'signals': []
    }
    
    # Layer 1 主题
    for theme, data in KEYWORDS['layer1_themes'].items():
        for kw in data['keywords']:
            if kw in text:
                if theme not in result['layer1']:
                    result['layer1'].append(theme)
                break
    
    # Layer 2 主题
    for parent_theme, sub_themes in KEYWORDS['layer2_themes'].items():
        for sub_theme, keywords in sub_themes.items():
            for kw in keywords:
                if kw in text:
                    tag = f"{parent_theme}>{sub_theme}"
                    if tag not in result['layer2']:
                        result['layer2'].append(tag)
                    break
    
    # 情绪
    for emotion, keywords in KEYWORDS['emotions'].items():
        for kw in keywords:
            if kw in text:
                if emotion not in result['emotions']:
                    result['emotions'].append(emotion)
                break
    
    # 场景
    for scene, keywords in KEYWORDS['scenes'].items():
        for kw in keywords:
            if kw in text:
                if scene not in result['scenes']:
                    result['scenes'].append(scene)
                break
    
    # 信号
    for signal_type, keywords in KEYWORDS['signals'].items():
        for kw in keywords:
            if kw in text:
                if signal_type not in result['signals']:
                    result['signals'].append(signal_type)
                break
    
    return result


def classify_content(row):
    """分类内容类型：UGC/营销/混合/中性"""
    text = f"{row.get('title', '')} {row.get('content', '')}"
    
    # 营销信号
    marketing_signals = ['广告', '推广', '合作', '赞助', '品牌', '优惠', '折扣', '限时', '抢购', '链接', '购买', '下单', '私信', '咨询', '关注我', '戳链接', '点击', '领取', '同款', '对接', '扣1']
    marketing_score = sum(1 for s in marketing_signals if s in text)
    
    # UGC信号
    ugc_signals = ['我家', '我家宝宝', '我家孩子', '我家娃', '亲身经历', '亲测', '实测', '我家宝贝', '我孩子', '我娃', '我家小', '我的宝宝', '我家大宝', '我家二宝']
    ugc_score = sum(1 for s in ugc_signals if s in text)
    
    # 个人代词
    personal_pronouns = ['我', '我的', '我家', '我们']
    personal_score = sum(1 for s in personal_pronouns if s in text)
    
    # 判断
    has_marketing = marketing_score >= 2
    has_ugc = ugc_score >= 1 or personal_score >= 5
    
    if has_marketing and not has_ugc:
        return '营销'
    elif has_ugc and not has_marketing:
        return 'UGC'
    elif has_marketing and has_ugc:
        return '混合'
    else:
        return '中性'


if __name__ == '__main__':
    # 测试
    test_text = "新手妈妈求助：宝宝夜醒频繁怎么办？已经崩溃了，每天睡眠不足"
    tags = extract_tags(test_text)
    print(f"测试文本: {test_text}")
    print(f"标签: {json.dumps(tags, ensure_ascii=False, indent=2)}")
