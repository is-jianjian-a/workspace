---
title: AI产品需求调研方法论 v3
description: 基于社交媒体数据的AI产品需求调研完整工作流，从搜索词设计到洞察交付，支持过程可控、项目隔离、流程迭代
author: hermes
version: 3.0
name: ai-demand-research-v3
category: research
---

# AI产品需求调研方法论 v3

## 最终目的（以文件形式牢记）

> **以真实数据支撑的手机用户诉求和手机高价值新特性方向洞察。**
>
> 所有工作流的终点，是产出可指导手机产品决策的、有数据支撑的洞察报告。

---

## 核心设计原则

### 一、中间过程可控（Provenance）

每一步分析必须保存：输入数据、处理代码、输出结果、参数配置、执行时间。形成可追溯的链条，支持查阅、溯源、复盘、回滚。

### 二、专题专项，项目隔离

每个调研主题对应一个独立项目目录。用户说"开启新项目"或判断为不同主题时，才新建项目。回滚后重新生成，旧文件归档保留。

### 三、流程定义展示（迭代检查）

工作流HTML展示**当前定义的整体流程**（不是进度跟踪）。每次交流后检查流程是否需要迭代更新，用户满意后更新到skill中。支持点击节点查看该步骤的定义、输入输出规范、关键检查点。

### 四、三件套交付

| 交付件 | 内容 | 风格 |
|--------|------|------|
| 最终分析报告 | 洞察、机会、建议 | 酷炫交互式 |
| 过程技术报告 | 每步方法、代码、参数 | 技术文档风 |
| 任务改进建议 | 方法论改进、工具优化 | 结构化清单 |

**原则：内容宜多不宜少，交互性强，风格要酷。**

### 五、从搜索开始

流程起点是**搜索词设计**，不是数据加载。数据通过搜索采集获得，整个流程是搜索→采集→清洗→分析→洞察的闭环。

---

## 完整工作流

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AI产品需求调研 v3 工作流                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │  0.项目初始化 │ -> │ 1.搜索词设计  │ -> │ 2.数据采集   │ -> │ 3.数据清洗   │  │
│  │             │    │             │    │             │    │             │  │
│  │ - 创建项目目录│    │ - 场景词+情绪词│    │ - 爬虫/导出  │    │ - 格式标准化 │  │
│  │ - 配置主题   │    │ - 搜索词评审  │    │ - 多平台采集 │    │ - 互动量转换 │  │
│  │ - 工作流HTML │    │ - 搜索词清单  │    │ - 原始数据保存│    │ - 质量检查   │  │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      第一阶段：场景发现（泛化搜索）                      │   │
│  │                                                                      │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  │   │
│  │  │4.主题聚类 │->│5.信号提取 │->│6.内容质量 │->│7.高价值识别│->│8.机会映射 │  │   │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘  │   │
│  │                                                                      │   │
│  │  ┌─────────────────────────────────────────────────────────────┐   │   │
│  │  │ 9.三维标签化分析（新增）                                        │   │   │
│  │  │  - 9a.使用情境标签（空间/身体/并行活动）                        │   │   │
│  │  │  - 9b.触发-退出机制（触发因素/退出障碍/退出触发/使用后情绪）      │   │   │
│  │  │  - 9c.用户群体标签（身份/阶段/设备/使用深度）                    │   │   │
│  │  └─────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      第二阶段：现状分析（聚焦搜索）                      │   │
│  │                                                                      │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  │   │
│  │  │10.用户画像│->│11.解决方案 │->│12.痛点深度 │->│13.期望功能 │->│14.付费隐私 │  │   │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────────────────┐ │
│  │ 15.洞察生成  │ -> │ 16.搜索词优化 │ -> │ 17.三件套交付                     │ │
│  │             │    │             │    │  - 最终分析报告.html               │ │
│  │ - 机会矩阵   │    │ - 效果评估   │    │  - 过程技术报告.html               │ │
│  │ - P0/P1/P2  │    │ - 下一轮搜索词│    │  - 任务改进建议.html               │ │
│  │ - 用户原声   │    │ - 闭环反馈   │    │                                   │ │
│  └─────────────┘    └─────────────┘    └─────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 阶段详解

