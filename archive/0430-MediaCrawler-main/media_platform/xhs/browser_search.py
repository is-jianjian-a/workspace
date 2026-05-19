# -*- coding: utf-8 -*-
"""
小红书纯浏览器模拟方案
完全模拟用户行为：搜索 → 点击帖子 → 提取评论
不调用任何API
"""

import asyncio
import json
import re
from typing import Dict, List, Optional

from playwright.async_api import Page

from tools import utils


async def search_and_extract_via_browser(
    page: Page,
    keyword: str,
    max_notes: int = 5,
    max_comments_per_note: int = 20,
) -> List[Dict]:
    """
    纯浏览器模拟：搜索关键词，点击帖子，提取内容和评论
    
    Args:
        page: Playwright page对象
        keyword: 搜索关键词
        max_notes: 最大获取帖子数量
        max_comments_per_note: 每个帖子最大评论数
        
    Returns:
        List[Dict]: 帖子列表（包含评论）
    """
    notes = []
    
    try:
        # Step 1: 直接访问搜索结果页（更高效）
        search_url = f"https://www.xiaohongshu.com/search_result?keyword={keyword}&type=51"
        utils.logger.info(f"[BrowserSim] Step 1: Opening search page: {search_url}")
        await page.goto(search_url, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(3)
        
        # Step 2: 等待搜索结果加载，滚动加载更多
        utils.logger.info("[BrowserSim] Step 2: Waiting for search results ...")
        for _ in range(3):
            await page.evaluate("window.scrollBy(0, 800)")
            await asyncio.sleep(1)
        
        # Step 3: 提取搜索结果中的帖子链接
        note_links = await page.evaluate("""
            () => {
                const links = [];
                const seen = new Set();
                // 找到所有指向 /explore/ 的链接
                document.querySelectorAll('a[href*="/explore/"]').forEach(a => {
                    const href = a.getAttribute('href');
                    const match = href.match(/\/explore\/([a-zA-Z0-9]+)/);
                    if (match && !seen.has(match[1])) {
                        seen.add(match[1]);
                        links.push({
                            note_id: match[1],
                            href: href,
                            title: a.textContent.trim().slice(0, 50)
                        });
                    }
                });
                return links.slice(0, %d);
            }
        """ % max_notes)
        
        utils.logger.info(f"[BrowserSim] Found {len(note_links)} note links")
        
        # Step 5: 直接从搜索结果页提取帖子信息（不点击进详情页）
        # 小红书搜索结果的卡片上已有：标题、内容预览、作者、点赞数等
        utils.logger.info("[BrowserSim] Step 5: Extracting note info from search results page...")
        
        search_page_notes = await page.evaluate("""
            () => {
                const notes = [];
                const seen = new Set();
                
                // 小红书搜索结果页面结构（2024-2025）：
                // 每个帖子是一个 section.note-item
                // 包含：.title（标题）、.author（作者+日期）、.like（点赞数）
                
                const items = document.querySelectorAll('section.note-item');
                
                for (const item of items) {
                    // 获取链接
                    const link = item.querySelector('a[href*="/explore/"]');
                    if (!link) continue;
                    
                    const href = link.getAttribute('href');
                    const match = href.match(/\/explore\/([a-zA-Z0-9]+)/);
                    if (!match) continue;
                    
                    const noteId = match[1];
                    if (seen.has(noteId)) continue;
                    seen.add(noteId);
                    
                    // ===== 提取标题 =====
                    const titleEl = item.querySelector('.title');
                    const title = titleEl ? titleEl.textContent.trim() : '';
                    
                    // ===== 提取作者 =====
                    const nameEl = item.querySelector('.name');
                    const author = nameEl ? nameEl.textContent.trim() : '';
                    
                    // ===== 提取日期 =====
                    const timeEl = item.querySelector('.time');
                    const time = timeEl ? timeEl.textContent.trim() : '';
                    
                    // ===== 提取点赞数 =====
                    const countEl = item.querySelector('.count');
                    let likes = countEl ? countEl.textContent.trim() : '0';
                    // 过滤掉非数字文本（如"赞"）
                    if (likes === '赞' || !/^\d+$/.test(likes)) {
                        likes = '0';
                    }
                    
                    // ===== 提取封面图 =====
                    const img = item.querySelector('img');
                    const cover = img ? img.getAttribute('src') : '';
                    
                    // ===== 提取视频标识 =====
                    const videoBadge = item.querySelector('.video-badge, [class*="video"]');
                    const isVideo = !!videoBadge;
                    
                    notes.push({
                        note_id: noteId,
                        href: href,
                        title: title.slice(0, 100),
                        author: author,
                        time: time,
                        likes: likes,
                        cover: cover,
                        is_video: isVideo
                    });
                }
                
                return notes;
            }
        """)
        
        utils.logger.info(f"[BrowserSim] Extracted {len(search_page_notes)} notes from search page")
        
        # 将搜索页提取的数据转换为存储层期望的标准格式
        for note_info in search_page_notes[:max_notes]:
            # 作者和日期已经从页面正确分离
            author_name = note_info.get('author', '')
            publish_time = note_info.get('time', '')
            
            note_data = {
                'note_id': note_info['note_id'],
                'type': 'video' if note_info.get('is_video') else 'normal',
                'title': note_info.get('title', ''),
                'desc': '',  # 搜索页无法获取详细描述
                'video_url': '',
                'time': publish_time,
                'last_update_time': 0,
                'user': {
                    'user_id': '',
                    'nickname': author_name,
                    'avatar': ''
                },
                'interact_info': {
                    'liked_count': note_info.get('likes', '0'),
                    'collected_count': '0',
                    'comment_count': '0',
                    'share_count': '0'
                },
                'ip_location': '',
                'image_list': [{'url_default': note_info.get('cover', '')}] if note_info.get('cover') else [],
                'tag_list': [],
                'xsec_token': '',
                'comments': [],  # 搜索页无法获取评论
            }
            notes.append(note_data)
        
        # Step 6: 尝试用完整href（含xsec_token）打开帖子获取评论
        for i, link_info in enumerate(note_links[:3]):  # 只尝试前3个
            note_id = link_info['note_id']
            href = link_info['href']
            xsec_token = link_info.get('xsec_token', '')
            
            try:
                utils.logger.info(f"[BrowserSim] Step 6.{i+1}: Trying to open note {note_id} for comments...")
                
                # 方法A: 使用Playwright的真实鼠标API点击（硬件级模拟）
                # 先找到元素并滚动到视口
                element_info = await page.evaluate("""
                    (noteId) => {
                        const allLinks = document.querySelectorAll('a[href*="/explore/"]');
                        for (const link of allLinks) {
                            const linkHref = link.getAttribute('href');
                            if (linkHref && linkHref.includes(noteId)) {
                                // 滚动到视口中心
                                link.scrollIntoView({ behavior: 'instant', block: 'center' });
                                // 等待一帧确保位置更新
                                return new Promise((resolve) => {
                                    requestAnimationFrame(() => {
                                        const rect = link.getBoundingClientRect();
                                        resolve({
                                            found: true,
                                            x: rect.left + rect.width / 2,
                                            y: rect.top + rect.height / 2,
                                            href: linkHref,
                                            width: rect.width,
                                            height: rect.height
                                        });
                                    });
                                });
                            }
                        }
                        return { found: false };
                    }
                """, note_id)
                
                if not element_info or not element_info.get('found'):
                    utils.logger.warning(f"[BrowserSim] Could not find note {note_id} on page")
                    continue
                
                # 等待滚动完成
                await asyncio.sleep(0.5)
                
                # 使用Playwright的真实鼠标移动和点击
                x, y = element_info['x'], element_info['y']
                w, h = element_info.get('width', 0), element_info.get('height', 0)
                
                if x <= 0 or y <= 0 or w <= 0 or h <= 0:
                    utils.logger.warning(f"[BrowserSim] Invalid element position ({x}, {y}) size ({w}, {h})")
                    continue
                
                utils.logger.info(f"[BrowserSim] Element at ({x}, {y}), size ({w}, {h}). Moving mouse...")
                
                # 先移动鼠标到元素（模拟真实移动轨迹）
                await page.mouse.move(x, y, steps=10)
                await asyncio.sleep(0.3)
                
                # 真实点击（down + up）
                await page.mouse.down()
                await asyncio.sleep(0.15)
                await page.mouse.up()
                
                utils.logger.info(f"[BrowserSim] Clicked note at ({x}, {y}), waiting for navigation...")
                await asyncio.sleep(5)
                
                current_url = page.url
                utils.logger.info(f"[BrowserSim] URL after click: {current_url}")
                
                # 检查是否被拦截
                if '404' in current_url or '无法浏览' in current_url or 'error' in current_url:
                    utils.logger.warning(f"[BrowserSim] Note {note_id} blocked (404)")
                    # 返回搜索页
                    await page.goto(f"https://www.xiaohongshu.com/search_result?keyword={keyword}", wait_until="networkidle", timeout=30000)
                    await asyncio.sleep(2)
                    continue
                
                # 提取评论
                comments = await _extract_comments_from_page(page, note_id, max_comments_per_note)
                
                # 找到对应的note并添加评论
                for note in notes:
                    if note['note_id'] == note_id:
                        note['comments'] = comments
                        utils.logger.info(f"[BrowserSim] Note {note_id}: {len(comments)} comments extracted")
                        break
                
                # 返回搜索页
                await page.goto(f"https://www.xiaohongshu.com/search_result?keyword={keyword}", wait_until="networkidle", timeout=30000)
                await asyncio.sleep(2)
                
            except Exception as e:
                utils.logger.warning(f"[BrowserSim] Failed to get comments for {note_id}: {e}")
                try:
                    await page.goto(f"https://www.xiaohongshu.com/search_result?keyword={keyword}", wait_until="networkidle", timeout=30000)
                    await asyncio.sleep(2)
                except Exception:
                    pass
                continue
        
        utils.logger.info(f"[BrowserSim] Total extracted: {len(notes)} notes with comments")
        return notes
        
    except Exception as e:
        utils.logger.error(f"[BrowserSim] Browser simulation failed: {e}")
        return []


async def _extract_note_content(page: Page, note_id: str) -> Dict:
    """从帖子详情页提取内容"""
    try:
        # 等待内容加载
        await asyncio.sleep(2)
        
        # 提取标题、内容、作者信息
        result = await page.evaluate("""
            () => {
                const data = {note_id: '%s'};
                
                // 标题
                const titleEl = document.querySelector('h1, .title, [class*="title"]');
                data.title = titleEl ? titleEl.textContent.trim() : '';
                
                // 内容/正文
                const contentEl = document.querySelector('.content, [class*="content"], [class*="desc"]');
                data.content = contentEl ? contentEl.textContent.trim() : '';
                
                // 作者
                const authorEl = document.querySelector('[class*="author"], [class*="nickname"], [class*="user-name"]');
                data.author = authorEl ? authorEl.textContent.trim() : '';
                
                // 点赞数
                const likeEl = document.querySelector('[class*="like"], [class*="赞"]');
                data.likes = likeEl ? likeEl.textContent.trim() : '0';
                
                // 收藏数
                const collectEl = document.querySelector('[class*="collect"], [class*="收藏"]');
                data.collects = collectEl ? collectEl.textContent.trim() : '0';
                
                // 评论数
                const commentEl = document.querySelector('[class*="comment-count"], [class*="评论"]');
                data.comment_count = commentEl ? commentEl.textContent.trim() : '0';
                
                return data;
            }
        """ % note_id)
        
        return result if result else {'note_id': note_id}
    except Exception as e:
        utils.logger.warning(f"[BrowserSim] Extract note content failed: {e}")
        return {'note_id': note_id}


async def _extract_comments_from_page(page: Page, note_id: str, max_comments: int = 20) -> List[Dict]:
    """从帖子详情页提取评论"""
    comments = []
    
    try:
        # 等待评论区域加载
        await asyncio.sleep(2)
        
        # 尝试点击"查看评论"或滚动到评论区域
        comment_btn_selectors = [
            'text=查看评论',
            'text=评论',
            '[class*="comment-btn"]',
            '[class*="comment-section"]',
        ]
        
        for selector in comment_btn_selectors:
            try:
                btn = await page.query_selector(selector)
                if btn:
                    await btn.click()
                    await asyncio.sleep(1)
                    break
            except Exception:
                continue
        
        # 滚动加载更多评论
        for _ in range(5):
            await page.evaluate("window.scrollBy(0, 500)")
            await asyncio.sleep(0.5)
        
        # 提取评论
        dom_comments = await page.evaluate("""
            () => {
                const comments = [];
                const seen = new Set();
                
                // 尝试多种评论选择器
                const selectors = [
                    '[class*="comment-item"]',
                    '[class*="comment-list"] > div',
                    '[class*="comment"] > div',
                    '[class*="reply-item"]',
                    'div[class*="comment"]:not([class*="comment-count"])',
                ];
                
                for (const selector of selectors) {
                    const elements = document.querySelectorAll(selector);
                    elements.forEach(el => {
                        // 提取评论内容
                        const contentEl = el.querySelector('[class*="content"], span, p') || el;
                        const content = contentEl.textContent.trim();
                        
                        // 去重
                        if (content && content.length > 0 && !seen.has(content)) {
                            seen.add(content);
                            
                            // 提取用户名
                            const userEl = el.querySelector('[class*="user"], [class*="nickname"], [class*="name"]');
                            
                            // 提取点赞数
                            const likeEl = el.querySelector('[class*="like"], [class*="赞"]');
                            
                            comments.push({
                                content: content.slice(0, 500),
                                user: userEl ? userEl.textContent.trim() : '',
                                likes: likeEl ? likeEl.textContent.trim() : '0'
                            });
                        }
                    });
                    if (comments.length > 0) break;
                }
                
                return comments.slice(0, %d);
            }
        """ % max_comments)
        
        for i, c in enumerate(dom_comments):
            comments.append({
                'comment_id': f'{note_id}_c{i}',
                'note_id': note_id,
                'content': c.get('content', ''),
                'nickname': c.get('user', ''),
                'like_count': c.get('likes', '0'),
                'create_time': None,
                'raw': c,
            })
        
        return comments
        
    except Exception as e:
        utils.logger.warning(f"[BrowserSim] Extract comments failed: {e}")
        return []
