---
name: ugc-research-v3
description: |
  AI产品需求调研方法论v3：基于UGC（用户生成内容）信号分析，从社交媒体数据中提取真实消费者需求。
  
  当用户需要以下场景时触发此skill：
  - "调研XX需求的UGC数据" / "分析用户在社交媒体上对XX的讨论"
  - "从UGC中发现产品机会" / "基于小红书/抖音/知乎数据做需求分析"
  - "消费者视角的需求调研" / "排除创造者视角，只看用户想要什么"
  - "UGC信号融合分析" / "三层信号分析框架"
  - "生成HTML需求调研报告" / "UGC数据可视化报告"
  
  核心特征：严格区分消费者视角vs创造者视角，Signal Fusion三层分析框架，
  数据驱动的HTML交互报告，每结论15-20条UGC原文支撑。
---

# UGC需求调研v3 — AI产品需求调研方法论

## 核心原则

### 1. 消费者视角优先（不可妥协）
- **内容消费者视角**：看视频/用产品的人想要什么功能（保留）
- **内容创造者视角**：做视频/创作内容的人想要什么工具（排除）
- **混合视角**：一律归为创造者视角，不保留
- **常见创造者关键词**：生成视频、自动剪辑、二创工具、教程教学、变现赚钱、涨粉爆款、脚本分镜、口播录制、模板素材
- **常见消费者关键词**：看视频、学习笔记、摘要总结、翻译字幕、推荐过滤、倍速跳过、画质清晰、投屏同步

**快速判断流程**：
```
1. 读取UGC标题+内容
2. 检查是否含创造者关键词
   ├─ 是 → 检查是否含消费者关键词
   │       ├─ 否 → 排除（纯创造者）
   │       └─ 是 → 排除（混合视角，保守策略）
   └─ 否 → 检查是否含消费者关键词
           ├─ 是 → 保留（纯消费者）
           └─ 否 → 人工判断或根据二层主题决定
```

**校准案例**（详见 `references/consumer_creator_keywords.md`）：
- ✅ 保留："看到AI视频会有强烈不适感"（观看体验）
- ✅ 保留："十年后人眼还能分辨ai视频吗？"（认知担忧）
- ❌ 排除："AI一键生成带货短视频最新玩法"（变现+创作）
- ❌ 排除："让AI帮你剪视频（教程）"（创作工具+教程）

### 2. 数据真实性红线
- 所有统计数据必须来自JSON文件，禁止编造
- 每个结论必须 backed by 15-20条真实UGC原文（标题+内容+互动数+标签）
- 评分必须设计完整公式并在报告中给出详细公式

### 3. 搜索词中性正交
- 搜索词 = 场景词 × 功能/痛点/体验词
- 禁止预设方向的搜索词
- 每组10个组合，Phase 2基于机会映射结果分类设计

## 工作流（6阶段）

### Phase 0: 数据获取与确认
1. 用户指定搜索词（1个或多个）
2. 确认搜索平台（xhs | dy | ks | bili | zhihu）
3. 检查数据库中已有数据数量（目标400-600条）
4. **如果数量不对，先找用户确认，不要继续**
5. 创建项目目录：`projects/{主题}-{日期}/`

### Phase 1: 数据清洗
```python
# 输入：SQLite数据库中的原始UGC
# 输出：01-cleaned/cleaned_ugcs.json

步骤：
1. 从数据库提取所有相关UGC（note_id, platform, title, content, likes, comments, tags）
2. 去重：URL+标题+内容MD5
3. 基础字段标准化（平台代码转中文名）
4. 保存清洗后数据
```

