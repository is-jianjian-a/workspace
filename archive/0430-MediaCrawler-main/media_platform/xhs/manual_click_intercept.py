# -*- coding: utf-8 -*-
"""
方案A实现：用户手动点击 + 页面内XHR拦截

核心原理：
1. 在页面中注入脚本，重写 XMLHttpRequest 和 fetch API
2. 拦截所有小红书API请求的响应
3. 将响应数据存储在 window.__xhsCapturedData 中
4. Playwright定期读取捕获的数据

优势：
- 不需要CDP Fetch域（避免兼容性问题）
- 可以完整捕获响应体
- 与用户手动点击完全同步
"""

import asyncio
import json
from playwright.async_api import async_playwright
from typing import Dict, List, Optional
import utils


# 注入页面的拦截脚本
XHR_INTERCEPT_SCRIPT = """
(function() {
    'use strict';
    
    // 初始化存储
    if (!window.__xhsCapturedData) {
        window.__xhsCapturedData = {
            feeds: [],      // 帖子详情
            comments: [],   // 评论
            subComments: [], // 子评论
            _lastReadIndex: { feeds: 0, comments: 0, subComments: 0 }
        };
    }
    
    const CAPTURED = window.__xhsCapturedData;
    
    // 判断是否是目标API
    function isTargetApi(url) {
        return url && (
            url.includes('/api/sns/web/v1/feed') ||
            url.includes('/api/sns/web/v2/comment/page') ||
            url.includes('/api/sns/web/v1/comment/sub/page')
        );
    }
    
    // 分类存储响应
    function storeResponse(url, data) {
        try {
            const parsed = JSON.parse(data);
            
            if (url.includes('/api/sns/web/v1/feed')) {
                CAPTURED.feeds.push({
                    url: url,
                    data: parsed,
                    timestamp: Date.now()
                });
                console.log('[XHS-Capture] Feed captured:', url);
                
            } else if (url.includes('/api/sns/web/v1/comment/sub/page')) {
                CAPTURED.subComments.push({
                    url: url,
                    data: parsed,
                    timestamp: Date.now()
                });
                console.log('[XHS-Capture] Sub-comment captured');
                
            } else if (url.includes('/api/sns/web/v2/comment/page')) {
                CAPTURED.comments.push({
                    url: url,
                    data: parsed,
                    timestamp: Date.now()
                });
                console.log('[XHS-Capture] Comment captured, count:', 
                    parsed.data?.comments?.length || 0);
            }
            
        } catch (e) {
            console.log('[XHS-Capture] Failed to parse JSON:', e.message);
        }
    }
    
    // 重写 XMLHttpRequest
    const OriginalXHR = window.XMLHttpRequest;
    window.XMLHttpRequest = function() {
        const xhr = new OriginalXHR();
        const originalOpen = xhr.open;
        let requestUrl = '';
        
        xhr.open = function(method, url) {
            requestUrl = url;
            return originalOpen.apply(xhr, arguments);
        };
        
        const originalSend = xhr.send;
        xhr.send = function() {
            const onReadyStateChange = function() {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    if (isTargetApi(requestUrl)) {
                        storeResponse(requestUrl, xhr.responseText);
                    }
                }
            };
            
            xhr.addEventListener('readystatechange', onReadyStateChange);
            return originalSend.apply(xhr, arguments);
        };
        
        return xhr;
    };
    
    // 重写 fetch
    const originalFetch = window.fetch;
    window.fetch = async function(url, options) {
        const response = await originalFetch.apply(window, arguments);
        
        if (isTargetApi(url)) {
            // 克隆响应以便读取
            const clone = response.clone();
            try {
                const text = await clone.text();
                storeResponse(url, text);
            } catch (e) {
                console.log('[XHS-Capture] Failed to read fetch response:', e);
            }
        }
        
        return response;
    };
    
    console.log('[XHS-Capture] Interception script injected successfully');
})();
"""


