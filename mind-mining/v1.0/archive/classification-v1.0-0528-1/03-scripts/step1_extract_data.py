#!/usr/bin/env python3
"""
Step 1: 从MediaCrawler数据库提取含华为/苹果关键词的小红书数据
保存到项目本地SQLite数据库
"""

import sqlite3
import json
import os
from datetime import datetime

# 路径配置
SOURCE_DB = '/Users/zhijian/workspace/MediaCrawler/database/sqlite_tables.db'
PROJECT_DIR = '/Users/zhijian/workspace/mind-mining/v1.0'
LOCAL_DB = os.path.join(PROJECT_DIR, '01-data', 'project_data.db')
RAW_JSON = os.path.join(PROJECT_DIR, '01-data', 'xhs_apple_huawei_raw.json')

# 确保目录存在
os.makedirs(os.path.dirname(LOCAL_DB), exist_ok=True)

# 连接源数据库
print(f"[{datetime.now()}] 连接源数据库: {SOURCE_DB}")
source_conn = sqlite3.connect(SOURCE_DB)
source_cursor = source_conn.cursor()

# 查询source_keyword包含华为或苹果的数据
query = """
SELECT 
    id,
    user_id,
    nickname,
    avatar,
    ip_location,
    add_ts,
    last_modify_ts,
    note_id,
    type,
    title,
    desc,
    video_url,
    time,
    last_update_time,
    liked_count,
    collected_count,
    comment_count,
    share_count,
    image_list,
    tag_list,
    note_url,
    source_keyword,
    xsec_token,
    raw_data
FROM xhs_note
WHERE 
    source_keyword LIKE '%华为%'
    OR source_keyword LIKE '%苹果%'
ORDER BY id
"""

print(f"[{datetime.now()}] 执行查询...")
source_cursor.execute(query)
rows = source_cursor.fetchall()

print(f"[{datetime.now()}] 查询完成，共 {len(rows)} 条数据")

# 获取列名
columns = [description[0] for description in source_cursor.description]
print(f"列名: {columns}")

# 创建本地数据库
print(f"[{datetime.now()}] 创建本地数据库: {LOCAL_DB}")
local_conn = sqlite3.connect(LOCAL_DB)
local_cursor = local_conn.cursor()

# 创建表（简化版，只保留关键字段）
local_cursor.execute('''
CREATE TABLE IF NOT EXISTS xhs_notes (
    id INTEGER PRIMARY KEY,
    note_id TEXT UNIQUE NOT NULL,
    nickname TEXT,
    title TEXT,
    content TEXT,
    liked_count INTEGER DEFAULT 0,
    collected_count INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    share_count INTEGER DEFAULT 0,
    tag_list TEXT,
    source_keyword TEXT,
    note_url TEXT,
    created_at INTEGER,
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# 创建索引
local_cursor.execute('CREATE INDEX IF NOT EXISTS idx_note_id ON xhs_notes(note_id)')
local_cursor.execute('CREATE INDEX IF NOT EXISTS idx_source_keyword ON xhs_notes(source_keyword)')

# 清空表（如果存在）
local_cursor.execute('DELETE FROM xhs_notes')
local_conn.commit()

# 插入数据
print(f"[{datetime.now()}] 插入数据到本地数据库...")
inserted = 0
skipped = 0
raw_data_list = []

for row in rows:
    row_dict = dict(zip(columns, row))
    
    # 检查note_id是否有效
    note_id = row_dict.get('note_id')
    if not note_id:
        skipped += 1
        continue
    
    try:
        local_cursor.execute('''
            INSERT INTO xhs_notes 
            (id, note_id, nickname, title, content, liked_count, collected_count, 
             comment_count, share_count, tag_list, source_keyword, note_url, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            row_dict.get('id'),
            note_id,
            row_dict.get('nickname', ''),
            row_dict.get('title', ''),
            row_dict.get('desc', ''),
            row_dict.get('liked_count', 0) or 0,
            row_dict.get('collected_count', 0) or 0,
            row_dict.get('comment_count', 0) or 0,
            row_dict.get('share_count', 0) or 0,
            row_dict.get('tag_list', ''),
            row_dict.get('source_keyword', ''),
            row_dict.get('note_url', ''),
            row_dict.get('time')
        ))
        inserted += 1
        
        # 同时构建JSON数据
        raw_data_list.append({
            'id': row_dict.get('id'),
            'note_id': note_id,
            'nickname': row_dict.get('nickname', ''),
            'title': row_dict.get('title', ''),
            'content': row_dict.get('desc', ''),
            'liked_count': row_dict.get('liked_count', 0) or 0,
            'collected_count': row_dict.get('collected_count', 0) or 0,
            'comment_count': row_dict.get('comment_count', 0) or 0,
            'share_count': row_dict.get('share_count', 0) or 0,
            'tag_list': row_dict.get('tag_list', ''),
            'source_keyword': row_dict.get('source_keyword', ''),
            'note_url': row_dict.get('note_url', ''),
            'time': row_dict.get('time')
        })
        
    except sqlite3.IntegrityError:
        # note_id重复，跳过
        skipped += 1
        continue

local_conn.commit()

# 保存JSON
print(f"[{datetime.now()}] 保存JSON到: {RAW_JSON}")
with open(RAW_JSON, 'w', encoding='utf-8') as f:
    json.dump(raw_data_list, f, ensure_ascii=False, indent=2)

# 统计source_keyword分布
print(f"\n[{datetime.now()}] 统计source_keyword分布...")
local_cursor.execute('SELECT source_keyword, COUNT(*) FROM xhs_notes GROUP BY source_keyword ORDER BY COUNT(*) DESC')
keyword_stats = local_cursor.fetchall()

print(f"\n{'='*60}")
print(f"提取完成！")
print(f"{'='*60}")
print(f"数据库查询结果: {len(rows)}条")
print(f"成功插入: {inserted}条")
print(f"跳过(无note_id或重复): {skipped}条")
print(f"\n本地数据库: {LOCAL_DB}")
print(f"原始JSON: {RAW_JSON}")
print(f"\nsource_keyword分布:")
for kw, count in keyword_stats:
    print(f"  {kw}: {count}条")

# 验证
local_cursor.execute('SELECT COUNT(*) FROM xhs_notes')
verify_count = local_cursor.fetchone()[0]
print(f"\n验证: 本地数据库共 {verify_count} 条")

source_conn.close()
local_conn.close()

print(f"[{datetime.now()}] 完成！")
