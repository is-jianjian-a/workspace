# AI产品需求调研工作流 v4.0

---
skill_version: "4.0.0"
skill_name: "ai-demand-research"
description: "基于JTBD框架的AI产品需求调研工作流，支持过程可控、专题隔离、流程可视化、三件套交付"
author: "zhijian"
last_updated: "2026-05-14"
tags: ["product-research", "jtbd", "user-insight", "ugc-analysis", "opportunity-discovery"]
---

## 一、设计原则

### 1.1 核心目标
以真实数据支撑的手机用户诉求和手机高价值新特性方向洞察。

### 1.2 五大设计原则

| 原则 | 说明 | 实现方式 |
|------|------|---------|
| **过程可控** | 每步输入、处理代码、输出结果均保存为文件 | 标准化目录结构 + 脚本命名规范 |
| **专题专项** | 每个调研主题独立项目，隔离数据与产出 | 主题命名目录 + 项目清单 |
| **流程展示** | 交互式HTML直观展示工作流状态 | workflow_status.html 自动更新 |
| **三件套交付** | 最终分析报告 + 过程技术报告 + 任务改进建议 | 结构化模板 + 交互式HTML |
| **真实数据洞察** | 所有洞察必须有数据支撑，可追溯至原始UGC | 数据血缘 + 引用溯源 |

### 1.3 v4 改进核心（vs v3）

v4 是最小可行改进集，聚焦三大根本问题：

| 根本问题 | v3 症状 | v4 解决方案 | 方法论 |
|---------|---------|------------|--------|
| 痛点脱离任务上下文 | 提取的信号是关键词，缺少情境 | **Job Story**（情境+动机+结果） | JTBD框架 |
| 优先级主观模糊 | P0/P1/P2 缺乏量化标准 | **Kano分类 + RICE评分** | Kano模型 + RICE框架 |
| 洞察无法验证真伪 | 报告交付即结束 | **假设→实验→验证→学习闭环** | 假设驱动开发 |

---

## 二、工作流总览

### 2.1 四阶段十六步

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 阶段一：感知 (SENSING)        →  阶段二：理解 (UNDERSTANDING)               │
│   1.项目初始化                    5.Job Story提取                           │
│   2.搜索词设计                    6.Job地图绘制                             │
│   3.数据采集                      7.用户画像分析                            │
│   4.数据清洗                      8.Kano分类                                │
│                                   9.RICE评分                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ 阶段三：验证 (VALIDATION)     →  阶段四：交付 (DELIVERY)                    │
│  10.假设形成                     14.洞察生成                                │
│  11.实验设计                     15.搜索词优化                              │
│  12.快速验证                     16.三件套交付                              │
│  13.学习闭环                                                                │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 每步标准格式

每一步必须产出以下文件：

```
步骤N-步骤名称/
├── input/              ← 输入数据（引用上一步输出，不复制）
├── script/             ← 处理代码
│   └── stepN_xxx.py    ← 可独立运行的脚本
├── output/             ← 输出结果
│   ├── result.json     ← 结构化数据
│   └── result.md       ← 人类可读报告
└── meta.json           ← 步骤元数据
    ├── step_id: "N"
    ├── step_name: "步骤名称"
    ├── method: "使用的方法论"
    ├── input_files: [...]
    ├── output_files: [...]
    ├── status: "completed|failed|skipped"
    └── timestamp: "ISO8601"
```

---

## 三、详细步骤

### 阶段一：感知 (SENSING)

#### 步骤1：项目初始化

**目标**：创建标准化的项目目录结构，记录项目元数据。

**输入**：用户提供的调研主题、目标产品/功能领域、初步背景信息。

**处理**：
1. 生成项目目录（见第四节）
2. 创建 `project_manifest.json`
3. 初始化 `workflow_status.html`

**输出**：
- `00-meta/project_manifest.json`
- `00-meta/workflow_status.html`

**project_manifest.json 模板**：
```json
{
  "project_id": "{主题}_{YYYYMMDD}",
  "theme": "调研主题",
  "target_product": "目标产品/功能领域",
  "created_at": "ISO8601",
  "version": "4.0.0",
  "status": "active",
  "current_step": 1,
  "total_steps": 16,
  "search_round": 1,
  "data_sources": ["xiaohongshu", "bilibili", "zhihu", "coolapk", "appstore"],
  "jtbd_focus": ["functional", "emotional"],
  "notes": "用户提供的背景信息"
}
```

