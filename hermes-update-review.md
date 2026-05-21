# Hermes Agent 更新审查报告

> 当前版本：v0.13.0 (2026.5.7) → 落后 1018 commits
> 审查范围：约 v0.9.0 ~ v0.13.0+ 之间的全部更新
> 生成时间：2026-05-21

---

## 一、主要更新功能分类总结

### 1.1 核心 Agent 与模型层（高影响）

| 功能 | 影响度 | 说明 |
|------|--------|------|
| **Claude Prompt Cache 跨会话复用** | ⭐⭐⭐⭐⭐ | 1小时前缀缓存，Anthropic/OpenRouter/Nous Portal 均支持，大幅降低长上下文成本 |
| **Computer Use (CUA-Driver)** | ⭐⭐⭐⭐⭐ | 通用 any-model 计算机使用后端，支持 set_value/结构化窗口/MIME 检测 |
| **Prompt Caching 1h TTL** | ⭐⭐⭐⭐⭐ | 跨会话缓存，对长报告生成类任务成本影响显著 |
| **Context Compressor 重构** | ⭐⭐⭐⭐ | 包含系统提示+工具 schema 的 token 估算、tail 保护修复、feasibility 检查增强 |
| **Reasoning Content 跨提供商隔离** | ⭐⭐⭐⭐ | DeepSeek/Kimi 的 reasoning_content 不再泄漏到其他提供商 |
| **Codex Spark 模型支持** | ⭐⭐⭐⭐ | gpt-5.3-codex-spark，128k 上下文 |
| **OpenRouter Pareto Code Router** | ⭐⭐⭐ | min_coding_score 路由旋钮 |
| **xAI Responses API 升级** | ⭐⭐⭐ | TTS 支持、reasoning.effort 透传 |
| **Kimi K2.6 / DeepSeek V4 Pro** | ⭐⭐⭐ | 新增模型支持，1M 上下文 |
| **Azure Foundry 原生支持** | ⭐⭐⭐ | OpenAI/Anthropic API 模式自动检测 |
| **Bedrock Transport** | ⭐⭐⭐ | Converse API 原生支持 |
| **GMI Cloud / Xiaomi MiMo / Z.AI** | ⭐⭐ | 新增提供商 |
| **Ollama Cloud** | ⭐⭐ | 动态模型发现 |
| **Vercel Sandbox 后端** | ⭐⭐ | 云端代码执行环境 |
| **MiniMax OAuth / M2.7** | ⭐⭐ | PKCE 浏览器流 + 新模型 |

### 1.2 并行与编排系统（与你高度相关）

| 功能 | 影响度 | 说明 |
|------|--------|------|
| **Kanban 多项目看板** | ⭐⭐⭐⭐⭐ | 多 profile 协作板，支持 worker 工具集、orchestrator 角色、任务依赖 |
| **Kanban Orchestrator 重构** | ⭐⭐⭐⭐⭐ | 移除硬编码专家名单，新增 Step-0 Profile 发现 |
| **Kanban Dashboard 批量操作** | ⭐⭐⭐⭐ | 多选拖拽、列全选、批量重新分配 |
| **Kanban 诊断引擎** | ⭐⭐⭐⭐ | 任务 distress signal 自动检测 |
| **Delegate Task 增强** | ⭐⭐⭐⭐ | 显示实际并发/深度限制、接受 JSON 字符串批量任务、继承 fallback_chain |
| **Cron Job 链式执行** | ⭐⭐⭐⭐ | `context_from` 字段支持 job 输出链式传递 |
| **Cron No-Agent 模式** | ⭐⭐⭐⭐ | 纯脚本 watchdog 模式，无 LLM 开销 |
| **SubAgent 超时诊断** | ⭐⭐⭐ | 0 API 调用超时时自动 dump 诊断信息 |
| **Kanban Worker 生命周期** | ⭐⭐⭐ | 按 run_id 隔离、phantom-card 重试指导 |
| **Kanban max_spawn 实时并发限制** | ⭐⭐⭐ | 按运行中 worker 数量限制，非 per-tick 预算 |

### 1.3 工具与文件系统（与你高度相关）

