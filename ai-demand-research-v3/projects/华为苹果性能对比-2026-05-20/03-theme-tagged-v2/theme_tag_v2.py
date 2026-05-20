#!/usr/bin/env python3
"""
华为苹果性能对比UGC精确主题段落打标脚本 V2
三个主题：流畅丝滑、卡顿问题、稳定性
严格精简quote，只保留与主题直接相关的1-3句话
"""

import json
import re
import os

# 主题关键词定义 - 更精确
SMOOTH_KEYWORDS = ['丝滑', '流畅', '顺滑', '跟手', '动画顺滑', '高刷体验', '120hz', '120赫兹', '高刷新率', '帧率稳定', '不掉帧', '响应速度', '反应速度', '动效', '零卡顿']
LAG_KEYWORDS = ['卡顿', '掉帧', '卡死', '反应慢', '反应迟钝', '延迟', '转圈圈', '加载慢', '打开慢', '启动慢', '卡爆', '卡到', '卡的相当', '巨卡', '卡卡卡', '很卡', '太卡', '有点卡', '小卡', '卡帧', '锁帧', '卡了', '卡的要死']
STABILITY_KEYWORDS = ['闪退', '崩溃', '死机', '重启', 'bug', '发热严重', '发烫', '系统不稳定', '过热', '烫手', '温度高']

def extract_sentences(text):
    """将文本拆分为句子列表，保留原始标点信息"""
    # 先按换行分割，再按标点分割
    lines = text.split('\n')
    sentences = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # 按句号、感叹号、问号分割，但保留这些标点
        parts = re.split(r'([。！？])', line)
        current = ''
        for part in parts:
            current += part
            if part in '。！？':
                s = current.strip()
                if s and len(s) > 3:  # 过滤过短的
                    sentences.append(s)
                current = ''
        if current.strip() and len(current.strip()) > 3:
            sentences.append(current.strip())
    return sentences

def find_best_quote(text, keywords, theme_name):
    """找到最相关的1-3句话，严格精简"""
    sentences = extract_sentences(text)
    matches = []
    
    for sent in sentences:
        sent_lower = sent.lower()
        for kw in keywords:
            if kw in sent:
                # 过滤条件
                if theme_name == '流畅丝滑':
                    # 排除纯负面描述（如"不流畅"、"卡顿"）
                    if '不流畅' in sent or '不丝滑' in sent:
                        if '流畅' not in sent.replace('不流畅', '') and '丝滑' not in sent.replace('不丝滑', ''):
                            continue
                    # 排除只是提到"视频流畅度"这类非系统流畅的
                    if '视频' in sent and '流畅' in sent and '系统' not in sent and '动画' not in sent and '丝滑' not in sent:
                        # 但保留明确说视频流畅的
                        pass
                
                if theme_name == '卡顿问题':
                    # 排除"不卡顿"、"零卡顿"等正面描述
                    if '不卡顿' in sent or '零卡顿' in sent or '不卡' in sent:
                        if '卡顿' not in sent.replace('不卡顿', '').replace('零卡顿', '') and '卡死' not in sent:
                            continue
                    # 排除"无比流畅"等
                    if '无比流畅' in sent or '非常流畅' in sent:
                        continue
                
                if theme_name == '稳定性':
                    # 排除只是提到"bug"但不是系统bug的（如"唯一的bug就是赠送的壳"）
                    if 'bug' in sent_lower:
                        # 检查是否是系统/软件bug
                        if not any(w in sent for w in ['系统', '软件', 'app', '应用', '闪退', '崩溃', '死机']):
                            if 'bug' in sent and ('壳' in sent or '发货' in sent or '包装' in sent):
                                continue
                    # 排除"散热"正面描述
                    if '散热' in sent and '发烫' not in sent and '发热' not in sent:
                        continue
                    # 排除"不发热"等正面但非稳定性主题的
                    if '不发热' in sent or '不烫' in sent:
                        if '发热' not in sent.replace('不发热', '') and '烫' not in sent.replace('不烫', ''):
                            pass  # 保留，这是正面稳定性
                
                matches.append(sent)
                break
    
    # 合并相邻的句子（如果它们都匹配同一个主题）
    if not matches:
        return []
    
    # 去重并保持顺序
    seen = set()
    unique_matches = []
    for m in matches:
        if m not in seen:
            seen.add(m)
            unique_matches.append(m)
    
    # 限制1-3句，优先保留包含更多关键词的
    def score(s):
        count = sum(1 for kw in keywords if kw in s)
        # 长度惩罚，越短越好
        return count * 100 - len(s)
    
    unique_matches.sort(key=score, reverse=True)
    return unique_matches[:3]

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
        '17p': 'iPhone17Pro', '16p': 'iPhone16Pro', '15p': 'iPhone15Pro',
        'macbookpro': 'MacBookPro', 'macbook pro': 'MacBookPro',
        'ipad': 'iPad', 'ipad pro': 'iPadPro',
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
    
    if theme == '卡顿问题':
        # 卡顿主题默认负面，除非明确说"不卡"
        if '不卡' in quote and '卡顿' not in quote and '卡死' not in quote and '掉帧' not in quote:
            return '正面'
        return '负面'
    
    if theme == '稳定性':
        # 提到闪退/崩溃/死机/发热严重等是负面
        if any(w in quote for w in ['闪退', '崩溃', '死机', '重启', 'bug', '发热严重', '发烫', '过热', '烫手']):
            return '负面'
        if '系统不稳定' in quote:
            return '负面'
        if '稳定' in quote and '不稳定' not in quote:
            return '正面'
        if '不烫' in quote or '不发烫' in quote or '温度控制好' in quote or '不发热' in quote:
            return '正面'
        if '散热' in quote and '好' in quote:
            return '正面'
        return '负面'
    
    if theme == '流畅丝滑':
        # 明确的负面
        if '不丝滑' in quote or '不流畅' in quote:
            return '负面'
        if '有点卡' in quote or '小卡顿' in quote or '小小的掉帧' in quote:
            return '负面'
        if '流畅度一般' in quote or '流畅度不够' in quote:
            return '负面'
        if '卡卡' in quote and '不卡' not in quote:
            return '负面'
        if '卡顿' in quote or '掉帧' in quote or '卡死' in quote:
            return '负面'
        if '延迟' in quote and '不延迟' not in quote and '没延迟' not in quote:
            return '负面'
        # 明确的正面
        if any(w in quote for w in ['丝滑', '流畅', '顺滑', '跟手', '爽', '香', '舒服']):
            if '不' not in quote or '不错' in quote or '不卡' in quote:
                return '正面'
        if '不卡' in quote and '卡顿' not in quote:
            return '正面'
        if '零卡顿' in quote:
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
    smooth_quotes = find_best_quote(full_text, SMOOTH_KEYWORDS, '流畅丝滑')
    for quote in smooth_quotes:
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
    lag_quotes = find_best_quote(full_text, LAG_KEYWORDS, '卡顿问题')
    for quote in lag_quotes:
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
    stability_quotes = find_best_quote(full_text, STABILITY_KEYWORDS, '稳定性')
    for quote in stability_quotes:
        brand = determine_brand(quote, title, tags, full_text)
        sentiment = determine_sentiment(quote, '稳定性')
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
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)
        
        print(f"Batch {batch_num:03d}: {len(records)} records -> {len(all_results)} tags")
    
    print("\nDone! All batches processed.")

if __name__ == '__main__':
    main()