### Phase 2: 相关性筛选（最关键！）
```python
# 输入：cleaned_ugcs.json
# 输出：02-screened/relevant_ugcs.json + excluded_ugcs.json

步骤：
1. 定义创造者关键词列表（排除）
2. 定义消费者关键词列表（保留）
3. 第一轮筛选：关键词匹配
   - 纯创造者关键词 → 排除
   - 纯消费者关键词 → 保留
   - 混合关键词 → 进入第二轮
4. 第二轮筛选：语义判断
   - 逐条阅读混合UGC的标题+内容
   - 判断核心视角是消费者还是创造者
   - 无法判断的，保守排除
5. 生成视角审核HTML供用户抽查
6. 用户确认后锁定筛选结果
```

**关键判断标准**：
- 讨论"AI怎么帮我做视频" → 创造者，排除
- 讨论"看视频时希望AI帮我做什么" → 消费者，保留
- 讨论"AI生成视频的真假/影响" → 消费者（观看体验），保留
- 教程类、工具推荐类（面向创作者）→ 排除

**用户修正响应流程**：
当用户对筛选结果提出修正（如"这条应该是消费者视角""混合视角全部归为创造者"）：
1. 记录修正案例到关键词词典的修正案例集
2. 按用户指示重新分类（如混合视角全部→创造者）
3. 对保留的消费者视角UGC进行**二次严格筛选**
4. 识别并移除漏网的创造者视角UGC（教程、变现、工具推荐等）
5. 生成新的审核报告，标注修正后的分类
6. 请用户确认最终筛选结果

### Phase 3: 信号识别（Layer 1）
```python
# 输入：relevant_ugcs.json
# 输出：03-layer1/layer1_classified.json

四分类体系：
1. 需求信号：用户明确表达"我想要XX功能"
2. 使用反馈：用户使用后的评价/吐槽/建议
3. 关注讨论：用户在讨论什么话题（非直接需求）
4. 噪声：无关或信息不足

执行方式：
- 优先用delegate_task子Agent批量分类（每批20-30条）
- LLM超时后fallback到规则分类
- 输出可交互HTML审核报告
```

### Phase 4: 信号结构化（Layer 2）
```python
# 输入：layer1中标记为"需求信号"和"使用反馈"的UGC
# 输出：04-layer2/layer2_structured.json

提取字段：
- scene: 使用场景（工作/学习/通勤/睡前等）
- pain_point: 痛点描述
- need: 需求描述
- emotion: 情绪（期待/惊喜/沮丧/焦虑等）
- emotion_intensity: 情绪强度（高/中/低）
- current_solution: 当前解决方案（如有）

执行方式：
- delegate_task子Agent批量处理
- 每批20-30条
- 输出结构化数据+审核HTML
```

### Phase 5: 统一映射（Layer 3）
```python
# 输入：layer2_structured.json
# 输出：05-mapping/opportunity_mapping.json

原则：
1. 不预设功能域
2. 对着UGC和Layer 1/2结果发散思考
3. 逐条映射到功能机会点
4. 聚合相似机会点（话题聚合颗粒度要细）

反例：
- ❌ "备孕/生育"（太宽泛）
- ✅ "备孕方法与经验""久备不孕/医疗""备孕心理与情绪"（具体角度）

"其他"类别控制在5%以内
```

### Phase 6: 报告生成
```python
# 输入：所有前序阶段数据
# 输出：06-report/

生成文件：
1. stats_summary.json — 统计摘要
2. insights.json — 洞察分析
3. final_report.html — 主分析报告（嵌入数据、纯CSS、可交互）
4. ugc_audit_report.html — UGC全文核查报告（供用户审核分类准确性）
```

## HTML报告规范

### 技术要求
- 数据用Python `json.dumps()` 嵌入，禁止子Agent直接写JSON
- JS用传统函数`function(){}`，禁止箭头函数
- 必须检查单引号嵌套（如onclick内部引号冲突）
- 必须用`node --check`验证JS语法
- 多批次并行时必须强制统一字段名
- 交付前主动验证，不能等用户发现错误

