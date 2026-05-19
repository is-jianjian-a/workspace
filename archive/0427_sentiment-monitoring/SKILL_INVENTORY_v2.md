# 舆情监控专家 - 完整技能体系与监控通道（更新版）

## 一、ClawHub 已吸收技能（国际平台）

### P0 - 核心监控技能

#### 1. Xpoz Social Search (@atyachin)
- **安装**: `clawhub install xpoz-social-search`
- **下载量**: 2.7k | **收藏**: 7 | **安全**: Benign
- **覆盖平台**: Twitter (1B+), Instagram (400M+), Reddit (100M+)
- **核心能力**: 实时搜索、话题标签追踪、KOL发现、15亿+帖子索引

#### 2. Social Sentiment (@atyachin)
- **安装**: `clawhub install social-sentiment`
- **下载量**: 3.9k | **收藏**: 4 | **安全**: Suspicious（需审查）
- **覆盖平台**: Twitter, Reddit, Instagram
- **核心能力**: 品牌情感分析、公关危机检测、批量分析70K+帖子

#### 3. Social Intelligence (@atyachin)
- **安装**: `clawhub install social-intelligence`
- **下载量**: 1.8k | **收藏**: 5 | **安全**: Benign
- **覆盖平台**: Twitter, Instagram, Reddit
- **核心能力**: 综合社交情报、专家发现、KOL监控、数据导出

### P1 - 辅助监控技能

#### 4. Sentiment Tracker (@ivangdavila)
- **安装**: `clawhub install sentiment-tracker`
- **下载量**: 778 | **收藏**: 2 | **安全**: Benign
- **覆盖平台**: Twitter/X, Reddit, YouTube, Hacker News, 新闻网站
- **核心能力**: 多实体仪表板、自动化追踪、负面spikes预警

---

## 二、SkillHub 国内平台技能（按平台分类）

### 微博 (Weibo)

| 技能名称 | 下载量 | 收藏 | 来源 | 核心能力 |
|---------|--------|------|------|---------|
| **微博热搜采集** | 489 | 0 | ClawHub | 多频道热搜采集与可视化 |
| **微博热搜** | 346 | 0 | ClawHub | 获取热搜榜单，无需API Key |
| **微博热手** | 170 | 0 | SkillHub | 获取热搜榜，返回排名/标题/热度值 |
| **微博热搜榜数据** | 1.8k | 4 | ClawHub | 返回热搜标题、热度值、跳转链接 |
| **微博百度抖音热搜榜单** | 993 | 10 | ClawHub | 极速数据API，多平台热榜 |
| **每日热榜** | 5.8k | 5 | ClawHub | 54个平台热榜，含微博/知乎/B站/抖音 |
| **微博数据备份** | 31 | 0 | SkillHub | 备份收藏/发布内容，Markdown格式 |

**推荐首选**: `每日热榜` (5.8k下载) - 覆盖微博+多平台
**专用监控**: `微博热搜采集` - 多频道深度采集

### 小红书 (Xiaohongshu/RedNote)

| 技能名称 | 下载量 | 收藏 | 来源 | 核心能力 |
|---------|--------|------|------|---------|
| **小红书搜索建议关键词** | 4.5k | 4 | ClawHub | 搜索联想词收集、关键词调研 |
| **小红书舆情分析** | 3.6k | 5 | **SkillHub** | 搜索笔记、获取详情、评论、热点话题跟踪 |
| **小红书商业洞察与竞品分析** | 3.2k | 7 | **SkillHub** | 关键词搜索、笔记详情、爆款挖掘、竞品分析、KOL筛选 |
| **小红书议题报告** | 3.0k | 2 | ClawHub | 小红书热帖+媒体+Twitter三源交叉验证 |
| **小红书爆款图文写作** | 1.0万 | 7 | ClawHub | 爆款文案生成 |
| **小红书内容生成器** | 5.3k | 3 | ClawHub | 标题/正文/标签生成 |

**推荐首选**: `小红书舆情分析` (3.6k下载, SkillHub) - 直接支持舆情监控
**辅助分析**: `小红书商业洞察与竞品分析` (3.2k下载) - 竞品对标
**关键词挖掘**: `小红书搜索建议关键词` (4.5k下载) - 发现热门话题

