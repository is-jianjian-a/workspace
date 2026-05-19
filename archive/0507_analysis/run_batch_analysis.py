#!/usr/bin/env python3
"""
MediaCrawler VOC分析 - v3方案批处理执行脚本
自动处理120个批次的数据分析
"""

import json
import os
import sys
import time
from pathlib import Path

# 配置
BATCH_DIR = '/Users/zhijian/workspace-strict/MediaCrawler/analysis/batches'
FILTERED_DIR = '/Users/zhijian/workspace-strict/MediaCrawler/analysis/batches_filtered'
RESULTS_DIR = '/Users/zhijian/workspace-strict/MediaCrawler/analysis/batch_results'
SCHEMA_FILE = '/Users/zhijian/workspace-strict/MediaCrawler/analysis/v3_classification_schema.json'

# 视频相关关键词
VIDEO_KEYWORDS = [
    '视频', '抖音', '快手', 'b站', 'bilibili', '直播', '追剧', '看剧', '刷视频', 
    '短视频', '长视频', '爱奇艺', '腾讯', '优酷', '芒果', '会员', '画质', '卡顿',
    '加载', '倍速', '弹幕', '字幕', '投屏', '下载', '缓存', '推荐', '算法',
    '播放', '清晰度', '4K', '高清', '画质', '音质', '音量', '全屏', '小窗',
    '后台', '锁屏', '听视频', '倍速', '快进', '快退', '进度条', '暂停',
    '续播', '历史记录', '收藏', '点赞', '评论', '分享', '转发', '关注',
    '订阅', '通知', '推送', '提醒', '广告', '跳过', 'VIP', '付费', '充值',
    '订阅', '自动续费', '退款', '客服', '投诉', '反馈', '建议', '优化',
    '改进', '升级', '更新', '版本', '功能', '设置', '权限', '隐私',
    '青少年', '家长', '儿童', '模式', '时间', '时长', '限制', '防沉迷',
    '护眼', '夜间', '深色', '模式', '主题', '皮肤', '界面', 'UI',
    '交互', '体验', '流畅', '顺滑', '跟手', '响应', '延迟', '延迟',
    '网络', 'WiFi', '流量', '移动数据', '5G', '4G', '网速', '带宽',
    '缓存', '存储', '空间', '内存', '清理', '删除', '下载', '离线',
    '同步', '多设备', '跨平台', '手机', '平板', '电脑', '电视', '投影',
    '投屏', '镜像', 'DLNA', 'AirPlay', 'Chromecast', 'HDMI', '无线',
    'AI', '人工智能', '智能', '算法', '推荐', '个性化', '定制',
    '总结', '摘要', '提取', '识别', '翻译', '字幕', '配音', '剪辑',
    '生成', '合成', '增强', '修复', '优化', '降噪', '超分', 'HDR',
    '语音', '助手', '问答', '对话', '交互', '控制', '手势', '体感',
    '眼动', '追踪', '注视', '检测', '情绪', '情感', '心情', '状态'
]

