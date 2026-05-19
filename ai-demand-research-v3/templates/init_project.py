#!/usr/bin/env python3
"""
项目初始化脚本
创建一个新的调研项目目录结构

用法:
    python init_project.py --topic "手机AI功能用户诉求调研" --platforms xhs,bilibili,zhihu
"""

import os
import sys
import json
import argparse
import shutil
from datetime import datetime
from pathlib import Path


def create_project(topic: str, platforms: str = None, base_dir: str = None):
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
        "01-search-design/input", "01-search-design/code", "01-search-design/output",
        "02-raw-data/input", "02-raw-data/output",
        "03-cleaned/input", "03-cleaned/code", "03-cleaned/output",
        "04-phase1-discovery/step1-topic-clustering/input",
        "04-phase1-discovery/step1-topic-clustering/code",
        "04-phase1-discovery/step1-topic-clustering/output",
        "04-phase1-discovery/step2-signal-extract/input",
        "04-phase1-discovery/step2-signal-extract/code",
        "04-phase1-discovery/step2-signal-extract/output",
        "04-phase1-discovery/step3-content-quality/input",
        "04-phase1-discovery/step3-content-quality/code",
        "04-phase1-discovery/step3-content-quality/output",
        "04-phase1-discovery/step4-high-value-identify/input",
        "04-phase1-discovery/step4-high-value-identify/code",
        "04-phase1-discovery/step4-high-value-identify/output",
        "04-phase1-discovery/step5-opportunity-mapping/input",
        "04-phase1-discovery/step5-opportunity-mapping/code",
        "04-phase1-discovery/step5-opportunity-mapping/output",
        "04-phase1-discovery/step6-three-dimension-tagging/step6a-usage-context",
        "04-phase1-discovery/step6-three-dimension-tagging/step6b-trigger-exit",
        "04-phase1-discovery/step6-three-dimension-tagging/step6c-user-group",
        "05-phase2-analysis/step1-user-profile/input",
        "05-phase2-analysis/step1-user-profile/code",
        "05-phase2-analysis/step1-user-profile/output",
        "05-phase2-analysis/step2-solution-analysis/input",
        "05-phase2-analysis/step2-solution-analysis/code",
        "05-phase2-analysis/step2-solution-analysis/output",
        "05-phase2-analysis/step3-pain-deep-dive/input",
        "05-phase2-analysis/step3-pain-deep-dive/code",
        "05-phase2-analysis/step3-pain-deep-dive/output",
        "05-phase2-analysis/step4-expectation-analysis/input",
        "05-phase2-analysis/step4-expectation-analysis/code",
        "05-phase2-analysis/step4-expectation-analysis/output",
        "05-phase2-analysis/step5-payment-privacy/input",
        "05-phase2-analysis/step5-payment-privacy/code",
        "05-phase2-analysis/step5-payment-privacy/output",
        "06-insights/input", "06-insights/code", "06-insights/output",
        "07-search-optimize/input", "07-search-optimize/code", "07-search-optimize/output",
        "08-reports",
        "archive",
    ]
    
    for d in dirs:
        (project_dir / d).mkdir(parents=True, exist_ok=True)
    
    # 创建 project.json
    project_meta = {
        "project_name": project_name,
        "topic": topic,
        "platforms": platforms.split(",") if platforms else ["xhs"],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "status": "initialized",
        "current_phase": None,
        "current_step": None,
        "version_counter": 0,
        "phases": {
            "preparation": {"status": "pending", "steps_completed": 0, "total_steps": 4},
            "phase1": {"status": "pending", "steps_completed": 0, "total_steps": 6},
            "phase2": {"status": "pending", "steps_completed": 0, "total_steps": 5},
            "insights": {"status": "pending", "steps_completed": 0, "total_steps": 1},
            "optimize": {"status": "pending", "steps_completed": 0, "total_steps": 1},
            "reports": {"status": "pending", "steps_completed": 0, "total_steps": 3}
        }
    }
    
    with open(project_dir / "00-meta" / "project.json", "w", encoding="utf-8") as f:
        json.dump(project_meta, f, ensure_ascii=False, indent=2)
    
    # 复制工作流定义HTML
    workflow_template = Path(__file__).parent / "workflow_definition.html"
    if workflow_template.exists():
        shutil.copy2(workflow_template, project_dir / "00-meta" / "workflow-definition.html")
    
    # 创建搜索词模板
    search_template = f"""# 搜索词设计模板

## 调研主题
{topic}

## 目标平台
{platforms or 'xhs'}

## 第一阶段：泛化发现搜索词

### 场景1：___
| 搜索词 | 类型 | 优先级 |
|--------|------|--------|
| | | |

### 场景2：___
| 搜索词 | 类型 | 优先级 |
|--------|------|--------|
| | | |

## 第二阶段：聚焦验证搜索词

### P0机会1：___
| 维度 | 搜索词 |
|------|--------|
| 工具使用 | |
| 痛点暴露 | |
| 行为描述 | |
| 期望表达 | |

## 检查清单
- [ ] 覆盖完整链路（做什么→遇到什么→情绪如何→怎么办）
- [ ] 无同质化词
- [ ] 去掉偏期望而非现状的词
- [ ] 每个场景5-10个词
"""
    
    with open(project_dir / "01-search-design" / "search-keywords-template.md", "w", encoding="utf-8") as f:
        f.write(search_template)
    
    # 创建初始 manifest
    manifest = {
        "step_id": "project-init",
        "step_name": "项目初始化",
        "version": 1,
        "timestamp": datetime.now().isoformat(),
        "status": "completed",
        "input": {"files": [], "checksum": None},
        "code": {"file": "templates/init_project.py", "checksum": None},
        "output": {"files": ["00-meta/project.json", "00-meta/workflow-definition.html", "01-search-design/search-keywords-template.md"], "checksums": {}},
        "parameters": {"topic": topic, "platforms": platforms},
        "notes": "项目目录结构创建完成"
    }
    
    with open(project_dir / "00-meta" / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 项目创建成功: {project_dir}")
    print(f"   主题: {topic}")
    print(f"   平台: {platforms or 'xhs'}")
    print(f"   目录: {project_dir}")
    
    return project_dir


def main():
    parser = argparse.ArgumentParser(description="初始化AI需求调研项目")
    parser.add_argument("--topic", required=True, help="调研主题")
    parser.add_argument("--platforms", default="xhs", help="目标平台，逗号分隔")
    parser.add_argument("--base-dir", help="项目基础目录")
    
    args = parser.parse_args()
    
    project_dir = create_project(args.topic, args.platforms, args.base_dir)
    
    if project_dir:
        print(f"\n🚀 下一步:")
        print(f"   1. 编辑搜索词: {project_dir}/01-search-design/search-keywords-template.md")
        print(f"   2. 查看工作流: 打开 {project_dir}/00-meta/workflow-definition.html")
        print(f"   3. 开始数据采集")


if __name__ == "__main__":
    main()