### 抖音 (Douyin)

| 技能名称 | 下载量 | 收藏 | 来源 | 核心能力 |
|---------|--------|------|------|---------|
| **抖音下载器** | 6.8k | 6 | ClawHub | 视频下载、解析 |
| **抖音视频发布** | 5.9k | 3 | ClawHub | 浏览器自动化发布 |
| **抖音热榜** | 5.3k | 3 | ClawHub | 热榜/热搜数据，含视频/挑战赛/音乐 |
| **抖音视频智能助手** | 4.2k | 3 | ClawHub | 视频转录、总结 |
| **抖音搜索视频全量分析** | 3.6k | 2 | ClawHub | 扫码登录、批量搜索、报告生成 |
| **抖音违禁词检测** | 3.2k | 0 | ClawHub | 敏感词检测、离线词库 |
| **抖音文案一键提取** | 2.6k | 1 | **SkillHub** | 提取标题/简介/口播文案 |
| **抖音搜索关键词** | 1.8k | 2 | ClawHub | 视频/图文/用户多维度检索 |
| **抖音自动回复助手** | 2.3k | 4 | ClawHub | 评论监控、智能回复 |

**推荐首选**: `抖音热榜` (5.3k下载) - 热搜监控
**深度分析**: `抖音搜索视频全量分析` (3.6k下载) - 话题研究报告
**评论监控**: `抖音自动回复助手` (2.3k下载) - 评论监控+回复

### 知乎 (Zhihu)

| 技能名称 | 下载量 | 收藏 | 来源 | 核心能力 |
|---------|--------|------|------|---------|
| **知乎发帖** | 871 | 0 | ClawHub | 专栏文章/想法发布 |
| **知乎数据获取** | 745 | 0 | ClawHub | 三级认证降级、数据可靠获取 |
| **知乎草稿写手** | 321 | 0 | ClawHub | 热榜选题、AI生成回答 |
| **CN Web Search** | 7.1k | 20 | ClawHub | 聚合22+搜索引擎，含知乎 |
| **知乎写作助手** | 1.6k | 1 | ClawHub | 回答/文章/专栏生成 |
| **知乎** | 2.5k | 2 | ClawHub | API凭证管理、发布/点赞/评论 |
| **知乎热榜监控** | 1.6k | 0 | ClawHub | 热门话题、问题、趋势分析 |

**推荐首选**: `知乎热榜监控` (1.6k下载) - 热榜趋势
**数据获取**: `知乎数据获取` (745下载) - 可靠数据抓取
**综合搜索**: `CN Web Search` (7.1k下载) - 含知乎的聚合搜索

### B站 (Bilibili)

| 技能名称 | 下载量 | 收藏 | 来源 | 核心能力 |
|---------|--------|------|------|---------|
| **B站热门视频监控** | 1.0万 | 17 | ClawHub | 热门视频追踪 |
| **Bilibili All In One** | 8.3k | 6 | ClawHub | 综合B站工具 |
| **Bilibili & YouTube Watcher** | 2.8k | 6 | ClawHub | 双平台监控 |
| **B站视频-弹幕评论获取与深度分析** | 217 | 0 | **SkillHub** | 弹幕+评论获取+深度分析 |
| **B站视频弹幕与评论分析** | 133 | 0 | **SkillHub** | 弹幕评论分析 |
| **B站视频-弹幕舆情分析** | 106 | 0 | **SkillHub** | 弹幕舆情分析 |
| **B站-提取视频所有弹幕** | 70 | 0 | **SkillHub** | 弹幕提取 |
| **B站视频深度分析专家** | 152 | 0 | **SkillHub** | 视频深度分析 |

**推荐首选**: `B站热门视频监控` (1.0万下载) - 热门追踪
**舆情分析**: `B站视频-弹幕舆情分析` (106下载, SkillHub) - 弹幕情感分析
**深度分析**: `B站视频-弹幕评论获取与深度分析` (217下载, SkillHub) - 全量分析

### 今日头条 (Toutiao)

