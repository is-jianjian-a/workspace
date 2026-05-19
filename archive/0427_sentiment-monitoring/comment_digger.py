#!/usr/bin/env python3
"""
评论深挖工具 - 进入单条内容页面抓取评论
支持: 微博、B站、抖音、小红书
"""

import json
import time
import re
import os
from playwright.sync_api import sync_playwright

class CommentDigger:
    def __init__(self, output_dir="./output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def weibo_comments(self, weibo_url, max_comments=50):
        """
        深挖微博评论 - 使用有头浏览器确保登录状态
        需要先点击评论按钮展开评论区域
        """
        print(f"[→] 深挖微博评论: {weibo_url}")
        
        cookie_file = "weibo_cookies.json"
        
        with sync_playwright() as p:
            # 使用有头浏览器，确保登录状态有效
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(
                viewport={'width': 1280, 'height': 900}
            )
            
            # 加载cookie
            if os.path.exists(cookie_file):
                with open(cookie_file, 'r', encoding='utf-8') as f:
                    cookies = json.load(f)
                context.add_cookies(cookies)
                print("[✓] 已加载微博cookie")
            else:
                print("[✗] 未找到微博cookie，请先登录")
                browser.close()
                return []
            
            page = context.new_page()
            page.goto(weibo_url, wait_until='networkidle')
            
            print("[→] 等待页面加载...")
            time.sleep(8)
            
            # 检查是否需要登录
            html = page.content()
            if '登录' in html and len(html) < 200000:
                print("\n" + "="*60)
                print("[!] 微博需要登录")
                print("请在弹出窗口中完成登录")
                print("等待60秒...")
                print("="*60 + "\n")
                
                for i in range(60):
                    time.sleep(1)
                    html = page.content()
                    if '登录' not in html:
                        print(f"[✓] 登录成功！（{i+1}秒）")
                        # 保存cookie
                        cookies = context.cookies()
                        with open(cookie_file, 'w', encoding='utf-8') as f:
                            json.dump(cookies, f, ensure_ascii=False, indent=2)
                        break
                    if (i+1) % 10 == 0:
                        print(f"  ...等待中 ({i+1}/60秒)")
            
            # 点击评论按钮展开评论
            print("[→] 点击评论按钮...")
            
            # 尝试多种方式点击评论按钮
            clicked = False
            
            # 方式1: 通过文本内容找评论按钮
            try:
                # 查找包含"评论"文本的按钮或span
                comment_btns = page.query_selector_all('button, span, a, div')
                for btn in comment_btns:
                    text = btn.inner_text().strip()
                    if text == '评论' or text == '评论 ':
                        btn.click()
                        print("[✓] 已点击评论按钮")
                        clicked = True
                        time.sleep(3)
                        break
            except Exception as e:
                print(f"  方式1失败: {e}")
            
            # 方式2: 通过evaluate点击
            if not clicked:
                try:
                    result = page.evaluate('''() => {
                        // 查找评论按钮
                        const allElements = document.querySelectorAll('button, span, a, div');
                        for (const el of allElements) {
                            if (el.textContent.trim() === '评论') {
                                el.click();
                                return true;
                            }
                        }
                        return false;
                    }''')
                    if result:
                        print("[✓] 已通过JS点击评论按钮")
                        clicked = True
                        time.sleep(3)
                except Exception as e:
                    print(f"  方式2失败: {e}")
            
            # 方式3: 查找评论数量链接（如"评论 123"）
            if not clicked:
                try:
                    comment_links = page.query_selector_all('a[href*="comment"]')
                    if comment_links:
                        comment_links[0].click()
                        print("[✓] 已点击评论链接")
                        clicked = True
                        time.sleep(3)
                except Exception as e:
                    print(f"  方式3失败: {e}")
            
            if not clicked:
                print("[!] 未能点击评论按钮，尝试直接滚动查找评论")
            
            # 滚动加载评论
            print("[→] 滚动加载评论...")
            comments = []
            last_count = 0
            no_change_count = 0
            
            for i in range(15):
                # 获取当前评论元素 - 使用更宽泛的选择器
                comment_elements = page.query_selector_all('[class*="comment"], [class*="Comment"], [class*="reply"], [class*="Reply"]')
                current_count = len(comment_elements)
                
                if current_count > last_count:
                    print(f"  滚动{i+1}: 发现 {current_count} 条评论元素")
                    last_count = current_count
                    no_change_count = 0
                else:
                    no_change_count += 1
                    if no_change_count >= 3:
                        print("  评论加载完成")
                        break
                
                page.evaluate('window.scrollBy(0, 1000)')
                time.sleep(2)
            
            # 提取评论内容 - 尝试多种选择器
            print("[→] 提取评论内容...")
            
            # 方式1: 通过选择器提取
            selectors = [
                '[class*="comment"]',
                '[class*="Comment"]',
                '[class*="reply"]',
                '[class*="Reply"]'
            ]
            
            for selector in selectors:
                elements = page.query_selector_all(selector)
                print(f"  选择器 '{selector}': {len(elements)} 个元素")
                
                for elem in elements[:max_comments]:
                    try:
                        text = elem.inner_text()
                        if text and len(text) > 10:
                            lines = [l.strip() for l in text.split('\n') if l.strip()]
                            if len(lines) >= 2:
                                comments.append({
                                    'author': lines[0][:50],
                                    'text': '\n'.join(lines[1:])[:500]
                                })
                    except:
                        continue
                
                if comments:
                    break
            
            # 方式2: 从页面所有文本中提取可能的评论
            if not comments:
                print("[→] 尝试从页面文本提取评论...")
                
                # 获取页面中所有可能包含评论的div
                all_divs = page.query_selector_all('div')
                seen_texts = set()  # 去重
                
                for div in all_divs:
                    try:
                        text = div.inner_text()
                        # 评论特征：包含中文，长度适中，不是导航元素
                        if text and 20 <= len(text) <= 500 and re.search(r'[\u4e00-\u9fff]', text):
                            # 排除非评论内容
                            exclude = ['首页', '关注', '热门', '登录', '注册', '热搜', 'Copyright',
                                      '播放', '倍速', '高清', '标清', '字幕', 'Color', 'Opacity',
                                      '媒体流', '直播', '小窗', '对话窗口', 'Escape', '微博视频号',
                                      '已编辑', '转发', '收藏',
                                      '帮助中心', '微博客服', '自助服务', '常见问题',
                                      '合作&服务', '微博营销', '合作热线', '开放平台',
                                      '举报中心', '违规投诉', '处理大厅', '舞弊举报',
                                      '关于微博', 'About Weibo', '客户端下载', '微博招聘',
                                      '网站备案', '营业执照', '隐私安全']
                            if not any(kw in text for kw in exclude):
                                # 去重检查
                                text_hash = hash(text[:100])
                                if text_hash in seen_texts:
                                    continue
                                seen_texts.add(text_hash)
                                
                                # 检查是否有嵌套的div（评论通常有嵌套结构）
                                child_divs = div.query_selector_all('div')
                                if len(child_divs) >= 2:
                                    # 进一步过滤：评论应该包含实际内容，不只是时间/地点
                                    # 提取纯文本（去掉时间、地点等元信息）
                                    lines = [l.strip() for l in text.split('\n') if l.strip()]
                                    # 检查是否有实质性的评论内容（至少一行不是纯时间/地点）
                                    has_content = False
                                    for line in lines:
                                        # 如果时间格式或地点格式，跳过
                                        if re.match(r'^\d{2}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{2}', line):
                                            continue
                                        if line.startswith('来自') or line.startswith('回复@'):
                                            continue
                                        if line in ['1', '转发', '评论', '赞', '收藏']:
                                            continue
                                        if len(line) > 5 and re.search(r'[\u4e00-\u9fff]', line):
                                            has_content = True
                                            break
                                    
                                    if has_content:
                                        comments.append({
                                            'text': text[:500]
                                        })
                    except:
                        continue
                    
                    if len(comments) >= max_comments:
                        break
            
            # 方式3: 从HTML正则提取
            if not comments:
                print("[→] 尝试从HTML提取评论...")
                html = page.content()
                # 微博评论通常在特定结构中
                comment_pattern = r'<div[^>]*class="[^"]*(?:comment|Comment)[^"]*"[^>]*>(.*?)</div>'
                matches = re.findall(comment_pattern, html, re.DOTALL)
                
                for match in matches[:max_comments]:
                    # 提取文本
                    text = re.sub(r'<[^>]+>', '', match)
                    text = re.sub(r'\s+', ' ', text).strip()
                    if text and len(text) > 10:
                        comments.append({'text': text[:500]})
            
            print(f"[✓] 提取 {len(comments)} 条有效评论")
            
            # 保存结果
            if comments:
                weibo_id = re.search(r'/([A-Za-z0-9]+)$', weibo_url)
                weibo_id = weibo_id.group(1) if weibo_id else 'unknown'
                
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"weibo_comments_{weibo_id}_{timestamp}.json"
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump({
                        'url': weibo_url,
                        'count': len(comments),
                        'comments': comments
                    }, f, ensure_ascii=False, indent=2)
                
                print(f"[✓] 结果已保存: {filepath}")
            
            browser.close()
            return comments
    
    def bilibili_comments(self, bvid, max_comments=50):
        """
        深挖B站视频评论
        """
        print(f"[→] 深挖B站评论: {bvid}")
        
        url = f"https://www.bilibili.com/video/{bvid}"
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={'width': 1280, 'height': 900}
            )
            page = context.new_page()
            page.goto(url, wait_until='networkidle')
            
            print("[→] 等待页面加载...")
            time.sleep(8)
            
            # 滚动到评论区
            print("[→] 滚动到评论区...")
            for i in range(8):
                page.evaluate('window.scrollBy(0, 1000)')
                time.sleep(2)
            
            # 提取评论
            comments = []
            
            # 尝试多种选择器
            selectors = [
                '.reply-item',
                '.comment-item',
                '[class*="reply"]',
                '[class*="comment"]'
            ]
            
            for selector in selectors:
                elements = page.query_selector_all(selector)
                print(f"  选择器 '{selector}': {len(elements)} 个元素")
                
                for elem in elements[:max_comments]:
                    try:
                        text = elem.inner_text()
                        if text and len(text) > 5:
                            lines = [l.strip() for l in text.split('\n') if l.strip()]
                            if len(lines) >= 2:
                                comments.append({
                                    'author': lines[0][:50],
                                    'text': '\n'.join(lines[1:])[:500]
                                })
                    except:
                        continue
                
                if comments:
                    break
            
            # 如果没找到，尝试从页面文本提取
            if not comments:
                print("[→] 尝试从页面文本提取评论...")
                html = page.content()
                # B站评论通常在特定class中
                comment_pattern = r'<span[^>]*class="[^"]*reply[^"]*"[^>]*>([^<]{5,500})</span>'
                texts = re.findall(comment_pattern, html)
                for text in texts[:max_comments]:
                    clean = re.sub(r'\s+', ' ', text).strip()
                    if clean and len(clean) > 5:
                        comments.append({'text': clean})
            
            print(f"[✓] 提取 {len(comments)} 条评论")
            
            # 保存
            if comments:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"bilibili_comments_{bvid}_{timestamp}.json"
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump({
                        'bvid': bvid,
                        'url': url,
                        'count': len(comments),
                        'comments': comments
                    }, f, ensure_ascii=False, indent=2)
                
                print(f"[✓] 结果已保存: {filepath}")
            
            browser.close()
            return comments
    
    def douyin_comments(self, video_url, max_comments=30):
        """
        深挖抖音视频评论 - 需要登录
        """
        print(f"[→] 深挖抖音评论: {video_url}")
        
        cookie_file = "douyin_cookies.json"
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)  # 抖音必须有头
            context = browser.new_context(
                viewport={'width': 1280, 'height': 900}
            )
            
            # 加载cookie
            if os.path.exists(cookie_file):
                with open(cookie_file, 'r', encoding='utf-8') as f:
                    cookies = json.load(f)
                context.add_cookies(cookies)
                print("[✓] 已加载抖音cookie")
            
            page = context.new_page()
            page.goto(video_url, wait_until='domcontentloaded')
            
            print("[→] 等待页面加载...")
            time.sleep(8)
            
            # 检查登录
            html = page.content()
            if '登录' in html:
                print("[!] 需要登录，请在弹出窗口完成登录（60秒）")
                time.sleep(60)
            
            # 滚动加载评论
            print("[→] 滚动加载评论...")
            for i in range(5):
                page.evaluate('window.scrollBy(0, 800)')
                time.sleep(2)
            
            # 提取评论
            comments = []
            elements = page.query_selector_all('[class*="comment"], [class*="reply"]')
            
            for elem in elements[:max_comments]:
                try:
                    text = elem.inner_text()
                    if text and len(text) > 5:
                        lines = [l.strip() for l in text.split('\n') if l.strip()]
                        if lines:
                            comments.append({
                                'text': '\n'.join(lines)[:500]
                            })
                except:
                    continue
            
            print(f"[✓] 提取 {len(comments)} 条评论")
            
            # 保存
            if comments:
                video_id = re.search(r'/video/([0-9]+)', video_url)
                video_id = video_id.group(1) if video_id else 'unknown'
                
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"douyin_comments_{video_id}_{timestamp}.json"
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump({
                        'url': video_url,
                        'count': len(comments),
                        'comments': comments
                    }, f, ensure_ascii=False, indent=2)
                
                print(f"[✓] 结果已保存: {filepath}")
            
            browser.close()
            return comments
    
    def xiaohongshu_comments(self, note_url, max_comments=30):
        """
        深挖小红书笔记评论 - 需要登录
        """
        print(f"[→] 深挖小红书评论: {note_url}")
        
        cookie_file = "xiaohongshu_cookies.json"
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(
                viewport={'width': 1280, 'height': 900}
            )
            
            # 加载cookie
            if os.path.exists(cookie_file):
                with open(cookie_file, 'r', encoding='utf-8') as f:
                    cookies = json.load(f)
                context.add_cookies(cookies)
                print("[✓] 已加载小红书cookie")
            
            page = context.new_page()
            page.goto(note_url, wait_until='domcontentloaded')
            
            print("[→] 等待页面加载...")
            time.sleep(8)
            
            # 检查登录
            html = page.content()
            if '登录' in html and len(html) < 300000:
                print("[!] 需要登录，请在弹出窗口完成登录（60秒）")
                time.sleep(60)
            
            # 滚动加载评论
            print("[→] 滚动加载评论...")
            for i in range(5):
                page.evaluate('window.scrollBy(0, 800)')
                time.sleep(2)
            
            # 提取评论
            comments = []
            elements = page.query_selector_all('[class*="comment"], [class*="reply"]')
            
            for elem in elements[:max_comments]:
                try:
                    text = elem.inner_text()
                    if text and len(text) > 5:
                        lines = [l.strip() for l in text.split('\n') if l.strip()]
                        if lines:
                            comments.append({
                                'text': '\n'.join(lines)[:500]
                            })
                except:
                    continue
            
            print(f"[✓] 提取 {len(comments)} 条评论")
            
            # 保存
            if comments:
                note_id = re.search(r'/explore/([a-z0-9]+)', note_url)
                note_id = note_id.group(1) if note_id else 'unknown'
                
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"xiaohongshu_comments_{note_id}_{timestamp}.json"
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump({
                        'url': note_url,
                        'count': len(comments),
                        'comments': comments
                    }, f, ensure_ascii=False, indent=2)
                
                print(f"[✓] 结果已保存: {filepath}")
            
            browser.close()
            return comments


