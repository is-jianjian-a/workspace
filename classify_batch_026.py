import json

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

def classify_post(post):
    """对单条小红书帖子进行分类"""
    title = post.get("title", "")
    content = post.get("content", "")
    tags = post.get("tag_list", "")
    text = (title + " " + content + " " + tags).lower()
    
    # ========== 1. invalid / 无效帖 ==========
    # 极短内容无实质观点
    content_stripped = content.strip()
    if len(content_stripped) < 20 and len(title.strip()) < 15:
        return "其他"
    
    # 只有话题标签，无实质内容
    if content_stripped.startswith("#") and len(content_stripped) < 80:
        return "其他"
    
    # ========== 2. 问题求助 (高优先级) ==========
    help_keywords = ["怎么办", "怎么解决", "求助", "故障", "坏了", "维修", "换电池", "卡顿", "闪退", "死机", "售后", "失灵", "修"]
    if any(kw in text for kw in help_keywords):
        # 但如果是分享维修经验/攻略，归为使用体验
        if "教程" in text or "攻略" in text or "经验" in text:
            return "使用体验"
        return "问题求助"
    
    # ========== 3. 产品评测 (高优先级) ==========
    review_keywords = ["评测", "测评", "对比", "测试", "跑分", "参数", "配置", "性能", "拍照对比", "屏幕", "续航测试", "一图看懂", "全参数", "vs", "全维度", "深度对比", "理论寿命排行", "天梯图", "优缺点", "差距"]
    if any(kw in text for kw in review_keywords):
        # 排除纯提问类
        if "能给个建议" in text or "有懂手机的" in text:
            return "购买攻略"
        # 排除极短内容（只有标题党）
        if len(content_stripped) < 40:
            return "其他"
        return "产品评测"
    
    # ========== 4. 购买攻略 ==========
    guide_keywords = ["怎么选", "选购", "攻略", "推荐", "值得买", "性价比", "预算", "入手建议", "选哪个", "买哪个", "购买", "求推荐"]
    if any(kw in text for kw in guide_keywords):
        # 如果同时有详细评测内容，优先评测
        if any(kw in text for kw in ["评测", "测评", "测试", "跑分", "详细对比", "性能测试", "全维度对比", "深度对比"]):
            return "产品评测"
        # 排除纯提问但无实质观点的
        if len(content_stripped) < 30:
            return "其他"
        return "购买攻略"
    
    # ========== 5. 开箱晒单 ==========
    unbox_keywords = ["开箱", "到手", "入手", "新手机", "新机", "终于", "拿下", "入手了", "买了"]
    if any(kw in text for kw in unbox_keywords):
        # 检查是否更偏向评测
        if any(kw in text for kw in ["评测", "测评", "详细测试", "跑分", "性能测试"]):
            return "产品评测"
        return "开箱晒单"
    
    # ========== 6. 使用体验 ==========
    experience_keywords = ["体验", "感受", "用了", "使用", "手感", "流畅", "续航", "发热", "拍照效果", "日常", "一段时间", "已经用", "用了很久", "真实", "心得", "分享", "感触", "不习惯", "后悔", "换机"]
    if any(kw in text for kw in experience_keywords):
        # 排除纯情感吐槽
        if any(kw in text for kw in ["脑溢血", "太能忍了", "像个原始人", "真的好不习惯"]):
            return "情感表达"
        return "使用体验"
    
    # ========== 7. 情感表达 ==========
    emotion_keywords = ["丑", "好看", "喜欢", "讨厌", "纠结", "无语", "失望", "惊艳", "爱了", "绝了", "避雷", "踩雷", "真香", "后悔", "值得", "不值", "脑溢血", "太能忍了", "像个原始人", "好不习惯"]
    if any(kw in text for kw in emotion_keywords):
        return "情感表达"
    
    # ========== 8. 再次检查新闻 ==========
    if any(kw in text for kw in ["发布会", "宣布", "降价"]):
        if "体验" not in text and "感受" not in text and "用了" not in text:
            return "新闻资讯"
    
    # ========== 9. 纯提问/空泛内容 → 其他 ==========
    # 只有问句但无实质内容的短帖
    if len(content_stripped) < 50 and ("？" in title or "?" in title or "为什么" in title):
        return "其他"
    
    # ========== 默认 ==========
    return "其他"

def main():
    # 读取输入文件
    with open("/Users/zhijian/workspace/mind-mining/v1.0/batches/batch_026.json", "r", encoding="utf-8") as f:
        posts = json.load(f)
    
    results = []
    for post in posts:
        category = classify_post(post)
        result = {
            "id": post["id"],
            "note_id": post["note_id"],
            "nickname": post["nickname"],
            "title": post["title"],
            "category": category,
            "source_keyword": post.get("source_keyword", ""),
            "liked_count": post.get("liked_count", 0),
            "comment_count": post.get("comment_count", 0)
        }
        results.append(result)
    
    # 输出结果
    with open("/Users/zhijian/workspace/result_batch_026.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # 打印统计
    from collections import Counter
    stats = Counter([r["category"] for r in results])
    print("分类统计:")
    for cat, count in stats.most_common():
        print(f"  {cat}: {count}")
    print(f"\n总计: {len(results)} 条")
    
    # 打印每条分类详情
    print("\n分类详情:")
    for r in results:
        print(f"  [{r['category']}] {r['title'][:50]}...")

if __name__ == "__main__":
    main()