| 技能名称 | 下载量 | 收藏 | 来源 | 核心能力 |
|---------|--------|------|------|---------|
| **今日头条热榜** | 1.0k | 1 | ClawHub | 时政/财经/社会/科技/娱乐热榜 |
| **Toutiao News Trends** | 2.3k | 3 | ClawHub | 热点新闻、热度分数、标签 |
| **Url Reader** | 4.5k | 3 | ClawHub | 智能读取URL，支持今日头条 |
| **web-search** | 1.9k | 0 | ClawHub | 支持今日头条搜索 |
| **每日话题助手** | 595 | 0 | **SkillHub** | 聚合多平台热榜、智能筛选 |
| **Hot Topics** | 523 | 1 | ClawHub | 主流中文社交媒体热搜 |
| **新闻头条-聚合数据** | 349 | 0 | ClawHub | juhe.cn API实时查询 |

**推荐首选**: `今日头条热榜` (1.0k下载) - 热榜监控
**趋势分析**: `Toutiao News Trends` (2.3k下载) - 热度分数+标签

### 应用商店 (App Store)

| 技能名称 | 下载量 | 收藏 | 来源 | 核心能力 |
|---------|--------|------|------|---------|
| **App Store Optimization** | 2.4k | 4 | ClawHub | ASO关键词、竞品排名、元数据 |
| **ASO** | 1.0k | 4 | ClawHub | iOS/Android应用商店优化 |
| **competitive-teardown** | 153 | 0 | ClawHub | 整合应用商店评论+SEO+社交媒体 |
| **Niche Hunter App Store** | 267 | 1 | ClawHub | 应用商店市场情报、竞品分析 |
| **ASO Suite** | 272 | 1 | ClawHub | 跨设备ASO、热度/难度指标 |

**推荐首选**: `App Store Optimization` (2.4k下载) - 完整ASO工具包
**竞品分析**: `competitive-teardown` (153下载) - 整合评论+社交数据

---

## 三、跨平台综合技能

| 技能名称 | 下载量 | 收藏 | 来源 | 覆盖平台 |
|---------|--------|------|------|---------|
| **每日热榜** | 5.8k | 5 | ClawHub | 微博/知乎/B站/抖音等54平台 |
| **News Aggregator Skill** | 1.2万 | 22 | ClawHub | HN/GitHub/36Kr/腾讯/华尔街/V2EX/微博 |
| **Autoglm Browser Agent** | 2.3k | 1 | ClawHub | 微博/小红书/知乎/抖音/B站 |
| **CN Web Search** | 7.1k | 20 | ClawHub | 22+搜索引擎含知乎/公众号 |
| **Hot Topics** | 523 | 1 | ClawHub | 主流中文社交媒体热搜 |
| **每日话题助手** | 595 | 0 | **SkillHub** | 聚合多平台热榜 |

---

## 四、完整监控通道覆盖清单

### 国内平台（按优先级排序）

| 优先级 | 平台 | 监控技能 | 下载量 | 状态 |
|--------|------|---------|--------|------|
| P0 | 微博 | 微博热搜采集 + 每日热榜 | 489+5800 | 🟢 可用 |
| P0 | 小红书 | 小红书舆情分析 | 3600 | 🟢 可用 |
| P0 | 抖音 | 抖音热榜 + 搜索视频分析 | 5300+3600 | 🟢 可用 |
| P0 | 知乎 | 知乎热榜监控 + 数据获取 | 1600+745 | 🟢 可用 |
| P0 | B站 | B站热门视频监控 + 弹幕舆情 | 10000+106 | 🟢 可用 |
| P1 | 今日头条 | 今日头条热榜 + News Trends | 1000+2300 | 🟢 可用 |
| P1 | 微信公众号 | CN Web Search + 搜狗搜索 | 7100 | 🟡 间接 |
| P1 | 应用商店 | App Store Optimization | 2400 | 🟢 可用 |
| P2 | 快手 | 暂无专用技能 | - | 🔴 缺失 |
| P2 | 贴吧 | 暂无专用技能 | - | 🔴 缺失 |
| P2 | 豆瓣 | 暂无专用技能 | - | 🔴 缺失 |
| P2 | 虎扑 | 暂无专用技能 | - | 🔴 缺失 |
| P2 | 脉脉 | 暂无专用技能 | - | 🔴 缺失 |

### 国际平台