### 0. 项目初始化

**输入**：调研主题、目标平台、初步方向
**输出**：项目目录、project.json、工作流定义HTML

**操作**：
```bash
python scripts/init_project.py --topic "手机AI功能用户诉求调研" --platforms xhs,bilibili,zhihu
```

**创建内容**：
- 项目目录结构（00-meta/ 到 06-reports/ + archive/）
- project.json（主题、平台、状态、版本）
- workflow-definition.html（工作流定义展示）
- 搜索词模板文件（search-keywords-template.md）

---

### 1. 搜索词设计

**输入**：调研主题、目标场景、用户初步假设
**输出**：搜索词清单（search-keywords.json）

**设计原则**：
- 不用身份标签，用场景+情绪/状态词
- 公式：`场景词 + 情绪词/状态词 + 动作词`
- **正交搭配原则**：【场景词/平台词/行为词】×【功能/缺点/体验词】，不预设具体功能方向，让用户的真实表达决定主题分布
- **系统层面优先**：从手机系统层面打捞诉求，非APP功能层面

**搜索词类型**：
| 类型 | 说明 | 示例 |
|------|------|------|
| 场景词 | 用户在什么场景 | 半夜、通勤、睡前、碎片时间 |
| 情绪词 | 用户什么情绪 | 崩溃、焦虑、停不下来、无聊 |
| 动作词 | 用户在做什么 | 怎么办、怎么解决、求助、刷 |

**正交搭配示例**：
| 场景词 | 功能 | 缺点 | 不好用 | 问题 |
|--------|------|------|--------|------|
| 抖音 | 抖音 功能 | 抖音 缺点 | 抖音 不好用 | 抖音 问题 |
| 手机看视频 | 手机看视频 功能 | 手机看视频 缺点 | — | 手机看视频 问题 |

**搜索词评审检查点**：
- [ ] 是否覆盖"做什么→遇到什么→情绪如何→怎么办"完整链路
- [ ] 是否有同质化词（如"哄睡难"和"哄睡困难"只留一个）
- [ ] 是否去掉偏期望而非现状的词
- [ ] 每个场景是否5-10个词
- [ ] **是否采用正交搭配，避免预设功能方向**
- [ ] **是否从手机系统层面出发，而非APP功能层面**

**输出文件**：
- `01-search-design/search-keywords.json` — 结构化搜索词
- `01-search-design/search-keywords.md` — 人类可读版本
- `01-search-design/manifest.json` — 步骤清单

---

### 2. 数据采集

**输入**：搜索词清单、目标平台配置
**输出**：原始数据文件（JSONL/SQLite）

**采集方式**：
- 小红书：MediaCrawler
- B站/知乎/酷安：web_extract 或 browser 工具
- App Store/Google Play：专用API或爬虫

**保存规范**：
- 原始数据按搜索词分文件保存
- 文件名格式：`{platform}_{keyword}_{timestamp}.jsonl`
- 同步保存采集日志（采集时间、数量、异常）

**输出文件**：
- `02-raw-data/input/*.jsonl` — 原始数据
- `02-raw-data/crawl-log.json` — 采集日志
- `02-raw-data/manifest.json` — 步骤清单

---

### 3. 数据清洗

**输入**：原始数据文件
**输出**：清洗后的标准化数据（Parquet）

**关键操作**：
1. 格式统一（JSONL/Excel/SQLite → DataFrame）
2. 互动量标准化（parse_count处理"万+"、","等）
3. 文本合并（title + desc → text）
4. 去重、去空、异常值处理
5. 搜索词分布检查

**输出文件**：
- `03-cleaned/output/cleaned_data.parquet` — 清洗后数据
- `03-cleaned/output/cleaning_report.json` — 清洗报告
- `03-cleaned/code/data_cleaning.py` — 清洗代码
- `03-cleaned/manifest.json` — 步骤清单

---

### 第一阶段：场景发现（泛化搜索）

