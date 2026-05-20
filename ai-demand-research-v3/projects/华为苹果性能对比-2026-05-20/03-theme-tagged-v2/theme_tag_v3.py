#!/usr/bin/env python3
"""
华为苹果性能对比UGC精确主题段落打标脚本 V3
严格精简quote，只保留与主题直接相关的最短原文段落
"""

import json
import re
import os

def extract_sentences(text):
    """将文本拆分为句子列表"""
    lines = text.split('\n')
    sentences = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = re.split(r'([。！？])', line)
        current = ''
        for part in parts:
            current += part
            if part in '。！？':
                s = current.strip()
                if s and len(s) > 3:
                    sentences.append(s)
                current = ''
        if current.strip() and len(current.strip()) > 3:
            sentences.append(current.strip())
    return sentences

def find_matches(text, keywords, exclude_patterns=None):
    """找到包含关键词的句子，排除匹配exclude_patterns的"""
    sentences = extract_sentences(text)
    matches = []
    for sent in sentences:
        for kw in keywords:
            if kw in sent:
                if exclude_patterns:
                    skip = False
                    for ep in exclude_patterns:
                        if ep in sent:
                            skip = True
                            break
                    if skip:
                        continue
                matches.append(sent)
                break
    return matches

def determine_brand(quote, title, full_content):
    """从quote中推断品牌+机型"""
    quote_lower = quote.lower()
    full_lower = full_content.lower()
    title_lower = title.lower()
    
    huawei_models = {
        'mate60pro': '华为Mate60Pro', 'mate 60 pro': '华为Mate60Pro', 'mate60': '华为Mate60',
        'mate70pro': '华为Mate70Pro', 'mate 70 pro': '华为Mate70Pro', 'mate70': '华为Mate70',
        'mate80pro': '华为Mate80Pro', 'mate 80 pro': '华为Mate80Pro', 'mate80': '华为Mate80',
        'mate90': '华为Mate90', 'pura70': '华为Pura70', 'pura80': '华为Pura80',
        'pura90': '华为Pura90', 'p40': '华为P40', 'p50': '华为P50', 'p60': '华为P60',
        'p70': '华为P70', 'p80': '华为P80', 'p90': '华为P90',
        'purax': '华为PuraX', 'pura x': '华为PuraX', 'puraxmax': '华为PuraXMax', 'pura x max': '华为PuraXMax',
        'mate x5': '华为MateX5', 'matex5': '华为MateX5',
        'mate40pro': '华为Mate40Pro', 'mate 40 pro': '华为Mate40Pro', 'mate40': '华为Mate40',
        'mate60rs': '华为Mate60RS', 'mate 60 rs': '华为Mate60RS',
        'mate70pro+': '华为Mate70Pro+', 'mate 70 pro+': '华为Mate70Pro+',
        'mate80promax': '华为Mate80ProMax', 'mate80 pro max': '华为Mate80ProMax',
        'mate70air': '华为Mate70Air', 'mate 70 air': '华为Mate70Air',
        'nova15ultra': '华为Nova15Ultra', 'nova 15 ultra': '华为Nova15Ultra',
        'matebookgt14': '华为MateBookGT14', 'matebook gt14': '华为MateBookGT14',
    }
    
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
        '17p': 'iPhone17Pro', '16p': 'iPhone16Pro', '15p': 'iPhone15Pro',
        'macbookpro': 'MacBookPro', 'macbook pro': 'MacBookPro',
        'ipad': 'iPad', 'ipad pro': 'iPadPro',
    }
    
    huawei_found = []
    apple_found = []
    
    for key, model in huawei_models.items():
        if key in quote_lower:
            huawei_found.append(model)
    for key, model in apple_models.items():
        if key in quote_lower:
            apple_found.append(model)
    
    if not huawei_found and not apple_found:
        for key, model in huawei_models.items():
            if key in full_lower or key in title_lower:
                huawei_found.append(model)
        for key, model in apple_models.items():
            if key in full_lower or key in title_lower:
                apple_found.append(model)
    
    huawei_found = list(dict.fromkeys(huawei_found))
    apple_found = list(dict.fromkeys(apple_found))
    
    if huawei_found and apple_found:
        return '华为/苹果'
    elif huawei_found:
        return huawei_found[0]
    elif apple_found:
        return apple_found[0]
    
    if '华为' in quote or '鸿蒙' in quote or 'harmony' in quote_lower:
        if '苹果' in quote or 'iphone' in quote_lower or 'ios' in quote_lower:
            return '华为/苹果'
        return '华为'
    if '苹果' in quote or 'iphone' in quote_lower or 'ios' in quote_lower:
        return '苹果'
    
    has_huawei = '华为' in full_content or '鸿蒙' in full_content
    has_apple = '苹果' in full_content or 'iPhone' in full_content or 'iOS' in full_content
    if has_huawei and has_apple:
        return '华为/苹果'
    elif has_huawei:
        return '华为'
    elif has_apple:
        return '苹果'
    
    return '不明确'

def make_tag(note_id, title, theme, quote, brand_model, sentiment, reason):
    return {
        "note_id": note_id,
        "title": title,
        "theme": theme,
        "quote": quote,
        "brand_model": brand_model,
        "sentiment": sentiment,
        "reason": reason
    }

