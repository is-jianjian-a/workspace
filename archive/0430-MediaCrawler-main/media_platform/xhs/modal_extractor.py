# -*- coding: utf-8 -*-
"""
方案A替代实现：弹层DOM直接提取
用户手动点击帖子后，从弹层DOM中直接提取帖子详情和评论
"""

import asyncio
import json
from playwright.async_api import async_playwright
from typing import Dict, List, Optional
import sys
sys.path.insert(0, '.')
import utils


class XhsModalExtractor:
    """
    小红书弹层内容提取器
    检测弹层出现并从DOM中提取帖子详情和评论
    """
    
    def __init__(self, page, max_notes: int = 3, timeout: int = 120):
        self.page = page
        self.max_notes = max_notes
        self.timeout = timeout
        self.extracted_notes = []
        
    async def wait_for_modal(self, timeout: int = 10) -> bool:
        """
        等待弹层出现
        
        检测特征：
        1. .mask-paper 元素出现
        2. 高z-index元素出现
        3. 页面中出现新的固定定位元素
        """
        for i in range(timeout):
            has_modal = await self.page.evaluate("""
                () => {
                    // 检查常见的弹层特征
                    const mask = document.querySelector('.mask-paper');
                    const modal = document.querySelector('[class*="modal"], [class*="drawer"]');
                    
                    // 检查是否有覆盖大部分屏幕的固定定位元素
                    const overlays = Array.from(document.querySelectorAll('*')).filter(el => {
                        const style = window.getComputedStyle(el);
                        return style.position === 'fixed' && 
                               el.offsetWidth > window.innerWidth * 0.5 &&
                               el.offsetHeight > window.innerHeight * 0.5 &&
                               el !== document.body;
                    });
                    
                    return !!(mask || modal || overlays.length > 0);
                }
            """)
            
            if has_modal:
                return True
                
            await asyncio.sleep(1)
            
        return False
    
    async def extract_modal_content(self) -> Optional[Dict]:
        """
        从弹层DOM中提取帖子内容
        
        提取字段：
        - note_id: 帖子ID（从URL或DOM中提取）
        - title: 标题
        - desc: 详细描述
        - author: 作者信息
        - likes: 点赞数
        - comments: 评论列表
        """
        return await self.page.evaluate("""
            () => {
                // 查找弹层容器
                const modal = document.querySelector('.mask-paper') || 
                               document.querySelector('[class*="modal"]') ||
                               document.querySelector('[class*="drawer"]');
                
                if (!modal) return null;
                
                // 获取所有文本内容用于分析
                const allText = modal.textContent;
                
                // 尝试提取标题
                const titleEl = modal.querySelector('.title, h1, h2, h3');
                const title = titleEl ? titleEl.textContent.trim() : '';
                
                // 尝试提取描述/内容
                const descEl = modal.querySelector('.desc, .content, .detail, [class*="desc"]');
                const desc = descEl ? descEl.textContent.trim() : '';
                
                // 尝试提取作者
                const authorEl = modal.querySelector('.name, .author, [class*="author"]');
                const author = authorEl ? authorEl.textContent.trim() : '';
                
                // 尝试提取点赞数
                const likeEl = modal.querySelector('.count, .like, [class*="like"]');
                const likes = likeEl ? likeEl.textContent.trim() : '0';
                
                // 尝试提取评论
                const commentEls = modal.querySelectorAll('[class*="comment"], [class*="reply"]');
                const comments = Array.from(commentEls).map(el => ({
                    text: el.textContent.trim().substring(0, 200),
                    className: el.className
                }));
                
                // 获取笔记ID（从当前URL或DOM中的链接提取）
                let noteId = '';
                const noteLink = modal.querySelector('a[href*="/explore/"]');
                if (noteLink) {
                    const match = noteLink.href.match(/\/explore\/([a-zA-Z0-9]+)/);
                    if (match) noteId = match[1];
                }
                
                return {
                    note_id: noteId,
                    title: title,
                    desc: desc,
                    author: author,
                    likes: likes,
                    comments: comments,
                    allTextPreview: allText.substring(0, 500)
                };
            }
        """)
    
    async def close_modal(self):
        """关闭弹层（点击遮罩或按ESC）"""
        await self.page.evaluate("""
            () => {
                // 方法1: 点击遮罩层
                const mask = document.querySelector('.mask-paper');
                if (mask) {
                    mask.click();
                    return;
                }
                
                // 方法2: 按ESC键
                document.dispatchEvent(new KeyboardEvent('keydown', {
                    key: 'Escape',
                    keyCode: 27,
                    bubbles: true
                }));
                
                // 方法3: 查找关闭按钮
                const closeBtn = document.querySelector('[class*="close"], [class*="back"]');
                if (closeBtn) closeBtn.click();
            }
        """)
        await asyncio.sleep(1)
    
    async def run_extraction(self, keyword: str) -> List[Dict]:
        """
        主流程：引导用户点击并提取数据
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            提取的帖子列表
        """
        
        # 1. 导航到搜索页
        search_url = f"https://www.xiaohongshu.com/search_result?keyword={keyword}&type=51"
        await self.page.goto(search_url, wait_until='networkidle')
        await asyncio.sleep(3)
        
        # 2. 显示提示UI
        await self.page.evaluate(f"""
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
                    text-align: center;
                    box-shadow: 0 8px 32px rgba(255,36,66,0.4);
                `;
                div.innerHTML = `
                    <div style="font-size: 24px; margin-bottom: 8px;">🔴 手动点击模式</div>
                    <div>请点击下方帖子，我会自动提取详情和评论</div>
                    <div style="font-size: 14px; margin-top: 8px;">
                        目标: {self.max_notes}个 | 超时: {self.timeout}秒
                    </div>
                    <div id="crawler-progress" style="font-size: 13px; margin-top: 10px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.3);">
                        等待点击... 0/{self.max_notes}
                    </div>
                `;
                document.body.appendChild(div);
            }}
        """)
        
        # 3. 等待用户点击并提取
        start_time = asyncio.get_event_loop().time()
        extracted_count = 0
        
        while extracted_count < self.max_notes:
            elapsed = asyncio.get_event_loop().time() - start_time
            if elapsed > self.timeout:
                utils.logger.info(f"[ModalExtract] Timeout reached ({self.timeout}s)")
                break
            
            # 等待弹层出现
            has_modal = await self.wait_for_modal(timeout=10)
            
            if has_modal:
                utils.logger.info("[ModalExtract] Modal detected! Extracting content...")
                
                # 提取内容
                content = await self.extract_modal_content()
                
                if content:
                    self.extracted_notes.append(content)
                    extracted_count += 1
                    
                    utils.logger.info(f"[ModalExtract] ✓ Extracted: {content.get('title', 'N/A')[:50]}")
                    utils.logger.info(f"[ModalExtract]   Comments: {len(content.get('comments', []))}")
                    
                    # 更新UI
                    await self.page.evaluate(f"""
                        () => {{
                            const progress = document.getElementById('crawler-progress');
                            if (progress) {{
                                progress.textContent = '已提取 {extracted_count}/{self.max_notes}，请继续点击或等待...';
                            }}
                        }}
                    """)
                
                # 关闭弹层
                await self.close_modal()
                
                # 等待弹层关闭
                await asyncio.sleep(1)
                
            else:
                # 显示剩余时间
                remaining = int(self.timeout - elapsed)
                if remaining % 10 == 0 and remaining > 0:
                    utils.logger.info(f"[ModalExtract] Waiting... {remaining}s remaining")
                
                await asyncio.sleep(1)
        
        # 4. 完成提示
        await self.page.evaluate("""
            () => {
                const progress = document.getElementById('crawler-progress');
                if (progress) {
                    progress.textContent = '✓ 提取完成！';
                }
                setTimeout(() => {
                    const div = document.getElementById('crawler-hint');
                    if (div) {
                        div.style.transition = 'opacity 0.5s';
                        div.style.opacity = '0';
                        setTimeout(() => div.remove(), 500);
                    }
                }, 3000);
            }
        """)
        
        return self.extracted_notes