---

#### 步骤2：搜索词设计

**目标**：设计多轮搜索词，覆盖场景发现所需的数据维度。

**方法论**：搜索词公式 = 场景词 + 情绪词/状态词 + 动作词

**处理**：
1. 基于主题生成第一轮搜索词（5-8组）
2. 每组包含：核心词、同义词、平台适配词
3. 记录搜索词设计 rationale

**输出**：
- `02-scripts/step02_search_terms.py`
- `04-searches/search_terms_round1.json`

**search_terms.json 结构**：
```json
{
  "round": 1,
  "terms": [
    {
      "id": "T001",
      "query": "手机 卡顿 怎么办",
      "platform": "xiaohongshu",
      "rationale": "捕捉用户在遇到性能问题时的求助行为",
      "expected_signals": ["performance_pain", "help_seeking"]
    }
  ]
}
```

---

#### 步骤3：数据采集

**目标**：从UGC平台采集原始数据。

**数据源优先级**：
1. **P0**：小红书、B站、知乎、酷安、App Store评论
2. **P1**：微博、抖音、贴吧、V2EX
3. **P2**：专业论坛、Discord/Reddit（海外产品）

**处理**：
1. 运行爬虫脚本（Playwright + 指纹伪装）
2. 保存原始HTML/JSON响应
3. 记录采集元数据（时间、平台、数量、异常）

**输出**：
- `01-raw/{platform}_{timestamp}.json`
- `01-raw/crawl_log.json`

---

#### 步骤4：数据清洗

**目标**：将原始数据清洗为结构化、可分析的格式。

**处理**：
1. 去重（内容相似度 > 85% 视为重复）
2. 过滤（广告/水军/太短 < 20字）
3. 结构化（统一字段：id, platform, content, author, timestamp, likes, comments, url）
4. 质量评分（内容长度、信息密度、情感明确度）

**输出**：
- `03-cleaned/cleaned_data.json`
- `03-cleaned/quality_report.json`

**quality_report.json**：
```json
{
  "raw_count": 5000,
  "cleaned_count": 3200,
  "duplicate_removed": 1200,
  "filtered_out": 600,
  "quality_distribution": {
    "high": 800,
    "medium": 1600,
    "low": 800
  }
}
```

---

### 阶段二：理解 (UNDERSTANDING)

#### 步骤5：Job Story提取

**目标**：从UGC文本中提取 Job Story，将需求锚点从"信号"升级为"任务上下文"。

**方法论**：JTBD（Jobs-to-be-Done）

**Job Story 标准格式**：
```
当我在 [情境] 时，
我想要 [动机/目标]，
这样我就可以 [期望结果]。
```

**处理**：
1. NLP模型分析每条UGC，识别：情境(Context)、动机(Motivation)、期望结果(Desired Outcome)
2. 如果单条UGC信息不完整，合并同一主题下的多条内容
3. 标注 Job 类型：Functional（功能）/ Emotional（情感）/ Social（社会）
4. 为每个 Job Story 关联原始UGC ID（可追溯）

**输出**：
- `05-jobs/job_stories.json`
- `05-jobs/job_stories.md`（人类可读）

**job_stories.json 结构**：
```json
{
  "jobs": [
    {
      "id": "J001",
      "job_statement": "当我在通勤路上时，我想要快速了解今天的行业动态，这样我就可以在到达公司前做好准备",
      "job_type": "functional",
      "context": "通勤路上",
      "motivation": "快速了解今天的行业动态",
      "desired_outcome": "在到达公司前做好准备",
      "source_ugc_ids": ["UGC_1234", "UGC_5678"],
      "frequency": 23,
      "confidence": 0.85
    }
  ]
}
```

**质量检查**：
- 每个 Job Story 必须包含 Context + Motivation + Desired Outcome
- 必须关联至少1条原始UGC
- Confidence < 0.6 的 Job Story 标记为"需人工审核"

---

#### 步骤6：Job地图绘制

**目标**：将 Job Stories 组织成可视化的 Job 地图，识别任务流程中的痛点分布。

**方法论**：Job Map（Ulwick, 2002）

**Job Map 结构**：
```
任务阶段 → 子任务 → Job Story → 当前解决方案 → 痛点 → 期望改进
```

