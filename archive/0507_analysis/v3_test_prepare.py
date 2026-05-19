"""
v3方案验证脚本：批处理提取Opinion Units + 分类标注
使用现有200条数据中的前10条做小规模测试
"""

import json
import sys
sys.path.insert(0, '/Users/zhijian/workspace-strict/MediaCrawler/analysis')

# 读取现有数据 (v2版本的135条强相关VOC)
with open('/Users/zhijian/workspace-strict/MediaCrawler/analysis/v2_relevant_vocs_135.json', 'r', encoding='utf-8') as f:
    all_vocs = json.load(f)

# 读取分类体系
with open('/Users/zhijian/workspace-strict/MediaCrawler/analysis/v3_classification_schema.json', 'r', encoding='utf-8') as f:
    schema = json.load(f)

# 取前10条做测试
test_vocs = all_vocs[:10]

print(f"测试数据: {len(test_vocs)}条VOC")
print(f"数据来源: 小红书 (v2_relevant_vocs_135.json)")
print("="*60)

# 构建批处理Prompt
batch_prompt = f"""你是一位专业的用户研究分析师，擅长从用户原声(VOC)中提取结构化洞察。

## 任务说明
请对以下{len(test_vocs)}条用户原声进行批量分析。每条原声可能包含1个或多个"观点单元"(Opinion Unit)。

## 什么是Opinion Unit？
Opinion Unit是用户原声中的一个独立观点，包含：
- 摘录：原文中表达该观点的核心句子（尽量引用原话）
- 场景：属于哪种观看场景
- 类型：属于哪种诉求类型
- 主题：属于哪个主题标签
- 情感：用户的情感倾向
- AI相关：是否与AI功能有关

## 分类体系

### 场景维度 (Layer 1)
{json.dumps([{"id": c["id"], "name": c["name"], "def": c["definition"]} for c in schema["layer1_scene"]["categories"]], ensure_ascii=False, indent=2)}

### 诉求类型 (Layer 2)
{json.dumps([{"id": c["id"], "name": c["name"], "def": c["definition"]} for c in schema["layer2_type"]["categories"]], ensure_ascii=False, indent=2)}

### 主题标签 (Layer 3) - 预定义20个
{json.dumps([{"id": c["id"], "name": c["name"], "examples": c["examples"], "def": c["definition"]} for c in schema["layer3_topic"]["predefined"]], ensure_ascii=False, indent=2)}

**重要**: 如果某条观点无法匹配以上20个预定义主题，请标记主题为"other"，并在"new_topic_suggestion"字段建议一个新主题名称。

### 情感维度
- "positive": 正面/满意/赞赏
- "neutral": 中性/客观描述/无明确情感
- "negative": 负面/不满/抱怨

### AI相关分类
- is_ai_related: true/false
- ai_specificity: "explicit"(明确提到AI)/"implicit"(隐含AI需求)/"not_ai"
- ai_category: 如果is_ai_related为true，从以下选择：
  {json.dumps([{"id": c["id"], "name": c["name"]} for c in schema["ai_classification"]["ai_categories"]], ensure_ascii=False)}

## 输出格式
必须为每条原声的每个Opinion Unit输出一个JSON对象，格式如下：

```json
{{
  "voc_id": "原始VOC的编号",
  "unit_id": "{len(test_vocs)}条中的唯一编号，如 u_001",
  "excerpt": "原文摘录",
  "scene": "场景ID",
  "scene_name": "场景名称",
  "type": "类型ID",
  "type_name": "类型名称",
  "topic": "主题ID",
  "topic_name": "主题名称",
  "new_topic_suggestion": "如果topic是other，建议的新主题名称；否则空字符串",
  "sentiment": "positive/neutral/negative",
  "is_ai_related": true/false,
  "ai_specificity": "explicit/implicit/not_ai",
  "ai_category": "AI分类ID或空字符串",
  "confidence": 0.0-1.0,
  "reason": "分类理由，简要说明"
}}
```

## 待分析的用户原声
"""

# 添加VOC内容
for i, voc in enumerate(test_vocs, 1):
    content = voc.get('content', voc.get('note_content', ''))[:300]
    batch_prompt += f"""
--- VOC #{i} ---
ID: {voc.get('voc_id', f'voc_{i}')}
平台: {voc.get('platform', 'xhs')}
内容: {content}
URL: {voc.get('url', 'N/A')}
"""

batch_prompt += """

## 输出要求
1. 只输出JSON数组，不要输出任何其他文字
2. 每个VOC可能产生1-3个Opinion Unit（如果包含多个独立观点）
3. 如果某条VOC与手机视频观看完全无关，可以产生0个Unit
4. 确保JSON格式正确，可以被Python json.loads解析
5. 摘录尽量引用原文原话，不要过度改写

开始分析：
"""

# 保存prompt供查看
with open('/Users/zhijian/workspace-strict/MediaCrawler/analysis/v3_test_batch_prompt.txt', 'w', encoding='utf-8') as f:
    f.write(batch_prompt)

print(f"Prompt已保存到: v3_test_batch_prompt.txt")
print(f"Prompt长度: {len(batch_prompt)} 字符")
print(f"包含VOC数量: {len(test_vocs)}")
print("\n前500字符预览:")
print(batch_prompt[:500])
print("...")
