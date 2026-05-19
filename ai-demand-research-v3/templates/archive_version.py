#!/usr/bin/env python3
"""
版本归档脚本
当需要回滚重新生成时，将当前版本归档

用法:
    python archive_version.py --project-dir /path/to/project --step phase1-step3
    python archive_version.py --project-dir /path/to/project --full
"""

import os
import sys
import json
import shutil
import argparse
from datetime import datetime
from pathlib import Path


def archive_step(project_dir: str, step_id: str, reason: str = None):
    """归档单个步骤"""
    
    project_dir = Path(project_dir)
    
    # 读取 project.json
    project_json_path = project_dir / "00-meta" / "project.json"
    with open(project_json_path, "r", encoding="utf-8") as f:
        project_meta = json.load(f)
    
    # 递增版本号
    project_meta["version_counter"] += 1
    version = project_meta["version_counter"]
    
    # 确定步骤路径
    step_mapping = {
        # Preparation
        "step0-1": "00-meta",
        "step0-2": "01-search-design",
        "step0-3": "02-raw-data",
        "step0-4": "03-cleaned",
        # Phase 1
        "step1-1": "04-phase1-discovery/step1-topic-clustering",
        "step1-2": "04-phase1-discovery/step2-signal-extract",
        "step1-3": "04-phase1-discovery/step3-content-quality",
        "step1-4": "04-phase1-discovery/step4-high-value-identify",
        "step1-5": "04-phase1-discovery/step5-opportunity-mapping",
        "step1-6": "04-phase1-discovery/step6-three-dimension-tagging",
        # Phase 2
        "step2-1": "05-phase2-analysis/step1-user-profile",
        "step2-2": "05-phase2-analysis/step2-solution-analysis",
        "step2-3": "05-phase2-analysis/step3-pain-deep-dive",
        "step2-4": "05-phase2-analysis/step4-expectation-analysis",
        "step2-5": "05-phase2-analysis/step5-payment-privacy",
        # Insights & Optimize & Reports
        "step3-1": "06-insights",
        "step3-2": "07-search-optimize",
        "step3-3": "08-reports",
    }
    
    step_path = project_dir / step_mapping.get(step_id, step_id)
    
    if not step_path.exists():
        print(f"❌ 步骤不存在: {step_path}")
        return False
    
    # 创建归档目录
    archive_dir = project_dir / "archive" / f"v{version}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    archive_step_dir = archive_dir / step_mapping.get(step_id, step_id)
    archive_step_dir.mkdir(parents=True, exist_ok=True)
    
    # 复制当前步骤到归档
    for item in step_path.iterdir():
        if item.is_dir():
            shutil.copytree(item, archive_step_dir / item.name, dirs_exist_ok=True)
        else:
            shutil.copy2(item, archive_step_dir / item.name)
    
    # 创建归档记录
    archive_record = {
        "version": version,
        "step_id": step_id,
        "archived_at": datetime.now().isoformat(),
        "reason": reason or "用户要求重新生成",
        "original_path": str(step_path.relative_to(project_dir)),
        "archive_path": str(archive_step_dir.relative_to(project_dir))
    }
    
    with open(archive_dir / "archive_record.json", "w", encoding="utf-8") as f:
        json.dump(archive_record, f, ensure_ascii=False, indent=2)
    
    # 更新 project.json
    project_meta["updated_at"] = datetime.now().isoformat()
    with open(project_json_path, "w", encoding="utf-8") as f:
        json.dump(project_meta, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已归档 v{version}: {step_id}")
    print(f"   归档路径: {archive_dir}")
    
    return True


def archive_project(project_dir: str, reason: str = None):
    """归档整个项目"""
    
    project_dir = Path(project_dir)
    
    # 读取 project.json
    project_json_path = project_dir / "00-meta" / "project.json"
    with open(project_json_path, "r", encoding="utf-8") as f:
        project_meta = json.load(f)
    
    version = project_meta.get("version_counter", 0) + 1
    
    # 创建归档目录
    archive_dir = project_dir / "archive" / f"v{version}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    # 归档所有步骤
    step_dirs = [
        "01-search-design",
        "02-raw-data",
        "03-cleaned",
        "04-phase1-discovery",
        "05-phase2-analysis",
        "06-insights",
        "07-search-optimize",
        "08-reports"
    ]
    
    for step_dir in step_dirs:
        src = project_dir / step_dir
        if src.exists():
            dst = archive_dir / step_dir
            shutil.copytree(src, dst, dirs_exist_ok=True)
    
    # 创建归档记录
    archive_record = {
        "version": version,
        "archived_at": datetime.now().isoformat(),
        "reason": reason or "完整项目重新生成",
        "archived_dirs": step_dirs
    }
    
    with open(archive_dir / "archive_record.json", "w", encoding="utf-8") as f:
        json.dump(archive_record, f, ensure_ascii=False, indent=2)
    
    # 更新版本号
    project_meta["version_counter"] = version
    project_meta["updated_at"] = datetime.now().isoformat()
    with open(project_json_path, "w", encoding="utf-8") as f:
        json.dump(project_meta, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已完整归档 v{version}")
    print(f"   归档路径: {archive_dir}")
    
    return True


def main():
    parser = argparse.ArgumentParser(description="归档项目版本")
    parser.add_argument("--project-dir", required=True, help="项目目录路径")
    parser.add_argument("--step", help="要归档的特定步骤ID")
    parser.add_argument("--full", action="store_true", help="归档整个项目")
    parser.add_argument("--reason", help="归档原因")
    
    args = parser.parse_args()
    
    if args.full:
        archive_project(args.project_dir, args.reason)
    elif args.step:
        archive_step(args.project_dir, args.step, args.reason)
    else:
        print("请指定 --step 或 --full")
        sys.exit(1)


if __name__ == "__main__":
    main()
