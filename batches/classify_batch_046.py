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
    
    # 情感表达 - 纯情绪、吐槽、赞美
    emotion_keywords = ["丑", "好看", "喜欢", "讨厌", "纠结", "无语", "失望", "惊艳", "爱了", "绝了", "避雷", "踩雷", "真香", "后悔", "值得", "不值"]
    if any(kw in text for kw in emotion_keywords):
        # 但如果同时有明显评测/攻略属性，优先评测/攻略
        if not any(kw in text for kw in ["对比", "参数", "配置", "评测", "测评", "攻略", "推荐", "选购", "怎么选"]):
            return "情感表达"
    
    # 问题求助
    help_keywords = ["怎么办", "怎么解决", "求助", "故障", "坏了", "维修", "修", "换电池", "卡顿", "闪退", "死机"]
    if any(kw in text for kw in help_keywords):
        return "问题求助"
    
    # 新闻资讯
    news_keywords = ["发布", "发布会", "新闻", "资讯", "宣布", "曝光", "爆料", "最新消息", "市场份额", "销量", "排行", "定档"]
    if any(kw in text for kw in news_keywords):
        # 如果有详细对比/评测内容，优先评测
        if any(kw in text for kw in ["对比", "评测", "测评", "测试", "体验", "拍照对比"]):
            return "产品评测"
        return "新闻资讯"
    
    # 产品评测
    review_keywords = ["评测", "测评", "对比", "测试", "跑分", "参数", "配置", "性能", "拍照对比", "屏幕", "续航测试", "一图看懂", "全参数"]
    if any(kw in text for kw in review_keywords):
        return "产品评测"
    
    # 开箱晒单
    unbox_keywords = ["开箱", "到手", "入手", "买了", "新手机", "新机", "终于", "拿下", "入手了"]
    if any(kw in text for kw in unbox_keywords):
        # 检查是否更偏向评测
        if any(kw in text for kw in ["评测", "测评", "对比", "测试", "跑分"]):
            return "产品评测"
        return "开箱晒单"
    
    # 购买攻略
    guide_keywords = ["怎么选", "选购", "攻略", "值得买", "性价比", "降价", "优惠", "补贴", "618", "双11", "省钱", "预算", "入手建议", "购买"]
    if any(kw in text for kw in guide_keywords):
        return "购买攻略"
    
    # 使用体验
    experience_keywords = ["体验", "感受", "用了", "使用", "手感", "流畅", "续航", "发热", "拍照效果", "日常", "一段时间", "真实", "报告", "评价", "建议"]
    if any(kw in text for kw in experience_keywords):
        return "使用体验"
    
    # 情感表达 - 纯情绪、吐槽、赞美（放在后面，避免过度匹配）
    emotion_keywords_late = ["丑", "好看", "喜欢", "讨厌", "纠结", "无语", "失望", "惊艳", "爱了", "绝了", "避雷", "踩雷", "真香", "后悔", "不值"]
    if any(kw in text for kw in emotion_keywords_late):
        return "情感表达"
    
    # 默认分类
    return "其他"

def main():
    # 读取输入文件
    with open("/Users/zhijian/workspace/batches/batch_046.json", "r", encoding="utf-8") as f:
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
    with open("/Users/zhijian/workspace/batches/result_batch_046.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # 打印统计
    from collections import Counter
    stats = Counter([r["category"] for r in results])
    print("分类统计:")
    for cat, count in stats.most_common():
        print(f"  {cat}: {count}")
    print(f"\n总计: {len(results)} 条")

if __name__ == "__main__":
    main()