| 功能 | 影响度 | 说明 |
|------|--------|------|
| **File Tools 写入后 Lint** | ⭐⭐⭐⭐⭐ | write_file + patch 后自动运行 JSON/YAML/TOML/Python 语法检查 |
| **Read File 结果大小限制** | ⭐⭐⭐⭐ | 防止上下文窗口溢出 |
| **Search Files 路径/行号冲突修复** | ⭐⭐⭐ | 连字符数字文件名冲突 |
| **Patch Tool "Did you mean?"** | ⭐⭐⭐ | 匹配失败时提供相似文本建议 |
| **Browser Console 180x 加速** | ⭐⭐⭐⭐ | CDP supervisor 持久 WebSocket 路由 |
| **Browser Lightpanda 引擎** | ⭐⭐⭐ | 自动 Chrome 回退 |
| **Web Search 多后端** | ⭐⭐⭐⭐ | SearXNG、Brave Search、DDGS 原生支持 |
| **Web Extract 能力拆分** | ⭐⭐⭐ | search/extract 分 capability 后端选择 |
| **Execute Code Windows 支持** | ⭐⭐⭐⭐ | 移除 AF_UNIX 门控，Windows 原生可用 |
| **Execute Code UTF-8 强制** | ⭐⭐⭐ | PYTHONIOENCODING=utf-8 |
| **File Sync 远程回写** | ⭐⭐⭐ | SSH/Docker 终端后端支持双向同步 |

### 1.4 会话与记忆系统

| 功能 | 影响度 | 说明 |
|------|--------|------|
| **/handoff 跨平台会话转移** | ⭐⭐⭐⭐⭐ | Telegram → CLI → Web 等跨平台无缝转移 |
| **/goal 持久目标** | ⭐⭐⭐⭐⭐ | 跨多轮自动工作的 standing goal（已 revert 又部分恢复） |
| **Honcho 记忆系统重构** | ⭐⭐⭐⭐⭐ | 5-tool 表面、成本安全、会话隔离、RLock 线程安全 |
| **Session Search CJK 支持** | ⭐⭐⭐⭐ | 三元组 FTS5 索引 + LIKE 回退 |
| **Session Search 工具调用索引** | ⭐⭐⭐ | tool_calls / tool_name 纳入 FTS5 |
| **Memory Context 泄漏修复** | ⭐⭐⭐⭐ | 多轮边界 scrub，防止记忆上下文泄漏到回复 |
| **Hindsight 客户端** | ⭐⭐⭐ | 可选依赖，会话级 retain metadata |
| **Context Compression 语言感知** | ⭐⭐⭐ | 摘要现在尊重对话语言 |

### 1.5 安全与隐私

| 功能 | 影响度 | 说明 |
|------|--------|------|
| **Secret Redaction 默认开启** | ⭐⭐⭐⭐⭐ | 工具输出中的 API key/token 自动脱敏（可关闭） |
| **Sudo 硬化** | ⭐⭐⭐⭐ | 阻止 sudo -S 密码猜测、stdin/askpass/shell 特权标志拦截 |
| **PII Redaction (Gateway)** | ⭐⭐⭐⭐ | 用户 ID 哈希、手机号剥离 |
| **Dashboard 插件 API 认证** | ⭐⭐⭐⭐ | 要求 dashboard auth |
| **MCP OAuth 状态持久化** | ⭐⭐⭐ | 跨进程重启保留 |
| **Webhook HMAC 验证** | ⭐⭐⭐ | Twilio 签名验证 |
| **Approval 模式增强** | ⭐⭐⭐ | smart/manual/off 三模式，cron 独立 approval 模式 |

### 1.6 平台与 Gateway

| 功能 | 影响度 | 说明 |
|------|--------|------|
| **LINE 平台插件** | ⭐⭐⭐⭐ | 新增消息平台 |
| **Microsoft Teams 插件** | ⭐⭐⭐⭐ | 完整平台适配 |
| **IRC 平台插件** | ⭐⭐⭐ | 参考实现 |
| **Telegram Draft 流式** | ⭐⭐⭐⭐ | Bot API 9.5+ 原生草稿 |
| **Telegram 话题模式** | ⭐⭐⭐⭐ | DM 多会话话题 |
| **Feishu 文档评论** | ⭐⭐⭐ | 智能回复 + 三级访问控制 |
| **DingTalk QR 扫码** | ⭐⭐⭐ | 设备流认证 |
| **QQBot 官方 API v2** | ⭐⭐⭐ | 完整重写 |
| **Gateway 重启取证** | ⭐⭐⭐ | 非阻塞诊断、分阶段计时 |
| **Gateway 自动恢复** | ⭐⭐⭐ | 崩溃/重启后自动 resume 会话 |
| **i18n 16 语言** | ⭐⭐⭐⭐ | 网关命令 + Web Dashboard 全本地化 |

### 1.7 TUI / CLI 体验

