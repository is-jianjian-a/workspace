#!/usr/bin/env python3
"""
生成完整的HTML调研报告
包含：完整逻辑链路、推导依据、数据可视化、二层主题深度分析
"""

import json
from collections import Counter

project_dir = "/Users/zhijian/workspace/ai-demand-research-v3/projects/看视频时想要的AI功能-2026-05-18"

with open(f"{project_dir}/02-cleaned/all_classification_results_v3.json", 'r', encoding='utf-8') as f:
    all_results = json.load(f)

with open(f"{project_dir}/02-cleaned/theme_analysis_v3.json", 'r', encoding='utf-8') as f:
    theme_analysis = json.load(f)

with open(f"{project_dir}/01-raw/all_ugcs_523.json", 'r', encoding='utf-8') as f:
    all_ugcs = {u['id']: u for u in json.load(f)}

# 准备数据
related_results = [r for r in all_results if r['related'] and '其他' not in r['layer1']]
layer1_counter = Counter()
for r in all_results:
    for l1 in r['layer1']:
        if l1 != '其他':
            layer1_counter[l1] += 1
platform_counter = Counter(r['platform'] for r in all_results)

platform_names = {'xhs': '小红书', 'dy': '抖音', 'ks': '快手', 'bili': 'B站', 'zhihu': '知乎'}
platform_colors = {'xhs': '#ff2442', 'dy': '#000000', 'ks': '#ff6600', 'bili': '#00a1d6', 'zhihu': '#0084ff'}
theme_colors = {
    '视频生成/编辑': '#4f46e5', '学习/笔记': '#7c3aed', '内容搜索/定位': '#ec4899',
    '视频摘要/总结': '#f59e0b', '智能推荐/过滤': '#10b981', '语音/字幕相关': '#3b82f6',
    '情感/氛围': '#8b5cf6', '画质/修复': '#06b6d4', '效率/倍速': '#f97316', '跨设备/同步': '#84cc16'
}

