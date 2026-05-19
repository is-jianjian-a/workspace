# MediaCrawler 正确使用指南

## 问题复盘

### 之前遇到的问题
1. Chrome 后台启动方式错误（使用了 & 被系统阻止）
2. CDP 连接 404 错误（使用了错误的 WebSocket 端点）
3. 登录状态丢失（使用了全新的 user-data-dir）
4. 陷入重复执行的循环

## 正确方案

### 方案一：复用现有 Chrome 登录状态（推荐）

**前提条件**：Chrome 已经在运行，且已登录小红书/抖音等平台

**步骤**：

1. **在 Chrome 中开启远程调试**（只需一次）
   - 在 Chrome 地址栏输入：`chrome://inspect/#remote-debugging`
   - 勾选 "Allow remote debugging for this browser instance"
   - 确认显示 `Server running at: 127.0.0.1:9222`

2. **验证端口是否可用**
   ```bash
   curl http://localhost:9222/json/version
   ```

3. **运行 MediaCrawler**
   ```bash
   cd /Users/zhijian/workspace/MediaCrawler-main
   python3 main.py --platform xhs --lt cookie --crawler-type search --keywords "美食探店" --get-comment yes
   ```

**优点**：
- 复用已有登录状态，无需重新登录
- 保留所有 Cookie、扩展和浏览历史
- 反检测效果最好

### 方案二：二维码登录

**适用场景**：没有现有 Chrome 登录状态，或想使用新账号

**步骤**：

1. **关闭现有 Chrome**
   ```bash
   pkill -x "Google Chrome"
   ```

2. **启动带调试的 Chrome**（使用默认用户数据目录）
   ```bash
   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
     --remote-debugging-port=9222 \
     --no-first-run \
     --no-default-browser-check
   ```

3. **运行 MediaCrawler 使用二维码登录**
   ```bash
   cd /Users/zhijian/workspace/MediaCrawler-main
   python3 main.py --platform xhs --lt qrcode --crawler-type search --keywords "美食探店"
   ```

4. **扫码登录**
   - MediaCrawler 会显示二维码
   - 使用小红书/抖音 App 扫码
   - 登录状态会自动保存

### 方案三：手动提供 Cookie

**步骤**：

1. **从浏览器导出 Cookie**
   - 使用 EditThisCookie 等扩展
   - 或手动从开发者工具复制

2. **设置 Cookie**
   - 修改 `config/base_config.py` 中的 `COOKIES` 变量
   - 或使用环境变量

3. **运行**
   ```bash
   python3 main.py --platform xhs --lt cookie --cookies "your_cookie_string"
   ```

## 配置说明

### 关键配置项（config/base_config.py）

```python
# 启用 CDP 模式（连接现有浏览器）
ENABLE_CDP_MODE = True

# 连接现有浏览器（而不是启动新的）
CDP_CONNECT_EXISTING = True

# 调试端口
CDP_DEBUG_PORT = 9222

# 是否保存登录状态
SAVE_LOGIN_STATE = True

# 数据保存格式
SAVE_DATA_OPTION = "json"  # 可选: csv, json, jsonl, sqlite, db

# 是否抓取评论
ENABLE_GET_COMMENTS = True

# 每篇笔记最大评论数
CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES = 10
```

## 平台代号对照

| 平台 | 代号 | 登录方式 |
|------|------|----------|
| 小红书 | xhs | qrcode / phone / cookie |
| 抖音 | dy | qrcode / phone / cookie |
| 快手 | ks | qrcode / phone / cookie |
| B站 | bili | qrcode / phone / cookie |
| 微博 | wb | qrcode / phone / cookie |
| 贴吧 | tieba | qrcode / cookie |
| 知乎 | zhihu | qrcode / phone / cookie |

## 常用命令

```bash
# 小红书搜索
python3 main.py --platform xhs --lt qrcode --crawler-type search --keywords "美食探店"

# 抖音搜索
python3 main.py --platform dy --lt qrcode --crawler-type search --keywords "美食探店"

# 微博搜索（无需登录）
python3 main.py --platform wb --lt cookie --crawler-type search --keywords "美食探店"

# 指定帖子详情
python3 main.py --platform xhs --lt cookie --crawler-type detail --specified-id "帖子ID"

# 创作者主页
python3 main.py --platform xhs --lt cookie --crawler-type creator --creator-id "创作者ID"
```

## 数据输出

抓取的数据保存在 `data/` 目录：
- `json/` - JSON 格式
- `csv/` - CSV 格式
- `sqlite/` - SQLite 数据库

数据包含：
- 帖子/视频信息（标题、内容、作者、点赞数等）
- 评论内容（用户、内容、时间、点赞数）
- 二级评论（如果启用）

## 注意事项

1. **频率控制**：默认有 2 秒间隔，避免被封
2. **登录状态**：Cookie 可能过期，需要定期更新
3. **IP 代理**：可配置代理池避免被封
4. **反检测**：CDP 模式大幅降低检测风险

## 故障排除

### CDP 连接失败
- 确保 Chrome 已开启远程调试
- 检查端口 9222 是否被占用
- 查看 Chrome 是否有确认对话框

### 登录失败
- 检查 Cookie 是否过期
- 尝试二维码登录
- 确认账号没有被封

### 抓取失败
- 检查网络连接
- 确认目标平台可访问
- 查看日志了解具体错误
