# Hermes Agent v0.13.0 更新审查报告

**审查范围**: v0.13.0 (2026.5.7) → HEAD  
**Commit 数量**: 633 commits（其中 630 个 feat/fix 级别变更）  
**生成时间**: 2026-05-25  
**你的当前版本**: v0.13.0 (2026.5.7) — 落后 1399 commits

---

## 一、与你工作流高度相关的功能变更

### 1. Claude Prompt Cache 跨会话前缀缓存 ⭐⭐⭐⭐⭐
- **Commit**: `7b7636655` feat(prompt-cache): cross-session 1h prefix cache for Claude
- **影响**: 使用 Claude (Anthropic / OpenRouter / Nous Portal) 时，系统提示词（包括 skills、memory）现在跨会话缓存 1 小时
- **对你的意义**: 
  - 你的两阶段调研工作流（场景分析→深度分析）如果共享相似系统提示，后续会话启动更快
  - 但注意：缓存命中率取决于提示词前缀一致性，如果你频繁切换 skills 或修改 system prompt，缓存会失效
- **风险**: 无直接风险，纯性能优化

### 2. Secret Redaction 默认开启 ⚠️⚠️⚠️⚠️⚠️
- **Commit**: `fb1ce793e` feat(security): enable secret redaction by default
- **影响**: 所有工具输出中的敏感信息（API keys、tokens、密码、MEDIA 路径）默认被脱敏处理
- **对你的意义**:
  - **直接影响你**: 你之前遇到的 "MEDIA 路径在报告中显示为 [REDACTED]" 问题现在成为默认行为
  - 你的 HTML 报告如果依赖嵌入的本地文件路径（如 `MEDIA:/Users/zhijian/...`），这些路径在输出中会被隐藏
- **风险**: **高** — 如果你需要报告中的真实路径用于验证或分享，需要显式配置 `security.redaction_enabled: false` 或使用 `[[as_document]]` 指令
- **应对**: 在 `~/.hermes/config.yaml` 中检查 `security.redaction_enabled` 设置

### 3. Context Compressor 状态可视化 ⭐⭐⭐⭐
- **Commit**: `103e11926` feat(cli): show context compression count in status bar
- **影响**: CLI/TUI 状态栏现在显示压缩次数（🗜️ emoji）
- **对你的意义**: 你的长会话（两阶段调研通常 20+ 轮）现在可以直观看到压缩触发频率
- **风险**: 无，纯可视化改进

### 4. Kanban Orchestrator 重大升级 ⭐⭐⭐⭐⭐
多个相关 commits，核心变更：
- `236cbe16b` feat(kanban): add orchestrator board tools — 编排器获得看板路由工具
- `24d48ffb8` feat(kanban): add `specify` — 辅助 LLM 自动细化 triage 任务
- `6e5c49bdc` refactor(kanban-orchestrator): drop hardcoded specialist roster, add Step-0 profile discovery
- **影响**: 
  - 编排器不再使用硬编码专家列表，改为 Step-0 自动发现可用能力
  - 新增 `specify` 工具，可以让辅助模型自动将模糊任务拆分为具体子任务
- **对你的意义**: 
  - 你的两阶段调研工作流可以更好地映射到 Kanban：Phase 1（场景分析）→ Phase 2（深度分析）作为依赖任务链
  - `specify` 可以自动细化 "分析小红书数据" 为具体的数据清洗、关键词提取、场景分类等子任务
- **风险**: 中等 — 编排器行为变化可能导致现有 board 配置不兼容

### 5. File Tools 自动 Lint 检查 ⭐⭐⭐⭐
- **Commit**: 多个相关修复（`f6736ced8`, `4c57a5b31` 等）
- **影响**: `write_file` 和 `patch` 工具现在自动检查语法错误（Python/JSON/YAML/TOML 等）
- **对你的意义**: 
  - 你生成 HTML 报告时，如果内嵌的 JSON 数据有语法错误，工具会立即报错而不是静默失败
  - 但这也意味着某些"故意不完整"的写入会被拒绝