| 功能 | 影响度 | 说明 |
|------|--------|------|
| **TUI 长会话性能优化** | ⭐⭐⭐⭐⭐ | 虚拟滚动、增量 markdown、Ink 缓存 |
| **TUI 冷启动 -19s** | ⭐⭐⭐⭐ | Skills 缓存 + 懒加载 |
| **TUI 模型选择器** | ⭐⭐⭐⭐ | 内联 provider 断开、API key 设置 |
| **TUI 工具行内 diff** | ⭐⭐⭐⭐ | patch 结果直接嵌入 |
| **TUI 实时 todo 面板** | ⭐⭐⭐⭐ | 折叠/归档/进度追踪 |
| **TUI 状态栏压缩计数** | ⭐⭐⭐ | 显示上下文压缩次数 |
| **TUI 鼠标支持** | ⭐⭐⭐ | 选择、复制、滚轮 |
| **TUI 亮色主题** | ⭐⭐⭐ | 自动检测 + LIGHT_THEME 预设 |
| **CLI Ctrl+Enter 换行** | ⭐⭐⭐ | WSL/SSH/Windows Terminal |
| **CLI Markdown 表格垂直回退** | ⭐⭐⭐ | 超宽表格自动切换格式 |

### 1.8 Skills 与 Curator

| 功能 | 影响度 | 说明 |
|------|--------|------|
| **Curator 后台技能维护** | ⭐⭐⭐⭐⭐ | 自动审查、归档、合并 agent 创建的技能 |
| **Curator Pin 保护** | ⭐⭐⭐⭐ | pinned 技能免于所有自动转换 |
| **Skills 平台 frontmatter** | ⭐⭐⭐⭐ | 142 个技能补全平台声明 |
| **Skills 直接 URL 安装** | ⭐⭐⭐⭐ | HTTP(S) URL 直接安装 |
| **Skills 使用遥测** | ⭐⭐⭐ | use_count / view_count / patch_count |
| **新增内置技能** | ⭐⭐⭐ | Stocks、Maps、Airtable、SearXNG、Watchers、Humanizer 等 |
| **可选技能迁移** | ⭐⭐⭐ | 训练类技能移至 optional-skills |

### 1.9 插件系统

| 功能 | 影响度 | 说明 |
|------|--------|------|
| **插件平台注册表** | ⭐⭐⭐⭐⭐ | 动态加载平台适配器 |
| **插件钩子系统** | ⭐⭐⭐⭐ | pre_tool_call / post_tool_call / transform_tool_result / pre_llm_call / pre_gateway_dispatch |
| **插件 slash 命令注册** | ⭐⭐⭐⭐ | 插件自定义命令 |
| **Dashboard 插件系统** | ⭐⭐⭐⭐ | 页面级插件槽位 |
| **Dashboard 主题系统** | ⭐⭐⭐⭐ | 字体/布局/密度可配置 |
| **Langfuse 可观测性插件** | ⭐⭐⭐ | 内置 |
| **Achievement 插件** | ⭐⭐⭐ | 游戏化成就追踪 |

---

## 二、按你的使用习惯推荐关注的功能

### 🔴 最高优先级（直接影响工作流）

#### 1. **Kanban 多项目协作板 + Orchestrator 模式**
你的两阶段 AI 需求调研（Phase 1 场景分析 → Phase 2 深度用户状态分析）天然适合 Kanban 编排：
- **Phase 1** 可作为一个 Kanban task，由 orchestrator profile 分解为多个并行 subtask（关键词分解、场景分类、用户旅程映射）
- **Phase 2** 依赖 Phase 1 完成，自动触发
- 每个 subtask 可由不同 profile 的 worker 执行（如一个专门做数据清洗、一个专门做 HTML 报告生成）
- **Dashboard 批量操作**支持多选拖拽重新分配

**关键配置：**
```yaml
kanban:
  max_spawn: 5          # 控制并发 worker 数
  dispatch_in_gateway: true
```

#### 2. **File Tools 写入后自动 Lint**
你频繁生成 JSON 嵌入数据的 HTML 报告，现在 `write_file` 和 `patch` 后会自动运行：
- JSON 语法检查
- YAML/TOML 验证
- Python 语法检查

**这直接解决你过去遇到的「JSON 语法错误导致报告无法加载」问题。**

#### 3. **Secret Redaction 默认开启**
你的 HTML 报告常包含 API key、数据源路径等敏感信息。现在工具输出自动脱敏：
```bash
hermes config set security.redact_secrets true   # 已默认开启
```
**风险：** 如果报告需要展示原始数据路径，可能需要手动关闭或调整。

#### 4. **Context Compressor 增强**
- 包含系统提示 + 工具 schema 的 token 估算 → **更准确的长会话预算管理**
- Tail 保护修复 → **防止活跃任务丢失**
- 语言感知摘要 → **中文 UGC 数据摘要质量提升**
- 主模型 fallback → **aux 模型失败时自动降级**