class XhsManualClickInterceptor:
    """
    小红书手动点击拦截器
    通过页面内脚本拦截XHR/Fetch响应
    """
    
    def __init__(self, page, max_intercepts: int = 3, timeout: int = 120):
        self.page = page
        self.max_intercepts = max_intercepts
        self.timeout = timeout
        self._injected = False
        
    async def inject_interception_script(self):
        """在页面中注入拦截脚本"""
        if self._injected:
            return
            
        await self.page.evaluate(XHR_INTERCEPT_SCRIPT)
        self._injected = True
        utils.logger.info("[Interceptor] ✓ XHR interception script injected")
        
    async def get_captured_data(self) -> Dict:
        """从页面中获取捕获的数据"""
        return await self.page.evaluate("""
            () => {
                const data = window.__xhsCapturedData || {
                    feeds: [], comments: [], subComments: []
                };
                
                // 获取新数据（上次读取之后的新条目）
                const result = {
                    feeds: data.feeds.slice(data._lastReadIndex?.feeds || 0),
                    comments: data.comments.slice(data._lastReadIndex?.comments || 0),
                    subComments: data.subComments.slice(data._lastReadIndex?.subComments || 0)
                };
                
                // 更新读取索引
                data._lastReadIndex = {
                    feeds: data.feeds.length,
                    comments: data.comments.length,
                    subComments: data.subComments.length
                };
                
                return result;
            }
        """)
    
    async def get_stats(self) -> Dict:
        """获取当前捕获统计"""
        return await self.page.evaluate("""
            () => {
                const data = window.__xhsCapturedData || {
                    feeds: [], comments: [], subComments: []
                };
                return {
                    totalFeeds: data.feeds.length,
                    totalComments: data.comments.length,
                    totalSubComments: data.subComments.length
                };
            }
        """)
    
    async def clear_captured_data(self):
        """清空已捕获的数据"""
        await self.page.evaluate("""
            () => {
                if (window.__xhsCapturedData) {
                    window.__xhsCapturedData.feeds = [];
                    window.__xhsCapturedData.comments = [];
                    window.__xhsCapturedData.subComments = [];
                    window.__xhsCapturedData._lastReadIndex = {
                        feeds: 0, comments: 0, subComments: 0
                    };
                }
            }
        """)