- **风险**: 低 — 主要是质量提升，但可能需要适应新的错误提示

### 6. Browser Tool 180x 性能提升 ⭐⭐⭐⭐
- **Commit**: `d4b26df89` perf(browser): route browser_console eval through supervisor's persistent CDP WS (180x faster)
- **影响**: `browser_console` 的 JavaScript 执行速度提升 180 倍
- **对你的意义**: 如果你用 browser 工具做网页数据抓取（如小红书网页版），JavaScript 交互现在极快
- **风险**: 无

### 7. Vision 工具返回像素数据给视觉模型 ⭐⭐⭐⭐
- **Commit**: `3800972dd` feat(vision): vision_analyze returns pixels to vision-capable models, not aux text
- **影响**: `vision_analyze` 现在将原始像素数据传递给支持视觉的模型，而不是生成文本描述
- **对你的意义**: 如果你分析截图、图表、UI 设计稿，视觉模型（如 Claude 3.5 Sonnet、GPT-4V）可以直接"看到"图像内容
- **风险**: 无，但注意 token 消耗可能增加

### 8. Computer Use (CUA) 后端 ⭐⭐⭐⭐⭐
- **Commit**: `850413f12` feat(computer-use): cua-driver backend, universal any-model schema
- **影响**: 新增 Computer Use Agent 后端，支持任何模型进行计算机控制
- **对你的意义**: 如果你需要自动化操作 macOS 桌面（如批量处理文件、截图分析），现在可以通过 `computer_use` 工具实现
- **风险**: 中等 — 这是一个全新的大功能，可能存在稳定性问题

### 9. Goals (/goal) 系统改进 ⭐⭐⭐
- **Commit**: `404640a2b` feat(goals): /goal checklist + /subgoal user controls
- **影响**: `/goal` 命令新增清单和子目标控制（但随后被 `3e7145e0b` revert 回滚）
- **当前状态**: 该功能在最新代码中被回滚，可能仍在迭代中
- **风险**: 如果你之前使用 `/goal`，注意该功能可能不稳定

### 10. 新增 /handoff 跨平台会话转移 ⭐⭐⭐⭐
- **Commit**: `878611a79` feat(session): add /handoff command for cross-platform session transfer
- **影响**: 可以将当前会话从 CLI 转移到 Telegram/Discord 等平台，反之亦然
- **对你的意义**: 如果你在 WebUI 中开始一个调研任务，可以无缝转移到手机 Telegram 上继续
- **风险**: 低

---

## 二、安全相关的重要变更

### 1. Secret Redaction 默认开启（已在上文详述）
### 2. Sudo 密码猜测阻断
- **Commit**: `9520a1ccd` fix(terminal): block sudo -S password guessing when SUDO_PASSWORD is not set
- **影响**: 终端工具不再尝试猜测 sudo 密码
- **风险**: 如果你的工作流依赖自动 sudo，可能需要设置 `SUDO_PASSWORD` 环境变量

### 3. Discord 角色权限修复（CVSS 8.1）
- **Commit**: `ef1e56557` fix(discord): scope DISCORD_ALLOWED_ROLES to originating guild
- **影响**: 修复了 Discord 角色权限跨 Guild 泄漏的安全漏洞
- **风险**: 如果你使用 Discord 集成，需要检查角色配置

### 4. Teams 审批按钮白名单
- **Commit**: `b739fcdfc` fix(security): require explicit allowlist or TEAMS_ALLOW_ALL_USERS opt-in for Teams approval buttons
- **影响**: Teams 平台的审批按钮现在需要显式白名单
- **风险**: 如果你使用 Teams 集成，需要配置 `TEAMS_ALLOW_ALL_USERS=1` 或设置白名单

### 5. Webhook 安全加固
- **Commit**: `fb4f95356` fix: block INSECURE_NO_AUTH on non-localhost webhook bindings
- **影响**: Webhook 不再允许非 localhost 的无认证访问
- **风险**: 如果你使用 webhook 接收外部通知，需要配置认证

