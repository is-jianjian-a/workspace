# 舆情监控专家 - 完整技能体系与监控通道

## 一、ClawHub 已吸收技能（按优先级排序）

### P0 - 核心监控技能（已验证可用）

#### 1. Xpoz Social Search (@atyachin)
- **安装**: `clawhub install xpoz-social-search`
- **下载量**: 2.7k | **收藏**: 7 | **安全**: VirusTotal Benign
- **覆盖平台**: Twitter (1B+), Instagram (400M+), Reddit (100M+)
- **核心能力**:
  - 实时搜索帖子、话题标签、用户
  - 按关键词、日期范围筛选
  - 用户画像查询（按用户名/ID）
  - 子版块发现（Reddit）
- **工具列表**:
  - `getTwitterPostsByKeywords` - Twitter搜索
  - `getInstagramPostsByKeywords` - Instagram搜索
  - `getRedditPostsByKeywords` - Reddit搜索
  - `getTwitterUsersByKeywords` - 发现Twitter用户
  - `getInstagramUsersByKeywords` - 发现Instagram用户
  - `getRedditUsersByKeywords` - 发现Reddit用户
  - `getTwitterUser` - Twitter用户画像
  - `getInstagramUser` - Instagram用户画像
  - `getRedditUser` - Reddit用户画像
  - `searchTwitterUsers` - Twitter用户名搜索
  - `getRedditSubredditsByKeywords` - 发现子版块
  - `checkOperationStatus` - 轮询结果
- **使用场景**: 品牌提及搜索、竞品监控、KOL发现

#### 2. Social Sentiment (@atyachin)
- **安装**: `clawhub install social-sentiment`
- **下载量**: 3.9k | **收藏**: 4 | **安全**: VirusTotal Suspicious（需审查）
- **覆盖平台**: Twitter, Reddit, Instagram
- **核心能力**:
  - 品牌情感分析（正面/负面/中性）
  - 公关危机检测
  - 批量分析 1K-70K 帖子
  - CSV导出 + Python/pandas分析
  - 主题提取、病毒式投诉识别
- **4步工作流**:
  1. 搜索平台（多关键词组合）
  2. 下载CSV（最多64K行）
  3. Python情感分析（可自定义关键词）
  4. 生成报告（情感分数0-100）
- **使用场景**: 品牌声誉评估、危机预警、竞品对比

#### 3. Social Intelligence (@atyachin)
- **安装**: `clawhub install social-intelligence`
- **下载量**: 1.8k | **收藏**: 5 | **安全**: VirusTotal Benign
- **覆盖平台**: Twitter, Instagram, Reddit
- **核心能力**:
  - 综合社交情报平台
  - 专家发现、潜在客户生成
  - 品牌监控、情感分析
  - KOL发现（按内容质量而非粉丝数）
  - 数据导出（每次搜索最多64K行）
- **子技能**:
  - `xpoz-social-search` - 核心搜索
  - `expert-finder` - 专家发现
  - `lead-generation` - 潜在客户
  - `social-sentiment` - 情感分析
- **使用场景**: 综合情报分析、B2B舆情、行业专家监控

### P1 - 辅助监控技能

#### 4. Sentiment Tracker (@ivangdavila)
- **安装**: `clawhub install sentiment-tracker`
- **下载量**: 778 | **收藏**: 2 | **安全**: VirusTotal Benign
- **覆盖平台**: Twitter/X, Reddit, YouTube, Hacker News, 新闻网站
- **核心能力**:
  - 多实体仪表板对比
  - 自动化定时追踪
  - 负面 spikes 预警（>20%基线）
  - 病毒式负面帖子检测（>10x正常互动）
  - 本地数据存储（~/sentiment-analysis/）
- **数据源多样性原则**:
  - Twitter/X: 实时、情绪化、病毒内容
  - Reddit: 深度讨论、真实意见、小众社区
  - YouTube: 产品体验评论
  - Hacker News: 技术导向、怀疑态度、早期采用者
  - 新闻网站: 官方叙事、PR过滤
- **使用场景**: 长期品牌监控、自动化预警、多品牌对比

### P2 - 运营辅助技能（非核心监控）

#### 5. Social Media Agent (@psmamm)
- **安装**: `clawhub install social-media-agent`
- **下载量**: 8.9k | **收藏**: 11
- **能力**: Twitter自动化发帖、内容生成、互动追踪
- **用途**: 危机响应时的快速发声

#### 6. Social Media Scheduler (@1kalin)
- **安装**: `clawhub install social-media-scheduler`
- **下载量**: 11k | **收藏**: 13
- **能力**: 内容日历、发布排期
- **用途**: 监控期间的声明发布管理

## 二、国内平台监控通道（需自建）

由于 ClawHub 无国内平台技能，需自建以下监控通道：

### 微博监控
```
数据源: 微博搜索API、微博超话、热门话题、微博热搜
监控维度:
  - 品牌提及量、转发量、评论量
  - 热搜关联度
  - KOL/大V发声
  - 情感倾向（正面/负面/中性）
技术方案:
  - 微博开放平台API（需申请）
  - Python + requests + BeautifulSoup（爬虫）
  - 微博超话监控
```

### 小红书监控
```
数据源: 小红书搜索、笔记内容、评论区、话题标签
监控维度:
  - 笔记提及量、点赞/收藏/评论数
  - 种草/拔草比例
  - 品牌关联度
  - 用户画像（年龄、地域、兴趣）
技术方案:
  - 逆向API分析
  - Python爬虫（需处理反爬）
  - 关键词监控
```