# 生成HTML
html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>看视频时想要的AI功能 - 深度需求调研报告</title>
<style>
:root{--primary:#4f46e5;--secondary:#7c3aed;--bg:#f8fafc;--card:#fff;--text:#1e293b;--text-light:#64748b;--border:#e2e8f0;--success:#10b981;--warning:#f59e0b;--info:#3b82f6;--danger:#ef4444;}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.7}
.container{max-width:1200px;margin:0 auto;padding:20px}
.header{background:linear-gradient(135deg,var(--primary) 0%,var(--secondary) 100%);color:white;padding:50px 40px;border-radius:16px;margin-bottom:30px}
.header h1{font-size:2.2em;margin-bottom:12px}
.header .subtitle{font-size:1.1em;opacity:0.9;margin-bottom:24px}
.header .meta{display:flex;gap:24px;flex-wrap:wrap;font-size:0.9em;opacity:0.85}
.section{background:var(--card);padding:32px;border-radius:12px;margin-bottom:24px;box-shadow:0 1px 3px rgba(0,0,0,0.08)}
.section h2{font-size:1.4em;margin-bottom:20px;padding-bottom:12px;border-bottom:2px solid var(--border);color:var(--primary)}
.section h3{font-size:1.15em;margin:24px 0 12px;color:var(--secondary)}
.section h4{font-size:1em;margin:16px 0 8px}
.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin-bottom:24px}
.stat-card{background:linear-gradient(135deg,#f0f4ff 0%,#e0e7ff 100%);padding:20px;border-radius:10px;border-left:4px solid var(--primary)}
.stat-card .number{font-size:2em;font-weight:700;color:var(--primary)}
.stat-card .label{color:var(--text-light);font-size:0.9em;margin-top:4px}
.bar-chart{display:flex;flex-direction:column;gap:10px;margin:20px 0}
.bar-item{display:flex;align-items:center;gap:12px}
.bar-label{width:140px;font-size:0.9em;text-align:right;flex-shrink:0}
.bar-track{flex:1;height:28px;background:var(--border);border-radius:4px;overflow:hidden}
.bar-fill{height:100%;border-radius:4px;display:flex;align-items:center;justify-content:flex-end;padding-right:8px;font-size:0.8em;font-weight:600;color:white}
.bar-value{width:50px;font-size:0.85em;color:var(--text-light);flex-shrink:0}
.ugc-item{background:#f8fafc;border:1px solid var(--border);border-radius:8px;padding:16px;margin-bottom:12px}
.ugc-item .ugc-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
.ugc-item .platform{font-size:0.85em;font-weight:600;color:var(--primary);background:#e0e7ff;padding:2px 10px;border-radius:12px}
.ugc-item .likes{font-size:0.85em;color:var(--text-light)}
.ugc-item .title{font-weight:600;margin-bottom:6px}
.ugc-item .content{font-size:0.9em;color:var(--text-light);margin-bottom:10px;line-height:1.5}
.ugc-item .tags{display:flex;flex-wrap:wrap;gap:6px}
.tag{display:inline-block;padding:3px 10px;border-radius:12px;font-size:0.8em;font-weight:500}
.tag-l1{background:#e0e7ff;color:var(--primary)}
.tag-l2{background:#f3e8ff;color:var(--secondary)}
.tag-emotion{background:#fef3c7;color:#92400e}
.tag-scene{background:#d1fae5;color:#065f46}
.logic-chain{background:linear-gradient(135deg,#f0f9ff 0%,#e0f2fe 100%);border-left:4px solid var(--info);padding:20px;border-radius:8px;margin:16px 0}
.logic-chain .step{display:flex;align-items:flex-start;gap:12px;margin-bottom:12px}
.logic-chain .step-num{background:var(--info);color:white;width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.8em;font-weight:600;flex-shrink:0}
.logic-chain .arrow{text-align:center;color:var(--info);font-size:1.2em;margin:8px 0}
.insight-box{background:linear-gradient(135deg,#fefce8 0%,#fef9c3 100%);border-left:4px solid var(--warning);padding:16px 20px;border-radius:8px;margin:16px 0}
.rec-box{background:linear-gradient(135deg,#f0fdf4 0%,#dcfce7 100%);border-left:4px solid var(--success);padding:16px 20px;border-radius:8px;margin:16px 0}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:24px}
.collapsible{background:var(--card);border:1px solid var(--border);border-radius:8px;margin-bottom:12px;overflow:hidden}
.collapsible-header{padding:14px 16px;background:#f8fafc;cursor:pointer;display:flex;justify-content:space-between;align-items:center;font-weight:600}
.collapsible-header:hover{background:#f1f5f9}
.collapsible-content{padding:16px;display:none}
.collapsible-content.active{display:block}
.toggle-icon{transition:transform 0.3s}
.toggle-icon.rotated{transform:rotate(180deg)}
table{width:100%;border-collapse:collapse;margin-top:16px;font-size:0.9em}
th,td{padding:10px 12px;text-align:left;border-bottom:1px solid var(--border)}
th{background:#f8fafc;font-weight:600;color:var(--text-light);font-size:0.85em}
tr:hover{background:#f8fafc}
@media(max-width:768px){.two-col{grid-template-columns:1fr}.header h1{font-size:1.6em}.bar-label{width:100px;font-size:0.8em}}
</style>
</head>
<body>
<div class="container">

<div class="header">
<h1>🎬 看视频时想要的AI功能</h1>
<div class="subtitle">深度需求调研报告 - 基于523条社交媒体UGC的完整逻辑分析</div>
<div class="meta">
<span>📅 2026-05-18</span>
<span>📊 小红书 | 抖音 | 快手 | B站 | 知乎</span>
<span>🔍 搜索词: "看视频时想要的AI功能"</span>
<span>🤖 语义理解 + 规则增强 (排除社交/互动干扰)</span>
</div>
</div>

<div class="section">
<h2>📋 执行摘要</h2>
<p style="margin-bottom:16px">
本次调研采集了<strong>523条</strong>社交媒体UGC，经过三层筛选（排除无关内容、排除社交/互动干扰词、语义分类），
最终识别出<strong>185条</strong>与"看视频时想要的AI功能"真正相关的用户表达。
核心发现：<strong>视频生成/编辑</strong>是最强需求信号（118条，占有效UGC的63.8%），
其次是<strong>学习/笔记</strong>（47条，25.4%）和<strong>内容搜索/定位</strong>（37条，20.0%）。
</p>
<div class="stats-grid">
<div class="stat-card"><div class="number">523</div><div class="label">总采集UGC</div></div>
<div class="stat-card"><div class="number">185</div><div class="label">有效相关UGC</div></div>
<div class="stat-card"><div class="number">10</div><div class="label">识别需求主题</div></div>
<div class="stat-card"><div class="number">32</div><div class="label">细分功能点</div></div>
</div>
</div>

<div class="section">
<h2>📊 数据概览与筛选逻辑</h2>

<h3>筛选过程（三层过滤）</h3>
<div class="logic-chain">
<div class="step"><div class="step-num">1</div><div class="step-content"><strong>原始采集</strong>：523条UGC（小红书94 + 抖音87 + 快手119 + B站105 + 知乎118）</div></div>
<div class="arrow">↓</div>
<div class="step"><div class="step-num">2</div><div class="step-content"><strong>排除明显无关</strong>：过滤AI生图教程、编程工具、育儿内容、纯AI资讯等 → 剩余311条</div></div>
<div class="arrow">↓</div>
<div class="step"><div class="step-num">3</div><div class="step-content"><strong>排除社交/互动干扰</strong>：去掉纯"分享转发"、"弹幕评论"、"一起看"、"AI对话"等无实质功能需求的表达 → 剩余216条</div></div>
<div class="arrow">↓</div>
<div class="step"><div class="step-num">4</div><div class="step-content"><strong>语义分类</strong>：对216条进行10个主题、32个功能点分类 → 有效相关185条</div></div>
</div>

<h3>平台分布</h3>
<div class="bar-chart">
"""

# 平台分布图
max_platform = max(platform_counter.values())
for p, count in sorted(platform_counter.items(), key=lambda x: x[1], reverse=True):
    pct = count / sum(platform_counter.values()) * 100
    width = (count / max_platform) * 100
    color = platform_colors.get(p, '#4f46e5')
    html += f'<div class="bar-item"><div class="bar-label">{platform_names.get(p, p)}</div><div class="bar-track"><div class="bar-fill" style="width:{width}%;background:{color}">{count}</div></div><div class="bar-value">{pct:.1f}%</div></div>\n'

html += """</div>

<div class="insight-box">
<strong>数据质量洞察</strong>：523条原始UGC中，仅185条（35.4%）与"看视频时想要的AI功能"主题真正相关。
大量内容为AI生图技巧（如"AI抽卡"、"提示词技巧"）、编程工具（如"Cursor"、"Vibe Coding"）、
纯AI工具对比（如"五大AI区别"）等无关信息。<strong>建议优化搜索词</strong>，使用更精准的关键词组合如"看视频痛点"、"视频功能需求"。
</div>
</div>

<div class="section">
<h2>🎯 一层主题深度分析</h2>
<p style="margin-bottom:20px;color:var(--text-light)">
以下分析基于185条有效相关UGC。每个主题包含：典型UGC原文 → 分类依据 → 分布统计 → 交互量分析 → 产品建议推导。
<strong style="color:var(--danger)">注意：已排除"社交/分享"和"互动/问答"主题</strong>，聚焦真实视频AI功能需求。
</p>

<h3>主题分布总览</h3>
<div class="bar-chart">
"""

# 主题分布图
layer1_data = dict(layer1_counter.most_common())
max_layer1 = max(layer1_data.values()) if layer1_data else 1

for theme, count in layer1_data.items():
    pct = count / len(related_results) * 100
    width = (count / max_layer1) * 100
    color = theme_colors.get(theme, '#4f46e5')
    html += f'<div class="bar-item"><div class="bar-label">{theme}</div><div class="bar-track"><div class="bar-fill" style="width:{width}%;background:{color}">{count}</div></div><div class="bar-value">{pct:.1f}%</div></div>\n'

html += "</div>\n"

# 逐个主题详细分析
for theme, analysis in sorted(theme_analysis.items(), key=lambda x: x[1]['total'], reverse=True):
    total = analysis['total']
    avg_likes = analysis['avg_likes']
    max_likes = analysis['max_likes']
    
    html += f"""
<div class="collapsible">
<div class="collapsible-header" onclick="toggleCollapse(this)">
<span>📌 {theme} ({total}条, 平均点赞{avg_likes:.0f})</span>
<span class="toggle-icon">▼</span>
</div>
<div class="collapsible-content">

<h4>📊 数据画像</h4>
<div class="two-col">
<div>
<p><strong>UGC数量:</strong> {total}条 ({total/len(related_results)*100:.1f}%)</p>
<p><strong>平均点赞:</strong> {avg_likes:.0f}</p>
<p><strong>最高点赞:</strong> {max_likes:.0f}</p>
</div>
<div>
<p><strong>主要平台:</strong> {', '.join([f"{platform_names.get(k,k)}({v})" for k,v in sorted(analysis['platform_dist'].items(), key=lambda x:x[1], reverse=True)[:3]])}</p>
<p><strong>主要情绪:</strong> {', '.join([f"{k}({v})" for k,v in sorted(analysis['emotion_dist'].items(), key=lambda x:x[1], reverse=True)[:3]]) if analysis['emotion_dist'] else '无明显情绪'}</p>
<p><strong>主要场景:</strong> {', '.join([f"{k}({v})" for k,v in sorted(analysis['scene_dist'].items(), key=lambda x:x[1], reverse=True)[:3]]) if analysis['scene_dist'] else '无明确场景'}</p>
</div>
</div>

<h4>📝 典型UGC与分类依据</h4>
"""
    
    for i, ugc in enumerate(analysis['top_ugcs'][:3]):
        tags_html = ''.join([f'<span class="tag tag-l2">{t}</span>' for t in ugc['layer2']])
        emotions_html = ''.join([f'<span class="tag tag-emotion">{e}</span>' for e in ugc['emotions']])
        
        html += f"""
<div class="ugc-item">
<div class="ugc-header">
<span class="platform">{platform_names.get(ugc['platform'], ugc['platform'])}</span>
<span class="likes">👍 {ugc['likes']:.0f}</span>
</div>
<div class="title">{ugc['title']}</div>
<div class="content">{ugc['content'][:200]}...</div>
<div class="tags">
{tags_html}
{emotions_html}
</div>
</div>
"""
    
    # 二层主题分布
    if analysis['layer2_dist']:
        html += """
<h4>🔍 二层主题分布</h4>
<div class="bar-chart">
"""
        max_l2 = max(analysis['layer2_dist'].values())
        for l2, count in sorted(analysis['layer2_dist'].items(), key=lambda x: x[1], reverse=True)[:5]:
            width = (count / max_l2) * 100
            html += f'<div class="bar-item"><div class="bar-label" style="width:120px">{l2}</div><div class="bar-track"><div class="bar-fill" style="width:{width}%;background:#8b5cf6">{count}</div></div></div>\n'
        html += "</div>\n"
    
    # 推导逻辑
    html += f"""
<div class="logic-chain">
<div class="step">
<div class="step-num">→</div>
<div class="step-content">
<strong>推导逻辑</strong>：从{total}条UGC观察到用户对"{theme}"的需求表达，
平均互动量{avg_likes:.0f}，主要出现在{', '.join(list(analysis['platform_dist'].keys())[:2])}平台，
伴随情绪以{', '.join(list(analysis['emotion_dist'].keys())[:2]) if analysis['emotion_dist'] else '期待'}为主。
</div>
</div>
</div>

</div>
</div>
"""

html += "</div>\n"

print(f"主题分析完成，总长度: {len(html)} 字符")

# 保存中间结果
with open(f"{project_dir}/02-cleaned/report_v3_partial.html", 'w', encoding='utf-8') as f:
    f.write(html)

print("部分报告已保存")