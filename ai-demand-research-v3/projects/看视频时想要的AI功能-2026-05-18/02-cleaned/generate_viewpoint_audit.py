#!/usr/bin/env python3
"""生成视角审核HTML，区分创造者视角和消费者视角"""

import json

project_dir = "/Users/zhijian/workspace/ai-demand-research-v3/projects/看视频时想要的AI功能-2026-05-18"

with open(f"{project_dir}/02-cleaned/ugc_full_text_with_tags.json", 'r', encoding='utf-8') as f:
    ugc_list = json.load(f)

platform_names = {'xhs': '小红书', 'dy': '抖音', 'ks': '快手', 'bili': 'B站', 'zhihu': '知乎'}

# 定义创造者视角关键词
creator_keywords = [
    '生成视频', '文生视频', '图生视频', '一键成片', 'AI生成', '生成短片', '生成动画',
    '数字人', '虚拟主播', '换脸', 'deepfake', 'AI特效', '特效制作',
    '自动剪辑', '智能剪辑', '一键剪辑', '自动剪', 'AI剪辑', '剪辑工具',
    '高光', '精彩片段', '自动截取', '自动切片',
    '二创', '混剪', '合拍', '模板', '素材', '视频模板', '创作工具',
    '视频制作', '做视频', '剪视频', '拍视频', '录视频',
    '视频编辑', '视频剪辑软件', '剪辑软件', 'PR', '剪映', 'final cut',
    '视频后期', '后期制作', '调色', '配音', '配字幕',
    'up主', '博主', '创作者', '内容创作', '视频创作', '短视频创作',
    '流量', '涨粉', '爆款', '视频号', '自媒体',
]

# 定义消费者视角关键词
consumer_keywords = [
    '看视频', '观看', '播放', '看剧', '追剧', '看电影', '看番',
    '学习', '记笔记', '知识点', '复习', '课程', '网课', '教程',
    '摘要', '总结', '提炼', '要点', '精华', '省流',
    '搜索', '找', '定位', '跳转到', '时间戳',
    '推荐', '个性化', '过滤', '屏蔽', '不感兴趣', '同质化',
    '字幕', '翻译', '听不懂', '外语', '英文', '日文',
    '倍速', '快进', '跳过', '广告', '片头', '片尾',
    '画质', '高清', '4K', '模糊', '清晰',
    '投屏', '同步', '跨设备', '手机看', '电视',
    '氛围', '助眠', '解压', '放松', '沉浸式',
    '问视频', '解释', '什么意思', '为什么',
]

# 分类
creator_ugcs = []
consumer_ugcs = []
uncertain_ugcs = []

for ugc in ugc_list:
    if not ugc['related']:
        continue
    
    text = (ugc['title'] + ' ' + ugc['content']).lower()
    
    has_creator = any(kw in text for kw in creator_keywords)
    has_consumer = any(kw in text for kw in consumer_keywords)
    
    if has_creator and not has_consumer:
        creator_ugcs.append(ugc)
    elif has_consumer and not has_creator:
        consumer_ugcs.append(ugc)
    elif has_creator and has_consumer:
        uncertain_ugcs.append(ugc)
    else:
        creator_tags = {'AI生成视频', '自动剪辑', '二创工具'}
        if any(tag in creator_tags for tag in ugc['layer2']):
            creator_ugcs.append(ugc)
        else:
            consumer_ugcs.append(ugc)

# 保存JSON
with open(f"{project_dir}/02-cleaned/creator_view_ugcs.json", 'w', encoding='utf-8') as f:
    json.dump(creator_ugcs, f, ensure_ascii=False, indent=2)

with open(f"{project_dir}/02-cleaned/mixed_view_ugcs.json", 'w', encoding='utf-8') as f:
    json.dump(uncertain_ugcs, f, ensure_ascii=False, indent=2)

with open(f"{project_dir}/02-cleaned/consumer_view_ugcs.json", 'w', encoding='utf-8') as f:
    json.dump(consumer_ugcs, f, ensure_ascii=False, indent=2)

print(f"已保存三类UGC列表:")
print(f"  创造者视角: {len(creator_ugcs)}条")
print(f"  消费者视角: {len(consumer_ugcs)}条")
print(f"  混合视角: {len(uncertain_ugcs)}条")