#### 5. **Browser Console 180x 加速**
你偶尔用 browser 工具抓取网页数据，CDP supervisor 持久连接后：
- `browser_console` eval 速度提升 180 倍
- 对需要大量 JS 执行的页面（如动态加载的小红书）影响显著

#### 6. **Prompt Cache 跨会话复用**
如果你的调研工作流有固定的系统提示（如「你是一个产品研究员...」），1 小时缓存可显著降低成本。

---

### 🟡 中优先级（提升效率）

#### 7. **Cron Job No-Agent 模式**
你的 UGC 数据收集是手动进行的，但后续的数据清洗、报告生成可以自动化：
```bash
hermes cron create "0 9 * * *" --no-agent --script ~/scripts/daily_report.sh
```
纯脚本模式，无 LLM token 开销。

#### 8. **Skills 直接 URL 安装**
你可以将 ai-demand-research-v3 等自定义技能打包为 GitHub raw URL，团队成员一键安装：
```bash
hermes skills install https://raw.githubusercontent.com/.../SKILL.md
```

#### 9. **Curator 自动维护**
Agent 创建的技能会随时间积累，Curator 每 7 天自动：
- 标记闲置技能为 stale
- 归档过旧技能（保留 tar.gz 备份）
- 提示合并相似技能

**建议：** 将你的核心调研技能 pin 住，避免被误归档：
```bash
hermes curator pin ai-demand-research-v3
```

#### 10. **TUI 长会话性能**
如果你常用 `hermes --tui`，长会话（>50 轮）的滚动和渲染已大幅优化。

---

### 🟢 低优先级（了解即可）

- **新模型支持**（Kimi K2.6、DeepSeek V4 Pro、Codex Spark）：按需切换
- **新平台**（LINE、Teams）：与你当前工作无关
- **Dashboard 主题/插件**：除非你用 Web UI 管理
- **Voice/TTS 增强**：与你的文本工作流无关

---

## 三、机制变更导致工作连续性问题的风险

### 🔴 高风险

#### 1. **Secret Redaction 默认开启 → 数据路径可能被脱敏**
**风险：** 你的 HTML 报告生成脚本可能依赖 `read_file` 返回的完整路径来构建 `MEDIA:` 标签，脱敏后路径显示为 `***`。

**检测：**
```bash
hermes config get security.redact_secrets
```

**缓解：**
```bash
hermes config set security.redact_secrets false   # 如确认无敏感数据
# 或在脚本中使用绝对路径常量，不从工具输出中提取
```

#### 2. **Context Compressor 变更 → 长会话行为变化**
**风险：**
- 系统提示 + 工具 schema 现在计入压缩触发阈值 → **长会话可能更频繁触发压缩**
- Tail 保护修复后，短对话的压缩行为变化 → **可能影响多轮分析的上下文连续性**
- 语言感知摘要可能改变中文内容的压缩方式

**检测：** 观察长会话（>30 轮）是否出现「突然忘记前文任务」现象。

**缓解：**
```yaml
compression:
  enabled: true
  threshold: 0.50      # 可适当调高
  target_ratio: 0.20
```

#### 3. **Kanban Worker 工具集限制 → 子 Agent 权限变化**
**风险：** 如果你计划用 Kanban 编排调研工作流，worker 默认只能访问 `kanban_*` 工具集，无法调用 `web_search`、`read_file` 等。

**缓解：**
```yaml
# 在 task skills 中显式声明需要的工具集
# 注意：kanban 现在会 reject 工具集名称（只允许 skill 名称）
```

**重要变更：** Kanban 现在 **reject toolset names in task skills**，只允许 skill 名称。如果你的工作流依赖在 kanban task 中直接指定 `web` 或 `file` 工具集，需要改为指定包含这些工具的 skill。

#### 4. **Delegate Task 继承规则变化**
**风险：**
- `inherit_mcp_toolsets` 现在默认 `true` → 子 Agent 自动继承 MCP 工具，可能增加 token 开销
- `fallback_chain` 现在继承自 parent → 子 Agent 的 fallback 行为可能与你预期不同
- `acp_command` 在 `override_provider` 设置时自动清除

**检测：**
```bash
hermes config get delegation
```

#### 5. **File Tools 路径解析变更**
**风险：**
- `read_file` 现在限制结果大小 → 超大 JSONL/Excel 文件可能被截断
- `search_files` 路径/行号冲突修复 → 连字符数字文件名（如 `2024-01-data.jsonl`）的行为可能变化
- `write_file` + `patch` 后自动 lint → 如果写入的 JSON 有语法错误，现在会**阻塞并报错**，而不是静默写入