### 内容要求
- 完整逻辑链路：UGC原文→分类依据→分布统计→交互量分析→产品建议推导
- 每个机会点至少15-20条UGC原文支撑
- 纯CSS数据可视化（无外部CDN依赖）
- 可交互：标签页切换、筛选、排序

## 项目文件结构

```
projects/{主题}-{日期}/
├── 00-raw/                    # 原始数据（从数据库导出）
├── 01-cleaned/                # 清洗后数据
│   └── cleaned_ugcs.json
├── 02-screened/               # 相关性筛选后
│   ├── relevant_ugcs.json     # 消费者视角（保留）
│   ├── excluded_ugcs.json     # 创造者视角（排除）
│   └── viewpoint_audit.html   # 视角审核报告
├── 03-layer1/                 # 信号识别结果
│   ├── layer1_classified.json
│   └── layer1_audit_report.html
├── 04-layer2/                 # 信号结构化结果
│   ├── layer2_structured.json
│   └── layer2_audit_report.html
├── 05-mapping/                # 统一映射结果
│   ├── opportunity_mapping.json
│   └── mapping_audit_report.html
└── 06-report/                 # 最终报告
    ├── stats_summary.json
    ├── insights.json
    ├── final_report.html      # 主分析报告
    └── ugc_audit_report.html  # UGC全文核查报告
```

## 工具使用规范

### LLM批量分类
- 必须用`delegate_task`子Agent
- 每批20-30条并行处理
- 子Agent输出Python脚本而非直接写JSON
- LLM超时后fallback到规则分类

### 数据验证清单
- [ ] HTML文件可双击打开正常显示
- [ ] JS语法通过node --check验证
- [ ] 数据字段名跨批次一致
- [ ] 统计数据与JSON源文件一致
- [ ] 每个结论有≥15条UGC原文支撑

### Skill文件更新
- 优先使用`skill_manage(action='patch')`更新skill
- 如果返回"not found"错误，直接使用`write_file`写文件到`~/.hermes/skills/<skill-name>/references/`目录
- 这是已验证的workaround

## 常见陷阱

1. **SQLite陷阱**：xhs_note_comment.note_id可能无法JOIN，desc是保留字需引号，互动量是TEXT类型需parse_count，source_keyword可能含前导空格
2. **子Agent超时**：600秒内无法完成批量处理，需设计fallback机制
3. **API Key无效**：提前测试API可用性，无效时立即切换方案
4. **数据质量问题**：36%+ UGC可能与主题无关，需严格筛选
5. **话题聚合过宽**：必须基于具体讨论角度细分，"其他"控制在5%以内
6. **skill_manage更新失败**：对现有skill的patch/write_file操作可能返回"not found"错误。当遇到此错误时，直接使用 `write_file` 工具写文件到 `~/.hermes/skills/<skill-name>/references/` 或 `templates/` 目录下，绕过skill_manage的查找逻辑。这是已验证的工作方式。

## 用户偏好嵌入

- **规划优先**：先输出规划文档（数据源、文件夹结构、执行步骤、质量红线、时间预估、待确认事项），用户确认后再行动
- **验证 mandatory**：交付前主动验证所有可交付物
- **嵌入式HTML**：数据嵌入HTML，确保离线可查看
- **消费者视角严格**：混合视角一律排除，宁可错杀不可错放
- **真实UGC支撑**：每个结论必须有15-20条原文，禁止编造
- **用户校准介入**：当用户对相关性标签提出修正时，必须：
  1. 记录修正案例到 `references/consumer_creator_keywords.md` 的修正案例集
  2. 根据修正重新筛选（如"混合视角全部归为创造者"）
  3. 对保留数据再次严格筛选
  4. 生成新的审核报告供用户确认
- **修正后二次筛选**：用户修正后（如"混合视角全部归为创造者"），必须对保留的消费者视角UGC进行二次严格筛选，识别并移除漏网的创造者内容（教程、变现、工具推荐等），然后重新生成统计和报告