async def manual_click_search(
    page, 
    keyword: str, 
    max_notes: int = 3, 
    timeout: int = 120
) -> tuple[List[Dict], List[Dict]]:
    """
    方案A主入口：引导用户手动点击搜索结果，拦截API获取数据
    
    流程：
    1. 打开搜索页
    2. 注入XHR拦截脚本
    3. 显示提示UI
    4. 等待用户手动点击
    5. 轮询捕获的数据
    6. 解析并返回数据
    
    Args:
        page: Playwright Page对象（已连接到用户浏览器）
        keyword: 搜索关键词
        max_notes: 最大拦截帖子数（feed API响应数）
        timeout: 超时时间（秒）
        
    Returns:
        (notes_list, comments_list)
    """
    
    # 1. 导航到搜索页
    search_url = f"https://www.xiaohongshu.com/search_result?keyword={keyword}&type=51"
    utils.logger.info(f"[ManualClick] Opening search page: {search_url}")
    
    await page.goto(search_url, wait_until='networkidle')
    await asyncio.sleep(3)
    
    # 2. 等待搜索结果加载
    try:
        await page.wait_for_selector('section.note-item', timeout=10000)
        utils.logger.info("[ManualClick] Search results loaded")
    except Exception as e:
        utils.logger.error(f"[ManualClick] Failed to load search results: {e}")
        return [], []
    
    # 3. 注入拦截脚本
    interceptor = XhsManualClickInterceptor(page, max_notes, timeout)
    await interceptor.inject_interception_script()
    await interceptor.clear_captured_data()
    
    # 4. 显示提示UI
    await page.evaluate(f"""
        () => {{
            const old = document.getElementById('crawler-hint');
            if (old) old.remove();
            
            const div = document.createElement('div');
            div.id = 'crawler-hint';
            div.style.cssText = `
                position: fixed;
                top: 20px;
                left: 50%;
                transform: translateX(-50%);
                background: linear-gradient(135deg, #ff2442, #ff5c7f);
                color: white;
                padding: 20px 40px;
                border-radius: 12px;
                font-size: 18px;
                font-weight: bold;
                z-index: 99999;
                box-shadow: 0 8px 32px rgba(255,36,66,0.4);
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                text-align: center;
                line-height: 1.6;
                max-width: 600px;
                word-wrap: break-word;
            `;
            div.innerHTML = `
                <div style="font-size: 24px; margin-bottom: 8px;">🔴 手动点击模式已启动</div>
                <div>请点击下方任意帖子，我会自动捕获详情和评论</div>
                <div style="font-size: 14px; opacity: 0.9; margin-top: 8px;">
                    目标: {max_notes}个帖子 | 超时: {timeout}秒
                </div>
                <div id="crawler-status" style="font-size: 13px; margin-top: 10px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.3);">
                    等待点击... 0/{max_notes}
                </div>
            `;
            document.body.appendChild(div);
        }}
    """)
    
    # 5. 等待用户点击并捕获数据
    utils.logger.info("[ManualClick] Waiting for user clicks...")
    start_time = asyncio.get_event_loop().time()
    captured_feeds = []
    captured_comments = []
    
    while True:
        elapsed = asyncio.get_event_loop().time() - start_time
        if elapsed > timeout:
            utils.logger.info(f"[ManualClick] Timeout reached ({timeout}s)")
            break
        
        # 获取新捕获的数据
        new_data = await interceptor.get_captured_data()
        
        new_feeds = new_data.get('feeds', [])
        new_comments = new_data.get('comments', [])
        
        if new_feeds:
            captured_feeds.extend(new_feeds)
            utils.logger.info(f"[ManualClick] +{len(new_feeds)} new feed(s), total: {len(captured_feeds)}/{max_notes}")
            
            # 更新UI
            await page.evaluate(f"""
                () => {{
                    const status = document.getElementById('crawler-status');
                    if (status) {{
                        status.textContent = '已捕获 {len(captured_feeds)}/{max_notes} 个帖子，请继续点击...';
                    }}
                }}
            """)
        
        if new_comments:
            captured_comments.extend(new_comments)
            utils.logger.info(f"[ManualClick] +{len(new_comments)} new comment response(s)")
        
        # 检查是否达到目标
        if len(captured_feeds) >= max_notes:
            utils.logger.info(f"[ManualClick] Reached target: {len(captured_feeds)} feeds")
            break
        
        # 显示剩余时间（每10秒）
        remaining = int(timeout - elapsed)
        if remaining % 10 == 0 and remaining > 0:
            utils.logger.info(f"[ManualClick] Waiting... {remaining}s remaining")
        
        await asyncio.sleep(1)  # 1秒轮询间隔
    
    # 6. 更新UI为完成状态
    await page.evaluate("""
        () => {
            const status = document.getElementById('crawler-status');
            if (status) {
                status.textContent = '✓ 捕获完成！正在处理数据...';
            }
            setTimeout(() => {
                const div = document.getElementById('crawler-hint');
                if (div) {
                    div.style.transition = 'opacity 0.5s';
                    div.style.opacity = '0';
                    setTimeout(() => div.remove(), 500);
                }
            }, 2000);
        }
    """)
    
    # 7. 解析捕获的数据
    notes = []
    for feed in captured_feeds:
        data = feed.get('data', {})
        
        if 'data' in data and 'items' in data['data']:
            for item in data['data']['items']:
                note_card = item.get('note_card', {})
                
                note_data = {
                    'note_id': item.get('id', ''),
                    'title': note_card.get('title', ''),
                    'desc': note_card.get('desc', ''),
                    'type': note_card.get('type', 'normal'),
                    'user': note_card.get('user', {}),
                    'interact_info': note_card.get('interact_info', {}),
                    'time': note_card.get('time', ''),
                    'last_update_time': note_card.get('last_update_time', 0),
                    'ip_location': note_card.get('ip_location', ''),
                    'image_list': note_card.get('image_list', []),
                    'tag_list': note_card.get('tag_list', []),
                    'xsec_token': item.get('xsec_token', ''),
                    'note_url': f"https://www.xiaohongshu.com/explore/{item.get('id', '')}",
                }
                notes.append(note_data)
    
    comments = []
    for comment_resp in captured_comments:
        data = comment_resp.get('data', {})
        
        if 'data' in data and 'comments' in data['data']:
            for comment in data['data']['comments']:
                comment_data = {
                    'id': comment.get('id', ''),
                    'content': comment.get('content', ''),
                    'create_time': comment.get('create_time', ''),
                    'like_count': comment.get('like_count', 0),
                    'user_info': comment.get('user_info', {}),
                    'sub_comment_count': comment.get('sub_comment_count', 0),
                    'pictures': comment.get('pictures', []),
                    'ip_location': comment.get('ip_location', ''),
                    'note_id': comment.get('note_id', ''),  # 可能为空，需要从URL关联
                }
                comments.append(comment_data)
    
    utils.logger.info(f"[ManualClick] Final results: {len(notes)} notes, {len(comments)} comments")
    
    return notes, comments


