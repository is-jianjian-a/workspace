"""
分析流水线模板
包含主题聚类、信号提取、内容质量评估、高价值识别

用法:
    python analysis_pipeline.py --input /path/to/cleaned_data.parquet --output-dir /path/to/phase1-output
"""

import json
import argparse
from pathlib import Path
from collections import Counter, defaultdict

import pandas as pd


# ============ 配置 ============

TOPICS = {
    '备孕怀孕': ['备孕', '怀孕', '产检', '孕吐', '胎动', '预产期', '待产包', '顺产', '剖腹产', ' maternity'],
    '喂养辅食': ['喂奶', '母乳', '奶粉', '辅食', '挑食', '过敏', '营养', '奶量', '断奶', '追奶'],
    '睡眠作息': ['睡觉', '夜醒', '哄睡', '入睡', '睡眠', '作息', '夜奶', '自主入睡', '落地醒', '睡整觉'],
    '健康疾病': ['发烧', '感冒', '咳嗽', '湿疹', '过敏', '疫苗', '生病', '医院', '医生', '就医'],
    '发育成长': ['发育', '生长', '身高', '体重', '大运动', '语言', '认知', '早教', ' milestones'],
    '情绪心理': ['焦虑', '抑郁', '情绪', '脾气', '哭闹', '安全感', '分离焦虑', '产后抑郁'],
    '教育引导': ['教育', '早教', '启蒙', '绘本', '玩具', '专注力', '规则', '管教', '学习'],
    '日常护理': ['洗澡', '穿衣', '换尿布', '护肤', '防晒', '刷牙', '护理', '清洁'],
    '母婴用品': ['纸尿裤', '奶瓶', '推车', '安全座椅', '衣服', '玩具', '用品', '待产包'],
    '妈妈恢复': ['产后', '恢复', '减肥', '妊娠纹', '盆底肌', '腹直肌', '月子', '身材'],
}

SIGNALS = {
    '痛点信号': ['难', '痛苦', '崩溃', '焦虑', '担心', '害怕', '慌', '烦', '累', '困', '无助', '绝望', '后悔', '自责', '内疚', '受不了', '撑不住'],
    '决策信号': ['怎么选', '哪个好', '推荐', '对比', '测评', '攻略', '清单', '必买', '种草', '值得买'],
    '求助信号': ['怎么办', '正常吗', '求助', '请教', '有经验', '过来人', '建议', '指点', '求助帖'],
    '行为信号': ['每天', '经常', '总是', '习惯', '规律', '记录', '打卡', '坚持', '养成'],
    '期望信号': ['希望', '想要', '期待', '如果能', '要是', '最好', '理想', '完美', '解决'],
}

MARKETING_SIGNALS = ['好物', '推荐', '测评', '必买', '清单', '品牌', '链接', '优惠', '团购', '种草', '带货', '广告', '推广', ' sponsored']
UGC_SIGNALS = ['求助', '怎么办', '正常吗', '崩溃', '焦虑', '后悔', '吐槽', '日记', '记录', '日常', '我的', '我家', '真实', '亲身经历']

PAIN_CATEGORIES = {
    '操作繁琐': ['麻烦', '复杂', '繁琐', '费劲', '累', '没时间', '忙不过来', '手忙脚乱'],
    '信息过载': ['信息', '太多', '杂乱', '分散', '不知道看哪个', '看不过来', '眼花缭乱'],
    '知识焦虑': ['焦虑', '担心', '害怕', '慌', '不确定', '不知道', '迷茫', '没底'],
    '选择困难': ['纠结', '选哪个', '怎么选', '对比', '哪个好', '拿不定主意', '犹豫不决'],
    '质量参差': ['不靠谱', '不科学', '错误', '误区', '坑', '踩雷', '被骗', '智商税'],
    '缺乏系统': ['零散', '碎片化', '不系统', '不成体系', '东拼西凑', '缺乏整体'],
    '实操困难': ['理论', '实操', '实践', '落地', '执行', '坚持', '做不到', '知易行难'],
}


# ============ 核心函数 ============

def match_topic(text: str, topics: dict = TOPICS) -> str:
    """匹配主题"""
    text = str(text)
    for topic, keywords in topics.items():
        for kw in keywords:
            if kw in text:
                return topic
    return '其他'


