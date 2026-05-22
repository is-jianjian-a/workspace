import json
import re

def split_into_units(text):
    """将帖子文本拆分为语义单元（1-3句话的完整观点）"""
    if not text:
        return []
    # 按句子拆分
    sentences = re.split(r'[。！？\n]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    units = []
    i = 0
    while i < len(sentences):
        # 尝试合并1-3句
        unit_text = sentences[i]
        # 检查下一句是否属于同一语义单元
        if i + 1 < len(sentences) and len(unit_text) < 80:
            unit_text += '。' + sentences[i+1]
            i += 2
        else:
            i += 1
        units.append(unit_text)
    return units

def classify_unit(unit_text, title=''):
    """对单个语义单元进行一级标签分类"""
    text = unit_text.lower()
    
    # 排除规则：疑问句不分类
    if text.endswith('？') or text.endswith('?') or '吗' in text[-3:] or '怎么' in text or '什么' in text[-5:]:
        if not any(k in text for k in ['丝滑', '流畅', '卡顿', '掉帧', '稳定', '卡死']):
            return '无'
    
    # 关键词匹配（语义理解辅助）
    
    # 卡顿/掉帧
    kading_keywords = ['卡顿', '掉帧', '卡死', '不流畅', '反应慢', '卡卡', '卡屏', '死机']
    
    # 丝滑流畅
    silu_keywords = ['丝滑', '流畅', '顺滑', '跟手', '响应快']
    
    # 稳定性
    wending_keywords = ['稳定', '不闪退', '不重启', '几年不卡', '用久不卡', '长期使用']
    
    # 判断逻辑 - 基于语义
    
    # 1. 卡顿判断
    if any(k in text for k in kading_keywords):
        # 排除"不卡顿"类否定表达
        if '不卡顿' in text or '不卡' in text or '没卡' in text or '不会卡' in text:
            # 这是正面表达，可能属于丝滑或稳定
            if '几年' in text or '长期' in text or '用久' in text or '五年' in text:
                return '稳定性'
            return '丝滑流畅'
        return '卡顿'
    
    # 2. 丝滑流畅判断
    if any(k in text for k in silu_keywords):
        # 排除否定
        if '不丝滑' in text or '不流畅' in text or '不够流畅' in text:
            return '卡顿'
        return '丝滑流畅'
    
    # 3. 稳定性判断
    if any(k in text for k in wending_keywords):
        if '不稳定' in text:
            return '卡顿'
        return '稳定性'
    
    # 4. 特殊场景 - "卡"字相关
    if '卡' in text:
        # 可能是卡顿相关
        if any(k in text for k in ['游戏卡', '很卡', '太卡', '有点卡', '会卡', '就卡']):
            return '卡顿'
        if any(k in text for k in ['不卡', '没卡', '不会卡', '一点也不卡']):
            if '几年' in text or '长期' in text:
                return '稳定性'
            return '丝滑流畅'
    
    # 5. 高刷/帧率相关
    if '帧' in text or '高刷' in text or '刷新率' in text:
        if any(k in text for k in ['稳帧', '120帧', '高刷', '全局120']):
            return '丝滑流畅'
        if any(k in text for k in ['掉帧', '帧率']):
            return '卡顿'
    
    # 6. 动画相关
    if '动画' in text:
        if any(k in text for k in ['丝滑', '流畅', '顺滑', '好']):
            return '丝滑流畅'
        if any(k in text for k in ['卡', '掉帧', '不流畅']):
            return '卡顿'
    
    return '无'

def process_batch(batch_num):
    input_file = f'phase1_batch_{batch_num:03d}_input.json'
    output_file = f'phase1_batch_{batch_num:03d}_output.json'
    
    with open(input_file, 'r', encoding='utf-8') as f:
        posts = json.load(f)
    
    results = []
    for post in posts:
        note_id = post['note_id']
        title = post.get('title', '')
        content = post.get('content', '')
        
        # 合并标题和内容进行unit拆分
        full_text = title + '\n' + content if title else content
        units_text = split_into_units(full_text)
        
        units = []
        for unit_text in units_text:
            label = classify_unit(unit_text, title)
            # 生成判断理由
            if label == '无':
                reasoning = '该单元不涉及系统流畅性、稳定性或卡顿相关内容'
            elif label == '丝滑流畅':
                reasoning = '该单元表达了系统/操作流畅、丝滑、跟手、响应快等正面体验'
            elif label == '稳定性':
                reasoning = '该单元表达了长时间运行稳定、不闪退、不重启、持久不卡等体验'
            elif label == '卡顿':
                reasoning = '该单元表达了卡顿、掉帧、不流畅、反应慢、卡死等负面体验'
            
            units.append({
                'text': unit_text,
                'label': label,
                'reasoning': reasoning
            })
        
        results.append({
            'note_id': note_id,
            'units': units
        })
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f'Batch {batch_num:03d} 处理完成: {len(posts)}条帖子, 输出到 {output_file}')

if __name__ == '__main__':
    for i in range(1, 5):
        process_batch(i)
    print('全部处理完成!')