# CLI入口
def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='评论深挖工具')
    parser.add_argument('url', help='内容URL')
    parser.add_argument('--platform', choices=['weibo', 'bilibili', 'douyin', 'xiaohongshu'], 
                       required=True, help='平台类型')
    parser.add_argument('--max', type=int, default=50, help='最大评论数')
    
    args = parser.parse_args()
    
    digger = CommentDigger()
    
    if args.platform == 'weibo':
        comments = digger.weibo_comments(args.url, args.max)
    elif args.platform == 'bilibili':
        # 从URL提取bvid
        bvid = args.url.split('/')[-1].split('?')[0]
        comments = digger.bilibili_comments(bvid, args.max)
    elif args.platform == 'douyin':
        comments = digger.douyin_comments(args.url, args.max)
    elif args.platform == 'xiaohongshu':
        comments = digger.xiaohongshu_comments(args.url, args.max)
    
    # 打印结果
    print(f"\n{'='*60}")
    print(f"评论列表 - 共 {len(comments)} 条")
    print(f"{'='*60}")
    
    for i, c in enumerate(comments[:20], 1):
        print(f"\n[{i}] @{c.get('author', '匿名')}")
        print(f"    {c.get('text', '')[:200]}...")
        if c.get('likes'):
            print(f"    👍 {c['likes']}")

if __name__ == '__main__':
    main()
