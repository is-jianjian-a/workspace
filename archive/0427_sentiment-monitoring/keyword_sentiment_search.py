#!/usr/bin/env python3
"""
关键词舆情搜索工具
支持多平台搜索：微博、头条、B站、抖音
通过搜索引擎抓取用户原声内容
"""

import urllib.request
import urllib.parse
import json
import re
import time
from datetime import datetime
from typing import List, Dict, Optional

class KeywordSentimentSearch:
    """关键词舆情搜索器"""
    
    def __init__(self):
        self.results = {}
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def search_weibo(self, keyword: str, num: int = 10) -> List[Dict]:
        """搜索微博内容 - 使用微博搜索API"""
        print(f'搜索微博: "{keyword}"...')
        
        # 使用微博搜索接口
        encoded_kw = urllib.parse.quote(keyword)
        url = f"https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D{encoded_kw}&page_type=searchall"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://m.weibo.cn/search?containerid=100103type%3D1%26q%3D' + encoded_kw
        }
        
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                if data.get('ok') == 1:
                    cards = data.get('data', {}).get('cards', [])
                    items = []
                    
                    for card in cards[:num]:
                        if card.get('card_type') == 9:  # 微博帖子
                            mblog = card.get('mblog', {})
                            user = mblog.get('user', {})
                            
                            items.append({
                                'platform': '微博',
                                'title': mblog.get('text', '')[:100] + '...' if len(mblog.get('text', '')) > 100 else mblog.get('text', ''),
                                'content': mblog.get('text', ''),
                                'author': user.get('screen_name', '未知'),
                                'author_id': user.get('id', ''),
                                'time': mblog.get('created_at', ''),
                                'reposts': mblog.get('reposts_count', 0),
                                'comments': mblog.get('comments_count', 0),
                                'likes': mblog.get('attitudes_count', 0),
                                'url': f"https://weibo.com/{user.get('id', '')}/{mblog.get('bid', '')}"
                            })
                    
                    print(f'  找到 {len(items)} 条微博')
                    return items
                else:
                    print(f'  API 返回错误: {data.get("msg", "未知错误")}')
                    return []
                    
        except Exception as e:
            print(f'  微博搜索失败: {e}')
            return []
    
    def search_toutiao(self, keyword: str, num: int = 10) -> List[Dict]:
        """搜索头条内容 - 使用头条搜索API"""
        print(f'搜索头条: "{keyword}"...')
        
        encoded_kw = urllib.parse.quote(keyword)
        url = f"https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset=0&format=json&keyword={encoded_kw}&autoload=true&count={num}&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis&timestamp={int(time.time()*1000)}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://www.toutiao.com/search/?keyword=' + encoded_kw
        }
        
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                items = []
                for item in data.get('data', [])[:num]:
                    if item and 'title' in item:
                        items.append({
                            'platform': '头条',
                            'title': item.get('title', ''),
                            'content': item.get('abstract', item.get('title', '')),
                            'author': item.get('source', '未知'),
                            'time': item.get('datetime', ''),
                            'url': item.get('article_url', item.get('share_url', '')),
                            'comments': item.get('comment_count', 0),
                            'likes': item.get('digg_count', 0)
                        })
                
                print(f'  找到 {len(items)} 条头条')
                return items
                
        except Exception as e:
            print(f'  头条搜索失败: {e}')
            return []
    
    def search_bilibili(self, keyword: str, num: int = 10) -> List[Dict]:
        """搜索B站内容 - 使用B站搜索API"""
        print(f'搜索B站: "{keyword}"...')
        
        encoded_kw = urllib.parse.quote(keyword)
        url = f"https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword={encoded_kw}&page=1&pagesize={num}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://search.bilibili.com/'
        }
        
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                if data.get('code') == 0:
                    videos = data.get('data', {}).get('result', [])
                    items = []
                    
                    for video in videos[:num]:
                        items.append({
                            'platform': 'B站',
                            'title': video.get('title', '').replace('<em class=\"keyword\">', '').replace('</em>', ''),
                            'content': video.get('description', ''),
                            'author': video.get('author', '未知'),
                            'time': video.get('pubdate', ''),
                            'url': f"https://www.bilibili.com/video/{video.get('bvid', '')}",
                            'views': video.get('play', 0),
                            'comments': video.get('review', 0),
                            'likes': video.get('like', 0)
                        })
                    
                    print(f'  找到 {len(items)} 条B站视频')
                    return items
                else:
                    print(f'  API 错误: {data.get("message", "未知错误")}')
                    return []
                    
        except Exception as e:
            print(f'  B站搜索失败: {e}')
            return []
    
    def search_all(self, keyword: str, num: int = 10):
        """搜索所有平台"""
        print(f'\n{"="*60}')
        print(f'关键词舆情搜索: "{keyword}"')
        print(f'时间: {self.timestamp}')
        print(f'{"="*60}\n')
        
        all_results = []
        
        # 微博
        weibo_results = self.search_weibo(keyword, num)
        all_results.extend(weibo_results)
        time.sleep(1)
        
        # 头条
        toutiao_results = self.search_toutiao(keyword, num)
        all_results.extend(toutiao_results)
        time.sleep(1)
        
        # B站
        bilibili_results = self.search_bilibili(keyword, num)
        all_results.extend(bilibili_results)
        
        self.results[keyword] = all_results
        
        print(f'\n总计找到 {len(all_results)} 条内容')
        return all_results
    
    def generate_report(self, keyword: str) -> str:
        """生成搜索报告"""
        results = self.results.get(keyword, [])
        
        report = []
        report.append(f'# 关键词舆情搜索报告')
        report.append(f'关键词: "{keyword}"')
        report.append(f'生成时间: {self.timestamp}\n')
        report.append(f'总计: {len(results)} 条内容\n')
        
        # 按平台分组
        platforms = {}
        for item in results:
            p = item.get('platform', '未知')
            if p not in platforms:
                platforms[p] = []
            platforms[p].append(item)
        
        for platform, items in platforms.items():
            report.append(f'## {platform} ({len(items)}条)')
            report.append('')
            
            for i, item in enumerate(items[:5], 1):  # 每个平台显示前5条
                report.append(f'{i}. **{item.get("title", "")[:60]}...**')
                report.append(f'   作者: {item.get("author", "未知")}')
                report.append(f'   时间: {item.get("time", "")}')
                
                # 互动数据
                interactions = []
                if item.get('likes'):
                    interactions.append(f'赞:{item["likes"]}')
                if item.get('comments'):
                    interactions.append(f'评:{item["comments"]}')
                if item.get('reposts'):
                    interactions.append(f'转:{item["reposts"]}')
                if item.get('views'):
                    interactions.append(f'播:{item["views"]}')
                
                if interactions:
                    report.append(f'   互动: {" | ".join(interactions)}')
                
                if item.get('url'):
                    report.append(f'   链接: {item["url"]}')
                
                # 内容摘要
                content = item.get('content', '')
                if content and len(content) > 20:
                    report.append(f'   摘要: {content[:100]}...')
                
                report.append('')
        
        return '\n'.join(report)
    
    def save_report(self, keyword: str, filename: Optional[str] = None):
        """保存报告到文件"""
        if not filename:
            safe_kw = re.sub(r'[^\w\u4e00-\u9fff]', '_', keyword)[:20]
            filename = f'keyword_search_{safe_kw}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        
        report = self.generate_report(keyword)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return filename


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='关键词舆情搜索工具')
    parser.add_argument('keyword', help='搜索关键词')
    parser.add_argument('-n', '--num', type=int, default=10, help='每个平台返回数量 (默认10)')
    parser.add_argument('-o', '--output', help='输出文件名')
    
    args = parser.parse_args()
    
    # 执行搜索
    searcher = KeywordSentimentSearch()
    results = searcher.search_all(args.keyword, args.num)
    
    # 生成并保存报告
    filename = searcher.save_report(args.keyword, args.output)
    print(f'\n报告已保存: {filename}')
    
    # 打印摘要
    print('\n' + '='*60)
    print(searcher.generate_report(args.keyword)[:2000])
    print('...')