**处理**：
1. 将所有 Job Stories 按任务阶段分组（如：认知→考虑→使用→忠诚）
2. 在每个阶段内，识别子任务
3. 映射：当前用户如何完成此任务（现有解决方案）
4. 标注：痛点在任务流程中的位置
5. 识别：任务流程中的"断点"（用户放弃或转换的地方）

**输出**：
- `06-jobmap/job_map.json`
- `06-jobmap/job_map.html`（可视化）

---

#### 步骤7：用户画像分析

**目标**：基于UGC数据构建用户画像，理解谁在表达这些需求。

**处理**：
1. 从UGC文本中提取用户属性（身份、设备、使用深度、场景）
2. 聚类用户群体（K-means或主题模型）
3. 为每个群体标注：代表Job Stories、核心痛点、期望功能

**输出**：
- `07-personas/user_personas.json`
- `07-personas/user_personas.md`

---

#### 步骤8：Kano分类

**目标**：对每个高优先级 Job/需求进行 Kano 分类，判断需求类型。

**方法论**：Kano Model（狩野纪昭, 1984）

**分类标准**（基于UGC推断）：

| 类型 | 判断标准 | 策略 |
|------|---------|------|
| 基本型 (Must-be) | 用户默认期望具备，缺失导致强烈不满 | 必须满足，不用于竞争 |
| 期望型 (Performance) | 表现越好满意度越高 | 投资回报率驱动优化 |
| 兴奋型 (Delighter) | 超出预期，显著提升满意度 | 差异化竞争的核心 |
| 无差异型 (Indifferent) | 用户不在意 | 不投入资源 |
| 反向型 (Reverse) | 过度功能让用户反感 | 避免或移除 |

**处理**：
1. 对每个 Job Story，分析UGC中的情感倾向和期望强度
2. 推断 Kano 分类（NLP模型 + 规则引擎）
3. 标记 Confidence（高/中/低）
4. 人工审核低 Confidence 的分类

**输出**：
- `08-kano/kano_classification.json`
- `08-kano/kano_matrix.html`（可视化矩阵）

---

#### 步骤9：RICE评分

**目标**：对机会进行量化评分，替代主观 P0/P1/P2。

**方法论**：RICE Framework（Intercom, 2016）

**公式**：
```
RICE Score = (Reach × Impact × Confidence) / Effort
```

**维度定义**（基于UGC数据估算）：

| 维度 | 定义 | 数据来源 | 评分方式 |
|------|------|---------|---------|
| Reach | 每季度影响多少用户 | UGC提及频次 × 平台用户基数估算 | 具体用户数 |
| Impact | 对每个用户的影响程度 | 情感强度 + 行为意愿表达 | 3=巨大, 2=高, 1=中, 0.5=低 |
| Confidence | 对评估数值的信心 | 数据支撑度 + 三角验证状态 | 100%=高, 80%=中, 50%=低 |
| Effort | 实现所需人月 | 产品团队评估（调研阶段先标注"待评估"） | 人月数 |

**处理**：
1. 为每个 Job Story / 机会计算 RICE Score
2. 按分数排序，生成 Top N 列表
3. 标注数据来源和估算依据

**输出**：
- `09-rice/rice_scores.json`
- `09-rice/rice_ranking.html`（可交互排序表）

**rice_scores.json 结构**：
```json
{
  "opportunities": [
    {
      "id": "O001",
      "job_id": "J001",
      "description": "通勤场景音频摘要功能",
      "reach": 150000,
      "impact": 2,
      "confidence": 0.8,
      "effort": 3,
      "rice_score": 80000,
      "kano_type": "delighter",
      "data_sources": ["xiaohongshu:45 mentions", "zhihu:23 mentions"]
    }
  ]
}
```

---

### 阶段三：验证 (VALIDATION)

#### 步骤10：假设形成

**目标**：将洞察转化为可验证的假设陈述。

**方法论**：假设驱动开发（Hypothesis-Driven Development）

**假设声明标准格式**：
```
如果 我们 [做某个方案]，
那么 [某指标] 会改善 [X]%，
因为 [基于调研的推理]。
```

**处理**：
1. 为每个 Top 机会（RICE Score 前10）形成假设
2. 假设必须基于步骤5-9的数据
3. 标注假设类型：需求真实性 / 解决方案吸引力 / 量化效果 / 定价敏感度

**输出**：
- `10-hypotheses/hypotheses.json`
- `10-hypotheses/hypotheses.md`

