#!/usr/bin/env python3
"""
多平台舆情监控抓取工具 - 完整版
支持: 微博(需登录)、B站(无需登录)、今日头条(无需登录)、抖音(需登录)、小红书(需登录)

使用方法:
  1. 首次使用微博: python3 sentiment_monitor.py --login-weibo
  2. 搜索所有平台: python3 sentiment_monitor.py "关键词"
  3. 指定平台: python3 sentiment_monitor.py "关键词" --platform weibo
"""

import json
import time
import re
import os
import sys
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

class SentimentMonitor:
    def __init__(self, output_dir="./output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.cookies_file = os.path.join(output_dir, "weibo_cookies.json")
        # 也检查当前目录
        if not os.path.exists(self.cookies_file) and os.path.exists("weibo_cookies.json"):
            self.cookies_file = "weibo_cookies.json"
        
    def _save_results(self, platform, keyword, results):
        """保存抓取结果到JSON文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{platform}_{keyword.replace(' ', '_')}_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        data = {
            "platform": platform,
            "keyword": keyword,
            "timestamp": timestamp,
            "count": len(results),
            "results": results
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"[✓] 结果已保存: {filepath}")
        return filepath
    
    def weibo_login(self, timeout=120):
        """
        启动有头浏览器让用户登录微博
        保存cookie供后续使用
        """
        print("[→] 启动微博登录流程...")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,
                args=['--start-maximized']
            )
            context = browser.new_context(
                viewport={'width': 1280, 'height': 900},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            )
            page = context.new_page()
            
            print("[→] 打开微博登录页面...")
            page.goto('https://weibo.com/login.php', wait_until='domcontentloaded')
            
            print(f"[!] 请在弹出的浏览器窗口中完成微博登录")
            print(f"[!] 你有 {timeout} 秒时间...")
            time.sleep(timeout)
            
            # 保存cookie
            cookies = context.cookies()
            with open(self.cookies_file, 'w', encoding='utf-8') as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)
            
            print(f"[✓] Cookie已保存 ({len(cookies)} 个)")
            browser.close()
            return True
    
    def weibo_search(self, keyword, max_results=20):
        """
        使用已保存的cookie搜索微博
        """
        if not os.path.exists(self.cookies_file):
            print("[✗] 未找到微博cookie，请先调用 weibo_login()")
            return []
        
        print(f"[→] 微博搜索: {keyword}")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={'width': 1280, 'height': 900}
            )
            
            # 加载cookie
            with open(self.cookies_file, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            context.add_cookies(cookies)
            
            page = context.new_page()
            
            # 搜索
            encoded_keyword = keyword.replace(' ', '%20')
            url = f'https://s.weibo.com/weibo?q={encoded_keyword}'
            
            try:
                page.goto(url, wait_until='domcontentloaded', timeout=30000)
                time.sleep(5)
            except PlaywrightTimeout:
                print("[✗] 页面加载超时")
                browser.close()
                return []
            
            # 获取HTML并解析
            html = page.content()
            browser.close()
            
            # 提取微博内容
            results = self._parse_weibo_html(html, max_results)
            
            # 保存结果
            self._save_results("weibo", keyword, results)
            
            return results
    
    def _parse_weibo_html(self, html, max_results=20):
        """解析微博搜索HTML提取内容"""
        pattern = r'<p[^>]*node-type="feed_list_content"[^>]*>(.*?)</p>'
        matches = re.findall(pattern, html, re.DOTALL)
        
        posts = []
        for match in matches[:max_results]:
            # 去除HTML标签
            text = re.sub(r'<[^>]+>', ' ', match)
            # 去除多余空白
            text = re.sub(r'\s+', ' ', text).strip()
            # 去除展开/收起
            text = re.sub(r'展开\s*c?\s*', '', text)
            text = re.sub(r'收起\s*c?\s*', '', text)
            
            if text and len(text) > 10:
                posts.append(text)
        
        # 去重
        seen = set()
        unique_posts = []
        for p in posts:
            if p not in seen:
                seen.add(p)
                unique_posts.append(p)
        
        print(f"[✓] 提取 {len(unique_posts)} 条微博")
        return unique_posts
    
    def bilibili_search(self, keyword, max_results=15):
        """
        搜索B站视频（无需登录）
        """
        print(f"[→] B站搜索: {keyword}")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={'width': 1280, 'height': 900},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            )
            page = context.new_page()
            
            # 直接访问搜索结果URL
            encoded_keyword = keyword.replace(' ', '+')
            search_url = f'https://search.bilibili.com/all?keyword={encoded_keyword}'
            page.goto(search_url, wait_until='domcontentloaded')
            time.sleep(5)
            
            # 获取视频列表
            html = page.content()
            browser.close()
            
            # 解析视频列表
            results = self._parse_bilibili_html(html, max_results)
            
            # 保存结果
            self._save_results("bilibili", keyword, results)
            
            return results
    
    def _parse_bilibili_html(self, html, max_results=15):
        """解析B站搜索HTML"""
        # B站搜索结果页面结构 - 从title属性提取
        title_pattern = r'<a[^>]*href="//www\.bilibili\.com/video/([A-Za-z0-9]+)"[^>]*title="([^"]+)"'
        matches = re.findall(title_pattern, html)
        
        # 如果失败，尝试从h3标签提取
        if not matches:
            bv_pattern = r'href="//www\.bilibili\.com/video/([A-Za-z0-9]+)"'
            bvids = re.findall(bv_pattern, html)
            title_pattern2 = r'<h3[^>]*class="bili-video-card__info--tit"[^>]*><a[^>]*title="([^"]+)"'
            titles = re.findall(title_pattern2, html)
            matches = list(zip(bvids[:len(titles)], titles)) if titles else []
        
        # 最后尝试：从页面中所有title属性提取视频标题
        if not matches:
            all_titles = re.findall(r'title="([^"]+)"', html)
            video_titles = [t for t in all_titles if '白冰' in t or '偷税' in t]
            matches = [(f'unknown_{i}', t) for i, t in enumerate(video_titles[:max_results])]
        
        videos = []
        for bvid, title in matches[:max_results]:
            title_clean = re.sub(r'<[^>]+>', '', title)
            title_clean = re.sub(r'\s+', ' ', title_clean).strip()
            
            if title_clean:
                videos.append({
                    "bvid": bvid,
                    "title": title_clean,
                    "url": f"https://www.bilibili.com/video/{bvid}" if not bvid.startswith('unknown') else "N/A"
                })
        
        print(f"[✓] 提取 {len(videos)} 个B站视频")
        return videos
    
    def toutiao_search(self, keyword, max_results=15):
        """
        搜索今日头条
        优先使用已保存的cookie，如果触发验证码则提示用户
        """
        print(f"[→] 头条搜索: {keyword}")
        
        toutiao_cookies = "./toutiao_cookies.json"
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={'width': 1280, 'height': 900}
            )
            
            # 如果有cookie则加载
            if os.path.exists(toutiao_cookies):
                with open(toutiao_cookies, 'r', encoding='utf-8') as f:
                    cookies = json.load(f)
                context.add_cookies(cookies)
                print("[✓] 已加载头条cookie")
            
            page = context.new_page()
            
            encoded_keyword = keyword.replace(' ', '%20')
            url = f'https://so.toutiao.com/search/?dvpf=pc&keyword={encoded_keyword}'
            
            page.goto(url, wait_until='domcontentloaded')
            time.sleep(5)
            
            # 检查是否有验证码
            iframe = page.query_selector('iframe[src*="verifycenter"]')
            if iframe:
                print("[✗] 头条触发了验证码！")
                print("[!] 请运行: python3 login_toutiao_headful.py")
                print("[!] 在弹出窗口中完成验证，然后重试")
                browser.close()
                return []
            
            html = page.content()
            browser.close()
            
            results = self._parse_toutiao_html(html, max_results)
            
            self._save_results("toutiao", keyword, results)
            
            return results
    
    def _parse_toutiao_html(self, html, max_results=15):
        """解析头条搜索HTML - 从script标签中提取JSON数据"""
        import re
        
        # 查找所有script标签
        script_pattern = r'<script[^>]*>(.*?)</script>'
        scripts = re.findall(script_pattern, html, re.DOTALL)
        
        articles = []
        seen_titles = set()
        
        for script in scripts:
            if len(script) > 5000 and ('"title"' in script or '"abstract"' in script):
                # 提取标题
                titles = re.findall(r'"title"\s*:\s*"([^"]{10,300})"', script)
                # 提取摘要
                abstracts = re.findall(r'"abstract"\s*:\s*"([^"]{10,500})"', script)
                # 提取来源
                sources = re.findall(r'"source"\s*:\s*"([^"]{2,50})"', script)
                
                for i, title in enumerate(titles):
                    # 清理HTML标签
                    clean_title = re.sub(r'\\u003cem\\u003e|\\u003c/em\\u003e', '', title)
                    clean_title = re.sub(r'\s+', ' ', clean_title).strip()
                    
                    # 去重
                    if clean_title and clean_title not in seen_titles and len(clean_title) > 10:
                        seen_titles.add(clean_title)
                        
                        abstract = ''
                        if i < len(abstracts):
                            abstract = re.sub(r'\\u003cem\\u003e|\\u003c/em\\u003e', '', abstracts[i])
                            abstract = re.sub(r'\s+', ' ', abstract).strip()
                        
                        source = sources[i] if i < len(sources) else ''
                        
                        articles.append({
                            "title": clean_title,
                            "abstract": abstract,
                            "source": source
                        })
        
        print(f"[✓] 提取 {len(articles[:max_results])} 条头条内容")
        return articles[:max_results]
    
    def douyin_search(self, keyword, max_results=10):
        """
        搜索抖音 - 必须使用有头浏览器（无头会触发验证码）
        首次需要登录，后续cookie可能部分有效
        """
        print(f"[→] 抖音搜索: {keyword}")
        
        import urllib.parse
        encoded_keyword = urllib.parse.quote(keyword)
        
        with sync_playwright() as p:
            # 必须使用有头浏览器，否则触发验证码
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(
                viewport={'width': 1280, 'height': 900}
            )
            
            # 尝试加载历史cookie
            cookie_file = "douyin_cookies.json"
            if os.path.exists(cookie_file):
                try:
                    with open(cookie_file, 'r', encoding='utf-8') as f:
                        cookies = json.load(f)
                    context.add_cookies(cookies)
                    print("[✓] 已加载历史cookie")
                except:
                    pass
            
            page = context.new_page()
            
            # 先访问首页建立session
            page.goto('https://www.douyin.com', wait_until='domcontentloaded')
            time.sleep(3)
            
            # 访问搜索页
            url = f'https://www.douyin.com/search/{encoded_keyword}'
            page.goto(url, wait_until='domcontentloaded')
            
            # 检测登录状态
            time.sleep(5)
            html = page.content()
            
            # 检查是否需要登录
            if '登录后即可搜索' in html:
                print("\n" + "="*60)
                print("[!] 抖音需要登录")
                print("请在弹出窗口中完成扫码或手机验证码登录")
                print("等待90秒...")
                print("="*60 + "\n")
                
                logged_in = False
                for i in range(90):
                    time.sleep(1)
                    html = page.content()
                    if '登录后即可搜索' not in html and len(html) > 100000:
                        print(f"[✓] 登录成功！（{i+1}秒）")
                        logged_in = True
                        
                        # 保存cookie
                        cookies = context.cookies()
                        with open(cookie_file, 'w', encoding='utf-8') as f:
                            json.dump(cookies, f, ensure_ascii=False, indent=2)
                        print("[✓] Cookie已保存")
                        break
                    
                    if (i+1) % 15 == 0:
                        print(f"  ...等待中 ({i+1}/90秒)")
                
                if not logged_in:
                    print("[✗] 登录超时")
                    browser.close()
                    return []
            else:
                print("[✓] 已登录状态")
            
            # 等待搜索结果加载
            print("[→] 等待搜索结果...")
            time.sleep(8)
            
            # 滚动加载更多
            print("[→] 滚动加载更多...")
            for i in range(5):
                page.evaluate('window.scrollBy(0, 1000)')
                time.sleep(2)
            
            time.sleep(3)
            
            # 获取最终HTML
            html = page.content()
            
            # 解析视频数据
            results = self._parse_douyin_html(page, html, max_results)
            
            self._save_results("douyin", keyword, results)
            
            browser.close()
            return results
    
    def _parse_douyin_html(self, page, html, max_results=10):
        """解析抖音搜索页面视频"""
        videos = []
        
        # 方式1: Playwright选择器提取
        selectors = [
            'div[class*="card"]',
            '[class*="search-card"]',
            '[class*="video-card"]',
        ]
        
        for selector in selectors:
            elements = page.query_selector_all(selector)
            for elem in elements[:max_results]:
                try:
                    text = elem.inner_text()
                    if text and len(text) > 10:
                        lines = [l.strip() for l in text.split('\n') if l.strip()]
                        if lines:
                            title = lines[0][:100]
                            videos.append({
                                'title': title,
                                'full_text': '\n'.join(lines[:5])
                            })
                except:
                    continue
            
            if videos:
                break
        
        # 方式2: 从HTML文本提取
        if not videos:
            text_pattern = r'<(?:div|span|p)[^>]*>([^<]{20,200})</'
            texts = re.findall(text_pattern, html)
            
            seen = set()
            for text in texts:
                clean = re.sub(r'\s+', ' ', text).strip()
                if clean and len(clean) > 15 and clean not in seen:
                    seen.add(clean)
                    if any(kw in clean for kw in ['白冰', '偷税', '网红', '探店']):
                        videos.append({'title': clean})
                
                if len(videos) >= max_results:
                    break
        
        # 去重
        unique = []
        seen_titles = set()
        for v in videos:
            title = v.get('title', '')
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique.append(v)
        
        print(f"[✓] 提取 {len(unique)} 条抖音视频")
        return unique[:max_results]
    
    def xiaohongshu_search(self, keyword, max_results=15):
        """
        搜索小红书 - 必须使用有头浏览器
        首次需要登录，后续使用保存的cookie
        """
        print(f"[→] 小红书搜索: {keyword}")
        
        import urllib.parse
        encoded_keyword = urllib.parse.quote(keyword)
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(
                viewport={'width': 1280, 'height': 900}
            )
            
            # 加载cookie
            cookie_file = "xiaohongshu_cookies.json"
            if os.path.exists(cookie_file):
                with open(cookie_file, 'r', encoding='utf-8') as f:
                    cookies = json.load(f)
                context.add_cookies(cookies)
                print("[✓] 已加载cookie")
            
            page = context.new_page()
            
            # 访问搜索页
            url = f'https://www.xiaohongshu.com/search_result?keyword={encoded_keyword}'
            page.goto(url, wait_until='domcontentloaded')
            
            print("[→] 等待页面加载...")
            time.sleep(8)
            
            # 检查是否需要登录
            html = page.content()
            
            if '登录' in html and len(html) < 300000:
                print("\n" + "="*60)
                print("[!] 小红书需要登录")
                print("请在弹出窗口中完成扫码登录")
                print("等待90秒...")
                print("="*60 + "\n")
                
                logged_in = False
                for i in range(90):
                    time.sleep(1)
                    html = page.content()
                    if '登录' not in html and len(html) > 300000:
                        print(f"[✓] 登录成功！（{i+1}秒）")
                        logged_in = True
                        
                        # 保存cookie
                        cookies = context.cookies()
                        with open(cookie_file, 'w', encoding='utf-8') as f:
                            json.dump(cookies, f, ensure_ascii=False, indent=2)
                        print("[✓] Cookie已保存")
                        break
                    
                    if (i+1) % 15 == 0:
                        print(f"  ...等待中 ({i+1}/90秒)")
                
                if not logged_in:
                    print("[✗] 登录超时")
                    browser.close()
                    return []
            else:
                print("[✓] 已登录状态或页面正常")
            
            # 滚动加载
            print("[→] 滚动加载更多...")
            for i in range(3):
                page.evaluate('window.scrollBy(0, 800)')
                time.sleep(2)
            
            time.sleep(3)
            
            # 获取最终HTML
            html = page.content()
            
            # 解析笔记
            notes = self._parse_xiaohongshu_html(page, html, max_results)
            
            self._save_results("xiaohongshu", keyword, notes)
            
            browser.close()
            return notes
    
    def _parse_xiaohongshu_html(self, page, html, max_results=15):
        """解析小红书搜索页面"""
        
        notes = []
        
        # 方式1: 通过常见class选择器
        selectors = [
            '[class*="note-item"]',
            '[class*="feed-item"]',
            '[class*="card"]',
            'a[href*="/explore/"]',
        ]
        
        for selector in selectors:
            elements = page.query_selector_all(selector)
            print(f"  选择器 '{selector}': {len(elements)} 个元素")
            
            for elem in elements[:max_results]:
                try:
                    text = elem.inner_text()
                    if text and len(text) > 10:
                        lines = [l.strip() for l in text.split('\n') if l.strip()]
                        if lines:
                            title = lines[0][:100]
                            notes.append({
                                'title': title,
                                'full_text': '\n'.join(lines[:5])
                            })
                except:
                    continue
            
            if notes:
                break
        
        # 方式2: 从HTML提取文本
        if not notes:
            text_pattern = r'<(?:div|span|p)[^>]*>([^<]{20,200})</'
            texts = re.findall(text_pattern, html)
            
            seen = set()
            for text in texts:
                clean = re.sub(r'\s+', ' ', text).strip()
                if clean and len(clean) > 15 and clean not in seen:
                    seen.add(clean)
                    if any(kw in clean for kw in ['白冰', '偷税', '网红', '探店']):
                        notes.append({'title': clean})
                
                if len(notes) >= max_results:
                    break
        
        # 去重
        unique = []
        seen_titles = set()
        for n in notes:
            title = n.get('title', '')
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique.append(n)
        
        print(f"[✓] 提取 {len(unique)} 条笔记")
        return unique[:max_results]
    
    def run_all(self, keyword):
        """
        一键搜索所有可用平台
        """
        print(f"\n{'='*60}")
        print(f"开始多平台舆情搜索: {keyword}")
        print(f"{'='*60}\n")
        
        all_results = {}
        
        # B站（无需登录）
        try:
            bilibili_results = self.bilibili_search(keyword)
            all_results['bilibili'] = bilibili_results
        except Exception as e:
            print(f"[✗] B站搜索失败: {e}")
            all_results['bilibili'] = []
        
        # 微博（需要cookie）
        if os.path.exists(self.cookies_file):
            try:
                weibo_results = self.weibo_search(keyword)
                all_results['weibo'] = weibo_results
            except Exception as e:
                print(f"[✗] 微博搜索失败: {e}")
                all_results['weibo'] = []
        else:
            print("[⚠] 跳过微博（未登录）")
            all_results['weibo'] = []
        
        # 头条（无需登录，但可能触发验证码）
        try:
            toutiao_results = self.toutiao_search(keyword)
            all_results['toutiao'] = toutiao_results
        except Exception as e:
            print(f"[✗] 头条搜索失败: {e}")
            all_results['toutiao'] = []
        
        # 抖音（需要登录，有头浏览器）
        try:
            print("[→] 抖音搜索: 需要启动有头浏览器...")
            douyin_results = self.douyin_search(keyword)
            all_results['douyin'] = douyin_results
        except Exception as e:
            print(f"[✗] 抖音搜索失败: {e}")
            all_results['douyin'] = []
        
        # 小红书（需要登录，有头浏览器）
        try:
            print("[→] 小红书搜索: 需要启动有头浏览器...")
            xhs_results = self.xiaohongshu_search(keyword)
            all_results['xiaohongshu'] = xhs_results
        except Exception as e:
            print(f"[✗] 小红书搜索失败: {e}")
            all_results['xiaohongshu'] = []
        
        # 汇总
        total = sum(len(v) for v in all_results.values())
        print(f"\n{'='*60}")
        print(f"搜索完成！共获取 {total} 条结果")
        print(f"  - 微博: {len(all_results['weibo'])} 条")
        print(f"  - B站: {len(all_results['bilibili'])} 条")
        print(f"  - 头条: {len(all_results['toutiao'])} 条")
        print(f"  - 抖音: {len(all_results['douyin'])} 条")
        print(f"  - 小红书: {len(all_results['xiaohongshu'])} 条")
        print(f"{'='*60}")
        
        # 打印头条详情
        if all_results['toutiao']:
            print(f"\n📰 今日头条详情:")
            print(f"{'='*60}")
            for i, item in enumerate(all_results['toutiao'][:10], 1):
                print(f"\n[{i}] {item.get('title', '')}")
                if item.get('abstract'):
                    print(f"    📄 {item['abstract'][:120]}...")
                if item.get('source'):
                    print(f"    📰 来源: {item['source']}")
        
        # 打印抖音详情
        if all_results['douyin']:
            print(f"\n🎵 抖音详情:")
            print(f"{'='*60}")
            for i, item in enumerate(all_results['douyin'][:10], 1):
                print(f"\n[{i}] {item.get('title', '')[:80]}...")
                if item.get('full_text'):
                    text = item['full_text'].replace('\n', ' | ')
                    print(f"    {text[:150]}...")
        
        # 打印小红书详情
        if all_results['xiaohongshu']:
            print(f"\n📕 小红书详情:")
            print(f"{'='*60}")
            for i, item in enumerate(all_results['xiaohongshu'][:10], 1):
                print(f"\n[{i}] {item.get('title', '')[:80]}...")
                if item.get('full_text'):
                    text = item['full_text'].replace('\n', ' | ')
                    print(f"    {text[:150]}...")
        
        return all_results


# CLI入口
def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='多平台舆情监控工具')
    parser.add_argument('keyword', nargs='?', help='搜索关键词')
    parser.add_argument('--platform', choices=['weibo', 'bilibili', 'toutiao', 'douyin', 'xiaohongshu', 'all'], 
                       default='all', help='选择平台 (默认: all)')
    parser.add_argument('--login-weibo', action='store_true', help='登录微博')
    parser.add_argument('--login-douyin', action='store_true', help='登录抖音')
    parser.add_argument('--output', default='./output', help='输出目录')
    
    args = parser.parse_args()
    
    monitor = SentimentMonitor(output_dir=args.output)
    
    if args.login_weibo:
        monitor.weibo_login()
    elif args.login_douyin:
        print("[!] 抖音登录功能开发中，请手动访问 https://www.douyin.com 登录")
    elif args.keyword:
        if args.platform == 'all':
            results = monitor.run_all(args.keyword)
        elif args.platform == 'weibo':
            results = monitor.weibo_search(args.keyword)
            print(json.dumps(results, ensure_ascii=False, indent=2))
        elif args.platform == 'bilibili':
            results = monitor.bilibili_search(args.keyword)
            print(json.dumps(results, ensure_ascii=False, indent=2))
        elif args.platform == 'toutiao':
            results = monitor.toutiao_search(args.keyword)
            print(json.dumps(results, ensure_ascii=False, indent=2))
        elif args.platform == 'douyin':
            results = monitor.douyin_search(args.keyword)
            print(json.dumps(results, ensure_ascii=False, indent=2))
        elif args.platform == 'xiaohongshu':
            results = monitor.xiaohongshu_search(args.keyword)
            print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
