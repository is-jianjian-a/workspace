
#!/usr/bin/env python3
"""
合并脚本：将子Agent的输出与输入数据合并，生成标准化的最终格式
"""

import json
import sys

def map_sentiment(sentiment):
    """将英文情感映射为中文"""
    mapping = {
        'positive': '正向',
        'negative': '负向',
        'neutral': '中性',
        'mixed': '混合'
    }
    return mapping.get(sentiment.lower(), '中性')

def map_intensity(intensity):
    """将英文强度映射为中文"""
    mapping = {
        'strong': '强',
        'medium': '中',
        'weak': '弱'
    }
    return mapping.get(intensity.lower(), '中')

def map_confidence(confidence):
    """将confidence映射为高中低"""
    if isinstance(confidence, (int, float)):
        if confidence >= 0.8:
            return '高'
        elif confidence >= 0.5:
            return '中'
        else:
            return '低'
    return confidence

def merge_batch(batch_num, input_file, result_file, output_file):
    """合并单批次结果"""
    
    # 读取输入数据
    with open(input_file, 'r', encoding='utf-8') as f:
        input_posts = {p['note_id']: p for p in json.load(f)}
    
    # 读取子Agent输出
    with open(result_file, 'r', encoding='utf-8') as f:
        agent_results = json.load(f)
    
    # 合并生成最终格式
    final_opinions = []
    opinion_idx = 0
    
    for post_result in agent_results:
        note_id = post_result.get('note_id') or post_result.get('post_id')
        post = input_posts.get(note_id)
        
        if not post:
            print(f"Warning: note_id {note_id} not found in input")
            continue
        
        opinions = post_result.get('opinions') or post_result.get('brand_opinions', [])
        
        for op in opinions:
            opinion_idx += 1
            
            # 字段映射
            brand_target = op.get('brand_target') or op.get('brand', '其他')
            sentiment_polarity = op.get('sentiment_polarity') or map_sentiment(op.get('sentiment', 'neutral'))
            sentiment_intensity = op.get('sentiment_intensity') or map_intensity(op.get('intensity', 'medium'))
            
            # sentiment_reason: 优先使用quote，其次是reasoning，最后是opinion_text
            sentiment_reason = op.get('sentiment_reason') or op.get('quote') or op.get('reasoning') or op.get('opinion_text', '')
            
            confidence = map_confidence(op.get('confidence', '中'))
            
            is_fluency = op.get('is_fluency_related', False)
            if isinstance(is_fluency, str):
                is_fluency = is_fluency.lower() in ('true', 'yes', '是')
            
            final_op = {
                'opinion_id': f'batch{batch_num}_{opinion_idx}',
                'note_id': note_id,
                'title': post['title'],
                'source_keyword': post['source_keyword'],
                'liked_count': post['liked_count'],
                'comment_count': post['comment_count'],
                'opinion_text': op.get('opinion_text', ''),
                'brand_target': brand_target,
                'sentiment_polarity': sentiment_polarity,
                'sentiment_intensity': sentiment_intensity,
                'sentiment_reason': sentiment_reason,
                'confidence': confidence,
                'full_title': post['title'],
                'full_content': post['content'],
                'is_fluency_related': is_fluency
            }
            final_opinions.append(final_op)
    
    # 保存最终输出
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_opinions, f, ensure_ascii=False, indent=2)
    
    print(f"Merged {len(final_opinions)} opinions from {len(agent_results)} posts")
    print(f"Saved to: {output_file}")
    return final_opinions

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python merge_script.py <batch_num> <input_file> <result_file> <output_file>")
        sys.exit(1)
    
    merge_batch(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