**hypotheses.json 结构**：
```json
{
  "hypotheses": [
    {
      "id": "H001",
      "opportunity_id": "O001",
      "statement": "如果我们为通勤场景提供音频摘要功能，那么该场景的日活留存会提升15%，因为调研显示73%的通勤用户因'无法快速获取信息'而放弃使用",
      "type": "solution_attractiveness",
      "validation_method": "prototype_test",
      "validation_timeline": "2周",
      "source_jobs": ["J001", "J015"],
      "status": "pending_validation"
    }
  ]
}
```

---

#### 步骤11：实验设计

**目标**：为每个假设设计最小可行实验。

**实验方法选择矩阵**：

| 假设类型 | 推荐实验方法 | 验证周期 | 所需资源 |
|---------|------------|---------|---------|
| 需求真实性 | 5-8次半结构化访谈 | 1周 | 用户招募池 |
| 解决方案吸引力 | 原型测试（可用性测试） | 1-2周 | 原型工具 |
| 量化效果预估 | A/B测试或灰度发布 | 2-4周 | 产品埋点 |
| 定价敏感度 | Van Westendorp价格敏感性调查 | 1周 | 问卷工具 |

**处理**：
1. 为每个假设选择验证方法
2. 设计实验计划（样本量、指标、成功标准）
3. 标注所需资源和依赖

**输出**：
- `11-experiments/experiment_plans.json`
- `11-experiments/experiment_plans.md`

---

#### 步骤12：快速验证

**目标**：执行实验，收集验证数据。

**说明**：此步骤由产品团队主导执行，调研团队提供支持。

**处理**：
1. 产品团队按实验计划执行
2. 记录实验过程和结果
3. 标注结果置信度

**输出**：
- `12-validation/validation_results.json`
- `12-validation/validation_evidence/`（访谈录音、测试录像、数据截图）

---

#### 步骤13：学习闭环

**目标**：分析验证结果，更新机会评估。

**处理**：
1. 对比假设预测 vs 实际结果
2. 更新机会的 Confidence 评分
3. 识别"验证失败"的机会，分析原因
4. 生成"已验证机会"清单（Confidence ≥ 80%）
5. 记录学习要点，供后续调研参考

**输出**：
- `13-learning/learning_summary.json`
- `13-learning/validated_opportunities.json`
- `13-learning/failed_assumptions_analysis.md`

---

### 阶段四：交付 (DELIVERY)

#### 步骤14：洞察生成

**目标**：综合所有分析，生成结构化洞察。

**处理**：
1. 汇总已验证的机会（步骤13输出）
2. 按 RICE Score 排序
3. 为每个 Top 机会生成洞察卡片：
   - Job Story
   - 痛点证据（引用原始UGC）
   - 用户群体
   - Kano分类
   - RICE Score
   - 验证状态
   - 建议方向

**输出**：
- `14-insights/insights.json`
- `14-insights/insight_cards.html`

---

#### 步骤15：搜索词优化

**目标**：基于本轮发现，优化下一轮搜索词。

**处理**：
1. 识别"信号不足"的领域（需要更多数据）
2. 识别"意外发现"的方向（值得深入）
3. 生成下一轮搜索词建议
4. 更新 project_manifest.json 的 search_round

**输出**：
- `15-next-round/search_terms_round{N+1}.json`
- `15-next-round/research_gaps.md`

---

#### 步骤16：三件套交付

**目标**：生成最终交付件。

**交付件清单**：

| 交付件 | 文件名 | 核心内容 | 交互特性 |
|--------|--------|---------|---------|
| 最终分析报告 | `final-analysis-report.html` | Job地图、Top机会、用户画像、Kano矩阵、RICE排序 | 可点击的Job地图、可排序的RICE表、可筛选的用户群体 |
| 过程技术报告 | `technical-report.html` | 每步输入/处理/输出、数据质量、模型性能、异常处理 | 可追溯链条、数据血缘图、代码高亮 |
| 任务改进建议报告 | `improvement-report.html` | 方法论反思、工具优化、流程改进、下一轮建议 | 改进前后对比、优先级矩阵、实施路线图 |

**输出**：
- `16-reports/final-analysis-report.html`
- `16-reports/technical-report.html`
- `16-reports/improvement-report.html`
- `16-reports/delivery_manifest.json`

---

## 四、项目目录结构

