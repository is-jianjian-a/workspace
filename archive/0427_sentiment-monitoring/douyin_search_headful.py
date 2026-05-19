#!/usr/bin/env python3
"""抖音有头浏览器搜索抓取 - 登录后自动抓取"""

from playwright.sync_api import sync_playwright
import json
import time
import os
import re

COOKIE_FILE = "/Users/zhijian/workspace/sentiment-monitoring/douyin_cookies.json"
OUTPUT_DIR = "/Users/zhijian/workspace/sentiment-monitoring/output"

def douyin_search(keyword, max_results=15):
    """
    抖音搜索 - 必须使用有头浏览器
    首次运行需要登录，后续使用保存的cookie
    """
    print(f"[→] 抖音搜索: {keyword}")
    
    # URL编码关键词
    import urllib.parse
    encoded_keyword = urllib.parse.quote(keyword)
    
    with sync_playwright() as p:
        # 必须使用有头浏览器，否则触发验证码
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': 1280, 'height': 900}
        )
        
        # 加载cookie（如果存在）
        if os.path.exists(COOKIE_FILE):
            with open(COOKIE_FILE, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            context.add_cookies(cookies)
            print("[✓] 已加载抖音cookie")
        
        page = context.new_page()
        
        # 访问搜索页
        url = f'https://www.douyin.com/search/{encoded_keyword}'
        page.goto(url, wait_until='domcontentloaded')
        
        print("[→] 等待页面加载...")
        time.sleep(5)
        
        # 检查是否需要登录
        html = page.content()
        if '登录后即可搜索' in html:
            print("\n" + "="*60)
            print("[!] 需要登录抖音")
            print("请完成扫码或手机验证码登录...")
            print("等待60秒...")
            print("="*60 + "\n")
            
            # 等待用户登录
            for i in range(60):
                time.sleep(1)
                html = page.content()
                if '登录后即可搜索' not in html:
                    print(f"[✓] 登录成功！（{i+1}秒）")
                    # 保存cookie
                    cookies = context.cookies()
                    with open(COOKIE_FILE, 'w', encoding='utf-8') as f:
                        json.dump(cookies, f, ensure_ascii=False, indent=2)
                    print("[✓] Cookie已保存")
                    break
                if (i+1) % 10 == 0:
                    print(f"  ...等待中 ({i+1}/60秒)")
        
        # 等待搜索结果加载
        print("[→] 等待搜索结果...")
        time.sleep(5)
        
        # 滚动加载更多
        print("[→] 滚动加载更多...")
        for i in range(3):
            page.evaluate('window.scrollBy(0, 800)')
            time.sleep(2)
        
        time.sleep(3)
        
        # 获取页面内容
        html = page.content()
        
        # 解析视频数据
        videos = parse_douyin_html(html, max_results)
        
        # 保存结果
        if videos:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"douyin_{keyword}_{timestamp}.json"
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(videos, f, ensure_ascii=False, indent=2)
            
            print(f"[✓] 结果已保存: {filepath}")
        
        browser.close()
        return videos

def parse_douyin_html(html, max_results=15):
    """解析抖音搜索HTML，提取视频信息"""
    
    # 抖音数据通常在script标签的JSON中
    # 尝试多种提取方式
    
    videos = []
    
    # 方式1: 查找SSR渲染的数据
    ssr_pattern = r'<script[^>]*>window\._SSR_HYDRATED_DATA\s*=\s*(.*?);</script>'
    ssr_matches = re.findall(ssr_pattern, html, re.DOTALL)
    
    for ssr_data in ssr_matches:
        try:
            import urllib.parse
            decoded = urllib.parse.unquote(ssr_data)
            data = json.loads(decoded)
            
            # 尝试提取视频列表
            if isinstance(data, dict):
                # 查找包含视频的路径
                for key in data.keys():
                    if 'search' in key.lower() or 'video' in key.lower():
                        print(f"  找到key: {key}")
        except:
            pass
    
    # 方式2: 查找data-aweme-info属性
    aweme_pattern = r'data-aweme-info="([^"]+)"'
    aweme_matches = re.findall(aweme_pattern, html)
    
    for aweme_str in aweme_matches[:max_results]:
        try:
            import html as html_lib
            decoded = html_lib.unescape(aweme_str)
            data = json.loads(decoded)
            
            video = {
                'title': data.get('desc', ''),
                'author': data.get('author', {}).get('nickname', ''),
                'aweme_id': data.get('aweme_id', ''),
                'digg_count': data.get('statistics', {}).get('digg_count', 0),
                'comment_count': data.get('statistics', {}).get('comment_count', 0),
                'share_count': data.get('statistics', {}).get('share_count', 0),
            }
            videos.append(video)
        except:
            continue
    
    # 方式3: 从script中提取所有可能的视频JSON
    if not videos:
        script_pattern = r'<script[^>]*>(.*?)</script>'
        scripts = re.findall(script_pattern, html, re.DOTALL)
        
        for script in scripts:
            if len(script) > 5000:
                # 查找视频描述
                descs = re.findall(r'"desc"\s*:\s*"([^"]{10,300})"', script)
                authors = re.findall(r'"nickname"\s*:\s*"([^"]{2,50})"', script)
                
                for i, desc in enumerate(descs[:max_results]):
                    video = {
                        'title': desc,
                        'author': authors[i] if i < len(authors) else '',
                    }
                    if video not in videos:
                        videos.append(video)
    
    print(f"[✓] 提取 {len(videos)} 条抖音视频")
    return videos[:max_results]

if __name__ == '__main__':
    import sys
    keyword = sys.argv[1] if len(sys.argv) > 1 else "网红白冰偷税"
    results = douyin_search(keyword)
    
    print(f"\n{'='*60}")
    print(f"🎵 抖音搜索结果 - {len(results)} 条")
    print(f"{'='*60}")
    
    for i, video in enumerate(results[:10], 1):
        print(f"\n[{i}] {video.get('title', '')[:60]}...")
        if video.get('author'):
            print(f"    👤 作者: {video['author']}")
        if video.get('digg_count'):
            print(f"    👍 点赞: {video['digg_count']}  💬 评论: {video.get('comment_count', 0)}")