基于采集的泛化搜索数据，识别高价值场景。

#### 4. 主题聚类分析

**输入**：清洗后数据
**输出**：主题分布统计、主题-内容映射

**操作**：构建主题词典，匹配每条内容的主题

**输出文件**：
- `04-phase1-discovery/step1-topic-clustering/output/topic_stats.json`
- `04-phase1-discovery/step1-topic-clustering/output/topic_content_map.csv`
- `04-phase1-discovery/step1-topic-clustering/manifest.json`

#### 5. 需求信号提取

**输入**：清洗后数据
**输出**：信号统计（痛点/决策/求助/行为/期望）

**信号词典**：
```python
signals = {
    '痛点信号': ['难', '痛苦', '崩溃', '焦虑', '担心', '害怕', '慌', '烦', '累', '困', '无助', '绝望', '后悔', '自责', '内疚'],
    '决策信号': ['怎么选', '哪个好', '推荐', '对比', '测评', '攻略', '清单', '必买', '种草'],
    '求助信号': ['怎么办', '正常吗', '求助', '请教', '有经验', '过来人', '建议'],
    '行为信号': ['每天', '经常', '总是', '习惯', '规律', '记录', '打卡', '坚持'],
    '期望信号': ['希望', '想要', '期待', '如果能', '要是', '最好', '理想', '完美', '解决']
}
```

#### 6. 内容质量评估

**输入**：清洗后数据
**输出**：UGC/营销/混合/中性分布

**分类规则**：
- 纯营销：只有营销信号，无UGC信号
- 纯UGC：只有UGC信号，无营销信号
- 混合：两者都有
- 中性：两者都无

#### 7. 高价值内容识别

**输入**：主题、信号、质量分析结果
**输出**：高价值内容TOP N

**筛选标准**：
- 互动量 > 5000（或前20%）
- 包含痛点信号或期望信号
- 优先纯UGC内容

#### 8. 产品机会映射

**输入**：主题分布、信号统计、高价值内容
**输出**：P0/P1/P2机会清单

**评估矩阵**：
| 维度 | 权重 | 评估标准 |
|------|------|---------|
| 需求强度 | 30% | 痛点覆盖率、互动量 |
| 供给缺口 | 25% | 现有工具满意度、信息分散度 |
| 技术可行性 | 20% | AI/数据/硬件可实现性 |
| 商业价值 | 15% | 付费意愿、用户生命周期 |
| 竞争壁垒 | 10% | 数据壁垒、专家资源 |

#### 9. 三维标签化分析（v2新增，v3保留）

**9a. 使用情境标签化**
- 空间情境：通勤路上、床上睡前、工作间隙、家庭场景、户外等待
- 身体状态：疲惫、焦虑、无聊、困倦、兴奋
- 并行活动：吃饭时、做家务、带娃时、运动时、学习工作时

**9b. 触发-退出机制标签化**
- 触发因素：习惯性打开、无聊驱动、情绪逃避、社交需求、信息获取
- 退出障碍：算法陷阱、沉没成本、社交压力、内容未完成、情绪依赖
- 退出触发：外部打断、生理限制、时间意识、情绪转变、任务完成
- 使用后情绪：更焦虑、放松满足、空虚后悔、无感、充实

**9c. 用户群体标签化**
- 身份标签：新手妈妈、职场妈妈、全职妈妈、学生、上班族
- 阶段标签：新生儿、小月龄、婴儿期、幼儿期、学龄前
- 设备偏好：iPhone、华为、小米、OPPO、vivo
- 使用深度：轻度、中度、重度

**第一阶段输出**：
1. 主题分布图
2. 需求信号统计
3. UGC vs 营销对比
4. 高价值内容TOP N
5. 产品机会清单（P0/P1/P2）
6. 使用情境分布
7. 触发-退出机制分析
8. 用户群体画像

---

### 第二阶段：现状分析（聚焦搜索）

针对第一阶段识别的P0机会，设计聚焦搜索词，深入验证。

#### 搜索词设计（第二阶段）

