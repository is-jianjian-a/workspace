#!/usr/bin/env python3
"""生成HTML报告后半部分并拼接完整报告"""

import json
from collections import Counter

project_dir = "/Users/zhijian/workspace/ai-demand-research-v3/projects/看视频时想要的AI功能-2026-05-18"

with open(f"{project_dir}/02-cleaned/all_classification_results_v3.json", 'r', encoding='utf-8') as f:
    all_results = json.load(f)

with open(f"{project_dir}/02-cleaned/theme_analysis_v3.json", 'r', encoding='utf-8') as f:
    theme_analysis = json.load(f)

with open(f"{project_dir}/02-cleaned/report_v3_partial.html", 'r', encoding='utf-8') as f:
    html = f.read()

related_results = [r for r in all_results if r['related'] and '其他' not in r['layer1']]

# 情绪分布
emotion_counter = Counter()
for r in related_results:
    for e in r['emotions']:
        emotion_counter[e] += 1

# 场景分布
scene_counter = Counter()
for r in related_results:
    for s in r['scenes']:
        scene_counter[s] += 1

# 二层主题分布
layer2_counter = Counter()
for r in related_results:
    for l2 in r['layer2']:
        layer2_counter[l2] += 1

# 情绪和场景分析部分
html += """
<div class="section">
<h2>😊 情绪与场景分析</h2>

<h3>情绪分布</h3>
<p style="margin-bottom:12px;color:var(--text-light)">
情绪标签反映了用户在表达需求时的心理状态。通过分析情绪与主题的关联，可以判断哪些需求是"痛点"（负面情绪），哪些是"期待"（正面情绪）。
</p>
<div class="bar-chart">
"""

emotion_colors = {
    '期待/渴望': '#10b981', '惊喜/兴奋': '#3b82f6', '困惑/迷茫': '#f59e0b',
    'frustration': '#ef4444', '焦虑/急迫': '#f97316', '疲惫/厌倦': '#8b5cf6'
}

max_emotion = max(emotion_counter.values()) if emotion_counter else 1
for emotion, count in emotion_counter.most_common():
    pct = count / len(related_results) * 100
    width = (count / max_emotion) * 100
    color = emotion_colors.get(emotion, '#4f46e5')
    html += f'<div class="bar-item"><div class="bar-label">{emotion}</div><div class="bar-track"><div class="bar-fill" style="width:{width}%;background:{color}">{count}</div></div><div class="bar-value">{pct:.1f}%</div></div>\n'

html += """
</div>

<div class="insight-box">
<strong>情绪洞察</strong>：
<strong>期待/渴望</strong>（41条，22.2%）是主导情绪，表明用户对新功能有强烈期待而非单纯抱怨；
<strong>惊喜/兴奋</strong>（32条，17.3%）说明部分AI视频功能已超出用户预期；
负面情绪（困惑/迷茫 6.5%、frustration 5.4%、焦虑 3.2%、疲惫 3.8%）合计约19%，
说明当前市场痛点表达不够直接，用户更多在"期待更好的解决方案"而非"抱怨现有问题"。
</div>

<h3>场景分布</h3>
<p style="margin-bottom:12px;color:var(--text-light)">
场景标签识别了用户在什么情境下会产生视频AI功能需求。这直接影响产品设计的优先级和功能定位。
</p>
<div class="bar-chart">
"""

scene_colors = {
    '工作/学习': '#4f46e5', '家庭/陪伴': '#ec4899', '吃饭/碎片': '#f59e0b',
    '睡前/休息': '#8b5cf6', '运动/健身': '#10b981', '通勤/路上': '#06b6d4'
}

max_scene = max(scene_counter.values()) if scene_counter else 1
for scene, count in scene_counter.most_common():
    pct = count / len(related_results) * 100
    width = (count / max_scene) * 100
    color = scene_colors.get(scene, '#4f46e5')
    html += f'<div class="bar-item"><div class="bar-label">{scene}</div><div class="bar-track"><div class="bar-fill" style="width:{width}%;background:{color}">{count}</div></div><div class="bar-value">{pct:.1f}%</div></div>\n'

html += """
</div>

<div class="insight-box">
<strong>场景洞察</strong>：
<strong>工作/学习</strong>场景占绝对主导（47条，25.4%），说明视频AI功能的核心价值在于<strong>知识获取和学习效率提升</strong>；
<strong>家庭/陪伴</strong>（9条，4.9%）和<strong>吃饭/碎片</strong>（8条，4.3%）次之；
<strong>通勤/路上</strong>仅1条（0.5%），说明当前数据未充分覆盖移动场景需求，或该场景下用户更倾向于音频而非视频。
</div>
</div>

<div class="section">
<h2>🔍 二层主题深度分析</h2>
<p style="margin-bottom:20px;color:var(--text-light)">
二层主题是功能层面的细分需求，直接对应产品功能设计。以下分析每个二层主题的UGC数量、典型表达和推导逻辑。
</p>

<h3>二层主题分布Top10</h3>
<div class="bar-chart">
"""

layer2_data = dict(layer2_counter.most_common(10))
max_l2 = max(layer2_data.values()) if layer2_data else 1

