"""
数据加载与清洗模板
兼容 Excel / JSONL / SQLite 三种数据源

用法:
    python data_loader.py --input /path/to/data.xlsx --output /path/to/output/cleaned_data.parquet
"""

import os
import sys
import json
import argparse
import sqlite3
import hashlib
from pathlib import Path

import pandas as pd


def parse_count(value):
    """处理特殊格式如'10万+'、'1.2万'、'1,234'"""
    if not value:
        return 0
    if isinstance(value, (int, float)):
        return int(value)
    value = str(value).strip().replace(',', '')
    if '万' in value:
        try:
            return int(float(value.replace('万+', '').replace('万', '')) * 10000)
        except:
            return 0
    if '+' in value:
        value = value.replace('+', '')
    try:
        return int(value)
    except:
        return 0


def load_data(input_path: str) -> pd.DataFrame:
    """根据文件扩展名自动选择加载方式"""
    
    input_path = Path(input_path)
    suffix = input_path.suffix.lower()
    
    if suffix == '.xlsx' or suffix == '.xls':
        df = pd.read_excel(input_path)
        print(f"✅ 已加载 Excel: {len(df)} 行")
        
    elif suffix == '.jsonl':
        contents = []
        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    contents.append(json.loads(line))
        df = pd.DataFrame(contents)
        print(f"✅ 已加载 JSONL: {len(df)} 行")
        
    elif suffix == '.db' or suffix == '.sqlite':
        conn = sqlite3.connect(input_path)
        # 自动检测表名
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]
        print(f"📋 数据库表: {tables}")
        
        # 优先使用 xhs_note
        table_name = 'xhs_note' if 'xhs_note' in tables else tables[0]
        df = pd.read_sql_query(f"SELECT * FROM {table_name};", conn)
        print(f"✅ 已加载 SQLite 表 '{table_name}': {len(df)} 行")
        conn.close()
        
    else:
        raise ValueError(f"不支持的文件格式: {suffix}")
    
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """数据清洗与标准化"""
    
    print("\n🔧 开始数据清洗...")
    
    # 1. 互动量转换
    count_columns = ['liked_count', 'collected_count', 'comment_count', 'share_count']
    for col in count_columns:
        if col in df.columns:
            df[f'{col}_num'] = df[col].apply(parse_count)
            print(f"   ✓ 转换 {col}")
    
    # 2. 计算总互动量
    num_cols = [c for c in df.columns if c.endswith('_count_num')]
    if num_cols:
        df['total_interaction'] = df[num_cols].sum(axis=1)
        print(f"   ✓ 计算总互动量 (基于 {len(num_cols)} 个字段)")
    
    # 3. 合并标题和描述
    if 'title' in df.columns and 'desc' in df.columns:
        df['text'] = df['title'].fillna('') + ' ' + df['desc'].fillna('')
        print("   ✓ 合并标题和描述")
    elif 'title' in df.columns:
        df['text'] = df['title'].fillna('')
    elif 'desc' in df.columns:
        df['text'] = df['desc'].fillna('')
    
    # 4. 检查搜索词分布
    if 'source_keyword' in df.columns:
        print(f"\n📊 搜索词分布:")
        print(df['source_keyword'].value_counts().head(10))
    
    # 5. 互动量统计
    if 'total_interaction' in df.columns:
        print(f"\n📈 互动量统计:")
        print(f"   平均总互动: {df['total_interaction'].mean():.0f}")
        print(f"   中位数: {df['total_interaction'].median():.0f}")
        print(f"   最大值: {df['total_interaction'].max()}")
        print(f"   最小值: {df['total_interaction'].min()}")
    
    # 6. 数据质量检查
    print(f"\n🔍 数据质量:")
    print(f"   总行数: {len(df)}")
    print(f"   空文本行数: {df['text'].isna().sum() if 'text' in df.columns else 'N/A'}")
    
    return df


def save_manifest(output_dir: str, input_path: str, df: pd.DataFrame, params: dict):
    """保存步骤清单"""
    
    manifest = {
        "step_id": "data-cleaning",
        "step_name": "数据加载与清洗",
        "version": 1,
        "timestamp": pd.Timestamp.now().isoformat(),
        "status": "completed",
        "input": {
            "files": [input_path],
            "checksum": None  # 可计算文件hash
        },
        "code": {
            "file": "02-cleaned/code/data_cleaning.py",
            "checksum": None
        },
        "output": {
            "files": ["cleaned_data.parquet", "cleaning_report.json"],
            "checksums": {}
        },
        "parameters": params,
        "statistics": {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "memory_usage_mb": df.memory_usage(deep=True).sum() / 1024 / 1024
        },
        "notes": "数据清洗完成，互动量已标准化"
    }
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    
    print(f"\n📝 清单已保存: {output_dir / 'manifest.json'}")


def main():
    parser = argparse.ArgumentParser(description="数据加载与清洗")
    parser.add_argument("--input", required=True, help="输入数据文件路径")
    parser.add_argument("--output", required=True, help="输出目录路径")
    parser.add_argument("--min-interaction", type=int, default=0, help="最小互动量过滤")
    
    args = parser.parse_args()
    
    # 加载数据
    df = load_data(args.input)
    
    # 清洗数据
    df = clean_data(df)
    
    # 过滤
    if args.min_interaction > 0 and 'total_interaction' in df.columns:
        df = df[df['total_interaction'] >= args.min_interaction]
        print(f"\n🔍 过滤后行数: {len(df)} (最小互动量 >= {args.min_interaction})")
    
    # 保存
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = output_dir / "cleaned_data.parquet"
    df.to_parquet(output_path, index=False)
    print(f"\n💾 数据已保存: {output_path}")
    
    # 保存统计报告
    report = {
        "total_rows": len(df),
        "columns": list(df.columns),
        "interaction_stats": df['total_interaction'].describe().to_dict() if 'total_interaction' in df.columns else None,
        "keyword_distribution": df['source_keyword'].value_counts().to_dict() if 'source_keyword' in df.columns else None
    }
    
    with open(output_dir / "cleaning_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # 保存清单
    save_manifest(args.output, args.input, df, {
        "min_interaction": args.min_interaction,
        "parse_count_enabled": True
    })
    
    print("\n✅ 数据清洗完成!")


if __name__ == "__main__":
    main()