---

## 三、模型与推理相关变更

### 1. 新增模型支持
- **Codex Spark**: `dcc8de83a` feat(codex): add gpt-5.3-codex-spark model
- **Tencent hy3-preview**: `2c1921241` feat(models): add paid tencent/hy3-preview route on OpenRouter
- **Alibaba Coding Plan**: `8ad117a3d` fix(models): add alibaba-coding-plan to _PROVIDER_MODELS
- **Kimi K2.6**: `91eef6255` fix: correct context-length resolution for kimi-k2.6

### 2. 推理参数传递
- **Commit**: `cd712b176` feat(transports/codex): pass reasoning.effort to xAI Responses API
- **影响**: xAI (Grok) 模型的 reasoning effort 参数现在正确传递
- **Commit**: `d6e1fadbf` fix(xai): omit reasoning.effort for grok models that reject it
- **影响**: 部分 Grok 模型会拒绝 reasoning.effort，现在自动跳过

### 3. 上下文长度修复
- **Commit**: `a78e622df` fix(agent): honor configured model max tokens
- **影响**: 现在正确尊重配置的 max_tokens，而不是使用硬编码值
- **风险**: 如果你之前依赖默认的 max_tokens，现在可能需要显式配置

---

## 四、平台与 Gateway 变更

### 1. Telegram 多项改进
- **Draft 流式传输**: `4ed293b38` feat(telegram): native draft streaming via sendMessageDraft (Bot API 9.5+)
- **通知模式**: `236f3b052` feat(gateway): add Telegram notification mode to suppress intermediate push notifications
- **消息分割**: `bf1f40996` fix(telegram): split-and-deliver oversized edits instead of silent truncation
- **白名单**: `69d025e4a` feat(gateway): add allowed_chats whitelist

### 2. 新增平台支持
- **LINE Messaging**: `50f9fee98` feat(gateway): add LINE Messaging API platform plugin
- **Google Chat**: `44cd79e79` feat(plugins/google_chat): Google Chat platform adapter
- **QQ Bot**: `de584cd1d` feat(qqbot): add inline-keyboard approvals and update prompts

### 3. Gateway 自动恢复
- **Commit**: `fad684b1f` feat(gateway): auto-resume interrupted sessions after restart
- **影响**: Gateway 重启后自动恢复中断的会话
- **风险**: 低，但注意恢复状态可能不完全一致

### 4. 会话转移
- **Commit**: `00ce5f04d` feat(session): make /handoff actually transfer the session live
- **影响**: 真正的实时会话转移（不仅仅是复制历史）

---

## 五、工具与 Skills 变更

### 1. 新增 Skills
- **Stocks & Finance**: `896a7ce26` feat: add stocks & finance skill (Yahoo Finance, no API key)
- **API Testing**: `4c57a5b31` feat(skills): add api-testing optional skill
- **Watchers**: `ea8e60882` feat(skills): watchers skill — poll RSS / HTTP JSON / GitHub via cron

### 2. Skills 平台声明
- **Commit**: `98db898c0` feat(skills): declare platforms frontmatter for all 79 undeclared built-in skills
- **影响**: 所有 skills 现在声明支持的平台（Linux/macOS/Windows）
- **风险**: 部分 skills 在 Windows 上被自动禁用

### 3. MCP 支持增强
- **SSE Transport**: `12289c263` feat: add SSE transport support for MCP client
- **OAuth 持久化**: `c4a799231` fix(mcp-oauth): persist OAuth server metadata across process restarts
- **Image 结果**: `c8e3e3918` fix(mcp): surface image tool results as MEDIA tags

---

## 六、CLI 与 TUI 改进

### 1. CJK / 宽字符表格对齐
- **Commit**: `1d0071675` fix(cli,tui): align CJK / wide-char markdown tables
- **影响**: 中文表格在终端中现在正确对齐
- **对你的意义**: 你的中文报告中的表格在 CLI 中显示更美观

