#!/usr/bin/env python3
"""
知乎VOC数据采集模块
基于 justjavac 开源数据实现，无需登录、无反爬
"""
import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os

class ZhihuCollector:
    """知乎数据采集器"""
    
    # 数据源配置
    SOURCES = {
        "hot_search": {
            "name": "知乎热搜榜",
            "url_template": "https://raw.githubusercontent.com/justjavac/zhihu-trending-top-search/main/raw/{date}.json",
            "fields": ["query_display", "real_query"],
            "description": "知乎搜索热搜，每小时更新"
        },
        "hot_questions": {
            "name": "知乎热门话题",
            "url_template": "https://raw.githubusercontent.com/justjavac/zhihu-trending-hot-questions/master/raw/{date}.json",
            "fields": ["title", "url"],
            "description": "知乎热门问题，每小时更新"
        },
        "hot_video": {
            "name": "知乎热门视频",
            "url_template": "https://raw.githubusercontent.com/justjavac/zhihu-trending-hot-video/main/raw/{date}.json",
            "fields": ["title", "url"],
            "description": "知乎热门视频，每小时更新"
        }
    }
    
    def __init__(self, output_dir: str = "./output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    def _fetch_data(self, url: str) -> Optional[List[Dict]]:
        """获取远程JSON数据"""
        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            print(f"[×] 获取失败: {url} - {e}")
            return None
    
    def fetch_hot_search(self, date: Optional[str] = None) -> List[Dict]:
        """
        获取知乎热搜榜
        
        Args:
            date: 日期字符串 YYYY-MM-DD，默认今天
            
        Returns:
            标准化后的热搜数据列表
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        source = self.SOURCES["hot_search"]
        url = source["url_template"].format(date=date)
        
        print(f"[→] 获取 {source['name']} ({date})...")
        raw_data = self._fetch_data(url)
        
        if not raw_data:
            return []
        
        # 标准化数据
        normalized = []
        for item in raw_data:
            query = item.get("query_display") or item.get("real_query", "")
            if query:
                normalized.append({
                    "source": source["name"],
                    "platform": "知乎",
                    "type": "hot_search",
                    "title": query,
                    "url": f"https://www.zhihu.com/search?q={urllib.parse.quote(query)}",
                    "raw_data": item,
                    "fetched_at": datetime.now().isoformat()
                })
        
        print(f"[✓] 获取 {len(normalized)} 条热搜")
        return normalized
    
    def fetch_hot_questions(self, date: Optional[str] = None) -> List[Dict]:
        """
        获取知乎热门话题/问题
        
        Args:
            date: 日期字符串 YYYY-MM-DD，默认今天
            
        Returns:
            标准化后的热门问题数据列表
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        source = self.SOURCES["hot_questions"]
        url = source["url_template"].format(date=date)
        
        print(f"[→] 获取 {source['name']} ({date})...")
        raw_data = self._fetch_data(url)
        
        if not raw_data:
            return []
        
        # 标准化数据
        normalized = []
        for item in raw_data:
            title = item.get("title", "")
            if title:
                normalized.append({
                    "source": source["name"],
                    "platform": "知乎",
                    "type": "hot_question",
                    "title": title,
                    "url": item.get("url", ""),
                    "raw_data": item,
                    "fetched_at": datetime.now().isoformat()
                })
        
        print(f"[✓] 获取 {len(normalized)} 条热门问题")
        return normalized
    
    def fetch_all(self, date: Optional[str] = None) -> Dict[str, List[Dict]]:
        """
        获取所有知乎数据源
        
        Args:
            date: 日期字符串 YYYY-MM-DD，默认今天
            
        Returns:
            按类型分类的数据字典
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        print(f"\n{'='*60}")
        print(f"知乎数据采集 - {date}")
        print(f"{'='*60}")
        
        results = {
            "hot_search": self.fetch_hot_search(date),
            "hot_questions": self.fetch_hot_questions(date),
        }
        
        total = sum(len(v) for v in results.values())
        print(f"\n[✓] 总计获取 {total} 条数据")
        
        return results
    
    def save(self, data: Dict[str, List[Dict]], date: Optional[str] = None) -> str:
        """
        保存数据到JSON文件
        
        Args:
            data: fetch_all() 返回的数据
            date: 日期字符串，用于文件名
            
        Returns:
            保存的文件路径
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # 合并所有数据
        all_items = []
        for items in data.values():
            all_items.extend(items)
        
        # 保存文件
        filename = f"zhihu_voc_{date}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                "meta": {
                    "platform": "知乎",
                    "date": date,
                    "total": len(all_items),
                    "sources": list(data.keys()),
                    "generated_at": datetime.now().isoformat()
                },
                "data": all_items
            }, f, ensure_ascii=False, indent=2)
        
        print(f"[✓] 已保存到: {filepath}")
        return filepath
    
    def run(self, date: Optional[str] = None) -> str:
        """
        一键执行：获取并保存数据
        
        Args:
            date: 日期字符串 YYYY-MM-DD，默认今天
            
        Returns:
            保存的文件路径
        """
        data = self.fetch_all(date)
        return self.save(data, date)


# CLI入口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="知乎VOC数据采集")
    parser.add_argument("--date", help="指定日期 (YYYY-MM-DD)，默认今天")
    parser.add_argument("--output", default="./output", help="输出目录")
    parser.add_argument("--type", choices=["hot_search", "hot_questions", "all"], 
                       default="all", help="采集类型")
    args = parser.parse_args()
    
    collector = ZhihuCollector(output_dir=args.output)
    
    if args.type == "all":
        filepath = collector.run(args.date)
    elif args.type == "hot_search":
        data = collector.fetch_hot_search(args.date)
        filepath = collector.save({"hot_search": data}, args.date)
    elif args.type == "hot_questions":
        data = collector.fetch_hot_questions(args.date)
        filepath = collector.save({"hot_questions": data}, args.date)
    
    print(f"\n完成! 文件: {filepath}")