# 生成审核HTML
html = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>视角审核 - 创造者vs消费者</title>
<style>
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f8fafc;padding:20px}
.container{max-width:1200px;margin:0 auto}
.header{background:linear-gradient(135deg,#4f46e5 0%,#7c3aed 100%);color:white;padding:30px;border-radius:12px;margin-bottom:20px}
.section{background:white;padding:20px;border-radius:8px;margin-bottom:16px;box-shadow:0 1px 3px rgba(0,0,0,0.08)}
.ugc-item{background:#f8fafc;border:1px solid #e2e8f0;border-radius:6px;padding:12px;margin-bottom:8px}
.ugc-item .title{font-weight:600;margin-bottom:4px}
.ugc-item .content{font-size:0.9em;color:#64748b;margin-bottom:6px}
.ugc-item .tags{display:flex;gap:4px;flex-wrap:wrap}
.tag{padding:2px 8px;border-radius:10px;font-size:0.75em}
.tag-creator{background:#fee2e2;color:#991b1b}
.tag-consumer{background:#d1fae5;color:#065f46}
.tag-mixed{background:#fef3c7;color:#92400e}
.tabs{display:flex;gap:8px;margin-bottom:16px}
.tab{padding:8px 16px;border-radius:20px;background:#e0e7ff;color:#4f46e5;cursor:pointer;font-size:0.9em;font-weight:600;border:none}
.tab.active{background:#4f46e5;color:white}
.panel{display:none}
.panel.active{display:block}
</style>
</head>
<body>
<div class="container">
<div class="header">
<h1>🎬 视角审核：创造者 vs 消费者</h1>
<p>请审核以下UGC的视角分类是否准确。创造者视角应排除，消费者视角应保留。</p>
</div>

<div class="tabs">
<button class="tab active" onclick="showPanel('creator')">🔴 创造者视角 (""" + str(len(creator_ugcs)) + """) </button>
<button class="tab" onclick="showPanel('mixed')">🟡 混合视角 (""" + str(len(uncertain_ugcs)) + """) </button>
<button class="tab" onclick="showPanel('consumer')">🟢 消费者视角 (""" + str(len(consumer_ugcs)) + """) </button>
</div>

<div id="creator" class="panel active">
<div class="section">
<h2>🔴 创造者视角（建议排除）</h2>
<p style="color:#64748b;font-size:0.9em">这些UGC主要从内容创作者角度出发，讨论AI如何帮助制作/编辑视频，而非作为消费者看视频时想要什么AI功能。</p>
"""

for ugc in creator_ugcs:
    html += f"""
<div class="ugc-item">
<div class="title">[{platform_names.get(ugc['platform'], ugc['platform'])}] {ugc['title'][:100]}</div>
<div class="content">{ugc['content'][:200]}...</div>
<div class="tags">
<span class="tag tag-creator">二层: {', '.join(ugc['layer2']) if ugc['layer2'] else '无'}</span>
</div>
</div>
"""

html += "</div></div>"

html += """
<div id="mixed" class="panel">
<div class="section">
<h2>🟡 混合视角（需人工判断）</h2>
<p style="color:#64748b;font-size:0.9em">这些UGC同时包含创造者和消费者视角，请逐条判断是否应保留。</p>
"""

for ugc in uncertain_ugcs:
    html += f"""
<div class="ugc-item">
<div class="title">[{platform_names.get(ugc['platform'], ugc['platform'])}] {ugc['title'][:100]}</div>
<div class="content">{ugc['content'][:200]}...</div>
<div class="tags">
<span class="tag tag-mixed">二层: {', '.join(ugc['layer2']) if ugc['layer2'] else '无'}</span>
</div>
</div>
"""

html += "</div></div>"

html += """
<div id="consumer" class="panel">
<div class="section">
<h2>🟢 消费者视角（建议保留）</h2>
<p style="color:#64748b;font-size:0.9em">这些UGC从内容消费者角度出发，讨论看视频时想要的AI功能。</p>
"""

for ugc in consumer_ugcs:
    html += f"""
<div class="ugc-item">
<div class="title">[{platform_names.get(ugc['platform'], ugc['platform'])}] {ugc['title'][:100]}</div>
<div class="content">{ugc['content'][:200]}...</div>
<div class="tags">
<span class="tag tag-consumer">二层: {', '.join(ugc['layer2']) if ugc['layer2'] else '无'}</span>
</div>
</div>
"""

html += """
</div></div>

<script>
function showPanel(id) {
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.getElementById(id).classList.add('active');
    event.target.classList.add('active');
}
</script>

</body>
</html>
"""

with open(f"{project_dir}/02-cleaned/viewpoint_audit.html", 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n✅ 视角审核HTML已生成: {project_dir}/02-cleaned/viewpoint_audit.html")
print(f"   文件大小: {len(html):,} 字符")