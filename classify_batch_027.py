import json
from collections import Counter

# 8类UGC内容分类定义
CATEGORIES = {
    "产品评测": "对产品进行详细测试、评价、对比，包含具体参数、性能、体验等",
    "使用体验": "分享个人真实使用感受、心得、场景化体验",
    "购买攻略": "购买建议、选购指南、价格对比、促销信息、渠道推荐",
    "问题求助": "遇到产品问题寻求帮助、故障排查、维修咨询",
    "开箱晒单": "新品开箱、购买后展示、外观展示",
    "新闻资讯": "行业新闻、产品发布、市场动态、价格变动",
    "情感表达": "纯情绪表达、吐槽、赞美、品牌忠诚/反感",
    "其他": "无法归入以上类别的内容"
}

def classify_item(item):
    """对单条UGC内容进行分类"""
    text = item.get("text", "").lower()
    raw = item.get("raw_data", {})
    content = raw.get("content", "").lower()
    full_text = (text + " " + content).lower()
    
    # ========== 1. 问题求助 (最高优先级) ==========
    help_keywords = ["怎么办", "怎么解决", "求助", "故障", "坏了", "维修", "换电池", "卡顿", "闪退", "死机", "售后", "失灵", "修", "咋办", "求助"]
    if any(kw in full_text for kw in help_keywords):
        # 但如果是分享维修经验/攻略，归为使用体验
        if "教程" in full_text or "攻略" in full_text or "经验" in full_text:
            return "使用体验"
        return "问题求助"
    
    # ========== 2. 购买攻略 ==========
    guide_keywords = ["怎么选", "选购", "攻略", "推荐", "值得买", "性价比", "预算", "入手建议", "选哪个", "买哪个", "购买"]
    if any(kw in full_text for kw in guide_keywords):
        # 如果同时有详细评测内容，优先评测
        if any(kw in full_text for kw in ["评测", "测评", "测试", "跑分", "详细对比", "性能测试", "全维度对比"]):
            return "产品评测"
        return "购买攻略"
    
    # ========== 3. 开箱晒单 ==========
    unbox_keywords = ["开箱", "到手", "入手", "新手机", "新机", "终于", "拿下", "入手了", "买了"]
    if any(kw in full_text for kw in unbox_keywords):
        # 检查是否更偏向评测
        if any(kw in full_text for kw in ["评测", "测评", "详细测试", "跑分", "性能测试"]):
            return "产品评测"
        return "开箱晒单"
    
    # ========== 4. 产品评测 (高优先级) ==========
    review_keywords = ["评测", "测评", "对比", "测试", "跑分", "参数", "配置", "性能", "拍照对比", "屏幕", "续航测试", "一图看懂", "全参数", "vs", "全维度", "深度对比", "理论寿命排行", "天梯图"]
    if any(kw in full_text for kw in review_keywords):
        return "产品评测"
    
    # ========== 5. 使用体验 ==========
    experience_keywords = ["体验", "感受", "用了", "使用", "手感", "流畅", "续航", "发热", "拍照效果", "日常", "一段时间", "已经用", "用了很久", "真实", "心得", "分享", "感触", "不习惯", "后悔", "换机"]
    if any(kw in full_text for kw in experience_keywords):
        # 排除纯情感吐槽
        if any(kw in full_text for kw in ["脑溢血", "太能忍了", "像个原始人"]):
            return "情感表达"
        return "使用体验"
    
    # ========== 6. 新闻资讯 ==========
    # 新闻通常是客观报道，不带个人体验
    news_keywords = ["新闻", "资讯", "宣布", "曝光", "爆料", "最新消息", "市场份额", "销量排行", "销量", "行业"]
    if any(kw in full_text for kw in news_keywords):
        return "新闻资讯"
    
    # 纯降价/市场动态报道
    if "降价" in full_text and ("资讯" in full_text or "新闻" in full_text or "宣布" in full_text or "集体" in full_text):
        return "新闻资讯"
    
    # 发布会资讯
    if "发布会" in full_text and ("一张图" in full_text or "资讯" in full_text or "新闻" in full_text):
        return "新闻资讯"
    
    # 市场份额/排行数据
    if "市场份额" in full_text or "排行" in full_text:
        return "新闻资讯"
    
    # ========== 7. 情感表达 ==========
    emotion_keywords = ["丑", "好看", "喜欢", "讨厌", "纠结", "无语", "失望", "惊艳", "爱了", "绝了", "避雷", "踩雷", "真香", "后悔", "值得", "不值", "脑溢血", "太能忍了", "像个原始人", "好不习惯", "烦死了", "恶心", "气到", "烦"]
    if any(kw in full_text for kw in emotion_keywords):
        return "情感表达"
    
    # ========== 8. 再次检查新闻 ==========
    if any(kw in full_text for kw in ["发布会", "宣布", "降价"]):
        if "体验" not in full_text and "感受" not in full_text and "用了" not in full_text:
            return "新闻资讯"
    
    # ========== 默认 ==========
    return "其他"

def main():
    # 读取输入文件
    input_path = "/Users/zhijian/workspace/archive/0507_analysis/batches/batch_027.json"
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    items = data.get("items", [])
    
    results = []
    for item in items:
        category = classify_item(item)
        raw = item.get("raw_data", {})
        result = {
            "id": item["id"],
            "platform": item.get("platform", ""),
            "file_type": item.get("file_type", ""),
            "text": item.get("text", ""),
            "category": category,
            "nickname": raw.get("nickname", ""),
            "like_count": raw.get("like_count", 0),
            "sub_comment_count": raw.get("sub_comment_count", "0")
        }
        results.append(result)
    
    # 输出结果
    output_path = "/Users/zhijian/workspace/result_batch_027.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # 打印统计
    stats = Counter([r["category"] for r in results])
    print("分类统计:")
    for cat, count in stats.most_common():
        print(f"  {cat}: {count}")
    print(f"\n总计: {len(results)} 条")
    
    # 打印每条分类详情
    print("\n分类详情:")
    for r in results:
        text_preview = r['text'][:50] + "..." if len(r['text']) > 50 else r['text']
        print(f"  [{r['category']}] {text_preview}")

if __name__ == "__main__":
    main()
