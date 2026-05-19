import json

# Read the original batch file
with open('/Users/zhijian/workspace/ai-demand-research-v3/projects/宝爸宝妈-2026-05-19/02-classified/batch_02.json', 'r', encoding='utf-8') as f:
    notes = json.load(f)

# Classification results
classifications = [
    {"note_id": "69f0a0c5000000001a02d8b5", "classification": "宝妈育儿类", "reason": "分享带娃日常日程", "confidence": "高"},
    {"note_id": "67b8ae71000000002902c210", "classification": "宝妈育儿类", "reason": "二胎家庭育儿经验分享", "confidence": "高"},
    {"note_id": "67d8d7fc000000001e001fd6", "classification": "信息缺失类", "reason": "上下文缺失无法判断", "confidence": "高"},
    {"note_id": "677c8d92000000000203e178", "classification": "信息缺失类", "reason": "标题内容均为空", "confidence": "高"},
    {"note_id": "67c519e1000000000e005d29", "classification": "宝妈育儿类", "reason": "育儿嫂带娃问题分享", "confidence": "高"},
    {"note_id": "68987b7f0000000023031dd9", "classification": "宝妈育儿类", "reason": "育儿理念经验分享", "confidence": "高"},
    {"note_id": "684af466000000002301d260", "classification": "宝妈育儿类", "reason": "找育儿嫂经历分享", "confidence": "高"},
    {"note_id": "691fcf70000000000d03e793", "classification": "信息缺失类", "reason": "内容为空不可见", "confidence": "高"},
    {"note_id": "68429fa9000000001101d90e", "classification": "宝妈育儿类", "reason": "宝宝睡眠规律分享", "confidence": "高"},
    {"note_id": "6859f9b800000000200196f9", "classification": "宝妈育儿类", "reason": "教育理念讨论分享", "confidence": "高"},
    {"note_id": "680988d5000000001d002774", "classification": "信息缺失类", "reason": "依赖图片内容不可见", "confidence": "高"},
    {"note_id": "68d6b7fb000000000e00c1be", "classification": "宝妈育儿类", "reason": "宝宝生长发育科普", "confidence": "高"},
    {"note_id": "6881963d0000000010024acf", "classification": "宝妈育儿类", "reason": "双职工育儿经验分享", "confidence": "高"},
    {"note_id": "69a17446000000001a021742", "classification": "宝妈育儿类", "reason": "育儿工具经验分享", "confidence": "高"},
    {"note_id": "6949c78e000000001b022f16", "classification": "宝妈育儿类", "reason": "城市养娃挑战讨论", "confidence": "高"},
    {"note_id": "69d7639c000000001f00392b", "classification": "信息缺失类", "reason": "内容截断不完整", "confidence": "高"},
    {"note_id": "692eaf6b000000001e034032", "classification": "宝妈育儿类", "reason": "育儿嫂带娃问题吐槽", "confidence": "高"},
    {"note_id": "697429920000000022021bc8", "classification": "宝妈育儿类", "reason": "育儿补贴话题讨论", "confidence": "高"},
    {"note_id": "67e4a596000000001b03be0e", "classification": "宝妈育儿类", "reason": "育儿干货经验分享", "confidence": "高"},
    {"note_id": "69492aa3000000001e008790", "classification": "宝妈育儿类", "reason": "教育理念深度讨论", "confidence": "高"},
    {"note_id": "68d904a4000000000b03cf69", "classification": "信息缺失类", "reason": "内容为空不可见", "confidence": "高"},
    {"note_id": "693fcf62000000001e016fb5", "classification": "宝妈育儿类", "reason": "育儿方法经验分享", "confidence": "高"},
    {"note_id": "6a08563700000000080278bc", "classification": "宝妈育儿类", "reason": "育儿福利政策资讯", "confidence": "高"},
    {"note_id": "6816b106000000000e006588", "classification": "宝妈育儿类", "reason": "宝宝睡眠安全科普", "confidence": "高"},
    {"note_id": "67ef9f3c000000001d0232f0", "classification": "宝妈育儿类", "reason": "育儿认知差异讨论", "confidence": "高"},
]

# Build result
result = []
for note in notes:
    cls = next((c for c in classifications if c["note_id"] == note["note_id"]), None)
    if cls:
        result.append({
            "note_id": note["note_id"],
            "source_keyword": note["source_keyword"],
            "title": note.get("title", ""),
            "content": note.get("content", ""),
            "classification": cls["classification"],
            "reason": cls["reason"],
            "confidence": cls["confidence"]
        })

# Write output
with open('/Users/zhijian/workspace/ai-demand-research-v3/projects/宝爸宝妈-2026-05-19/02-classified/batch_02_classified.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Written {len(result)} records to batch_02_classified.json")
