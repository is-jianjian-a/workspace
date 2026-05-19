#!/usr/bin/env python3
"""生成包含所有UGC全文+标签+匹配词词典的完整HTML报告"""

import json
from collections import Counter

project_dir = "/Users/zhijian/workspace/ai-demand-research-v3/projects/看视频时想要的AI功能-2026-05-18"

with open(f"{project_dir}/02-cleaned/ugc_full_text_with_tags.json", 'r', encoding='utf-8') as f:
    ugc_list = json.load(f)

with open(f"{project_dir}/02-cleaned/tagging_keywords.json", 'r', encoding='utf-8') as f:
    keywords = json.load(f)

# 提取所有匹配词
all_keywords = {}
for tag_type in ['layer1', 'layer2', 'emotion', 'scene']:
    all_keywords[tag_type] = {}
    for tag_name, tag_info in keywords['tags'][tag_type].items():
        if isinstance(tag_info, dict) and 'keywords' in tag_info:
            all_keywords[tag_type][tag_name] = tag_info['keywords']

platform_names = {'xhs': '小红书', 'dy': '抖音', 'ks': '快手', 'bili': 'B站', 'zhihu': '知乎'}
platform_colors = {'xhs': '#ff2442', 'dy': '#000000', 'ks': '#ff6600', 'bili': '#00a1d6', 'zhihu': '#0084ff'}

