# VOC 数据结构规范

## 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 格式：voc_{platform}_{序号:06d}，如 voc_bilibili_000001 |
| platform | string | 是 | 来源平台：bilibili/zhihu/app_store/google_play/kuan/xiaohongshu/douyin/weibo/v2ex/tieba |
| source_url | string | 是 | 原始链接，必须可访问 |
| source_type | string | 是 | comment/post/review/article/tweet/thread |
| author | string | 是 | 用户名或"匿名用户" |
| date | string | 是 | 原文发布时间，格式 YYYY-MM-DD |
| content | string | 是 | 原文内容，保留原样 |
| context | string | 否 | 上下文：视频标题/问题标题/应用名称等 |
| sentiment | string | 是 | positive/negative/neutral/expectation/pain_point |
| category | string | 是 | 主分类 |
| sub_category | string | 否 | 子分类 |
| ai_related | boolean | 是 | 是否与AI相关 |
| ai_mention_type | string | 否 | 提及的AI类型：cv/nlp/speech/multimodal/general |
| video_type | string | 否 | short_video/long_video/live/both |
| user_type | string | 否 | 推测的用户类型：student/office_worker/creator/elderly/disabled/learner/parent/other |
| verified | boolean | 是 | 是否已人工验证 |
| collection_date | string | 是 | 收集日期 YYYY-MM-DD |
| collector | string | 是 | 收集者标识 |
| notes | string | 否 | 备注 |

## category 分类标准

| 分类值 | 说明 | 示例 |
|--------|------|------|
| subtitle_translation | 字幕/翻译 | 自动字幕、实时翻译、双语字幕 |
| content_summary | 内容总结 | 视频摘要、章节划分、关键点提取 |
| video_quality | 画质/音质 | 画质增强、超分、HDR、音质优化 |
| recommendation | 推荐算法 | 个性化推荐、兴趣识别、去重 |
| interaction | 互动功能 | 弹幕、评论、投票、二创工具 |
| cross_device | 跨端体验 | 投屏、同步、多设备切换 |
| playback | 播放体验 | 倍速、断点续播、后台播放 |
| search_discovery | 搜索发现 | 语义搜索、以图搜视频 |
| creation_assist | 创作辅助 | AI剪辑、AI配音、AI特效 |
| accessibility | 无障碍 | 大字体、语音控制、辅助功能 |
| privacy_security | 隐私安全 | 内容过滤、防沉迷 |
| other | 其他 | 无法归入以上分类 |

## sentiment 判定标准

| 值 | 判定标准 |
|----|----------|
| positive | 明确表达喜欢、好用、方便、赞 |
| negative | 明确表达不满、难用、吐槽、抱怨 |
| neutral | 客观描述、无情感倾向 |
| expectation | 表达希望、建议、"如果能...就好了" |
| pain_point | 描述遇到的困难、问题、不便 |

## 示例

```json
{
  "id": "voc_bilibili_000001",
  "platform": "bilibili",
  "source_url": "https://www.bilibili.com/video/BV1xx411c7mD",
  "source_type": "comment",
  "author": "科技爱好者小明",
  "date": "2025-03-15",
  "content": "这个AI字幕功能太实用了，看生肉视频终于不用等字幕组了！",
  "context": "视频标题：B站AI字幕功能实测",
  "sentiment": "positive",
  "category": "subtitle_translation",
  "sub_category": "实时字幕",
  "ai_related": true,
  "ai_mention_type": "nlp",
  "video_type": "long_video",
  "user_type": "learner",
  "verified": true,
  "collection_date": "2025-04-24",
  "collector": "hermes",
  "notes": "高赞评论，表达明确"
}
```