围绕P0机会点，设计聚焦搜索词：
| 维度 | 示例（睡眠场景） |
|------|----------------|
| 工具使用 | 睡眠记录APP、哄睡神器 |
| 痛点暴露 | 夜醒频繁怎么办、落地醒怎么解决 |
| 行为描述 | 自主入睡训练、睡眠倒退期 |
| 期望表达 | 希望宝宝睡整觉、求睡眠神器 |

#### 10. 用户画像提取

**提取维度**：身份、阶段、设备、使用深度

#### 11. 当前解决方案分析

**提取维度**：使用什么APP/工具/平台、使用频率、满意度

#### 12. 痛点深度分析

**痛点分类**：操作繁琐、信息过载、知识焦虑、选择困难、质量参差、缺乏系统、实操困难

#### 13. 期望功能分析

**期望分类**：即时问答、知识库、个性化推荐、视频学习、社区交流、专家服务、AI辅助、系统学习

#### 14. 付费意愿与隐私顾虑

**付费信号**：愿意付费、看广告、价格敏感、需要试用
**隐私信号**：隐私、本地、不上传、不泄露、安全、加密

**第二阶段输出**：
1. 用户画像报告
2. 当前解决方案分析
3. 痛点深度分析
4. 期望功能分析
5. 付费意愿评估
6. 产品机会建议（P0/P1/P2功能清单）

---

### 15. 洞察生成

**输入**：两阶段分析结果
**输出**：结构化洞察、机会矩阵

**生成内容**：
- 核心洞察（3-5条）
- 机会矩阵（需求强度 × 技术可行性）
- P0机会详解（数据支撑 + 用户原声 + 建议方案）
- 用户诉求热力图

**输出文件**：
- `05-insights/output/insights.json`
- `05-insights/output/opportunity_matrix.json`
- `05-insights/manifest.json`

---

### 16. 搜索词优化

**输入**：本轮分析结果
**输出**：下一轮搜索词建议

**优化规则**：
- 高覆盖但低互动 → 需求已被满足，减少搜索
- 低覆盖但高互动 → 供给缺口，增加搜索
- 高痛点但低期望 → 需求未被识别，需教育市场

**形成闭环**：优化后的搜索词回到步骤1，启动新一轮迭代

---

### 17. 三件套交付

| 交付件 | 文件名 | 内容 |
|--------|--------|------|
| 最终分析报告 | `06-reports/final-analysis-report.html` | 洞察、机会、建议（酷炫交互式） |
| 过程技术报告 | `06-reports/technical-report.html` | 每步方法、代码、参数（技术文档风） |
| 任务改进建议 | `06-reports/improvement-report.html` | 方法论改进、工具优化（结构化清单） |

---

## 项目目录结构

```
projects/{topic-name}-{YYYY-MM-DD}/
├── 00-meta/
│   ├── project.json              # 项目配置与状态
│   ├── workflow-definition.html  # 工作流定义展示（迭代检查用）
│   └── session.log               # 操作日志
│
├── 01-search-design/             # 搜索词设计
│   ├── input/                    # 主题方向、初步假设
│   ├── code/
│   │   └── search_keyword_design.py
│   ├── output/
│   │   ├── search-keywords.json  # 结构化搜索词
│   │   └── search-keywords.md    # 人类可读版本
│   └── manifest.json
│
├── 02-raw-data/                  # 数据采集
│   ├── input/                    # 搜索词清单（符号链接）
│   ├── output/
│   │   ├── *.jsonl               # 原始数据（按搜索词分文件）
│   │   └── crawl-log.json        # 采集日志
│   └── manifest.json
│
├── 03-cleaned/                   # 数据清洗
│   ├── input/ -> 02-raw-data/output
│   ├── code/
│   │   └── data_cleaning.py
│   ├── output/
│   │   ├── cleaned_data.parquet
│   │   └── cleaning_report.json
│   └── manifest.json
│
├── 04-phase1-discovery/          # 第一阶段：场景发现
│   ├── step1-topic-clustering/
│   ├── step2-signal-extract/
│   ├── step3-content-quality/
│   ├── step4-high-value-identify/
│   ├── step5-opportunity-mapping/
│   └── step6-three-dimension-tagging/
│       ├── step6a-usage-context/
│       ├── step6b-trigger-exit/
│       └── step6c-user-group/
│
├── 05-phase2-analysis/           # 第二阶段：现状分析
│   ├── step1-user-profile/
│   ├── step2-solution-analysis/
│   ├── step3-pain-deep-dive/
│   ├── step4-expectation-analysis/
│   └── step5-payment-privacy/
│
├── 06-insights/                  # 洞察生成
│   ├── input/                    # 聚合两阶段输出
│   ├── code/
│   │   └── insight_generator.py
│   ├── output/
│   │   ├── insights.json
│   │   └── opportunity_matrix.json
│   └── manifest.json
│
├── 07-search-optimize/           # 搜索词优化
│   ├── input/
│   ├── code/
│   ├── output/
│   │   └── optimized-keywords.json
│   └── manifest.json
│
├── 08-reports/                   # 最终交付件
│   ├── final-analysis-report.html
│   ├── technical-report.html
│   └── improvement-report.html
│
└── archive/                      # 归档历史版本
    ├── v1-20260514-103000/
    ├── v2-20260514-142000/
    └── ...
```