def process_all():
    base_dir = '/Users/zhijian/workspace/ai-demand-research-v3/projects/华为苹果性能对比-2026-05-20/03-theme-tagged-v2'
    
    for batch_num in range(1, 6):
        input_file = os.path.join(base_dir, f'batch_{batch_num:03d}_input.json')
        output_file = os.path.join(base_dir, f'batch_{batch_num:03d}_output.json')
        
        with open(input_file, 'r', encoding='utf-8') as f:
            records = json.load(f)
        
        all_results = []
        
        for record in records:
            note_id = record['note_id']
            title = record.get('title', '')
            content = record.get('content', '')
            full_text = title + '\n' + content
            
            # ===== 主题1: 流畅丝滑 =====
            # 关键词匹配
            smooth_keywords = ['丝滑', '流畅', '顺滑', '跟手']
            smooth_matches = find_matches(full_text, smooth_keywords)
            for quote in smooth_matches:
                # 排除纯负面
                if '不丝滑' in quote or '不流畅' in quote:
                    if '丝滑' not in quote.replace('不丝滑', '') and '流畅' not in quote.replace('不流畅', ''):
                        continue
                if '卡顿' in quote and '不卡顿' not in quote and '零卡顿' not in quote:
                    # 如果同时有卡顿和丝滑/流畅，看哪个是主要表达
                    if '丝滑' not in quote and '流畅' not in quote.replace('不流畅', '').replace('卡顿', ''):
                        continue
                # 排除只是视频流畅度（非系统流畅）
                if '视频' in quote and '流畅度' in quote and '系统' not in quote and '动画' not in quote and '丝滑' not in quote:
                    continue
                # 排除过长quote（超过150字可能是包含无关内容）
                if len(quote) > 150:
                    # 尝试截取核心部分
                    continue
                
                brand = determine_brand(quote, title, full_text)
                sentiment = '正面'
                if '不丝滑' in quote or '不流畅' in quote or '卡顿' in quote or '掉帧' in quote or '延迟' in quote:
                    sentiment = '负面'
                if '流畅度一般' in quote or '流畅度不够' in quote or '不是很丝滑' in quote:
                    sentiment = '负面'
                if '欠缺' in quote or '差距' in quote:
                    sentiment = '负面'
                
                reason = "用户明确表达系统/应用流畅丝滑体验" if sentiment == '正面' else "用户表达流畅度不足"
                all_results.append(make_tag(note_id, title, '流畅丝滑', quote, brand, sentiment, reason))
            
            # ===== 主题2: 卡顿问题 =====
            lag_keywords = ['卡顿', '掉帧', '卡死', '反应慢', '反应迟钝', '延迟', '转圈圈']
            lag_exclude = ['不卡顿', '零卡顿', '不卡', '无比流畅', '非常流畅', '很流畅', '丝滑']
            lag_matches = find_matches(full_text, lag_keywords, lag_exclude)
            for quote in lag_matches:
                # 排除只是标题或太短的
                if len(quote) < 8:
                    continue
                # 排除过长
                if len(quote) > 150:
                    continue
                # 排除只是提到"卡顿"作为对比的正面描述
                if '不卡顿' in quote or '零卡顿' in quote:
                    continue
                
                brand = determine_brand(quote, title, full_text)
                all_results.append(make_tag(note_id, title, '卡顿问题', quote, brand, '负面', 
                    "用户明确表达卡顿/掉帧/反应慢等问题"))
            
            # ===== 主题3: 稳定性 =====
            stability_keywords = ['闪退', '崩溃', '死机', '重启', '发热严重', '发烫']
            stability_matches = find_matches(full_text, stability_keywords)
            for quote in stability_matches:
                # 排除非系统bug
                if 'bug' in quote.lower():
                    if not any(w in quote for w in ['系统', '软件', 'app', '应用', '闪退', '崩溃', '死机', '卡顿']):
                        if 'bug' in quote and ('壳' in quote or '发货' in quote or '包装' in quote):
                            continue
                # 排除只是"发热"但没有负面词的
                if '散热' in quote and '发烫' not in quote and '发热严重' not in quote:
                    continue
                # 排除过长
                if len(quote) > 150:
                    continue
                
                brand = determine_brand(quote, title, full_text)
                sentiment = '负面'
                if '不烫' in quote or '不发烫' in quote or '温度控制好' in quote or '不发热' in quote:
                    sentiment = '正面'
                if '稳定' in quote and '不稳定' not in quote:
                    sentiment = '正面'
                
                reason = "用户明确表达系统稳定性/发热问题" if sentiment == '负面' else "用户表达系统稳定/不发热"
                all_results.append(make_tag(note_id, title, '稳定性', quote, brand, sentiment, reason))
        
        # 去重：同一note_id同一theme只保留最短的quote
        dedup = {}
        for r in all_results:
            key = (r['note_id'], r['theme'])
            if key not in dedup or len(r['quote']) < len(dedup[key]['quote']):
                dedup[key] = r
        all_results = list(dedup.values())
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)
        
        print(f"Batch {batch_num:03d}: {len(records)} records -> {len(all_results)} tags")

if __name__ == '__main__':
    process_all()