**缓解：**
```python
# 在写入前主动验证 JSON
import json
json.dumps(data, ensure_ascii=False)  # 提前捕获错误
```

---

### 🟡 中风险

#### 6. **Session Search 行为变化**
- 现在按 `last_active` 排序而非开始时间 → `/resume` 和 `-c` 的行为变化
- CJK 查询现在走三元组 FTS5 → 中文搜索更精确，但可能遗漏某些变体

#### 7. **Honcho 记忆系统重构**
- 如果使用了 Honcho 作为 memory provider，5-tool 表面和会话隔离可能导致跨会话记忆行为变化
- `pin_peer_name` 需要显式 `strict: True`

#### 8. **Cron Job 环境隔离增强**
- Cron job 现在明确区分 gateway context → 如果你的 cron job 依赖 gateway 的会话状态，可能失效
- `context_from` 链式执行是新增功能，但旧 cron job 不会自动受益

#### 9. **TUI/CLI 快捷键变更**
- `Ctrl+Enter` 现在统一为换行（WSL/SSH/Windows Terminal）
- `Shift+Enter` 也支持换行
- 如果你习惯了旧版的行为，可能需要适应

#### 10. **Skills 平台 Frontmatter 过滤**
- 142 个技能现在声明了平台兼容性 → 某些技能在特定平台（如 Windows）可能被自动隐藏
- 你的自定义技能如果没有 `platforms` frontmatter，可能在某些平台不加载

---

### 🟢 低风险（了解即可）

- **模型列表刷新**：OpenRouter/Nous 的推荐模型列表定期更新，不影响已有配置
- **Provider 别名规范化**：`alibaba_coding` 等别名变更，不影响已有 `.env`
- **Docker 镜像优化**：层缓存改进，不影响本地使用
- **文档结构重组**：技能文档分类调整，不影响功能

---

## 四、建议的升级前检查清单

```bash
# 1. 备份当前配置
hermes backup --quick

# 2. 检查关键配置项
hermes config get security.redact_secrets
hermes config get compression.threshold
hermes config get delegation.inherit_mcp_toolsets
hermes config get kanban.max_spawn

# 3. 验证自定义技能的平台声明
grep -l "^platforms:" ~/.hermes/skills/*/SKILL.md || echo "部分技能缺少 platforms frontmatter"

# 4. 测试关键工作流（升级后）
# - 长会话（>30 轮）上下文连续性
# - write_file 后 JSON 验证行为
# - delegate_task 子 Agent 工具集继承
# - read_file 大文件截断行为

# 5. 更新
hermes update --yes
```

---

## 五、版本时间线

| 版本 | 日期 | 关键里程碑 |
|------|------|-----------|
| v0.9.0 | 2026.4.13 | TUI Ink 重构、Dashboard 初版、Kanban 引入 |
| v0.10.0 | 2026.4.16 | 插件系统、主题系统、i18n、Tool Gateway |
| v0.11.0 | 2026.4.23 | Cron No-Agent、Skills Hub、TUI 性能优化 |
| v0.12.0 | 2026.4.30 | Curator、Profile 分发、ComfyUI、Computer Use |
| v0.13.0 | 2026.5.7 | 当前版本 |
| v0.13.0+ | 2026.5.7~ | 1018 commits，包含上述全部更新 |

---

## 六、核心风险速查表

| 风险项 | 概率 | 影响 | 缓解措施 |
|--------|------|------|----------|
| Secret Redaction 隐藏数据路径 | 中 | 高 | 关闭 redaction 或改用常量路径 |
| Compressor 频繁压缩打断分析 | 中 | 高 | 调高 threshold |
| Kanban Worker 工具集限制 | 高 | 中 | 改用 skill 名称而非 toolset 名称 |
| File Lint 阻塞写入 | 低 | 中 | 写入前主动验证 JSON |
| Delegate fallback 继承变化 | 低 | 中 | 显式配置子 Agent fallback |
| Session Search 排序变化 | 低 | 低 | 适应 last_active 排序 |
| TUI 快捷键变化 | 低 | 低 | 使用 Ctrl+Enter 换行 |

---

> **总体建议：** 这次更新量极大（1018 commits），核心架构（插件系统、Kanban、Curator、Compressor）均有显著变化。建议先备份配置，在隔离环境中验证关键工作流后再升级。Kanban Orchestrator 模式对你的两阶段调研工作流有潜在巨大价值，值得投入时间学习。