---

## manifest.json 规范

每个步骤目录必须包含 `manifest.json`：

```json
{
  "step_id": "phase1-step3-signal-extract",
  "step_name": "需求信号提取",
  "version": 1,
  "timestamp": "2026-05-14T16:30:00+08:00",
  "input": {
    "files": ["../03-cleaned/output/cleaned_data.parquet"],
    "checksum": "sha256:abc123..."
  },
  "code": {
    "file": "code/signal_extract.py",
    "checksum": "sha256:def456..."
  },
  "output": {
    "files": ["output/signal_stats.json", "output/signal_details.csv"],
    "checksums": {"signal_stats.json": "sha256:ghi789..."}
  },
  "parameters": {
    "signal_threshold": 0.7,
    "min_interaction": 100
  },
  "notes": "使用v1.2信号词典，新增'后悔'信号"
}
```

---

## 关键原则

1. **不预设需求** — 用场景+情绪词搜索，而非功能名
2. **多维度交叉** — 主题+痛点+期望+行为，四维度验证
3. **关注异常信号** — 低覆盖+高互动 = 供给缺口
4. **UGC优先** — 纯UGC内容可信度高于营销内容
5. **从情绪到功能** — 痛点词→行为词→期望词→功能机会
6. **迭代优化** — 每轮分析后优化搜索词，持续深入
7. **过程可追溯** — 每一步的输入、代码、输出都必须保存
8. **项目隔离** — 不同主题严格隔离，避免数据污染
9. **闭环反馈** — 洞察反哺搜索词，形成迭代闭环

---

## 技能部署与路径陷阱

### 用户级技能路径

用户级技能必须放在**真实的** `~/.hermes/skills/` 路径下，而非 profile 隔离目录的符号链接后。Hermes 的技能发现机制扫描的是 `~/.hermes/skills/` 的物理目录结构；如果该路径是符号链接指向 profile 子目录，技能加载器可能无法正确解析。

**正确做法**：
```bash
# 确认路径是物理目录，不是符号链接
ls -la ~/.hermes/skills/
# 如果 skills 是链接，直接在物理目录创建
mkdir -p /Users/$USER/.hermes/skills/research/ai-demand-research-v3
```

**部署验证**：
```bash
# 1. 检查物理文件存在
find /Users/$USER/.hermes/skills/research/ai-demand-research-v3 -type f

# 2. 检查 skill_view 能加载
# 在新 session 中执行: skill_view(name='ai-demand-research-v3')
```

### 常见部署失败原因