# 兼容接口
async def search_and_extract_via_manual_click(
    page,
    keyword: str,
    max_notes: int = 3,
    max_comments_per_note: int = 10
) -> List[Dict]:
    """
    兼容browser_search.py接口的手动点击方案
    """
    notes, comments = await manual_click_search(page, keyword, max_notes)
    
    # 将评论关联到帖子（简化：按数量分配）
    # 实际应该根据note_id精确关联
    comments_per_note = len(comments) // len(notes) if notes else 0
    
    result = []
    for i, note in enumerate(notes):
        start_idx = i * comments_per_note
        end_idx = start_idx + max_comments_per_note
        note_comments = comments[start_idx:end_idx] if comments else []
        
        note_data = {
            'note_id': note.get('note_id', ''),
            'title': note.get('title', ''),
            'desc': note.get('desc', ''),
            'type': note.get('type', 'normal'),
            'user': note.get('user', {}),
            'interact_info': note.get('interact_info', {}),
            'time': note.get('time', ''),
            'last_update_time': note.get('last_update_time', 0),
            'ip_location': note.get('ip_location', ''),
            'image_list': note.get('image_list', []),
            'tag_list': note.get('tag_list', []),
            'xsec_token': note.get('xsec_token', ''),
            'comments': note_comments,
        }
        result.append(note_data)
    
    return result


# 测试入口
async def test_manual_click():
    """测试方案A"""
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else await context.new_page()
        
        notes, comments = await manual_click_search(
            page=page,
            keyword="哪吒2",
            max_notes=2,
            timeout=60
        )
        
        print(f"\n{'='*50}")
        print(f"测试完成！获取到 {len(notes)} 个帖子，{len(comments)} 条评论")
        print(f"{'='*50}")
        
        for note in notes:
            print(f"\nNote ID: {note['note_id']}")
            print(f"  Title: {note['title'][:50] if note['title'] else 'N/A'}")
            print(f"  Desc: {note['desc'][:80] if note['desc'] else 'N/A'}...")
            print(f"  Author: {note.get('user', {}).get('nickname', 'N/A')}")
            print(f"  Likes: {note.get('interact_info', {}).get('liked_count', 'N/A')}")
        
        if comments:
            print(f"\n--- 评论示例 ---")
            for c in comments[:3]:
                print(f"  - {c['content'][:50] if c['content'] else 'N/A'}")
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(test_manual_click())