### 2. Markdown 链接解析
- **Commit**: `75b428c85` feat(ui-tui): resolve markdown links to readable page titles
- **影响**: TUI 中的 markdown 链接现在显示为可读的页面标题

### 3. 按键改进
- **Shift+Enter**: `f5b635f6a` feat(cli): recognise Shift+Enter as a newline key
- **Ctrl+Enter**: `d1838041e` feat: Ctrl+Enter inserts newline on Windows Terminal
- **右键复制**: `a2920b176` fix(tui): right-click copies selection, only pastes when no selection

### 4. 性能优化
- **冷启动**: `0ec052ca2` perf(cli): cut ~19s from 'hermes' cold start
- **Dashboard 滚动**: `7cbef2bd4` fix(dashboard): route browser wheel into inner TUI scrolling

---

## 七、工作连续性风险评估

| 风险等级 | 变更 | 影响描述 | 应对措施 |
|---------|------|---------|---------|
| 🔴 **极高** | Secret Redaction 默认开启 | 你的 HTML 报告中的 MEDIA 路径被隐藏，可能导致报告无法正确显示嵌入文件 | 在 `config.yaml` 中设置 `security.redaction_enabled: false` 或使用 `[[as_document]]` 指令 |
| 🟠 **高** | Kanban Orchestrator 重构 | 编排器行为变化，现有 board 配置可能不兼容 | 测试现有 board，必要时重新配置 |
| 🟠 **高** | Computer Use (CUA) 新功能 | 全新大功能，可能存在稳定性问题 | 谨慎使用，不要在生产环境依赖 |
| 🟡 **中** | Goals (/goal) 回滚 | 该功能被回滚，如果之前使用会失效 | 等待稳定版本再使用 |
| 🟡 **中** | File Tools 自动 Lint | 某些"故意不完整"的写入会被拒绝 | 确保写入的内容语法正确 |
| 🟡 **中** | max_tokens 配置生效 | 之前可能依赖默认值，现在需要显式配置 | 检查 `config.yaml` 中的 `max_tokens` 设置 |
| 🟢 **低** | Claude Prompt Cache | 纯性能优化，无兼容性问题 | 无需操作 |
| 🟢 **低** | Browser Tool 180x 提升 | 纯性能优化 | 无需操作 |
| 🟢 **低** | Vision 工具返回像素 | 功能增强 | 注意 token 消耗 |

---

## 八、建议关注的具体功能

### 立即可用的改进（无风险）
1. **Claude Prompt Cache** — 你的长会话启动更快
2. **Browser Tool 180x 提升** — 网页抓取更快
3. **CJK 表格对齐** — 中文报告更美观
4. **Context Compressor 可视化** — 直观看到压缩频率

### 需要配置调整的功能
1. **Secret Redaction** — 如果你需要报告中的真实路径，立即调整配置
2. **max_tokens** — 检查是否配置了合适的值

### 值得尝试的新功能
1. **Kanban Orchestrator + specify** — 将你的两阶段调研映射为自动化流水线
2. **Computer Use** — 如果你需要桌面自动化
3. **Vision 工具像素返回** — 如果你分析图像内容

### 建议等待的功能
1. **Goals (/goal)** — 已被回滚，等待稳定

---

## 九、升级建议

### 立即执行
```bash
# 1. 备份当前配置
cp ~/.hermes/config.yaml ~/.hermes/config.yaml.backup

# 2. 更新 hermes
hermes update

# 3. 检查 Secret Redaction 设置，根据需要调整
grep redaction ~/.hermes/config.yaml

# 4. 验证关键功能
hermes --version
```

### 升级后验证清单
- [ ] HTML 报告中的 MEDIA 路径是否正确显示
- [ ] 现有的 Kanban board 是否正常工作
- [ ] 长会话的启动速度是否有提升
- [ ] File Tools 的自动 lint 是否影响你的工作流

---

*报告基于 630 个 feat/fix 级别 commits 分析生成，排除了 chore/test/docs/refactor 等次要变更。*