| 现象 | 原因 | 修复 |
|------|------|------|
| `skill_view` 报 "not found" | 文件在符号链接后，不在物理路径 | 使用绝对路径 `/Users/$USER/.hermes/skills/` 复制 |
| `skills_list` 能看到但 `skill_view` 失败 | 缓存与物理文件不同步 | 检查物理路径是否真的有文件 |
| 文件存在但加载为空 | SKILL.md 格式错误（YAML frontmatter 缺失）| 确认 `---` 开头，有 `name`/`description` 字段 |
| `cp` 后文件消失 | `~/.hermes/skills/` 是符号链接 | 用 `readlink -f` 检查，改用绝对物理路径 |

### macOS 路径陷阱（重要）

在 macOS 上，`~/.hermes/skills/` 可能是符号链接指向 `~/.hermes/profiles/<name>/home/.hermes/skills/`。Hermes 的技能发现机制扫描的是物理目录结构，符号链接后的文件可能无法被正确加载。

**症状**：
- `skills_list` 能看到技能名称但 `skill_view` 返回空或报错
- 文件明明存在但加载失败
- 重启 session 后技能消失

**诊断**：
```bash
# 检查 skills 是否为符号链接
ls -la ~/.hermes/skills/
# 如果是链接，查看真实路径
readlink -f ~/.hermes/skills/
```

**修复**：始终使用绝对物理路径部署：
```bash
# 不要这样
cp SKILL.md ~/.hermes/skills/research/ai-demand-research-v3/
# 要这样
SKILL_DIR="/Users/$USER/.hermes/skills/research/ai-demand-research-v3"
mkdir -p "$SKILL_DIR"
cp SKILL.md "$SKILL_DIR/"
```

### 从 workspace 部署到 skills 的标准流程

当用户要求将 workspace 中的文件创建为 skill 时：

```bash
# 1. 确认物理路径（不要用 ~ 或相对路径）
SKILL_DIR="/Users/$USER/.hermes/skills/research/ai-demand-research-v3"
mkdir -p "$SKILL_DIR"/{references,templates,scripts,assets}

# 2. 复制文件（用绝对路径）
cp /Users/$USER/workspace/ai-demand-research-v3/SKILL.md "$SKILL_DIR/"
cp /Users/$USER/workspace/ai-demand-research-v3/references/* "$SKILL_DIR/references/"
cp /Users/$USER/workspace/ai-demand-research-v3/templates/* "$SKILL_DIR/templates/"

# 3. 验证物理文件存在
find "$SKILL_DIR" -type f

# 4. 验证 skill 可加载
# skill_view(name='ai-demand-research-v3')
```

---

## 参考文件

### references/（方法论参考）
- `references/project-structure.md` — 目录结构详解 + manifest.json 规范 + 归档规则
- `references/workflow-definition-spec.md` — 工作流定义HTML规范（视觉设计、数据格式、迭代检查流程）
- `references/report-templates.md` — 三件套报告模板规范（最终分析/技术报告/改进建议）
- `references/search-keyword-design.md` — 搜索词设计指南（公式、检查清单、输出格式）
- `references/orthogonal-keyword-design.md` — **正交搭配搜索词设计原则（v3核心方法论）**：A轴×B轴组合、系统层面优先、实战案例、常见错误
- `references/three-dimension-tagging.md` — 三维标签化分析参考（完整词典、代码模板、跨场景适配）
- `references/sqlite-data-source.md` — SQLite数据源处理指南（字段类型、parse_count、陷阱警示）
- `references/report-v3-spec.md` — **报告规范 v3.1+**：双层主题标签体系、UGC级多维标签（平台/情绪/场景/二层主题）、可展开折叠UGC列表的交互与视觉规范

### templates/（可执行模板）
- `templates/init_project.py` — 项目初始化脚本（创建完整目录结构、project.json、搜索词模板）
- `templates/archive_version.py` — 版本归档脚本（单步骤归档 / 完整项目归档）
- `templates/data_cleaning.py` — 数据清洗模板（支持 Excel/JSONL/SQLite，输出 Parquet）
- `templates/analysis_pipeline.py` — 分析流水线模板（Phase1 场景发现 + Phase2 现状分析）
- `templates/workflow_definition.html` — 工作流定义HTML模板（深色主题、可点击节点、版本标记）
