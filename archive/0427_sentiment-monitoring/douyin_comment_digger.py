#!/usr/bin/env python3
"""
抖音评论深挖 - 改进版
"""

import json
import time
import re
import os
from playwright.sync_api import sync_playwright

class DouyinCommentDigger:
    def __init__(self, output_dir='./output'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.cookie_file = "douyin_cookies.json"
    
    def dig_video_comments(self, video_url, max_comments=50):
        """
        直接访问视频URL深挖评论
        """
        print(f"[→] 抖音视频: {video_url}")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(
                viewport={'width': 1280, 'height': 900}
            )
            
            # 加载cookie
            if os.path.exists(self.cookie_file):
                with open(self.cookie_file, 'r', encoding='utf-8') as f:
                    cookies = json.load(f)
                context.add_cookies(cookies)
                print("[✓] 已加载抖音cookie")
            
            page = context.new_page()
            page.goto(video_url, wait_until='domcontentloaded')
            time.sleep(15)
            
            # 检查是否需要登录
            html = page.content()
            if '登录' in html or '手机号登录' in html:
                print("\n" + "="*60)
                print("[!] 抖音需要登录才能查看评论")
                print("请在弹出窗口中完成登录")
                print("等待120秒...")
                print("="*60)
                
                # 播放声音提醒
                try:
                    import subprocess
                    subprocess.run(['say', '抖音需要登录，请在浏览器窗口中完成登录操作'], check=False)
                except:
                    pass
                
                for i in range(120):
                    time.sleep(1)
                    html = page.content()
                    if '登录' not in html and '手机号登录' not in html:
                        print(f"\n[✓] 登录成功！（{i+1}秒）")
                        # 保存cookie
                        cookies = context.cookies()
                        with open(self.cookie_file, 'w', encoding='utf-8') as f:
                            json.dump(cookies, f, ensure_ascii=False, indent=2)
                        break
                    if (i+1) % 10 == 0:
                        print(f"  ...等待中 ({i+1}/120秒)")
            
            # 滚动加载评论
            print("\n[→] 滚动加载评论...")
            for i in range(10):
                page.evaluate('window.scrollBy(0, 1500)')
                time.sleep(2)
            
            time.sleep(5)
            
            # 提取评论 - 改进过滤
            print("[→] 提取评论...")
            
            comments_data = page.evaluate('''() => {
                const results = [];
                const allDivs = document.querySelectorAll('div');
                
                for (const div of allDivs) {
                    const text = div.innerText || '';
                    // 评论特征：包含中文，长度适中
                    if (text.length > 15 && text.length < 300 && /[\u4e00-\u9fff]/.test(text)) {
                        // 排除明显的非评论内容
                        const exclude = ['首页', '推荐', '关注', '朋友', '消息', '我',
                                        '登录', '注册', '搜索', '热点', '直播',
                                        '广告', '推广', '抖音', 'douyin',
                                        '高清', '1080P', '720P', '540P', '智能',
                                        '合集', '更新至', '大家都在搜',
                                        '作者回复过', '展开', '认证徽章',
                                        '京公网安备', '网络文化许可证', '互联网宗教',
                                        '药品医疗器械', '互联网新闻信息服务许可证',
                                        '违法和不良信息举报', '体育饭圈专项举报',
                                        '全部公开课', '游戏二次元', '音乐影视', '美食知识',
                                        '小剧场生活vlog', '体育旅行', '亲子动物', '三农汽车',
                                        '美妆穿搭', '剧情', '搞笑', '情感', '明星',
                                        '综艺', '电视剧', '电影', '纪录片',
                                        '创作背景', '生平', '第一部分', '第二部分', 
                                        '第三部分', '第四部分', '第五部分', '第六部分',
                                        '结语', '深度解析', '一口气看完', '人文星闪耀计划',
                                        '影娱漫谈编辑部', '了不起的精讲团', '高质量科普视频',
                                        '重塑大脑', '变强之路', '学习方法', '强大自己', '心理学',
                                        '经济学', '财经', '商业思维', '认知觉醒', '行为心理学'];
                        
                        const hasExclude = exclude.some(kw => text.includes(kw));
                        if (!hasExclude) {
                            // 检查是否有嵌套结构（评论通常有用户名+内容+时间）
                            const childDivs = div.querySelectorAll('div');
                            if (childDivs.length >= 2 && childDivs.length <= 6) {
                                // 进一步检查：评论通常包含@用户名或时间信息
                                const hasTime = /\d{1,2}[月日]|\d{4}-\d{2}-\d{2}/.test(text);
                                const hasUser = text.includes('@') || text.includes('·');
                                
                                if (hasTime || hasUser || text.length > 30) {
                                    results.push(text.substring(0, 300));
                                }
                            }
                        }
                    }
                }
                
                return results;
            }''')
            
            print(f"[✓] 找到 {len(comments_data)} 条可能评论")
            
            # 去重和进一步过滤
            seen = set()
            comments = []
            for text in comments_data:
                # 排除纯UI文本
                if 'P' in text and '高清' in text:
                    continue
                if text.startswith('@') and len(text) < 50:
                    continue
                
                h = hash(text[:80])
                if h not in seen:
                    seen.add(h)
                    comments.append({'text': text})
                
                if len(comments) >= max_comments:
                    break
            
            print(f"[✓] 提取 {len(comments)} 条有效评论")
            
            # 保存结果
            if comments:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"douyin_comments_{timestamp}.json"
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump({
                        'video_url': video_url,
                        'count': len(comments),
                        'comments': comments
                    }, f, ensure_ascii=False, indent=2)
                
                print(f"[✓] 结果已保存: {filepath}")
            
            browser.close()
            return comments

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='抖音评论深挖')
    parser.add_argument('video_url', help='抖音视频URL')
    parser.add_argument('--max', type=int, default=50, help='最大评论数')
    args = parser.parse_args()
    
    digger = DouyinCommentDigger()
    comments = digger.dig_video_comments(args.video_url, args.max)
    
    print(f"\n{'='*60}")
    print(f"评论列表 - 共 {len(comments)} 条")
    print(f"{'='*60}\n")
    
    for i, comment in enumerate(comments[:20], 1):
        text = comment.get('text', '')
        print(f"[{i}] {text[:200]}...")
        print()