async def search_and_extract_via_modal(
    page,
    keyword: str,
    max_notes: int = 3,
    max_comments_per_note: int = 10
) -> List[Dict]:
    """
    兼容接口：通过弹层DOM提取帖子详情
    """
    extractor = XhsModalExtractor(page, max_notes, timeout=120)
    notes = await extractor.run_extraction(keyword)
    
    # 转换为标准格式
    result = []
    for note in notes:
        note_data = {
            'note_id': note.get('note_id', ''),
            'title': note.get('title', ''),
            'desc': note.get('desc', ''),
            'type': 'normal',
            'user': {'nickname': note.get('author', '')},
            'interact_info': {'liked_count': note.get('likes', '0')},
            'time': '',
            'last_update_time': 0,
            'ip_location': '',
            'image_list': [],
            'tag_list': [],
            'xsec_token': '',
            'comments': note.get('comments', [])[:max_comments_per_note],
        }
        result.append(note_data)
    
    return result


# 测试入口
async def test_modal_extraction():
    """测试弹层提取方案"""
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else await context.new_page()
        
        extractor = XhsModalExtractor(page, max_notes=2, timeout=60)
        notes = await extractor.run_extraction("哪吒2")
        
        print(f"\n{'='*50}")
        print(f"测试完成！提取到 {len(notes)} 个帖子")
        print(f"{'='*50}")
        
        for note in notes:
            print(f"\nNote ID: {note.get('note_id', 'N/A')}")
            print(f"  Title: {note.get('title', 'N/A')[:50]}")
            print(f"  Desc: {note.get('desc', 'N/A')[:80]}...")
            print(f"  Author: {note.get('author', 'N/A')}")
            print(f"  Likes: {note.get('likes', 'N/A')}")
            print(f"  Comments: {len(note.get('comments', []))}")
            for c in note.get('comments', [])[:3]:
                print(f"    - {c.get('text', 'N/A')[:50]}")
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(test_modal_extraction())