### 抖音监控
```
数据源: 抖音搜索、视频评论、话题挑战、直播间
监控维度:
  - 视频提及量、播放量、点赞/评论/转发
  - 评论区情感
  - 挑战赛参与
  - 直播间弹幕
技术方案:
  - 抖音开放平台API
  - 爬虫抓取（视频元数据+评论）
  - 关键词+话题监控
```

### B站监控
```
数据源: B站搜索、视频弹幕、评论区、专栏
监控维度:
  - 视频提及、播放量、弹幕密度
  - 弹幕情感分析
  - UP主评价
  - 专栏文章提及
技术方案:
  - B站API（bilibili-api-python）
  - 弹幕抓取（xml接口）
  - 评论爬虫
```

### 知乎监控
```
数据源: 知乎搜索、问题回答、专栏文章、想法
监控维度:
  - 问题提及、回答数、赞同数
  - 回答情感分析
  - 专业度评价
  - 高赞回答监控
技术方案:
  - 知乎API（有限）
  - Python爬虫（需登录态）
  - 关键词+话题监控
```

### 微信公众号监控
```
数据源: 搜狗微信搜索、新榜、清博大数据
监控维度:
  - 文章提及、阅读量、点赞数
  - 公众号影响力
  - 文章情感分析
技术方案:
  - 搜狗微信搜索爬虫
  - 新榜API（付费）
  - 清博大数据（付费）
```

### 其他国内平台
```
快手: 视频搜索+评论监控
贴吧: 帖子搜索+回复监控
豆瓣: 小组讨论+话题监控
虎扑: 社区帖子+评论监控
脉脉: 职场话题+公司评价监控
36氪/虎嗅: 科技媒体报道监控
```

## 三、国际平台补充监控

### 已覆盖（通过ClawHub技能）
- Twitter/X: Xpoz Social Search, Social Sentiment
- Reddit: Xpoz Social Search, Social Sentiment
- Instagram: Xpoz Social Search
- YouTube: Sentiment Tracker

### 需补充
```
Discord:
  - 服务器监控（需邀请Bot）
  - 关键词提及追踪
  - 情感分析

Telegram:
  - 频道监控（公开频道）
  - 群组消息追踪
  - 机器人消息抓取

Facebook:
  - 公开帖子搜索
  - 群组监控（需加入）
  - 评论情感分析

LinkedIn:
  - 帖子提及监控
  - 行业讨论追踪
  - 专业评价分析

TikTok（国际版）:
  - 视频搜索+评论
  - 话题挑战监控
  - 与抖音数据对比
```

## 四、整合监控架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    舆情监控指挥中心                              │
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
  │ 国内平台   │    │  国际平台    │    │  数据存储  │
  │ 监控集群   │    │  监控集群    │    │  + 分析   │
  └─────┬─────┘    └──────┬──────┘    └─────┬─────┘
        │                 │                 │
  ┌─────▼─────────────────▼─────────────────▼─────┐
  │              统一数据管道                      │
  │  采集 → 清洗 → 标准化 → 情感分析 → 存储 → 预警 │
  └───────────────────────────────────────────────┘
```

### 数据流
```
1. 采集层: 各平台API/爬虫 → 原始数据
2. 清洗层: 去重、过滤、格式化
3. 分析层: 情感分析、主题提取、趋势识别
4. 存储层: 时序数据库 + 文档数据库
5. 应用层: 实时监控、预警通知、报告生成
```

## 五、技能使用优先级矩阵

| 场景 | 首选技能 | 次选技能 | 备注 |
|------|---------|---------|------|
| 实时品牌搜索 | Xpoz Social Search | Social Intelligence | 国际平台 |
| 情感分析 | Social Sentiment | Sentiment Tracker | 批量分析用前者 |
| 长期监控 | Sentiment Tracker | 自建脚本 | 自动化预警 |
| KOL发现 | Social Intelligence | Xpoz Social Search | 按内容质量排序 |
| 竞品对比 | Sentiment Tracker | Social Sentiment | 多实体仪表板 |
| 危机检测 | Social Sentiment | Sentiment Tracker | 实时+阈值预警 |
| 国内平台 | 自建监控通道 | - | 需开发 |

## 六、安装命令汇总

```bash
# P0 - 核心监控技能
clawhub install xpoz-social-search
clawhub install social-sentiment
clawhub install social-intelligence

# P1 - 辅助监控
clawhub install sentiment-tracker

# P2 - 运营辅助（可选）
clawhub install social-media-agent
clawhub install social-media-scheduler
```

## 七、安全注意事项

1. **Social Sentiment** 被标记为 Suspicious，使用前需审查代码
2. 所有 Xpoz 技能需要 `mcporter` 二进制文件
3. 安装前验证 npm 包来源
4. 国内平台爬虫需遵守 robots.txt 和平台规则
5. 敏感数据存储需加密

## 八、下一步行动

1. [ ] 安装并测试 P0 技能
2. [ ] 配置 Xpoz API 访问密钥
3. [ ] 开发国内平台监控脚本（微博、小红书、抖音、B站、知乎）
4. [ ] 建立统一数据管道
5. [ ] 配置预警阈值和通知渠道
6. [ ] 建立报告模板和自动化流程
