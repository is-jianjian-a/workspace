# 项目目录结构详解

## 根目录

```
ai-demand-research-v2/
├── SKILL.md                    # 技能主文件（本方法论）
├── references/                 # 参考资料目录
├── templates/                  # 代码与报告模板
├── scripts/                    # 可复用脚本
├── assets/                     # 静态资源（CSS、JS、图片）
└── projects/                   # 各调研项目（运行时创建）
```

## 单个项目目录

```
projects/{topic-name}-{YYYY-MM-DD}/
├── 00-meta/                    # 项目元数据
│   ├── project.json            # 项目配置与状态
│   ├── workflow.html           # 工作流可视化（自动更新）
│   └── session.log             # 操作日志
│
├── 01-raw-data/                # 原始数据
│   ├── input/                  # 原始输入文件
│   └── manifest.json           # 数据源清单
│
├── 02-cleaned/                 # 数据清洗
│   ├── input/                  # 符号链接到 01-raw-data/input
│   ├── code/                   # 清洗代码
│   │   └── data_cleaning.py
│   ├── output/                 # 清洗后数据
│   │   └── cleaned_data.parquet
│   └── manifest.json           # 步骤清单
│
├── 03-phase1-discovery/        # 第一阶段：场景发现
│   ├── step1-topic-clustering/
│   │   ├── input/ -> ../../02-cleaned/output
│   │   ├── code/
│   │   │   └── topic_clustering.py
│   │   ├── output/
│   │   │   ├── topic_distribution.json
│   │   │   └── topic_content_map.csv
│   │   └── manifest.json
│   ├── step2-signal-extract/
│   ├── step3-content-quality/
│   ├── step4-high-value-identify/
│   ├── step5-opportunity-mapping/
│   └── step6-search-optimize/
│
├── 04-phase2-analysis/         # 第二阶段：现状分析
│   ├── step1-user-profile/
│   ├── step2-solution-analysis/
│   ├── step3-pain-deep-dive/
│   ├── step4-expectation-analysis/
│   └── step5-payment-privacy/
│
├── 05-insights/                # 洞察与机会
│   ├── input/                  # 聚合前两阶段输出
│   ├── code/
│   │   └── insight_generator.py
│   ├── output/
│   │   ├── insights.json       # 结构化洞察
│   │   └── opportunity_matrix.json
│   └── manifest.json
│
├── 06-reports/                 # 最终交付件（三件套）
│   ├── final-analysis-report.html    # 最终分析报告
│   ├── technical-report.html         # 过程技术报告
│   └── improvement-report.html       # 任务改进建议
│
└── archive/                    # 归档历史版本
    ├── v1-2026-05-14T10-30-00/     # 第一次分析版本
    ├── v2-2026-05-14T14-20-00/     # 回滚后重新生成
    └── ...
```

## 文件命名规范

### 代码文件
- `{step-name}.py` — 主处理脚本
- `{step-name}_test.py` — 测试脚本
- `utils_{module}.py` — 工具模块

### 数据文件
- `*.parquet` — 清洗后的结构化数据（推荐）
- `*.csv` — 中间结果、可人工查看的数据
- `*.json` — 统计结果、配置、清单
- `*.xlsx` — 最终报告中的表格附件

### 报告文件
- `*-report.html` — HTML交互式报告
- `*-report.md` — Markdown备用版本
- `*-slides.pptx` — PPT演示版本（可选）

## manifest.json 规范

每个步骤目录必须包含 `manifest.json`：

```json
{
  "step_id": "唯一标识符",
  "step_name": "人类可读名称",
  "version": 1,
  "timestamp": "ISO-8601格式",
  "status": "completed|failed|archived",
  "input": {
    "files": ["相对路径列表"],
    "checksum": "sha256:..."
  },
  "code": {
    "file": "代码文件路径",
    "checksum": "sha256:..."
  },
  "output": {
    "files": ["输出文件列表"],
    "checksums": {"file": "sha256:..."}
  },
  "parameters": {},
  "notes": ""
}
```

## archive/ 归档规则

**触发条件：**
1. 用户要求"回滚到某一步重新生成"
2. 用户要求"重新分析"
3. 同一主题但分析方法有重大变更

**归档内容：**
- 将被覆盖的步骤目录整体移入 `archive/v{N}-{timestamp}/`
- 保留完整的 input/code/output/manifest

**恢复方法：**
- 从 archive 复制回项目目录即可恢复
