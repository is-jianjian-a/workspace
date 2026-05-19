#!/usr/bin/env python3
"""
项目初始化脚本
创建一个新的调研项目目录结构

用法:
    python init_project.py --topic "育儿睡眠场景调研" --data-source /path/to/data.xlsx
"""

import os
import sys
import json
import argparse
import shutil
from datetime import datetime
from pathlib import Path


def create_project(topic: str, data_source: str = None, base_dir: str = None):
    """创建新项目目录结构"""
    
    # 生成项目名
    topic_slug = topic.replace(" ", "-").replace("_", "-")[:30]
    timestamp = datetime.now().strftime("%Y-%m-%d")
    project_name = f"{topic_slug}-{timestamp}"
    
    # 确定基础目录
    if base_dir is None:
        base_dir = Path(__file__).parent.parent / "projects"
    else:
        base_dir = Path(base_dir)
    
    project_dir = base_dir / project_name
    
    # 检查是否已存在
    if project_dir.exists():
        print(f"⚠️  项目已存在: {project_dir}")
        response = input("是否覆盖? (y/N): ")
        if response.lower() != 'y':
            print("已取消")
            return None
        shutil.rmtree(project_dir)
    
    # 创建目录结构
    dirs = [
        "00-meta",
        "01-raw-data/input",
        "02-cleaned/input", "02-cleaned/code", "02-cleaned/output",
        "03-phase1-discovery/step1-topic-clustering/input",
        "03-phase1-discovery/step1-topic-clustering/code",
        "03-phase1-discovery/step1-topic-clustering/output",
        "03-phase1-discovery/step2-signal-extract/input",
        "03-phase1-discovery/step2-signal-extract/code",
        "03-phase1-discovery/step2-signal-extract/output",
        "03-phase1-discovery/step3-content-quality/input",
        "03-phase1-discovery/step3-content-quality/code",
        "03-phase1-discovery/step3-content-quality/output",
        "03-phase1-discovery/step4-high-value-identify/input",
        "03-phase1-discovery/step4-high-value-identify/code",
        "03-phase1-discovery/step4-high-value-identify/output",
        "03-phase1-discovery/step5-opportunity-mapping/input",
        "03-phase1-discovery/step5-opportunity-mapping/code",
        "03-phase1-discovery/step5-opportunity-mapping/output",
        "03-phase1-discovery/step6-search-optimize/input",
        "03-phase1-discovery/step6-search-optimize/code",
        "03-phase1-discovery/step6-search-optimize/output",
        "04-phase2-analysis/step1-user-profile/input",
        "04-phase2-analysis/step1-user-profile/code",
        "04-phase2-analysis/step1-user-profile/output",
        "04-phase2-analysis/step2-solution-analysis/input",
        "04-phase2-analysis/step2-solution-analysis/code",
        "04-phase2-analysis/step2-solution-analysis/output",
        "04-phase2-analysis/step3-pain-deep-dive/input",
        "04-phase2-analysis/step3-pain-deep-dive/code",
        "04-phase2-analysis/step3-pain-deep-dive/output",
        "04-phase2-analysis/step4-expectation-analysis/input",
        "04-phase2-analysis/step4-expectation-analysis/code",
        "04-phase2-analysis/step4-expectation-analysis/output",
        "04-phase2-analysis/step5-payment-privacy/input",
        "04-phase2-analysis/step5-payment-privacy/code",
        "04-phase2-analysis/step5-payment-privacy/output",
        "05-insights/input", "05-insights/code", "05-insights/output",
        "06-reports",
        "archive",
    ]
    
    for d in dirs:
        (project_dir / d).mkdir(parents=True, exist_ok=True)
    
    # 创建 project.json
    project_meta = {
        "project_name": project_name,
        "topic": topic,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "status": "initialized",
        "data_source": data_source,
        "current_phase": None,
        "current_step": None,
        "version_counter": 0,
        "phases": {
            "phase1": {"status": "pending", "steps_completed": 0, "total_steps": 6},
            "phase2": {"status": "pending", "steps_completed": 0, "total_steps": 5},
            "insights": {"status": "pending", "steps_completed": 0, "total_steps": 1},
            "reports": {"status": "pending", "steps_completed": 0, "total_steps": 3}
        }
    }
    
    with open(project_dir / "00-meta" / "project.json", "w", encoding="utf-8") as f:
        json.dump(project_meta, f, ensure_ascii=False, indent=2)
    
    # 复制数据文件
    if data_source and os.path.exists(data_source):
        dest = project_dir / "01-raw-data" / "input" / Path(data_source).name
        shutil.copy2(data_source, dest)
        print(f"📁 数据文件已复制: {dest}")
    
    # 创建初始 manifest
    manifest = {
        "step_id": "project-init",
        "step_name": "项目初始化",
        "version": 1,
        "timestamp": datetime.now().isoformat(),
        "status": "completed",
        "input": {"files": [data_source] if data_source else [], "checksum": None},
        "code": {"file": "scripts/init_project.py", "checksum": None},
        "output": {"files": [], "checksums": {}},
        "parameters": {"topic": topic},
        "notes": "项目目录结构创建完成"
    }
    
    with open(project_dir / "01-raw-data" / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    
    # 创建初始 workflow.html
    workflow_html = generate_initial_workflow_html(project_name, topic)
    with open(project_dir / "00-meta" / "workflow.html", "w", encoding="utf-8") as f:
        f.write(workflow_html)
    
    print(f"✅ 项目创建成功: {project_dir}")
    print(f"   主题: {topic}")
    print(f"   目录: {project_dir}")
    
    return project_dir


def generate_initial_workflow_html(project_name: str, topic: str) -> str:
    """生成初始工作流HTML"""
    
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>工作流 - {topic}</title>
    <style>
        :root {{
            --bg-primary: #0a0a0f;
            --bg-secondary: #12121a;
            --bg-card: #1a1a2e;
            --border: #2a2a3e;
            --text-primary: #e0e0e0;
            --text-secondary: #8888a0;
            --accent: #6366f1;
            --accent-glow: rgba(99, 102, 241, 0.3);
            --success: #10b981;
            --warning: #f59e0b;
            --error: #ef4444;
            --info: #3b82f6;
            --archived: #6b7280;
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Microsoft YaHei", sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
        }}
        
        .header {{
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border);
            padding: 20px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .header h1 {{
            font-size: 24px;
            font-weight: 600;
            background: linear-gradient(135deg, var(--accent), #a855f7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .header .meta {{
            color: var(--text-secondary);
            font-size: 14px;
        }}
        
        .progress-bar {{
            width: 300px;
            height: 8px;
            background: var(--bg-card);
            border-radius: 4px;
            overflow: hidden;
        }}
        
        .progress-bar .fill {{
            height: 100%;
            width: 5%;
            background: linear-gradient(90deg, var(--accent), #a855f7);
            border-radius: 4px;
            transition: width 0.5s ease;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px;
        }}
        
        .phase {{
            margin-bottom: 40px;
            background: var(--bg-secondary);
            border-radius: 16px;
            border: 1px solid var(--border);
            overflow: hidden;
        }}
        
        .phase-header {{
            padding: 20px 30px;
            background: var(--bg-card);
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .phase-header h2 {{
            font-size: 18px;
            font-weight: 600;
        }}
        
        .phase-header .status {{
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 500;
        }}
        
        .status-pending {{ background: rgba(107, 114, 128, 0.2); color: var(--archived); }}
        .status-completed {{ background: rgba(16, 185, 129, 0.2); color: var(--success); }}
        .status-active {{ background: rgba(59, 130, 246, 0.2); color: var(--info); }}
        
        .steps {{
            padding: 20px 30px;
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
        }}
        
        .step {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px 20px;
            min-width: 200px;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
        }}
        
        .step:hover {{
            border-color: var(--accent);
            box-shadow: 0 0 20px var(--accent-glow);
            transform: translateY(-2px);
        }}
        
        .step .step-icon {{
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            margin-bottom: 8px;
        }}
        
        .step-pending .step-icon {{ border: 2px solid var(--archived); color: var(--archived); }}
        .step-completed .step-icon {{ background: var(--success); color: white; }}
        .step-active .step-icon {{ background: var(--info); color: white; animation: pulse 2s infinite; }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}
        
        .step h3 {{
            font-size: 14px;
            font-weight: 500;
            margin-bottom: 4px;
        }}
        
        .step .step-meta {{
            font-size: 12px;
            color: var(--text-secondary);
        }}
        
        .detail-panel {{
            display: none;
            position: fixed;
            right: 0;
            top: 0;
            width: 500px;
            height: 100vh;
            background: var(--bg-secondary);
            border-left: 1px solid var(--border);
            padding: 30px;
            overflow-y: auto;
            z-index: 100;
            box-shadow: -10px 0 40px rgba(0,0,0,0.5);
        }}
        
        .detail-panel.active {{ display: block; }}
        
        .detail-panel h3 {{
            font-size: 20px;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--border);
        }}
        
        .detail-section {{
            margin-bottom: 24px;
        }}
        
        .detail-section h4 {{
            font-size: 14px;
            color: var(--text-secondary);
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .file-list {{
            list-style: none;
        }}
        
        .file-list li {{
            padding: 8px 12px;
            background: var(--bg-card);
            border-radius: 8px;
            margin-bottom: 6px;
            font-size: 13px;
            font-family: "JetBrains Mono", monospace;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .file-list li .file-action {{
            color: var(--accent);
            cursor: pointer;
            font-size: 12px;
        }}
        
        .close-btn {{
            position: absolute;
            top: 20px;
            right: 20px;
            background: none;
            border: none;
            color: var(--text-secondary);
            font-size: 24px;
            cursor: pointer;
        }}
        
        .overlay {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 99;
        }}
        
        .overlay.active {{ display: block; }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>📊 {topic}</h1>
            <div class="meta">项目: {project_name} | 状态: 初始化完成</div>
        </div>
        <div class="progress-bar">
            <div class="fill" style="width: 5%"></div>
        </div>
    </div>
    
    <div class="container">
        <!-- Phase 1: 场景发现 -->
        <div class="phase">
            <div class="phase-header">
                <h2>🔍 第一阶段：场景发现</h2>
                <span class="status status-pending">待执行</span>
            </div>
            <div class="steps">
                <div class="step step-pending" data-step="phase1-step1">
                    <div class="step-icon">○</div>
                    <h3>数据加载与清洗</h3>
                    <div class="step-meta">待执行</div>
                </div>
                <div class="step step-pending" data-step="phase1-step2">
                    <div class="step-icon">○</div>
                    <h3>主题聚类分析</h3>
                    <div class="step-meta">待执行</div>
                </div>
                <div class="step step-pending" data-step="phase1-step3">
                    <div class="step-icon">○</div>
                    <h3>需求信号提取</h3>
                    <div class="step-meta">待执行</div>
                </div>
                <div class="step step-pending" data-step="phase1-step4">
                    <div class="step-icon">○</div>
                    <h3>内容质量评估</h3>
                    <div class="step-meta">待执行</div>
                </div>
                <div class="step step-pending" data-step="phase1-step5">
                    <div class="step-icon">○</div>
                    <h3>高价值内容识别</h3>
                    <div class="step-meta">待执行</div>
                </div>
                <div class="step step-pending" data-step="phase1-step6">
                    <div class="step-icon">○</div>
                    <h3>搜索词优化建议</h3>
                    <div class="step-meta">待执行</div>
                </div>
            </div>
        </div>
        
        <!-- Phase 2: 现状分析 -->
        <div class="phase">
            <div class="phase-header">
                <h2>📈 第二阶段：现状分析</h2>
                <span class="status status-pending">待执行</span>
            </div>
            <div class="steps">
                <div class="step step-pending" data-step="phase2-step1">
                    <div class="step-icon">○</div>
                    <h3>用户画像提取</h3>
                    <div class="step-meta">待执行</div>
                </div>
                <div class="step step-pending" data-step="phase2-step2">
                    <div class="step-icon">○</div>
                    <h3>解决方案分析</h3>
                    <div class="step-meta">待执行</div>
                </div>
                <div class="step step-pending" data-step="phase2-step3">
                    <div class="step-icon">○</div>
                    <h3>痛点深度分析</h3>
                    <div class="step-meta">待执行</div>
                </div>
                <div class="step step-pending" data-step="phase2-step4">
                    <div class="step-icon">○</div>
                    <h3>期望功能分析</h3>
                    <div class="step-meta">待执行</div>
                </div>
                <div class="step step-pending" data-step="phase2-step5">
                    <div class="step-icon">○</div>
                    <h3>付费意愿评估</h3>
                    <div class="step-meta">待执行</div>
                </div>
            </div>
        </div>
        
        <!-- Insights -->
        <div class="phase">
            <div class="phase-header">
                <h2>💡 洞察与机会</h2>
                <span class="status status-pending">待执行</span>
            </div>
            <div class="steps">
                <div class="step step-pending" data-step="insights-step1">
                    <div class="step-icon">○</div>
                    <h3>洞察生成与机会映射</h3>
                    <div class="step-meta">待执行</div>
                </div>
            </div>
        </div>
        
        <!-- Reports -->
        <div class="phase">
            <div class="phase-header">
                <h2>📑 最终交付件</h2>
                <span class="status status-pending">待执行</span>
            </div>
            <div class="steps">
                <div class="step step-pending" data-step="report-1">
                    <div class="step-icon">○</div>
                    <h3>最终分析报告</h3>
                    <div class="step-meta">待执行</div>
                </div>
                <div class="step step-pending" data-step="report-2">
                    <div class="step-icon">○</div>
                    <h3>过程技术报告</h3>
                    <div class="step-meta">待执行</div>
                </div>
                <div class="step step-pending" data-step="report-3">
                    <div class="step-icon">○</div>
                    <h3>任务改进建议</h3>
                    <div class="step-meta">待执行</div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="overlay" onclick="closeDetail()"></div>
    <div class="detail-panel" id="detailPanel">
        <button class="close-btn" onclick="closeDetail()">×</button>
        <h3 id="detailTitle">步骤详情</h3>
        <div id="detailContent">
            <p style="color: var(--text-secondary);">点击工作流节点查看详情</p>
        </div>
    </div>
    
    <script>
        const WORKFLOW_DATA = {{
            project: {{
                name: "{project_name}",
                topic: "{topic}",
                status: "initialized"
            }},
            phases: []
        }};
        
        function showDetail(stepId) {{
            document.getElementById('detailPanel').classList.add('active');
            document.querySelector('.overlay').classList.add('active');
            document.getElementById('detailTitle').textContent = '步骤: ' + stepId;
        }}
        
        function closeDetail() {{
            document.getElementById('detailPanel').classList.remove('active');
            document.querySelector('.overlay').classList.remove('active');
        }}
        
        document.querySelectorAll('.step').forEach(step => {{
            step.addEventListener('click', () => showDetail(step.dataset.step));
        }});
    </script>
</body>
</html>'''


def main():
    parser = argparse.ArgumentParser(description="初始化AI需求调研项目")
    parser.add_argument("--topic", required=True, help="调研主题")
    parser.add_argument("--data-source", help="数据源文件路径")
    parser.add_argument("--base-dir", help="项目基础目录")
    
    args = parser.parse_args()
    
    project_dir = create_project(args.topic, args.data_source, args.base_dir)
    
    if project_dir:
        print(f"\n🚀 下一步:")
        print(f"   1. 将数据文件放入: {project_dir}/01-raw-data/input/")
        print(f"   2. 开始数据清洗: 运行分析脚本")
        print(f"   3. 查看工作流: 打开 {project_dir}/00-meta/workflow.html")


if __name__ == "__main__":
    main()