# 生成HTML
html = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>看视频时想要的AI功能 - UGC全文与分类标签核查报告</title>
<style>
:root{--primary:#4f46e5;--secondary:#7c3aed;--bg:#f8fafc;--card:#fff;--text:#1e293b;--text-light:#64748b;--border:#e2e8f0;--success:#10b981;--warning:#f59e0b;--info:#3b82f6;--danger:#ef4444;}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.7}
.container{max-width:1400px;margin:0 auto;padding:20px}
.header{background:linear-gradient(135deg,var(--primary) 0%,var(--secondary) 100%);color:white;padding:40px;border-radius:16px;margin-bottom:30px}
.header h1{font-size:2em;margin-bottom:10px}
.header .subtitle{font-size:1em;opacity:0.9;margin-bottom:16px}
.header .meta{display:flex;gap:20px;flex-wrap:wrap;font-size:0.85em;opacity:0.85}
.section{background:var(--card);padding:28px;border-radius:12px;margin-bottom:20px;box-shadow:0 1px 3px rgba(0,0,0,0.08)}
.section h2{font-size:1.3em;margin-bottom:16px;padding-bottom:10px;border-bottom:2px solid var(--border);color:var(--primary)}
.section h3{font-size:1.1em;margin:20px 0 10px;color:var(--secondary)}
.section h4{font-size:1em;margin:14px 0 8px}
.tabs{display:flex;gap:8px;margin-bottom:20px;flex-wrap:wrap}
.tab{padding:8px 16px;border-radius:20px;background:#e0e7ff;color:var(--primary);cursor:pointer;font-size:0.9em;font-weight:600;border:none}
.tab.active{background:var(--primary);color:white}
.tab:hover{background:#c7d2fe}
.content-panel{display:none}
.content-panel.active{display:block}
.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin-bottom:16px}
.stat-card{background:linear-gradient(135deg,#f0f4ff 0%,#e0e7ff 100%);padding:16px;border-radius:10px;border-left:4px solid var(--primary)}
.stat-card .number{font-size:1.8em;font-weight:700;color:var(--primary)}
.stat-card .label{color:var(--text-light);font-size:0.85em;margin-top:4px}
.ugc-item{background:#f8fafc;border:1px solid var(--border);border-radius:8px;padding:16px;margin-bottom:12px}
.ugc-item .ugc-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;flex-wrap:wrap;gap:8px}
.ugc-item .platform{font-size:0.8em;font-weight:600;color:var(--primary);background:#e0e7ff;padding:2px 10px;border-radius:12px}
.ugc-item .likes{font-size:0.8em;color:var(--text-light)}
.ugc-item .title{font-weight:600;margin-bottom:6px;font-size:1em}
.ugc-item .content-full{font-size:0.9em;color:var(--text);margin-bottom:10px;line-height:1.6;white-space:pre-wrap;word-break:break-word;background:#fff;padding:12px;border-radius:6px;border:1px solid #e2e8f0}
.ugc-item .tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.tag{display:inline-block;padding:3px 10px;border-radius:12px;font-size:0.8em;font-weight:500}
.tag-l1{background:#e0e7ff;color:var(--primary)}
.tag-l2{background:#f3e8ff;color:var(--secondary)}
.tag-emotion{background:#fef3c7;color:#92400e}
.tag-scene{background:#d1fae5;color:#065f46}
.tag-related-yes{background:#d1fae5;color:#065f46}
.tag-related-no{background:#fee2e2;color:#991b1b}
.filter-bar{display:flex;gap:12px;margin-bottom:16px;flex-wrap:wrap;align-items:center}
.filter-bar select,.filter-bar input{padding:8px 12px;border:1px solid var(--border);border-radius:6px;font-size:0.9em}
.filter-bar label{font-size:0.9em;font-weight:600;color:var(--text-light)}
.keyword-dict{background:#f8fafc;border:1px solid var(--border);border-radius:8px;padding:16px;margin-bottom:12px}
.keyword-dict h4{margin-bottom:8px;color:var(--primary)}
.keyword-dict .word-list{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.keyword-dict .word{background:#e0e7ff;color:var(--primary);padding:2px 8px;border-radius:10px;font-size:0.8em}
.keyword-dict .word-match{background:#fef3c7;color:#92400e;padding:2px 8px;border-radius:10px;font-size:0.8em;font-weight:600}
table{width:100%;border-collapse:collapse;margin-top:12px;font-size:0.85em}
th,td{padding:8px 10px;text-align:left;border-bottom:1px solid var(--border)}
th{background:#f8fafc;font-weight:600;color:var(--text-light);font-size:0.8em}
tr:hover{background:#f8fafc}
.pagination{display:flex;gap:8px;justify-content:center;margin-top:20px;flex-wrap:wrap}
.page-btn{padding:6px 12px;border:1px solid var(--border);background:white;border-radius:6px;cursor:pointer;font-size:0.85em}
.page-btn:hover{background:var(--primary);color:white}
.page-btn.active{background:var(--primary);color:white;border-color:var(--primary)}
@media(max-width:768px){.container{padding:12px}.header{padding:24px}.header h1{font-size:1.5em}}
</style>
</head>
<body>
<div class="container">

<div class="header">
<h1>🎬 看视频时想要的AI功能</h1>
<div class="subtitle">UGC全文与分类标签核查报告 - 用于人工审核分类准确性</div>
<div class="meta">
<span>📅 2026-05-18</span>
<span>📊 总UGC: """ + str(len(ugc_list)) + """条</span>
<span>✅ 相关: """ + str(sum(1 for u in ugc_list if u['related'])) + """条</span>
<span>❌ 不相关: """ + str(sum(1 for u in ugc_list if not u['related'])) + """条</span>
</div>
</div>

<div class="tabs">
<button class="tab active" onclick="showTab('ugc-list')">📋 UGC全文列表</button>
<button class="tab" onclick="showTab('keyword-dict')">📖 匹配词词典</button>
<button class="tab" onclick="showTab('stats')">📊 分类统计</button>
</div>

<div id="ugc-list" class="content-panel active">
<div class="section">
<h2>📋 UGC全文与分类标签</h2>
<p style="margin-bottom:16px;color:var(--text-light);font-size:0.9em">
以下展示所有UGC的完整原文和对应的分类标签。你可以逐条检查分类是否准确。
<strong>绿色标签</strong>表示"相关"，<strong>红色标签</strong>表示"不相关"。
</p>

<div class="filter-bar">
<label>相关性:</label>
<select id="filter-related" onchange="filterUGCs()">
<option value="all">全部</option>
<option value="yes">相关</option>
<option value="no">不相关</option>
</select>

<label>平台:</label>
<select id="filter-platform" onchange="filterUGCs()">
<option value="all">全部</option>
<option value="xhs">小红书</option>
<option value="dy">抖音</option>
<option value="ks">快手</option>
<option value="bili">B站</option>
<option value="zhihu">知乎</option>
</select>

<label>一层主题:</label>
<select id="filter-layer1" onchange="filterUGCs()">
<option value="all">全部</option>
"""

# 添加一层主题选项
layer1_tags = sorted(set(tag for u in ugc_list for tag in u['layer1']))
for tag in layer1_tags:
    html += f'<option value="{tag}">{tag}</option>\n'

html += """
</select>

<label>搜索:</label>
<input type="text" id="filter-search" placeholder="搜索标题或内容..." oninput="filterUGCs()">
</div>

<div id="ugc-container">
"""

# 分页显示UGC，每页50条
page_size = 50
total_pages = (len(ugc_list) + page_size - 1) // page_size

for idx, ugc in enumerate(ugc_list):
    page_num = idx // page_size
    
    related_class = 'tag-related-yes' if ugc['related'] else 'tag-related-no'
    related_text = '相关' if ugc['related'] else '不相关'
    
    layer1_tags_html = ''.join([f'<span class="tag tag-l1">{t}</span>' for t in ugc['layer1']])
    layer2_tags_html = ''.join([f'<span class="tag tag-l2">{t}</span>' for t in ugc['layer2']])
    emotion_tags_html = ''.join([f'<span class="tag tag-emotion">{t}</span>' for t in ugc['emotions']])
    scene_tags_html = ''.join([f'<span class="tag tag-scene">{t}</span>' for t in ugc['scenes']])
    
    # 处理内容中的HTML特殊字符
    content_escaped = ugc['content'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    title_escaped = ugc['title'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    html += f"""
<div class="ugc-item" data-page="{page_num}" data-related="{'yes' if ugc['related'] else 'no'}" data-platform="{ugc['platform']}" data-layer1="{','.join(ugc['layer1'])}" data-search="{(ugc['title'] + ' ' + ugc['content']).lower()}">
<div class="ugc-header">
<div style="display:flex;gap:8px;align-items:center">
<span class="platform">{platform_names.get(ugc['platform'], ugc['platform'])}</span>
<span class="tag {related_class}">{related_text}</span>
<span class="likes">👍 {ugc['likes']:.0f}</span>
</div>
<span style="font-size:0.8em;color:var(--text-light)">ID: {ugc['id']}</span>
</div>
<div class="title">{title_escaped}</div>
<div class="content-full">{content_escaped}</div>
<div class="tags">
<span style="font-size:0.8em;color:var(--text-light);margin-right:8px">一层:</span>
{layer1_tags_html if layer1_tags_html else '<span style="color:var(--text-light);font-size:0.8em">无</span>'}
</div>
<div class="tags">
<span style="font-size:0.8em;color:var(--text-light);margin-right:8px">二层:</span>
{layer2_tags_html if layer2_tags_html else '<span style="color:var(--text-light);font-size:0.8em">无</span>'}
</div>
<div class="tags">
<span style="font-size:0.8em;color:var(--text-light);margin-right:8px">情绪:</span>
{emotion_tags_html if emotion_tags_html else '<span style="color:var(--text-light);font-size:0.8em">无</span>'}
</div>
<div class="tags">
<span style="font-size:0.8em;color:var(--text-light);margin-right:8px">场景:</span>
{scene_tags_html if scene_tags_html else '<span style="color:var(--text-light);font-size:0.8em">无</span>'}
</div>
</div>
"""

# 分页按钮
html += '</div><div class="pagination" id="pagination">'
for i in range(total_pages):
    html += f'<button class="page-btn {"active" if i == 0 else ""}" onclick="goToPage({i})">{i+1}</button>'
html += '</div></div></div>'

print(f"UGC列表生成完成，当前长度: {len(html)}")

# 匹配词词典面板
html += """
<div id="keyword-dict" class="content-panel">
<div class="section">
<h2>📖 匹配词词典</h2>
<p style="margin-bottom:16px;color:var(--text-light);font-size:0.9em">
以下展示每个标签使用的完整关键词列表。<strong>黄色高亮</strong>的词表示在UGC中实际命中过。
</p>

<h3>🏷️ 一层主题关键词</h3>
"""

# 统计每个关键词的命中次数
keyword_hits = {}
for tag_type in ['layer1', 'layer2', 'emotion', 'scene']:
    keyword_hits[tag_type] = {}
    for tag_name, words in all_keywords[tag_type].items():
        keyword_hits[tag_type][tag_name] = {}
        for word in words:
            count = 0
            for ugc in ugc_list:
                if word.lower() in (ugc['title'] + ' ' + ugc['content']).lower():
                    count += 1
            keyword_hits[tag_type][tag_name][word] = count

# 一层主题词典
for tag_name, words in all_keywords['layer1'].items():
    hits = keyword_hits['layer1'][tag_name]
    html += f"""
<div class="keyword-dict">
<h4>{tag_name}</h4>
<div class="word-list">
"""
    for word in words:
        hit_count = hits.get(word, 0)
        css_class = 'word-match' if hit_count > 0 else 'word'
        html += f'<span class="{css_class}">{word}({hit_count})</span>'
    html += "</div></div>\n"

html += "<h3>🔍 二层主题关键词</h3>\n"

# 二层主题词典
for tag_name, words in all_keywords['layer2'].items():
    hits = keyword_hits['layer2'][tag_name]
    html += f"""
<div class="keyword-dict">
<h4>{tag_name}</h4>
<div class="word-list">
"""
    for word in words:
        hit_count = hits.get(word, 0)
        css_class = 'word-match' if hit_count > 0 else 'word'
        html += f'<span class="{css_class}">{word}({hit_count})</span>'
    html += "</div></div>\n"

html += "<h3>😊 情绪关键词</h3>\n"

# 情绪词典
for tag_name, words in all_keywords['emotion'].items():
    hits = keyword_hits['emotion'][tag_name]
    html += f"""
<div class="keyword-dict">
<h4>{tag_name}</h4>
<div class="word-list">
"""
    for word in words:
        hit_count = hits.get(word, 0)
        css_class = 'word-match' if hit_count > 0 else 'word'
        html += f'<span class="{css_class}">{word}({hit_count})</span>'
    html += "</div></div>\n"

html += "<h3>🌍 场景关键词</h3>\n"

# 场景词典
for tag_name, words in all_keywords['scene'].items():
    hits = keyword_hits['scene'][tag_name]
    html += f"""
<div class="keyword-dict">
<h4>{tag_name}</h4>
<div class="word-list">
"""
    for word in words:
        hit_count = hits.get(word, 0)
        css_class = 'word-match' if hit_count > 0 else 'word'
        html += f'<span class="{css_class}">{word}({hit_count})</span>'
    html += "</div></div>\n"

html += "</div></div>\n"

# 统计面板
html += """
<div id="stats" class="content-panel">
<div class="section">
<h2>📊 分类统计</h2>

<h3>相关性分布</h3>
<div class="stats-grid">
"""

related_count = sum(1 for u in ugc_list if u['related'])
unrelated_count = sum(1 for u in ugc_list if not u['related'])

html += f"""
<div class="stat-card"><div class="number">{related_count}</div><div class="label">相关UGC</div></div>
<div class="stat-card"><div class="number">{unrelated_count}</div><div class="label">不相关UGC</div></div>
<div class="stat-card"><div class="number">{related_count/len(ugc_list)*100:.1f}%</div><div class="label">相关率</div></div>
</div>

<h3>一层主题分布</h3>
<table>
<thead><tr><th>主题</th><th>数量</th><th>占比</th></tr></thead>
<tbody>
"""

layer1_counter = Counter()
for ugc in ugc_list:
    if ugc['related']:
        for tag in ugc['layer1']:
            layer1_counter[tag] += 1

for tag, count in layer1_counter.most_common():
    pct = count / related_count * 100 if related_count > 0 else 0
    html += f'<tr><td>{tag}</td><td>{count}</td><td>{pct:.1f}%</td></tr>\n'

html += """</tbody>
</table>

<h3>二层主题分布Top15</h3>
<table>
<thead><tr><th>主题</th><th>数量</th><th>占比</th></tr></thead>
<tbody>
"""

layer2_counter = Counter()
for ugc in ugc_list:
    if ugc['related']:
        for tag in ugc['layer2']:
            layer2_counter[tag] += 1

for tag, count in layer2_counter.most_common(15):
    pct = count / related_count * 100 if related_count > 0 else 0
    html += f'<tr><td>{tag}</td><td>{count}</td><td>{pct:.1f}%</td></tr>\n'

html += """</tbody>
</table>

<h3>情绪分布</h3>
<table>
<thead><tr><th>情绪</th><th>数量</th><th>占比</th></tr></thead>
<tbody>
"""

emotion_counter = Counter()
for ugc in ugc_list:
    if ugc['related']:
        for tag in ugc['emotions']:
            emotion_counter[tag] += 1

for tag, count in emotion_counter.most_common():
    pct = count / related_count * 100 if related_count > 0 else 0
    html += f'<tr><td>{tag}</td><td>{count}</td><td>{pct:.1f}%</td></tr>\n'

html += """</tbody>
</table>

<h3>场景分布</h3>
<table>
<thead><tr><th>场景</th><th>数量</th><th>占比</th></tr></thead>
<tbody>
"""

scene_counter = Counter()
for ugc in ugc_list:
    if ugc['related']:
        for tag in ugc['scenes']:
            scene_counter[tag] += 1

for tag, count in scene_counter.most_common():
    pct = count / related_count * 100 if related_count > 0 else 0
    html += f'<tr><td>{tag}</td><td>{count}</td><td>{pct:.1f}%</td></tr>\n'

html += """</tbody>
</table>
</div>
</div>

</div>

<script>
function showTab(tabId) {
    document.querySelectorAll('.content-panel').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
    event.target.classList.add('active');
}

let currentPage = 0;
const pageSize = 50;

function goToPage(pageNum) {
    currentPage = pageNum;
    document.querySelectorAll('.ugc-item').forEach(item => {
        if (item.dataset.page == pageNum) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
    document.querySelectorAll('.page-btn').forEach((btn, idx) => {
        btn.classList.toggle('active', idx === pageNum);
    });
}

function filterUGCs() {
    const related = document.getElementById('filter-related').value;
    const platform = document.getElementById('filter-platform').value;
    const layer1 = document.getElementById('filter-layer1').value;
    const search = document.getElementById('filter-search').value.toLowerCase();
    
    document.querySelectorAll('.ugc-item').forEach(item => {
        let show = true;
        if (related !== 'all' && item.dataset.related !== related) show = false;
        if (platform !== 'all' && item.dataset.platform !== platform) show = false;
        if (layer1 !== 'all' && !item.dataset.layer1.includes(layer1)) show = false;
        if (search && !item.dataset.search.includes(search)) show = false;
        item.style.display = show ? 'block' : 'none';
    });
    
    document.getElementById('pagination').style.display = 'none';
}

// 初始化显示第一页
document.addEventListener('DOMContentLoaded', function() {
    goToPage(0);
});
</script>

</body>
</html>
"""

# 保存完整报告
output_path = f"{project_dir}/02-cleaned/ugc_full_text_audit_report.html"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ 完整HTML报告已生成: {output_path}")
print(f"   文件大小: {len(html):,} 字符")
print(f"   约 {len(html)//1024} KB")