#!/usr/bin/env python3
"""
MediaCrawler VOC分析 - 完整批处理分析脚本
自动分析所有120个批次的数据
"""

import json
import os
import sys
from collections import Counter

# 配置
FILTERED_DIR = '/Users/zhijian/workspace-strict/MediaCrawler/analysis/batches_filtered'
RESULTS_DIR = '/Users/zhijian/workspace-strict/MediaCrawler/analysis/batch_results'

# 分类关键词定义
VIDEO_KEYWORDS = {
    'scene': {
        'short_video': ['抖音', '快手', 'tiktok', '短视频'],
        'long_video': ['b站', 'bilibili', '爱奇艺', '腾讯', '优酷', '追剧', '长视频'],
        'live_stream': ['直播'],
        'general_video': []
    },
    'type': {
        'feature_request': ['希望', '建议', '能不能', '想要', '需要'],
        'pain_point': ['麻烦', '卡顿', '慢', '不好', '问题', '差'],
        'positive_feedback': ['爽', '开心', '满意', '不错', '好用'],
        'behavior_description': []
    },
    'topic': {
        'video_quality': ['画质', '清晰', '卡顿', '流畅', '加载'],
        'content_recommend': ['推荐', '算法', '个性化', '兴趣'],
        'playback_control': ['倍速', '进度', '暂停', '播放'],
        'download_cache': ['下载', '缓存', '离线', '存储'],
        'screen_cast': ['投屏', '电视', '大屏', '投影'],
        'payment_member': ['会员', '付费', 'VIP', '价格'],
        'ad_experience': ['广告', '跳过'],
        'subtitle_translate': ['字幕', '翻译', '语言'],
        'background_play': ['后台', '锁屏', '听视频', '小窗'],
        'ai_feature': ['AI', '智能', '自动', '识别'],
        'other': []
    }
}

def analyze_batch(batch_id):
    """分析单个批次"""
    filtered_file = os.path.join(FILTERED_DIR, f'batch_{batch_id:03d}_filtered.json')
    
    if not os.path.exists(filtered_file):
        return None
    
    with open(filtered_file, 'r', encoding='utf-8') as f:
        batch_data = json.load(f)
    
    items = batch_data['items']
    analysis_results = []
    
    for item in items:
        text = item.get('text', '')
        result = {
            'id': item['id'],
            'text': text[:200],
            'platform': item['platform'],
            'analysis': {}
        }
        
        # 判断场景
        for scene, keywords in VIDEO_KEYWORDS['scene'].items():
            if any(kw in text for kw in keywords):
                result['analysis']['scene'] = scene
                break
        else:
            result['analysis']['scene'] = 'general_video'
        
        # 判断诉求类型
        for t, keywords in VIDEO_KEYWORDS['type'].items():
            if any(kw in text for kw in keywords):
                result['analysis']['type'] = t
                break
        else:
            result['analysis']['type'] = 'behavior_description'
        
        # 判断主题
        for topic, keywords in VIDEO_KEYWORDS['topic'].items():
            if any(kw in text for kw in keywords):
                result['analysis']['topic'] = topic
                break
        else:
            result['analysis']['topic'] = 'other'
        
        # 判断AI相关性
        if any(kw in text for kw in ['AI', '人工智能', '智能推荐', '算法', '自动识别', '语音助手']):
            result['analysis']['is_ai_related'] = True
            result['analysis']['ai_specificity'] = 'explicit'
        elif any(kw in text for kw in ['自动', '智能', '推荐', '识别', '预测']):
            result['analysis']['is_ai_related'] = True
            result['analysis']['ai_specificity'] = 'implicit'
        else:
            result['analysis']['is_ai_related'] = False
            result['analysis']['ai_specificity'] = 'not_ai'
        
        analysis_results.append(result)
    
    # 统计
    scene_dist = Counter(r['analysis']['scene'] for r in analysis_results)
    type_dist = Counter(r['analysis']['type'] for r in analysis_results)
    topic_dist = Counter(r['analysis']['topic'] for r in analysis_results)
    ai_count = sum(1 for r in analysis_results if r['analysis']['is_ai_related'])
    ai_explicit = sum(1 for r in analysis_results if r['analysis']['ai_specificity'] == 'explicit')
    ai_implicit = sum(1 for r in analysis_results if r['analysis']['ai_specificity'] == 'implicit')
    
    return {
        'batch_id': batch_id,
        'total_items': len(analysis_results),
        'statistics': {
            'scene_distribution': dict(scene_dist),
            'type_distribution': dict(type_dist),
            'topic_distribution': dict(topic_dist),
            'ai_statistics': {
                'total_ai': ai_count,
                'explicit': ai_explicit,
                'implicit': ai_implicit,
                'not_ai': len(analysis_results) - ai_count
            }
        },
        'results': analysis_results
    }

def main():
    """主函数"""
    os.makedirs(RESULTS_DIR, exist_ok=True)
    
    print("=" * 80)
    print("MediaCrawler VOC分析 - 批处理分析")
    print("=" * 80)
    
    all_stats = []
    
    for batch_id in range(1, 121):
        result = analyze_batch(batch_id)
        if result:
            # 保存单个批次结果
            output_file = os.path.join(RESULTS_DIR, f'batch_{batch_id:03d}_analysis.json')
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            all_stats.append({
                'batch_id': batch_id,
                'total_items': result['total_items'],
                'ai_count': result['statistics']['ai_statistics']['total_ai'],
                'ai_explicit': result['statistics']['ai_statistics']['explicit'],
                'ai_implicit': result['statistics']['ai_statistics']['implicit']
            })
            
            if batch_id % 10 == 0:
                print(f"  已分析 {batch_id}/120 批次...")
    
    # 保存汇总统计
    summary = {
        'total_batches': len(all_stats),
        'total_items': sum(s['total_items'] for s in all_stats),
        'total_ai': sum(s['ai_count'] for s in all_stats),
        'total_explicit': sum(s['ai_explicit'] for s in all_stats),
        'total_implicit': sum(s['ai_implicit'] for s in all_stats),
        'batch_stats': all_stats
    }
    
    with open(os.path.join(RESULTS_DIR, 'summary.json'), 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print("=" * 80)
    print("分析完成!")
    print(f"  总批次: {summary['total_batches']}")
    print(f"  总条目: {summary['total_items']}")
    print(f"  AI相关: {summary['total_ai']} ({summary['total_ai']/summary['total_items']*100:.1f}%)")
    print(f"  明确AI: {summary['total_explicit']}")
    print(f"  隐含AI: {summary['total_implicit']}")
    print("=" * 80)

if __name__ == '__main__':
    main()
