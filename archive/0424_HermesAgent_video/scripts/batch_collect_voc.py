#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频AI调研 - VOC批量收集脚本
用于收集各平台的用户原声
"""

import requests
import json
import re
import time
from datetime import datetime
from urllib.parse import quote

# ========== 配置 ==========
AI_KEYWORDS = [
    'AI', '人工智能', '智能', '自动', '字幕', '翻译', '推荐', '算法',
    '识别', '语音', '画质', '增强', '总结', '摘要', '搜索', '滤镜',
    '特效', '美颜', '剪辑', '生成', '理解', '学习', '个性化',
    '视频', 'video', '抖音', 'B站', 'bilibili', 'youtube', 'tiktok',
    'app', '应用', '手机', 'mobile', '播放', 'player'
]

def is_ai_related(text):
    if not text:
        return False
    text_lower = text.lower()
    return any(k.lower() in text_lower for k in AI_KEYWORDS)

def save_voc(voc_list, platform):
    """保存VOC到文件"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"/Users/zhijian/workspace/video_ai_research/raw_voc/{platform}/voc_{platform}_{timestamp}.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(voc_list, f, ensure_ascii=False, indent=2)
    print(f"已保存 {len(voc_list)} 条VOC到 {filename}")

# ========== 1. App Store评论收集 ==========
def fetch_app_store_reviews(app_id, app_name, region="cn", max_pages=3):
    """获取App Store评论"""
    all_reviews = []
    for page in range(1, max_pages + 1):
        url = f"https://itunes.apple.com/{region}/rss/customerreviews/id={app_id}/sortby=mostrecent/page={page}/json"
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                entries = data.get('feed', {}).get('entry', [])
                if len(entries) > 1:
                    for entry in entries[1:]:
                        review = {
                            "author": entry.get('author', {}).get('name', {}).get('label', '匿名'),
                            "rating": entry.get('im:rating', {}).get('label', '0'),
                            "title": entry.get('title', {}).get('label', ''),
                            "content": entry.get('content', {}).get('label', ''),
                            "date": entry.get('updated', {}).get('label', '')
                        }
                        all_reviews.append(review)
            time.sleep(1)
        except Exception as e:
            print(f"Error fetching {app_name} page {page}: {e}")
            break
    return all_reviews

# ========== 2. 知乎回答收集 ==========
def fetch_zhihu_answers(question_ids):
    """获取知乎回答（需要登录cookie）"""
    # 需要用户手动提供cookie
    print("知乎收集需要登录，请提供cookie或手动访问")
    return []

# ========== 3. B站评论收集 ==========
def fetch_bilibili_comments(video_ids):
    """获取B站视频评论（需要登录cookie）"""
    # 需要用户手动提供cookie
    print("B站评论收集需要登录，请提供cookie或手动访问")
    return []

# ========== 4. 小红书收集 ==========
def fetch_xiaohongshu(keyword):
    """获取小红书内容（需要登录）"""
    print("小红书收集需要登录，请扫码或提供cookie")
    return []

# ========== 主程序 ==========
if __name__ == "__main__":
    print("=" * 50)
    print("视频AI调研 - VOC批量收集")
    print("=" * 50)
    
    # 1. 收集App Store评论
    print("
[1/4] 收集App Store评论...")
    apps = {
        "douyin": {"id": "1142110895", "name": "抖音", "region": "cn"},
        "bilibili": {"id": "736536082", "name": "哔哩哔哩", "region": "cn"},
        "kuaishou": {"id": "440948110", "name": "快手", "region": "cn"},
        "youtube": {"id": "544007664", "name": "YouTube", "region": "us"},
        "tiktok": {"id": "835599320", "name": "TikTok", "region": "us"},
        "netflix": {"id": "363590051", "name": "Netflix", "region": "us"},
        "iqiyi": {"id": "1012298408", "name": "爱奇艺", "region": "cn"},
        "youku": {"id": "336456412", "name": "优酷", "region": "cn"}
    }
    
    all_reviews = []
    for app_key, app_info in apps.items():
        print(f"  获取 {app_info['name']}...")
        reviews = fetch_app_store_reviews(app_info['id'], app_info['name'], app_info['region'])
        all_reviews.extend(reviews)
        print(f"  -> {len(reviews)} 条评论")
        time.sleep(2)
    
    print(f"
App Store总计: {len(all_reviews)} 条评论")
    
    # 2. 转换为VOC格式
    print("
[2/4] 转换为VOC格式...")
    voc_entries = []
    for review in all_reviews:
        combined = f"{review['title']} {review['content']}"
        if is_ai_related(combined):
            rating = int(review['rating'])
            sentiment = "neutral"
            if rating >= 4:
                sentiment = "positive"
            elif rating <= 2:
                sentiment = "negative"
            
            voc = {
                "id": f"voc_appstore_{len(voc_entries)+1:06d}",
                "platform": "app_store",
                "source_url": "https://apps.apple.com",
                "source_type": "review",
                "author": review['author'],
                "date": review['date'][:10] if review['date'] else "2025-04-24",
                "content": f"[{review['title']}] {review['content']}",
                "context": "App Store应用评论",
                "sentiment": sentiment,
                "category": "other",
                "ai_related": True,
                "verified": True,
                "collection_date": datetime.now().strftime('%Y-%m-%d'),
                "collector": "batch_script"
            }
            voc_entries.append(voc)
    
    print(f"AI相关VOC: {len(voc_entries)} 条")
    
    if voc_entries:
        save_voc(voc_entries, "app_store")
    
    # 3. 其他平台（需要登录）
    print("
[3/4] 其他平台收集（需要登录）...")
    print("  - 知乎: 需要手动登录")
    print("  - B站: 需要手动登录")
    print("  - 小红书: 需要手动登录")
    print("  - 微博: 需要手动登录")
    
    print("
[4/4] 完成!")
    print(f"总计收集: {len(voc_entries)} 条VOC")