| 优先级 | 平台 | 监控技能 | 下载量 | 状态 |
|--------|------|---------|--------|------|
| P0 | Twitter/X | Xpoz Social Search + Social Sentiment | 2700+3900 | 🟢 可用 |
| P0 | Reddit | Xpoz Social Search + Social Sentiment | 2700+3900 | 🟢 可用 |
| P0 | Instagram | Xpoz Social Search + Social Intelligence | 2700+1800 | 🟢 可用 |
| P1 | YouTube | Sentiment Tracker + Bilibili Watcher | 778+2800 | 🟢 可用 |
| P2 | Discord | 暂无专用技能 | - | 🔴 缺失 |
| P2 | Telegram | 暂无专用技能 | - | 🔴 缺失 |
| P2 | Facebook | 暂无专用技能 | - | 🔴 缺失 |
| P2 | LinkedIn | 暂无专用技能 | - | 🔴 缺失 |

---

## 五、技能安装命令汇总

```bash
# === ClawHub 国际平台核心技能 ===
clawhub install xpoz-social-search          # Twitter/Instagram/Reddit搜索
clawhub install social-sentiment            # 情感分析（需审查安全）
clawhub install social-intelligence         # 综合社交情报
clawhub install sentiment-tracker           # 多平台情感追踪

# === SkillHub 国内平台核心技能 ===
# 微博
clawhub install weibo-trending              # 微博热搜采集
clawhub install daily-hot-news              # 每日热榜（54平台）

# 小红书
clawhub install xiaohongshu-yq              # 小红书舆情分析
clawhub install xiaohongshu-tool            # 商业洞察与竞品分析
clawhub install xhs-suggest-keywords        # 搜索建议关键词

# 抖音
clawhub install douyin-hot                  # 抖音热榜
clawhub install douyin-report-search        # 搜索视频全量分析
clawhub install douyin-auto-reply           # 评论监控

# 知乎
clawhub install zhihu-hot-cn                # 知乎热榜监控
clawhub install zhihu-data-fetcher          # 知乎数据获取

# B站
clawhub install bilibili-hot-monitor        # B站热门监控

# 今日头条
clawhub install toutiao-hot                 # 今日头条热榜
clawhub install toutiao-news-trends         # 热点趋势

# 应用商店
clawhub install app-store-optimization      # ASO优化

# === 跨平台综合技能 ===
clawhub install news-aggregator-skill       # 新闻聚合（含微博）
clawhub install cn-web-search               # 中文搜索（含知乎/公众号）
clawhub install hot-topics                  # 多平台热搜
```

---

## 六、监控架构建议

```
┌─────────────────────────────────────────────────────────────────┐
│                    舆情监控指挥中心                                │
│              (Sentiment Monitoring Hub)                         │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   实时预警    │  │   情感分析    │  │   报告生成    │          │
│  │   Engine     │  │   Engine     │  │   Engine     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└──────────────────────────┬──────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
  ┌─────▼─────┐    ┌──────▼──────┐    ┌─────▼─────┐
  │ 国内平台   │    │  国际平台    │    │  跨平台    │
  │ 监控集群   │    │  监控集群    │    │  聚合层    │
  └─────┬─────┘    └──────┬──────┘    └─────┬─────┘
        │                 │                 │
  ┌─────▼─────────────────▼─────────────────▼─────┐
  │              统一数据管道                        │
  │  采集 → 清洗 → 标准化 → 情感分析 → 存储 → 预警  │
  └─────────────────────────────────────────────────┘
```

---

## 七、安全注意事项

1. **Social Sentiment** 被标记为 Suspicious，使用前需审查代码
2. 所有 Xpoz 技能需要 `mcporter` 二进制文件
3. 安装前验证 npm 包来源
4. 国内平台爬虫需遵守 robots.txt 和平台规则
5. 敏感数据存储需加密

---

## 八、下一步行动

1. [ ] 安装并测试 P0 国内平台技能（微博/小红书/抖音/知乎/B站）
2. [ ] 安装并测试 P0 国际平台技能（Xpoz系列）
3. [ ] 配置各平台API访问密钥
4. [ ] 建立统一数据管道
5. [ ] 配置预警阈值和通知渠道
6. [ ] 建立报告模板和自动化流程
7. [ ] 补充缺失平台（快手/贴吧/豆瓣/虎扑/脉脉/Discord/Telegram）