for l2, count in layer2_data.items():
    pct = count / len(related_results) * 100
    width = (count / max_l2) * 100
    html += f'<div class="bar-item"><div class="bar-label" style="width:120px">{l2}</div><div class="bar-track"><div class="bar-fill" style="width:{width}%;background:#7c3aed">{count}</div></div><div class="bar-value">{pct:.1f}%</div></div>\n'

html += """
</div>

<div class="insight-box">
<strong>二层主题洞察</strong>：
<strong>AI生成视频</strong>（82条，44.3%）是绝对核心需求，远超其他功能；
<strong>自动剪辑</strong>（37条，20.0%）和<strong>学习管理</strong>（33条，17.8%）分列二三；
<strong>智能摘要</strong>（30条，16.2%）和<strong>知识提取</strong>（18条，9.7%）体现了学习场景的强烈需求。
</div>
</div>

<div class="section">
<h2>🎯 产品建议推导</h2>
<p style="margin-bottom:20px;color:var(--text-light)">
以下产品建议基于完整的逻辑链路推导：从UGC原始表达 → 主题分类 → 分布统计 → 交互量分析 → 场景情绪关联 → 最终产品建议。
</p>

<h3>P0 优先级（核心功能）</h3>

<div class="rec-box">
<strong>🚀 1. AI视频生成与编辑工具集</strong><br><br>
<strong>推导依据</strong>：
<div class="logic-chain" style="margin:12px 0">
<div class="step"><div class="step-num">1</div><div class="step-content"><strong>UGC观察</strong>：118条UGC（63.8%有效样本）表达视频生成/编辑需求</div></div>
<div class="arrow">↓</div>
<div class="step"><div class="step-num">2</div><div class="step-content"><strong>细分拆解</strong>：AI生成视频82条（44.3%）、自动剪辑37条（20.0%）、二创工具16条（8.6%）</div></div>
<div class="arrow">↓</div>
<div class="step"><div class="step-num">3</div><div class="step-content"><strong>交互量验证</strong>：平均互动量9,342，最高达396,152，说明该需求具有极强的用户关注度和传播性</div></div>
<div class="arrow">↓</div>
<div class="step"><div class="step-num">4</div><div class="step-content"><strong>情绪佐证</strong>：以"期待/渴望"和"惊喜/兴奋"为主，用户actively seeking解决方案</div></div>
<div class="arrow">↓</div>
<div class="step"><div class="step-num">5</div><div class="step-content"><strong>产品建议</strong>：开发文生视频、图生视频、一键成片、智能高光剪辑、数字人/虚拟主播、视频风格迁移等功能集</div></div>
</div>
<strong>目标平台</strong>：抖音、快手、B站（创作属性强的平台）
</div>

<div class="rec-box">
<strong>🚀 2. 视频学习助手</strong><br><br>
<strong>推导依据</strong>：
<div class="logic-chain" style="margin:12px 0">
<div class="step"><div class="step-num">1</div><div class="step-content"><strong>UGC观察</strong>：47条UGC（25.4%）表达学习/笔记需求，且"工作/学习"场景占47条（25.4%）</div></div>
<div class="arrow">↓</div>
<div class="step"><div class="step-num">2</div><div class="step-content"><strong>细分拆解</strong>：学习管理33条（17.8%）、知识提取18条（9.7%）、笔记工具4条（2.2%）</div></div>
<div class="arrow">↓</div>
<div class="step"><div class="step-num">3</div><div class="step-content"><strong>典型UGC</strong>："视频→AI提取→Obsidian入库"、"一键总结视频内容"、"生成专属网课"</div></div>
<div class="arrow">↓</div>
<div class="step"><div class="step-num">4</div><div class="step-content"><strong>情绪佐证</strong>：以"期待/渴望"（19条）和"惊喜/兴奋"（15条）为主，焦虑情绪4条说明时间效率是痛点</div></div>
<div class="arrow">↓</div>
<div class="step"><div class="step-num">5</div><div class="step-content"><strong>产品建议</strong>：开发视频智能摘要、章节自动拆分、知识点提取、思维导图生成、视频笔记同步（Obsidian/Notion）、学习进度管理等功能</div></div>
</div>
<strong>目标平台</strong>：知乎、B站（知识属性强的平台）
</div>

<div class="rec-box">
<strong>🚀 3. 视频内容智能搜索</strong><br><br>
<strong>推导依据</strong>：
<div class="logic-chain" style="margin:12px 0">
<div class="step"><div class="step-num">1</div><div class="step-content"><strong>UGC观察</strong>：37条UGC（20.0%）表达内容搜索/定位需求</div></div>
<div class="arrow">↓</div>
<div class="step"><div class="step-num">2</div><div class="step-content"><strong>典型表达</strong>："哪个ai可以将视频发给它让它去分析"、"全网抓信息"、"AI智能搜索"</div></div>
<div class="arrow">↓</div>
<div class="step"><div class="step-num">3</div><div class="step-content"><strong>交互量验证</strong>：平均互动量698，虽不高但需求明确，说明是"刚需但未被很好满足"的蓝海</div></div>
<div class="arrow">↓</div>
<div class="step"><div class="step-num">4</div><div class="step-content"><strong>情绪佐证</strong>：以"期待/渴望"（15条）和"惊喜/兴奋"（12条）为主，说明用户对现有搜索工具不满意</div></div>
<div class="arrow">↓</div>
<div class="step"><div class="step-num">5</div><div class="step-content"><strong>产品建议</strong>：开发语义视频搜索、片段定位、关键词高亮、视频内容问答、跨视频知识关联等功能</div></div>
</div>
<strong>目标平台</strong>：全平台（尤其是知识类视频密集的平台）
</div>

<h3>P1 优先级（差异化功能）</h3>

<div class="rec-box" style="border-left-color:var(--warning);background:linear-gradient(135deg,#fefce8 0%,#fef9c3 100%)">
<strong>💎 4. 视频摘要与总结</strong>（30条，16.2%）- 与"学习助手"有重叠但侧重<strong>快速消费</strong>场景<br>
<strong>💎 5. 智能推荐与过滤</strong>（27条，14.6%）- 解决"同质化"、"重复内容"痛点，负面情绪中"疲惫/厌倦"占7条<br>
<strong>💎 6. 语音字幕与翻译</strong>（25条，13.5%）- 跨语言学习需求强烈，知乎占12条（48%）<br>
</div>

<h3>P2 优先级（长尾机会）</h3>

<div class="rec-box" style="border-left-color:var(--info);background:linear-gradient(135deg,#f0f9ff 0%,#e0f2fe 100%)">
<strong>🔹 7. 画质修复与增强</strong>（13条，7.0%）- 老视频修复、4K增强，技术门槛高但用户愿意付费<br>
<strong>🔹 8. 效率倍速与精简</strong>（12条，6.5%）- 智能倍速、跳过广告、内容精简，frustration情绪3条说明痛点明确<br>
<strong>🔹 9. 情感氛围调节</strong>（14条，7.6%）- 氛围音效、助眠解压、情绪适配，差异化明显<br>
<strong>🔹 10. 跨设备同步</strong>（9条，4.9%）- 多端同步、投屏控制，平均点赞仅22说明需求存在但不够强烈
</div>

</div>

<div class="section">
<h2>📈 关键结论与行动建议</h2>

<div class="insight-box">
<strong>📌 结论1：数据质量是最大挑战</strong><br>
523条原始UGC中仅185条（35.4%）与主题真正相关。大量无关内容（AI生图、编程工具、纯AI资讯）污染了数据集。
<strong>行动</strong>：优化搜索词策略，使用"看视频痛点"、"视频功能需求"、"AI视频助手"等更精准的关键词组合。
</div>

<div class="insight-box">
<strong>📌 结论2：创作工具是最大机会</strong><br>
视频生成/编辑需求占63.8%，远超其他主题。AI生成视频（44.3%）和自动剪辑（20.0%）是用户最迫切的需求。
<strong>行动</strong>：优先开发文生视频、图生视频、一键成片等创作工具，目标用户为内容创作者。
</div>

<div class="insight-box">
<strong>📌 结论3：学习场景是差异化蓝海</strong><br>
工作/学习场景占25.4%，且学习/笔记需求（25.4%）与视频摘要（16.2%）形成强关联。用户希望将视频内容转化为结构化知识。
<strong>行动</strong>：开发"视频学习助手"产品线，包含智能摘要、知识点提取、思维导图生成、笔记同步等功能。
</div>

<div class="insight-box">
<strong>📌 结论4：情绪以期待为主，市场教育成本低</strong><br>
"期待/渴望"情绪占22.2%，"惊喜/兴奋"占17.3%，负面情绪合计约19%。说明用户对新功能持开放态度，市场教育成本较低。
<strong>行动</strong>：产品定位应强调"创新"和"未来感"，而非"解决痛点"。
</div>

<div class="insight-box">
<strong>📌 结论5：平台差异显著，需差异化策略</strong><br>
抖音/快手偏创作工具（视频生成/编辑），知乎偏学习（笔记/知识提取），B站两者兼顾，小红书数据质量较差。
<strong>行动</strong>：针对不同平台用户特点设计差异化功能和营销策略。
</div>

</div>

<div style="text-align:center;padding:40px;color:var(--text-light);font-size:0.9em">
<p>AI产品需求调研报告 | 生成时间: 2026-05-18</p>
<p style="margin-top:8px">方法论: ai-demand-research-v3 | 分类方式: 语义理解 + 规则增强（排除社交/互动干扰）</p>
</div>

</div>

<script>
function toggleCollapse(header) {
    const content = header.nextElementSibling;
    const icon = header.querySelector('.toggle-icon');
    content.classList.toggle('active');
    icon.classList.toggle('rotated');
}
</script>

</body>
</html>
"""

# 保存完整报告
output_path = f"{project_dir}/02-cleaned/ai_demand_research_report_v3.html"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ 完整HTML报告已生成: {output_path}")
print(f"   文件大小: {len(html):,} 字符")
print(f"   约 {len(html)//1024} KB")