```
workspace/
└── ai-demand-research-v4/
    └── {调研主题}_YYYYMMDD/              ← 每个任务一个独立项目
        ├── 00-meta/                      ← 项目元数据
        │   ├── project_manifest.json
        │   └── workflow_status.html      ← 交互式工作流看板
        │
        ├── 01-raw/                       ← 原始数据（永不修改）
        │   ├── xiaohongshu_20260514.json
        │   ├── bilibili_20260514.json
        │   └── crawl_log.json
        │
        ├── 02-scripts/                   ← 每步处理代码
        │   ├── step01_init.py
        │   ├── step02_search_terms.py
        │   ├── step03_crawl.py
        │   ├── step04_clean.py
        │   ├── step05_extract_jobs.py
        │   ├── step06_job_map.py
        │   ├── step07_personas.py
        │   ├── step08_kano.py
        │   ├── step09_rice.py
        │   ├── step10_hypotheses.py
        │   ├── step11_experiments.py
        │   ├── step12_validate.py
        │   ├── step13_learn.py
        │   ├── step14_insights.py
        │   ├── step15_next_round.py
        │   └── step16_deliver.py
        │
        ├── 03-cleaned/                   ← 清洗后数据
        │   ├── cleaned_data.json
        │   └── quality_report.json
        │
        ├── 04-searches/                  ← 搜索词记录
        │   └── search_terms_round1.json
        │
        ├── 05-jobs/                      ← Job Story提取
        │   ├── job_stories.json
        │   └── job_stories.md
        │
        ├── 06-jobmap/                    ← Job地图
        │   ├── job_map.json
        │   └── job_map.html
        │
        ├── 07-personas/                  ← 用户画像
        │   ├── user_personas.json
        │   └── user_personas.md
        │
        ├── 08-kano/                      ← Kano分类
        │   ├── kano_classification.json
        │   └── kano_matrix.html
        │
        ├── 09-rice/                      ← RICE评分
        │   ├── rice_scores.json
        │   └── rice_ranking.html
        │
        ├── 10-hypotheses/                ← 假设声明
        │   ├── hypotheses.json
        │   └── hypotheses.md
        │
        ├── 11-experiments/               ← 实验设计
        │   ├── experiment_plans.json
        │   └── experiment_plans.md
        │
        ├── 12-validation/                ← 验证结果
        │   ├── validation_results.json
        │   └── validation_evidence/
        │
        ├── 13-learning/                  ← 学习闭环
        │   ├── learning_summary.json
        │   ├── validated_opportunities.json
        │   └── failed_assumptions_analysis.md
        │
        ├── 14-insights/                  ← 洞察生成
        │   ├── insights.json
        │   └── insight_cards.html
        │
        ├── 15-next-round/                ← 下一轮优化
        │   ├── search_terms_round2.json
        │   └── research_gaps.md
        │
        ├── 16-reports/                   ← 最终三件套
        │   ├── final-analysis-report.html
        │   ├── technical-report.html
        │   ├── improvement-report.html
        │   └── delivery_manifest.json
        │
        └── archive/                      ← 回滚归档
            └── v1_YYYYMMDD/              ← 旧版本自动移入
```

---

## 五、回滚与归档机制

### 5.1 触发条件
- 用户明确要求"回滚到步骤N"
- 发现某步骤输出存在严重质量问题
- 需要基于新的搜索词重新运行某步骤

### 5.2 归档流程
1. 将当前版本目录整体复制到 `archive/v{N}_{timestamp}/`
2. 在 `00-meta/project_manifest.json` 中记录归档历史
3. 从归档版本恢复指定步骤的输入
4. 重新运行该步骤及后续所有步骤
5. 更新 `workflow_status.html`

### 5.3 归档记录格式
```json
{
  "archives": [
    {
      "version": "v1",
      "timestamp": "2026-05-14T10:00:00Z",
      "reason": "搜索词调整，重新采集",
      "rollback_step": 3,
      "path": "archive/v1_20260514100000/"
    }
  ]
}
```

---

## 六、workflow_status.html 规范

### 6.1 功能要求
- 直观展示16步的当前状态（未开始/进行中/已完成/失败）
- 点击任意步骤可查看：输入文件列表、处理代码、输出文件列表
- 自动更新（每完成一步后刷新）
- 显示项目整体进度（如：7/16 步完成，43%）

### 6.2 视觉设计
- 深色主题，符合"酷"的风格要求
- 步骤用卡片式布局，状态用颜色区分
- 阶段用分组标题清晰划分
- 响应式设计，支持移动端查看