def extract_signals(text: str, signals: dict = SIGNALS) -> dict:
    """提取信号"""
    text = str(text)
    result = {}
    for signal_type, keywords in signals.items():
        count = sum(text.count(kw) for kw in keywords)
        result[signal_type] = count
    return result


def classify_content(text: str) -> str:
    """内容分类：UGC vs 营销"""
    text = str(text)
    has_marketing = any(s in text for s in MARKETING_SIGNALS)
    has_ugc = any(s in text for s in UGC_SIGNALS)
    
    if has_marketing and not has_ugc:
        return '纯营销'
    elif has_ugc and not has_marketing:
        return '纯UGC'
    elif has_marketing and has_ugc:
        return '混合'
    else:
        return '中性'


def identify_high_value(df: pd.DataFrame, min_interaction: int = 5000) -> pd.DataFrame:
    """识别高价值内容"""
    # 包含痛点或期望信号
    has_pain = df['text'].str.contains('|'.join(SIGNALS['痛点信号'][:10]))
    has_expect = df['text'].str.contains('|'.join(SIGNALS['期望信号'][:5]))
    
    high_value = df[
        (df['total_interaction'] >= min_interaction) &
        (has_pain | has_expect) &
        (df['content_type'] == '纯UGC')
    ].sort_values('total_interaction', ascending=False)
    
    return high_value


def analyze_topics(df: pd.DataFrame) -> dict:
    """主题聚类分析"""
    print("\n🔍 主题聚类分析...")
    
    df['topic'] = df['text'].apply(match_topic)
    topic_dist = df['topic'].value_counts().to_dict()
    
    # 主题互动量分析
    topic_interaction = df.groupby('topic')['total_interaction'].agg(['sum', 'mean', 'count']).to_dict()
    
    print(f"   识别主题: {len(topic_dist)} 个")
    for topic, count in sorted(topic_dist.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"   - {topic}: {count} 条")
    
    return {
        'distribution': topic_dist,
        'interaction_stats': topic_interaction
    }


def analyze_signals(df: pd.DataFrame) -> dict:
    """需求信号提取"""
    print("\n📡 需求信号提取...")
    
    signal_results = df['text'].apply(extract_signals)
    signal_df = pd.DataFrame(signal_results.tolist())
    
    signal_stats = {}
    for col in signal_df.columns:
        signal_stats[col] = {
            'total_count': int(signal_df[col].sum()),
            'content_count': int((signal_df[col] > 0).sum()),
            'avg_per_content': float(signal_df[col].mean())
        }
    
    print(f"   信号统计:")
    for signal, stats in sorted(signal_stats.items(), key=lambda x: x[1]['total_count'], reverse=True):
        print(f"   - {signal}: {stats['content_count']} 条内容, {stats['total_count']} 次出现")
    
    return signal_stats


def analyze_content_quality(df: pd.DataFrame) -> dict:
    """内容质量评估"""
    print("\n✨ 内容质量评估...")
    
    df['content_type'] = df['text'].apply(classify_content)
    type_dist = df['content_type'].value_counts().to_dict()
    
    # 各类型平均互动量
    type_interaction = df.groupby('content_type')['total_interaction'].mean().to_dict()
    
    print(f"   内容分布:")
    for ctype, count in type_dist.items():
        avg_inter = type_interaction.get(ctype, 0)
        print(f"   - {ctype}: {count} 条 (平均互动: {avg_inter:.0f})")
    
    return {
        'type_distribution': type_dist,
        'type_interaction': {k: float(v) for k, v in type_interaction.items()}
    }


def analyze_high_value(df: pd.DataFrame, top_n: int = 50) -> dict:
    """高价值内容识别"""
    print("\n💎 高价值内容识别...")
    
    high_value = identify_high_value(df)
    
    print(f"   高价值内容: {len(high_value)} 条")
    print(f"   平均互动量: {high_value['total_interaction'].mean():.0f}" if len(high_value) > 0 else "   无高价值内容")
    
    # 提取典型案例
    top_cases = []
    for _, row in high_value.head(top_n).iterrows():
        top_cases.append({
            'title': str(row.get('title', ''))[:100],
            'topic': row.get('topic', ''),
            'total_interaction': int(row.get('total_interaction', 0)),
            'content_type': row.get('content_type', ''),
            'text_preview': str(row.get('text', ''))[:200]
        })
    
    return {
        'count': len(high_value),
        'avg_interaction': float(high_value['total_interaction'].mean()) if len(high_value) > 0 else 0,
        'top_cases': top_cases
    }


