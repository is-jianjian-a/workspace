# 知乎VOC数据采集技术方案

## 1. 背景与挑战

### 知乎反爬机制
知乎采用 **ZSE (Zhihu Security Engine)** 反爬系统，所有未认证请求均被拦截：

| 端点 | 状态 | 错误码 | 说明 |
|------|------|--------|------|
| `www.zhihu.com/hot` | ❌ 403 | ZSE加密页面 | 返回 `zse-ck` 反爬脚本 |
| `/api/v3/feed/topstory/hot-lists` | ❌ 401 | AuthenticationError(101) | 需登录态 |
| `/api/v4/search_v3` | ❌ 400/403 | Bad Request | 需签名验证 |
| `/api/v4/topics/{id}/feeds` | ❌ 403 | Forbidden | 需认证 |
| 移动端API | ❌ 404 | Not Found | 端点已变更或需APP签名 |

**结论**: 直接抓取知乎不可行，需寻找替代数据源。

---

## 2. 推荐方案: justjavac 开源数据

### 2.1 数据源介绍

GitHub用户 **justjavac** 维护的知乎趋势数据项目，每小时自动抓取并归档：

| 项目 | 数据类型 | 字段 | 更新频率 | Stars |
|------|----------|------|----------|-------|
| [zhihu-trending-top-search](https://github.com/justjavac/zhihu-trending-top-search) | 知乎热搜榜 | `query_display`, `real_query` | 每小时 | 218 |
| [zhihu-trending-hot-questions](https://github.com/justjavac/zhihu-trending-hot-questions) | 知乎热门话题 | `title`, `url` | 每小时 | 198 |
| [zhihu-trending-hot-video](https://github.com/justjavac/zhihu-trending-hot-video) | 知乎热门视频 | `title`, `url` | 每小时 | 20 |

### 2.2 数据格式示例

**知乎热搜榜** (`raw/2026-05-06.json`):
```json
[
  {"query_display": "浏阳烟花厂爆炸致26死61伤", "real_query": "浏阳烟花厂爆炸致26死61伤"},
  {"query_display": "豆包付费版本曝光", "real_query": "豆包付费版本曝光"}
]
```

**知乎热门话题** (`raw/2025-05-12.json`):
```json
[
  {"title": "东航 MU5828 航班落地后安全出口被乘客打开...", "url": "https://www.zhihu.com/question/1904938806571917600"},
  {"title": "空战的时候可不可以先击落预警机?", "url": "https://www.zhihu.com/question/27704977"}
]
```

### 2.3 数据覆盖

- **历史范围**: 2020-11-24 至今（约1000天归档）
- **数据量**: 热搜榜17-50条/天，热门话题50+条/天
- **获取方式**: GitHub Raw CDN，无需认证
- **稳定性**: ⭐⭐⭐⭐⭐（持续运行5年+）

---

## 3. 实现代码

### 3.1 采集器核心代码

见 `/Users/zhijian/workspace/sentiment-monitoring/zhihu_collector.py`

```python
class ZhihuCollector:
    """知乎数据采集器 - 基于justjavac开源数据"""
    
    SOURCES = {
        "hot_search": {
            "url_template": "https://raw.githubusercontent.com/justjavac/"
                          "zhihu-trending-top-search/main/raw/{date}.json",
            "fields": ["query_display", "real_query"]
        },
        "hot_questions": {
            "url_template": "https://raw.githubusercontent.com/justjavac/"
                          "zhihu-trending-hot-questions/master/raw/{date}.json",
            "fields": ["title", "url"]
        }
    }
    
    def fetch_hot_search(self, date=None) -> List[Dict]:
        """获取知乎热搜榜"""
        
    def fetch_hot_questions(self, date=None) -> List[Dict]:
        """获取知乎热门话题"""
        
    def fetch_all(self, date=None) -> Dict[str, List[Dict]]:
        """获取所有数据源"""
        
    def save(self, data, date=None) -> str:
        """保存为标准化JSON"""
```

### 3.2 使用方法

```bash
# 获取今日数据
python3 zhihu_collector.py

# 获取指定日期
python3 zhihu_collector.py --date 2025-05-12

# 仅获取热搜榜
python3 zhihu_collector.py --type hot_search

# 指定输出目录
python3 zhihu_collector.py --output ./my_data
```

### 3.3 输出格式

```json
{
  "meta": {
    "platform": "知乎",
    "date": "2025-05-12",
    "total": 91,
    "sources": ["hot_search", "hot_questions"],
    "generated_at": "2026-05-06T16:47:37"
  },
  "data": [
    {
      "source": "知乎热搜榜",
      "platform": "知乎",
      "type": "hot_search",
      "title": "中美日内瓦经贸会谈联合声明",
      "url": "https://www.zhihu.com/search?q=...",
      "fetched_at": "2026-05-06T16:47:32"
    }
  ]
}
```

---

## 4. 备选方案

### 4.1 今日热榜 (tophub.today)

- **状态**: ✅ 已验证可行
- **数据**: 聚合多平台热搜（含知乎）
- **字段**: `title`, `hot_value`, `url`
- **限制**: 需反爬处理，数据字段较少
- **用途**: 作为补充数据源

### 4.2 ClawHub Skills

- **状态**: ⚠️ 待测试
- **技能**: 知乎热榜监控、CN Web Search
- **说明**: 可能封装了知乎API或爬虫

---

## 5. 方案对比

| 方案 | 可行性 | 数据质量 | 稳定性 | 维护成本 | 风险 |
|------|--------|----------|--------|----------|------|
| justjavac开源数据 | ✅ 高 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 低 | 无 |
| 今日热榜 | ✅ 中 | ⭐⭐⭐ | ⭐⭐⭐ | 中 | 低 |
| 直接抓取 | ❌ 不可行 | - | - | 高 | 🔴 高 |
| APP逆向 | ❌ 不推荐 | - | - | 极高 | 🔴 法律风险 |

---

## 6. 集成建议

### 6.1 定时任务

```bash
# crontab - 每小时抓取
0 * * * * cd /path/to/project && python3 zhihu_collector.py >> logs/zhihu.log 2>&1
```

### 6.2 与现有系统集成

```python
from zhihu_collector import ZhihuCollector

# 在sentiment_monitor.py中集成
collector = ZhihuCollector(output_dir="./output")
zhihu_data = collector.fetch_all()

# 合并到统一数据流
all_platform_data["知乎"] = zhihu_data
```

### 6.3 数据增强

- **关键词匹配**: 将热搜query与品牌关键词匹配，识别相关舆情
- **趋势分析**: 对比历史数据，识别热度变化趋势
- **跨平台关联**: 与微博、抖音等平台数据关联分析

---

## 7. 风险与限制

| 风险 | 说明 | 缓解措施 |
|------|------|----------|
| 数据源停止更新 | justjavac项目可能停更 | 监控项目状态，准备备选方案 |
| 数据延迟 | 开源数据有1小时延迟 | 对实时性要求高的场景需其他方案 |
| 数据字段有限 | 仅有title/url，无内容/评论 | 结合其他数据源补充 |
| GitHub访问限制 | 国内访问可能不稳定 | 使用CDN或代理 |

---

## 8. 结论

**推荐方案**: 使用 justjavac 开源数据作为知乎VOC采集的主要数据源

**优势**:
- ✅ 无需登录、无反爬
- ✅ 稳定可靠（运行5年+）
- ✅ 历史数据完整
- ✅ 零成本、零风险
- ✅ 易于集成和自动化

**下一步**:
1. 部署定时任务，每小时自动采集
2. 实现关键词匹配，筛选品牌相关舆情
3. 与微博、抖音等平台数据整合
4. 建立数据质量监控，检测源数据异常

---

*文档版本: v1.0*
*更新日期: 2026-05-06*
*作者: AI Agent*