### 6.3 更新机制
- 每完成一步，由该步的脚本自动更新 HTML
- 更新内容：步骤状态、输出文件链接、完成时间戳

---

## 七、质量检查清单

### 7.1 每步必检
- [ ] 输入文件存在且可读
- [ ] 处理代码可独立运行
- [ ] 输出文件符合格式规范
- [ ] 元数据文件完整
- [ ] 数据血缘可追溯（输出关联到输入）

### 7.2 阶段检查点

**阶段一结束检查**：
- [ ] 清洗后数据量 ≥ 原始数据的 50%
- [ ] 高质量数据（quality=high）≥ 20%

**阶段二结束检查**：
- [ ] 每个 Job Story 包含 Context + Motivation + Desired Outcome
- [ ] Kano分类覆盖率 = 100%（Top机会）
- [ ] RICE Score 计算有据可查

**阶段三结束检查**：
- [ ] 每个 Top 机会有对应的假设
- [ ] 假设有明确的验证方法
- [ ] 验证结果有数据支撑

**阶段四结束检查**：
- [ ] 三件套报告完整
- [ ] 报告中的每个洞察有数据引用
- [ ] 搜索词优化建议具体可执行

---

## 八、v4 边界说明

### 8.1 v4 包含（最小可行集）
- ✅ JTBD框架（Job Story提取 + Job地图）
- ✅ Kano分类 + RICE评分（双轨优先级）
- ✅ 假设验证闭环（假设→实验→验证→学习）
- ✅ 过程可控（每步输入/处理/输出保存）
- ✅ 专题专项（独立项目目录）
- ✅ 流程展示（workflow_status.html）
- ✅ 三件套交付（分析报告+技术报告+改进建议）

### 8.2 v4 不包含（留到v5）
- ❌ 持续发现模式（批处理→持续运行数据管道）
- ❌ 多源三角验证（UGC+行为数据+深度访谈三层）
- ❌ 用户旅程地图（CJM可视化）
- ❌ North Star Metric（结果导向衡量体系）
- ❌ 竞品评论采集（App Store/G2/Capterra）
- ❌ 机会解决方案树（OST）
- ❌ 设计思维后三阶段（构思/原型/测试）

---

## 九、使用方式

### 9.1 启动新调研

```bash
# 1. 创建新项目
python ai-demand-research-v4/scripts/init_project.py \
  --theme "手机AI功能用户诉求调研" \
  --target "智能手机AI助手功能" \
  --notes "关注用户对新AI功能的期望和痛点"

# 2. 按步骤执行（逐步进行，每步可检查）
cd projects/手机AI功能用户诉求调研_20260514
python ../../scripts/step02_search_terms.py
python ../../scripts/step03_crawl.py
# ... 依此类推

# 3. 或一键运行（自动执行所有步骤）
python ../../scripts/run_all.py

# 4. 查看工作流状态
open 00-meta/workflow_status.html
```

### 9.2 回滚操作

```bash
# 回滚到步骤5，重新运行
python ../../scripts/rollback.py --step 5 --reason "Job Story质量不达标"
```

### 9.3 查看报告

```bash
open 16-reports/final-analysis-report.html
```

---

## 十、参考方法论

| 方法论 | 应用领域 | 在v4中的使用 |
|--------|---------|------------|
| JTBD (Jobs-to-be-Done) | 需求定义 | 步骤5-6：Job Story提取、Job地图 |
| Kano Model | 需求分类 | 步骤8：Kano分类 |
| RICE Framework | 优先级排序 | 步骤9：RICE评分 |
| 假设驱动开发 | 验证闭环 | 步骤10-13：假设→实验→验证→学习 |

---

## 十一、版本历史

| 版本 | 日期 | 核心改进 |
|------|------|---------|
| v1.0 | 2026-04 | 初始版本，两阶段流程（场景发现+现状分析） |
| v2.0 | 2026-05 | 增加过程可控、专题专项、三件套交付 |
| v3.0 | 2026-05 | 优化搜索词设计、增加竞品分析、改进报告模板 |
| **v4.0** | **2026-05** | **引入JTBD框架、Kano+RICE优先级、假设验证闭环** |

---

*本工作流遵循"不预设需求、多维度交叉验证、UGC优先、从情绪到功能"的核心原则。*