def load_schema():
    """加载分类体系"""
    with open(SCHEMA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def filter_video_related(items):
    """筛选与视频相关的内容"""
    filtered = []
    for item in items:
        text = item.get('text', '')
        if any(kw in text for kw in VIDEO_KEYWORDS):
            filtered.append(item)
    return filtered

def generate_prompt(batch_id, items, schema):
    """生成批处理Prompt"""
    prompt = f"""你是一位专业的用户研究分析师，擅长从用户原声(VOC)中提取结构化洞察。

## 任务说明
请对以下{len(items)}条用户内容进行批量分析。每条内容可能包含1个或多个"观点单元"(Opinion Unit)。
只关注与【手机观看短视频/长视频/直播】相关的内容。

## 分类体系

### 场景维度 (Layer 1)
{json.dumps([{"id": c["id"], "name": c["name"], "def": c["definition"]} for c in schema["layer1_scene"]["categories"]], ensure_ascii=False, indent=2)}

### 诉求类型 (Layer 2)
{json.dumps([{"id": c["id"], "name": c["name"], "def": c["definition"]} for c in schema["layer2_type"]["categories"]], ensure_ascii=False, indent=2)}

### 主题标签 (Layer 3) - 预定义21个
{json.dumps([{"id": c["id"], "name": c["name"], "examples": c["examples"], "def": c["definition"]} for c in schema["layer3_topic"]["predefined"]], ensure_ascii=False, indent=2)}

**重要**: 如果某条观点无法匹配以上21个预定义主题，请标记主题为"other"，并在"new_topic_suggestion"字段建议一个新主题名称。

### 情感维度
- "positive": 正面/满意/赞赏
- "neutral": 中性/客观描述/无明确情感
- "negative": 负面/不满/抱怨

### AI相关分类
- is_ai_related: true/false
- ai_specificity: "explicit"(明确提到AI)/"implicit"(隐含AI需求)/"not_ai"
- ai_category: 如果is_ai_related为true，从以下选择：
  {json.dumps([{"id": c["id"], "name": c["name"]} for c in schema["ai_classification"]["ai_categories"]], ensure_ascii=False)}

## 输出格式
必须为每条内容的每个Opinion Unit输出一个JSON对象：

```json
{{
  "item_id": "原始内容编号",
  "unit_id": "批次内唯一编号",
  "excerpt": "原文摘录",
  "scene": "场景ID",
  "scene_name": "场景名称",
  "type": "类型ID",
  "type_name": "类型名称",
  "topic": "主题ID",
  "topic_name": "主题名称",
  "new_topic_suggestion": "如果topic是other，建议的新主题名称；否则空字符串",
  "sentiment": "positive/neutral/negative",
  "is_ai_related": true/false,
  "ai_specificity": "explicit/implicit/not_ai",
  "ai_category": "AI分类ID或空字符串",
  "confidence": 0.0-1.0,
  "reason": "分类理由"
}}
```

## 待分析的用户内容 (批次 {batch_id}/120)
"""
    
    for i, item in enumerate(items, 1):
        text = item.get('text', '')[:300]
        prompt += f"""
--- ITEM #{i} ---
ID: {item['id']}
平台: {item['platform']}
类型: {item['file_type']}
内容: {text}
"""
    
    prompt += f"""

## 输出要求
1. 只输出JSON数组，不要输出任何其他文字
2. 每条内容可能产生0-2个Opinion Unit（如果与手机视频无关，产生0个）
3. 确保JSON格式正确
4. 摘录尽量引用原文原话
5. 批次编号: batch_{batch_id:03d}

开始分析：
"""
    return prompt

def process_batch(batch_id, schema):
    """处理单个批次"""
    batch_file = os.path.join(BATCH_DIR, f'batch_{batch_id:03d}.json')
    filtered_file = os.path.join(FILTERED_DIR, f'batch_{batch_id:03d}_filtered.json')
    
    # 读取批次数据
    with open(batch_file, 'r', encoding='utf-8') as f:
        batch_data = json.load(f)
    
    items = batch_data['items']
    
    # 筛选视频相关内容
    filtered_items = filter_video_related(items)
    
    # 保存筛选结果
    filtered_data = {
        'batch_id': batch_id,
        'original_count': len(items),
        'filtered_count': len(filtered_items),
        'items': filtered_items
    }
    
    with open(filtered_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=2)
    
    # 生成Prompt
    if filtered_items:
        prompt = generate_prompt(batch_id, filtered_items, schema)
        prompt_file = os.path.join(FILTERED_DIR, f'prompt_{batch_id:03d}.txt')
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(prompt)
        return len(items), len(filtered_items), prompt_file
    else:
        return len(items), 0, None

def main():
    """主函数"""
    # 创建目录
    os.makedirs(FILTERED_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    
    # 加载分类体系
    schema = load_schema()
    
    # 统计
    total_original = 0
    total_filtered = 0
    total_prompts = 0
    
    print("=" * 80)
    print("MediaCrawler v3方案 - 批处理数据准备")
    print("=" * 80)
    
    # 处理所有批次
    for batch_id in range(1, 121):
        try:
            original, filtered, prompt_file = process_batch(batch_id, schema)
            total_original += original
            total_filtered += filtered
            if prompt_file:
                total_prompts += 1
            
            if batch_id % 10 == 0:
                print(f"  已处理 {batch_id}/120 批次...")
                
        except Exception as e:
            print(f"  批次 {batch_id} 处理失败: {e}")
            continue
    
    print("=" * 80)
    print("数据准备完成!")
    print(f"  原始内容总数: {total_original}")
    print(f"  视频相关内容: {total_filtered} ({total_filtered/total_original*100:.1f}%)")
    print(f"  生成Prompt数: {total_prompts}")
    print(f"  Prompt文件位置: {FILTERED_DIR}/")
    print("=" * 80)
    print("=" * 80)
    print("下一步: 使用LLM批量分析Prompt文件")
    print("建议: 使用claude -p命令或API批量调用")
    print("建议: 使用claude -p命令或API批量调用")

if __name__ == '__main__':
    main()
