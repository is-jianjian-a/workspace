#!/usr/bin/env python3
"""
华为苹果性能对比UGC精确主题段落打标脚本
三个主题：流畅丝滑、卡顿问题、稳定性
"""

import json
import re
import os

# 主题关键词定义
SMOOTH_KEYWORDS = ['丝滑', '流畅', '顺滑', '跟手', '动画', '高刷', '120hz', '120赫兹', '刷新率', '帧率稳定', '不掉帧', '不卡', '响应快', '反应快', '动效']
LAG_KEYWORDS = ['卡顿', '掉帧', '卡死', '反应慢', '延迟', '转圈圈', '加载慢', '打开慢', '启动慢', '不流畅', '卡爆', '卡到', '卡的要死', '卡的相当', '巨卡', '卡卡卡', '卡了', '很卡', '太卡', '有点卡', '小卡', '卡帧', '锁帧']
STABILITY_KEYWORDS = ['闪退', '崩溃', '死机', '重启', 'bug', '发热严重', '发烫', '系统稳定', '系统不稳定', '发热', '烫手', '温度高', '过热']

def extract_sentences(text):
    """将文本拆分为句子列表"""
    # 按句号、感叹号、问号、换行分割
    sentences = re.split(r'[。！？\n]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences

def find_theme_quotes(text, keywords):
    """找到包含主题关键词的句子，返回相关句子列表"""
    sentences = extract_sentences(text)
    matched = []
    for sent in sentences:
        for kw in keywords:
            if kw in sent:
                matched.append(sent)
                break
    return matched

def determine_brand(quote, title, tags, full_content):
    """从quote中推断品牌+机型"""
    quote_lower = quote.lower()
    full_lower = full_content.lower()
    title_lower = title.lower()
    
    # 华为机型映射
    huawei_models = {
        'mate60pro': '华为Mate60Pro', 'mate 60 pro': '华为Mate60Pro', 'mate60': '华为Mate60',
        'mate70pro': '华为Mate70Pro', 'mate 70 pro': '华为Mate70Pro', 'mate70': '华为Mate70',
        'mate80pro': '华为Mate80Pro', 'mate 80 pro': '华为Mate80Pro', 'mate80': '华为Mate80',
        'mate90': '华为Mate90', 'pura70': '华为Pura70', 'pura80': '华为Pura80',
        'pura90': '华为Pura90', 'p40': '华为P40', 'p50': '华为P50', 'p60': '华为P60',
        'p70': '华为P70', 'p80': '华为P80', 'p90': '华为P90',
        'purax': '华为PuraX', 'pura x': '华为PuraX', 'puraxmax': '华为PuraXMax',
        'mate x5': '华为MateX5', 'matex5': '华为MateX5',
        'mate40pro': '华为Mate40Pro', 'mate 40 pro': '华为Mate40Pro',
        'mate60rs': '华为Mate60RS', 'mate 60 rs': '华为Mate60RS',
        'mate70pro+': '华为Mate70Pro+', 'mate 70 pro+': '华为Mate70Pro+',
        'mate80promax': '华为Mate80ProMax', 'mate80 pro max': '华为Mate80ProMax',
        'mate70air': '华为Mate70Air', 'mate 70 air': '华为Mate70Air',
        'nova': '华为Nova',
    }
    
    # 苹果机型映射
    apple_models = {
        'iphone15pro': 'iPhone15Pro', 'iphone 15 pro': 'iPhone15Pro', 'iphone15': 'iPhone15',
        'iphone16pro': 'iPhone16Pro', 'iphone 16 pro': 'iPhone16Pro', 'iphone16': 'iPhone16',
        'iphone17pro': 'iPhone17Pro', 'iphone 17 pro': 'iPhone17Pro', 'iphone17': 'iPhone17',
        'iphone18': 'iPhone18', 'iphone14pro': 'iPhone14Pro', 'iphone 14 pro': 'iPhone14Pro',
        'iphone14': 'iPhone14', 'iphone13': 'iPhone13', 'iphone12': 'iPhone12',
        'iphone11': 'iPhone11', 'iphone 11 pro max': 'iPhone11ProMax',
        'iphone15promax': 'iPhone15ProMax', 'iphone 15 pro max': 'iPhone15ProMax',
        'iphone16promax': 'iPhone16ProMax', 'iphone 16 pro max': 'iPhone16ProMax',
        'iphone17promax': 'iPhone17ProMax', 'iphone 17 pro max': 'iPhone17ProMax',
        '16pm': 'iPhone16ProMax', '17pm': 'iPhone17ProMax', '15pm': 'iPhone15ProMax',
        '16pro': 'iPhone16Pro', '17pro': 'iPhone17Pro', '15pro': 'iPhone15Pro',
        '17p': 'iPhone17Pro', '16p': 'iPhone16Pro',
    }
    
    huawei_found = []
    apple_found = []
    
    # 检查quote
    for key, model in huawei_models.items():
        if key in quote_lower:
            huawei_found.append(model)
    for key, model in apple_models.items():
        if key in quote_lower:
            apple_found.append(model)
    
    # 如果quote中没有，扩展到全文
    if not huawei_found and not apple_found:
        for key, model in huawei_models.items():
            if key in full_lower or key in title_lower:
                huawei_found.append(model)
        for key, model in apple_models.items():
            if key in full_lower or key in title_lower:
                apple_found.append(model)
    
    # 去重并保持顺序
    huawei_found = list(dict.fromkeys(huawei_found))
    apple_found = list(dict.fromkeys(apple_found))
    
    if huawei_found and apple_found:
        return '华为/苹果'
    elif huawei_found:
        return huawei_found[0]
    elif apple_found:
        return apple_found[0]
    
    # 只提到品牌
    if '华为' in quote or '鸿蒙' in quote or 'harmony' in quote_lower:
        if '苹果' in quote or 'iphone' in quote_lower or 'ios' in quote_lower:
            return '华为/苹果'
        return '华为'
    if '苹果' in quote or 'iphone' in quote_lower or 'ios' in quote_lower:
        return '苹果'
    
    # 从全文推断品牌
    has_huawei = '华为' in full_content or '鸿蒙' in full_content
    has_apple = '苹果' in full_content or 'iPhone' in full_content or 'iOS' in full_content
    if has_huawei and has_apple:
        return '华为/苹果'
    elif has_huawei:
        return '华为'
    elif has_apple:
        return '苹果'
    
    return '不明确'

def determine_sentiment(quote, theme):
    """根据quote本身的情感色彩判断"""
    quote_lower = quote.lower()
    
    # 负面词汇
    negative_words = ['不', '没', '差', '烂', '垃圾', '恶心', '无语', '失望', '后悔', '难用', '烦', '恼火', '吐槽', '问题', 'bug', '崩', '死机', '闪退', '烫', '热', '卡', '慢', '迟钝', '延迟', '掉帧', '锁帧']
    
    # 正面词汇
    positive_words = ['丝滑', '流畅', '顺滑', '好', '棒', '香', '爽', '优秀', '出色', '不错', '满意', '喜欢', '爱', '赞', '强', '快', '稳', '舒服', '舒适', '沉浸', '惊喜']
    
    # 特殊处理
    if theme == '卡顿问题':
        # 卡顿主题本身通常是负面表达
        if any(w in quote for w in ['不卡', '没卡', '不卡顿', '不流畅']):
            return '负面'
        return '负面'
    
    if theme == '稳定性':
        # 提到闪退/崩溃/死机/发热严重等是负面
        if any(w in quote for w in ['闪退', '崩溃', '死机', '重启', 'bug', '发热严重', '发烫']):
            return '负面'
        if '稳定' in quote and '不稳定' not in quote and '稳定选' not in quote:
            return '正面'
        if '不烫' in quote or '不发烫' in quote or '温度控制好' in quote:
            return '正面'
        return '负面'
    
    if theme == '流畅丝滑':
        # 检查是否有明确的负面修饰
        if '不丝滑' in quote or '不流畅' in quote or '卡顿' in quote or '掉帧' in quote or '卡' in quote:
            return '负面'
        if '有点卡' in quote or '小卡顿' in quote or '小小的掉帧' in quote:
            return '负面'
        if '流畅度一般' in quote or '流畅度不够' in quote:
            return '负面'
        # 正面
        if any(w in quote for w in ['丝滑', '流畅', '顺滑', '跟手', '爽', '香']):
            return '正面'
    
    # 默认判断
    neg_count = sum(1 for w in negative_words if w in quote)
    pos_count = sum(1 for w in positive_words if w in quote)
    
    if neg_count > pos_count:
        return '负面'
    elif pos_count > neg_count:
        return '正面'
    return '中性'

def process_record(record):
    """处理单条UGC记录，返回标注列表"""
    results = []
    note_id = record['note_id']
    title = record.get('title', '')
    content = record.get('content', '')
    tags = record.get('tags', [])
    full_text = title + '\n' + content
    
    # 主题1: 流畅丝滑
    smooth_quotes = find_theme_quotes(full_text, SMOOTH_KEYWORDS)
    for quote in smooth_quotes:
        # 过滤掉只提到"不卡"但没有流畅相关描述的
        if quote == '不卡' or quote.strip() == '不卡':
            continue
        # 排除纯负面卡顿描述
        if '卡顿' in quote and '丝滑' not in quote and '流畅' not in quote:
            continue
        brand = determine_brand(quote, title, tags, full_text)
        sentiment = determine_sentiment(quote, '流畅丝滑')
        reason = "用户明确表达系统/应用流畅丝滑体验" if sentiment == '正面' else "用户表达流畅度不足"
        results.append({
            "note_id": note_id,
            "title": title,
            "theme": "流畅丝滑",
            "quote": quote,
            "brand_model": brand,
            "sentiment": sentiment,
            "reason": reason
        })
    
    # 主题2: 卡顿问题
    lag_quotes = find_theme_quotes(full_text, LAG_KEYWORDS)
    for quote in lag_quotes:
        # 排除已经被流畅主题覆盖的"不卡"类描述
        if '不卡' in quote and '卡顿' not in quote and '卡死' not in quote:
            continue
        brand = determine_brand(quote, title, tags, full_text)
        sentiment = determine_sentiment(quote, '卡顿问题')
        reason = "用户明确表达卡顿/掉帧/反应慢等问题"
        results.append({
            "note_id": note_id,
            "title": title,
            "theme": "卡顿问题",
            "quote": quote,
            "brand_model": brand,
            "sentiment": sentiment,
            "reason": reason
        })
    
    # 主题3: 稳定性
    stability_quotes = find_theme_quotes(full_text, STABILITY_KEYWORDS)
    for quote in stability_quotes:
        # 排除只提到"发热"但没有严重/烫等负面词的（如"散热改善"）
        if '散热' in quote and '发烫' not in quote and '发热严重' not in quote:
            continue
        if '温度控制好' in quote or '不烫' in quote or '不发烫' in quote:
            sentiment = '正面'
        else:
            sentiment = determine_sentiment(quote, '稳定性')
        brand = determine_brand(quote, title, tags, full_text)
        reason = "用户明确表达系统稳定性/发热问题" if sentiment == '负面' else "用户表达系统稳定/不发热"
        results.append({
            "note_id": note_id,
            "title": title,
            "theme": "稳定性",
            "quote": quote,
            "brand_model": brand,
            "sentiment": sentiment,
            "reason": reason
        })
    
    return results

def merge_similar_quotes(results):
    """合并同一note_id同一主题的相似quote，保留最精简的"""
    merged = {}
    for r in results:
        key = (r['note_id'], r['theme'])
        if key not in merged:
            merged[key] = r
        else:
            # 保留更短的quote（更精简）
            if len(r['quote']) < len(merged[key]['quote']):
                merged[key] = r
    return list(merged.values())

def main():
    base_dir = '/Users/zhijian/workspace/ai-demand-research-v3/projects/华为苹果性能对比-2026-05-20/03-theme-tagged-v2'
    
    for batch_num in range(1, 6):
        input_file = os.path.join(base_dir, f'batch_{batch_num:03d}_input.json')
        output_file = os.path.join(base_dir, f'batch_{batch_num:03d}_output.json')
        
        with open(input_file, 'r', encoding='utf-8') as f:
            records = json.load(f)
        
        all_results = []
        for record in records:
            results = process_record(record)
            all_results.extend(results)
        
        # 合并相似quote
        all_results = merge_similar_quotes(all_results)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)
        
        print(f"Batch {batch_num:03d}: {len(records)} records -> {len(all_results)} tags")
    
    print("\nDone! All batches processed.")

if __name__ == '__main__':
    main()