def generate_opportunities(topic_stats: dict, signal_stats: dict, quality_stats: dict, high_value_stats: dict) -> list:
    """生成产品机会建议"""
    print("\n🎯 产品机会映射...")
    
    opportunities = []
    
    # 基于主题热度
    topic_dist = topic_stats.get('distribution', {})
    for topic, count in sorted(topic_dist.items(), key=lambda x: x[1], reverse=True)[:5]:
        if topic == '其他':
            continue
        
        opp = {
            'topic': topic,
            'content_count': count,
            'pain_signals': signal_stats.get('痛点信号', {}).get('content_count', 0),
            'expectation_signals': signal_stats.get('期望信号', {}).get('content_count', 0),
            'priority': 'P0' if count > 1000 else 'P1' if count > 500 else 'P2'
        }
        opportunities.append(opp)
    
    print(f"   识别机会: {len(opportunities)} 个")
    for opp in opportunities[:3]:
        print(f"   - [{opp['priority']}] {opp['topic']}: {opp['content_count']} 条内容")
    
    return opportunities


def save_step_manifest(output_dir: Path, step_id: str, step_name: str, output_files: list, params: dict, notes: str = ""):
    """保存步骤清单"""
    manifest = {
        "step_id": step_id,
        "step_name": step_name,
        "version": 1,
        "timestamp": pd.Timestamp.now().isoformat(),
        "status": "completed",
        "input": {"files": [], "checksum": None},
        "code": {"file": f"code/{step_id}.py", "checksum": None},
        "output": {"files": output_files, "checksums": {}},
        "parameters": params,
        "notes": notes
    }
    
    with open(output_dir / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="分析流水线")
    parser.add_argument("--input", required=True, help="清洗后的数据文件")
    parser.add_argument("--output-dir", required=True, help="输出目录")
    parser.add_argument("--min-interaction", type=int, default=5000, help="高价值内容最小互动量")
    
    args = parser.parse_args()
    
    # 加载数据
    print(f"📂 加载数据: {args.input}")
    df = pd.read_parquet(args.input)
    print(f"   共 {len(df)} 行")
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Step 1: 主题聚类
    topic_stats = analyze_topics(df)
    with open(output_dir / "topic_stats.json", "w", encoding="utf-8") as f:
        json.dump(topic_stats, f, ensure_ascii=False, indent=2)
    
    # Step 2: 信号提取
    signal_stats = analyze_signals(df)
    with open(output_dir / "signal_stats.json", "w", encoding="utf-8") as f:
        json.dump(signal_stats, f, ensure_ascii=False, indent=2)
    
    # Step 3: 内容质量
    quality_stats = analyze_content_quality(df)
    with open(output_dir / "quality_stats.json", "w", encoding="utf-8") as f:
        json.dump(quality_stats, f, ensure_ascii=False, indent=2)
    
    # Step 4: 高价值内容
    high_value_stats = analyze_high_value(df, args.min_interaction)
    with open(output_dir / "high_value_stats.json", "w", encoding="utf-8") as f:
        json.dump(high_value_stats, f, ensure_ascii=False, indent=2)
    
    # Step 5: 机会映射
    opportunities = generate_opportunities(topic_stats, signal_stats, quality_stats, high_value_stats)
    with open(output_dir / "opportunities.json", "w", encoding="utf-8") as f:
        json.dump(opportunities, f, ensure_ascii=False, indent=2)
    
    # 保存增强后的数据
    df.to_parquet(output_dir / "analyzed_data.parquet", index=False)
    
    # 保存清单
    save_step_manifest(
        output_dir,
        "phase1-analysis",
        "场景发现分析",
        ["topic_stats.json", "signal_stats.json", "quality_stats.json", "high_value_stats.json", "opportunities.json", "analyzed_data.parquet"],
        {"min_interaction": args.min_interaction, "topics": list(TOPICS.keys()), "signals": list(SIGNALS.keys())},
        "第一阶段分析完成"
    )
    
    print("\n✅ 分析流水线完成!")
    print(f"   输出目录: {output_dir}")


if __name__ == "__main__":
    main()
