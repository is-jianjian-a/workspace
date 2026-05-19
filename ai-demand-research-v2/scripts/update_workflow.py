#!/usr/bin/env python3
"""
工作流HTML更新脚本
扫描项目目录，收集所有manifest.json，生成最新的workflow.html

用法:
    python update_workflow.py --project-dir /path/to/project
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path


def scan_project(project_dir: str):
    """扫描项目目录，收集所有步骤状态"""
    
    project_dir = Path(project_dir)
    
    # 读取 project.json
    project_json_path = project_dir / "00-meta" / "project.json"
    with open(project_json_path, "r", encoding="utf-8") as f:
        project_meta = json.load(f)
    
    phases = []
    
    # Phase 1: 场景发现
    phase1_steps = []
    phase1_dir = project_dir / "03-phase1-discovery"
    if phase1_dir.exists():
        step_dirs = sorted(phase1_dir.iterdir())
        for step_dir in step_dirs:
            if step_dir.is_dir():
                manifest_path = step_dir / "manifest.json"
                if manifest_path.exists():
                    with open(manifest_path, "r", encoding="utf-8") as f:
                        manifest = json.load(f)
                    phase1_steps.append(manifest)
    
    # 如果没有步骤完成，检查数据清洗步骤
    if not phase1_steps:
        cleaned_manifest = project_dir / "02-cleaned" / "manifest.json"
        if cleaned_manifest.exists():
            with open(cleaned_manifest, "r", encoding="utf-8") as f:
                manifest = json.load(f)
            phase1_steps.append(manifest)
    
    phases.append({
        "id": "phase1",
        "name": "场景发现",
        "status": "completed" if len(phase1_steps) >= 6 else ("active" if phase1_steps else "pending"),
        "steps": phase1_steps
    })
    
    # Phase 2: 现状分析
    phase2_steps = []
    phase2_dir = project_dir / "04-phase2-analysis"
    if phase2_dir.exists():
        step_dirs = sorted(phase2_dir.iterdir())
        for step_dir in step_dirs:
            if step_dir.is_dir():
                manifest_path = step_dir / "manifest.json"
                if manifest_path.exists():
                    with open(manifest_path, "r", encoding="utf-8") as f:
                        manifest = json.load(f)
                    phase2_steps.append(manifest)
    
    phases.append({
        "id": "phase2",
        "name": "现状分析",
        "status": "completed" if len(phase2_steps) >= 5 else ("active" if phase2_steps else "pending"),
        "steps": phase2_steps
    })
    
    # Insights
    insights_steps = []
    insights_manifest = project_dir / "05-insights" / "manifest.json"
    if insights_manifest.exists():
        with open(insights_manifest, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        insights_steps.append(manifest)
    
    phases.append({
        "id": "insights",
        "name": "洞察与机会",
        "status": "completed" if insights_steps else "pending",
        "steps": insights_steps
    })
    
    # Reports
    report_steps = []
    reports_dir = project_dir / "06-reports"
    if reports_dir.exists():
        report_files = list(reports_dir.glob("*.html"))
        for report_file in report_files:
            report_steps.append({
                "step_id": f"report-{report_file.stem}",
                "step_name": report_file.stem.replace("-", " ").title(),
                "status": "completed",
                "timestamp": datetime.fromtimestamp(report_file.stat().st_mtime).isoformat(),
                "output": {"files": [str(report_file.relative_to(project_dir))]}
            })
    
    phases.append({
        "id": "reports",
        "name": "最终交付件",
        "status": "completed" if len(report_steps) >= 3 else ("active" if report_steps else "pending"),
        "steps": report_steps
    })
    
    return project_meta, phases


def generate_workflow_html(project_meta: dict, phases: list) -> str:
    """生成工作流HTML"""
    
    # 计算进度
    total_steps = sum(len(p["steps"]) for p in phases)
    completed_steps = sum(len([s for s in p["steps"] if s.get("status") == "completed"]) for p in phases)
    progress = int((completed_steps / max(total_steps, 1)) * 100)
    
    # 生成阶段HTML
    phases_html = []
    phase_icons = {"phase1": "🔍", "phase2": "📈", "insights": "💡", "reports": "📑"}
    
    for phase in phases:
        status_class = f"status-{phase['status']}"
        status_text = {"pending": "待执行", "active": "执行中", "completed": "已完成"}.get(phase['status'], phase['status'])
        
        steps_html = []
        for step in phase["steps"]:
            step_status = step.get("status", "pending")
            step_version = step.get("version", 1)
            
            if step_status == "completed":
                icon = "✓"
                step_class = "step-completed"
            elif step_status == "active":
                icon = "⟳"
                step_class = "step-active"
            else:
                icon = "○"
                step_class = "step-pending"
            
            # 重新生成标记
            version_badge = f'<span style="color: var(--warning); font-size: 11px;">v{step_version}</span>' if step_version > 1 else ''
            
            output_files = step.get("output", {}).get("files", [])
            output_summary = f"{len(output_files)} 个输出文件" if output_files else "无输出"
            
            steps_html.append(f'''
                <div class="step {step_class}" data-step="{step.get('step_id', '')}" onclick="showDetail('{step.get('step_id', '')}')">
                    <div class="step-icon">{icon}</div>
                    <h3>{step.get('step_name', '未命名步骤')}</h3>
                    <div class="step-meta">{output_summary} {version_badge}</div>
                </div>
            ''')
        
        # 如果没有步骤，显示占位
        if not steps_html:
            steps_html = ['<div style="color: var(--text-secondary); padding: 20px;">暂无步骤数据</div>']
        
        phases_html.append(f'''
            <div class="phase">
                <div class="phase-header">
                    <h2>{phase_icons.get(phase['id'], '📋')} {phase['name']}</h2>
                    <span class="status {status_class}">{status_text}</span>
                </div>
                <div class="steps">
                    {''.join(steps_html)}
                </div>
            </div>
        ''')
    
    # 生成完整HTML
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>工作流 - {project_meta.get('topic', '未命名项目')}</title>
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
            position: sticky;
            top: 0;
            z-index: 50;
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
            margin-top: 4px;
        }}
        
        .progress-section {{
            display: flex;
            align-items: center;
            gap: 16px;
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
            width: {progress}%;
            background: linear-gradient(90deg, var(--accent), #a855f7);
            border-radius: 4px;
            transition: width 0.5s ease;
            box-shadow: 0 0 10px var(--accent-glow);
        }}
        
        .progress-text {{
            font-size: 14px;
            color: var(--text-secondary);
            font-weight: 500;
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
            transition: all 0.3s ease;
        }}
        
        .phase:hover {{
            border-color: var(--border);
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
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
        .status-active {{ background: rgba(59, 130, 246, 0.2); color: var(--info); }}
        .status-completed {{ background: rgba(16, 185, 129, 0.2); color: var(--success); }}
        
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
            font-weight: bold;
        }}
        
        .step-pending .step-icon {{ border: 2px solid var(--archived); color: var(--archived); }}
        .step-completed .step-icon {{ background: var(--success); color: white; }}
        .step-active .step-icon {{ background: var(--info); color: white; animation: pulse 2s infinite; }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; transform: scale(1); }}
            50% {{ opacity: 0.7; transform: scale(1.05); }}
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
        
        .detail-panel.active {{ display: block; animation: slideIn 0.3s ease; }}
        
        @keyframes slideIn {{
            from {{ transform: translateX(100%); }}
            to {{ transform: translateX(0); }}
        }}
        
        .detail-panel h3 {{
            font-size: 20px;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--border);
            padding-right: 40px;
        }}
        
        .detail-section {{
            margin-bottom: 24px;
        }}
        
        .detail-section h4 {{
            font-size: 12px;
            color: var(--text-secondary);
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }}
        
        .file-list {{
            list-style: none;
        }}
        
        .file-list li {{
            padding: 10px 12px;
            background: var(--bg-card);
            border-radius: 8px;
            margin-bottom: 6px;
            font-size: 13px;
            font-family: "JetBrains Mono", "Fira Code", monospace;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border: 1px solid transparent;
            transition: all 0.2s ease;
        }}
        
        .file-list li:hover {{
            border-color: var(--accent);
        }}
        
        .file-list li .file-action {{
            color: var(--accent);
            cursor: pointer;
            font-size: 12px;
            font-weight: 500;
        }}
        
        .close-btn {{
            position: absolute;
            top: 20px;
            right: 20px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            color: var(--text-secondary);
            font-size: 24px;
            cursor: pointer;
            width: 36px;
            height: 36px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
        }}
        
        .close-btn:hover {{
            background: var(--error);
            color: white;
            border-color: var(--error);
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
        
        .param-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}
        
        .param-table th, .param-table td {{
            padding: 8px 12px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}
        
        .param-table th {{
            color: var(--text-secondary);
            font-weight: 500;
            font-size: 12px;
            text-transform: uppercase;
        }}
        
        .code-preview {{
            background: #0d0d15;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 16px;
            font-family: "JetBrains Mono", "Fira Code", monospace;
            font-size: 12px;
            overflow-x: auto;
            max-height: 300px;
            overflow-y: auto;
        }}
        
        .timestamp {{
            color: var(--text-secondary);
            font-size: 12px;
            margin-top: 4px;
        }}
        
        .version-badge {{
            display: inline-block;
            padding: 2px 8px;
            background: rgba(245, 158, 11, 0.2);
            color: var(--warning);
            border-radius: 4px;
            font-size: 11px;
            font-weight: 500;
            margin-left: 8px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>📊 {project_meta.get('topic', '未命名项目')}</h1>
            <div class="meta">项目: {project_meta.get('project_name', '')} | 更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
        </div>
        <div class="progress-section">
            <div class="progress-bar">
                <div class="fill" style="width: {progress}%"></div>
            </div>
            <div class="progress-text">{progress}%</div>
        </div>
    </div>
    
    <div class="container">
        {''.join(phases_html)}
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
        const WORKFLOW_DATA = {json.dumps(phases, ensure_ascii=False, indent=2)};
        
        function showDetail(stepId) {{
            document.getElementById('detailPanel').classList.add('active');
            document.querySelector('.overlay').classList.add('active');
            
            // 查找步骤数据
            let stepData = null;
            for (const phase of WORKFLOW_DATA) {{
                for (const step of phase.steps) {{
                    if (step.step_id === stepId) {{
                        stepData = step;
                        break;
                    }}
                }}
                if (stepData) break;
            }}
            
            if (stepData) {{
                const versionBadge = stepData.version > 1 ? `<span class="version-badge">v${{stepData.version}}</span>` : '';
                document.getElementById('detailTitle').innerHTML = `${{stepData.step_name}}${{versionBadge}}`;
                
                let content = '';
                
                // 状态
                content += `<div class="detail-section">`;
                content += `<h4>状态</h4>`;
                content += `<div style="color: ${{stepData.status === 'completed' ? 'var(--success)' : 'var(--info)'}}; font-weight: 500;">${{stepData.status === 'completed' ? '✓ 已完成' : '⟳ 执行中'}}</div>`;
                if (stepData.timestamp) {{
                    content += `<div class="timestamp">完成时间: ${{stepData.timestamp}}</div>`;
                }}
                content += `</div>`;
                
                // 输入文件
                if (stepData.input && stepData.input.files) {{
                    content += `<div class="detail-section">`;
                    content += `<h4>输入文件</h4>`;
                    content += `<ul class="file-list">`;
                    for (const file of stepData.input.files) {{
                        content += `<li><span>${{file}}</span><span class="file-action">查看</span></li>`;
                    }}
                    content += `</ul></div>`;
                }}
                
                // 代码
                if (stepData.code && stepData.code.file) {{
                    content += `<div class="detail-section">`;
                    content += `<h4>处理代码</h4>`;
                    content += `<ul class="file-list">`;
                    content += `<li><span>${{stepData.code.file}}</span><span class="file-action">查看</span></li>`;
                    content += `</ul></div>`;
                }}
                
                // 输出文件
                if (stepData.output && stepData.output.files) {{
                    content += `<div class="detail-section">`;
                    content += `<h4>输出文件</h4>`;
                    content += `<ul class="file-list">`;
                    for (const file of stepData.output.files) {{
                        content += `<li><span>${{file}}</span><span class="file-action">查看</span></li>`;
                    }}
                    content += `</ul></div>`;
                }}
                
                // 参数
                if (stepData.parameters && Object.keys(stepData.parameters).length > 0) {{
                    content += `<div class="detail-section">`;
                    content += `<h4>参数</h4>`;
                    content += `<table class="param-table">`;
                    content += `<tr><th>参数</th><th>值</th></tr>`;
                    for (const [key, value] of Object.entries(stepData.parameters)) {{
                        content += `<tr><td>${{key}}</td><td>${{value}}</td></tr>`;
                    }}
                    content += `</table></div>`;
                }}
                
                // 备注
                if (stepData.notes) {{
                    content += `<div class="detail-section">`;
                    content += `<h4>备注</h4>`;
                    content += `<p style="color: var(--text-secondary); font-size: 13px;">${{stepData.notes}}</p>`;
                    content += `</div>`;
                }}
                
                document.getElementById('detailContent').innerHTML = content;
            }}
        }}
        
        function closeDetail() {{
            document.getElementById('detailPanel').classList.remove('active');
            document.querySelector('.overlay').classList.remove('active');
        }}
        
        // 键盘快捷键
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') closeDetail();
        }});
    </script>
</body>
</html>'''
    
    return html


def main():
    parser = argparse.ArgumentParser(description="更新工作流HTML")
    parser.add_argument("--project-dir", required=True, help="项目目录路径")
    
    args = parser.parse_args()
    
    project_meta, phases = scan_project(args.project_dir)
    html = generate_workflow_html(project_meta, phases)
    
    workflow_path = Path(args.project_dir) / "00-meta" / "workflow.html"
    with open(workflow_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    # 更新 project.json
    project_json_path = Path(args.project_dir) / "00-meta" / "project.json"
    project_meta["updated_at"] = datetime.now().isoformat()
    with open(project_json_path, "w", encoding="utf-8") as f:
        json.dump(project_meta, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 工作流已更新: {workflow_path}")


if __name__ == "__main__":
    main()
