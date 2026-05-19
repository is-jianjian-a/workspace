#!/usr/bin/env python3
"""
MediaCrawler 完整测试脚本
指导用户完成：
1. 启动 Chrome 并开启远程调试
2. 在小红书/抖音等平台登录
3. 运行 MediaCrawler 抓取内容
4. 查看抓取结果
"""

import subprocess
import os
import sys
import time
import json
import glob

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")

def print_step(step_num, text):
    print(f"\n【步骤 {step_num}】{text}")
    print("-" * 60)

def find_chrome():
    """查找 Chrome 路径"""
    paths = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chrome.app/Contents/MacOS/Google Chrome",
    ]
    for path in paths:
        if os.path.isfile(path):
            return path
    return None

def is_chrome_running():
    """检查 Chrome 是否运行"""
    try:
        result = subprocess.run(["pgrep", "-x", "Google Chrome"], capture_output=True, text=True)
        return result.returncode == 0 and result.stdout.strip()
    except:
        return False

def kill_chrome():
    """关闭 Chrome"""
    print("正在关闭 Chrome...")
    subprocess.run(["pkill", "-x", "Google Chrome"], check=False)
    time.sleep(2)

def start_chrome_with_debug():
    """启动带调试的 Chrome"""
    chrome_path = find_chrome()
    if not chrome_path:
        print("错误: 未找到 Chrome")
        return False
    
    user_data_dir = os.path.expanduser("~/tmp/chrome_dev_profile")
    os.makedirs(user_data_dir, exist_ok=True)
    
    cmd = [
        chrome_path,
        "--remote-debugging-port=9222",
        "--no-first-run",
        "--no-default-browser-check",
        f"--user-data-dir={user_data_dir}",
        "about:blank"
    ]
    
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(3)
    return True

def check_cdp_port():
    """检查 CDP 端口是否可用"""
    try:
        import httpx
        response = httpx.get("http://localhost:9222/json/version", timeout=2)
        return response.status_code == 200
    except:
        return False

def run_mediacrawler(platform, keyword, max_comments=5):
    """运行 MediaCrawler"""
    cmd = [
        "python3", "main.py",
        "--platform", platform,
        "--lt", "cookie",
        "--crawler-type", "search",
        "--keywords", keyword,
        "--get-comment", "yes",
        "--headless", "False",
        "--save-data-option", "json",
        "--max-comments-count-singlenotes", str(max_comments),
    ]
    
    print(f"运行命令: {' '.join(cmd)}")
    print("")
    
    result = subprocess.run(cmd, capture_output=True, text=True, cwd="/Users/zhijian/workspace/MediaCrawler-main")
    
    # 输出日志
    lines = result.stdout.split('\n')
    for line in lines:
        if 'INFO' in line or 'ERROR' in line or 'WARNING' in line:
            print(line)
    
    if result.returncode != 0:
        print(f"错误输出: {result.stderr[-500:]}")
    
    return result.returncode == 0

def show_results():
    """显示抓取结果"""
    data_dir = "/Users/zhijian/workspace/MediaCrawler-main/data"
    
    if not os.path.exists(data_dir):
        print("数据目录不存在")
        return
    
    # 查找最新的 JSON 文件
    json_files = glob.glob(os.path.join(data_dir, "**/*.json"), recursive=True)
    
    if not json_files:
        print("未找到数据文件")
        return
    
    # 按修改时间排序
    json_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    
    print(f"\n找到 {len(json_files)} 个数据文件")
    print(f"最新文件: {json_files[0]}")
    
    # 读取并显示部分内容
    try:
        with open(json_files[0], 'r', encoding='utf-8') as f:
            content = f.read()
            data = json.loads(content)
            
            if isinstance(data, list) and len(data) > 0:
                print(f"\n数据条数: {len(data)}")
                print("\n前3条数据预览:")
                for i, item in enumerate(data[:3]):
                    print(f"\n--- 条目 {i+1} ---")
                    if isinstance(item, dict):
                        for key, value in item.items():
                            if value and str(value).strip():
                                print(f"  {key}: {str(value)[:100]}")
            elif isinstance(data, dict):
                print(f"\n数据键: {list(data.keys())}")
                for key, value in list(data.items())[:5]:
                    print(f"  {key}: {str(value)[:100]}")
    except Exception as e:
        print(f"读取数据失败: {e}")

def main():
    print_header("MediaCrawler 完整测试流程")
    
    # 步骤1: 准备 Chrome
    print_step(1, "准备 Chrome 浏览器")
    
    if is_chrome_running():
        print("检测到 Chrome 正在运行")
        print("为了使用 CDP 模式，需要关闭现有 Chrome 并启动带调试的新实例")
        choice = input("是否关闭现有 Chrome 并启动调试模式? (y/n): ").strip().lower()
        
        if choice == 'y':
            kill_chrome()
            if not start_chrome_with_debug():
                print("启动 Chrome 失败")
                return
        else:
            print("请在现有 Chrome 中手动开启远程调试:")
            print("1. 在 Chrome 地址栏输入: chrome://inspect/#remote-debugging")
            print("2. 勾选 'Allow remote debugging for this browser instance'")
            print("3. 确认端口 9222 已开启")
            input("\n完成后按 Enter 继续...")
    else:
        print("Chrome 未运行，正在启动带调试的 Chrome...")
        if not start_chrome_with_debug():
            print("启动 Chrome 失败")
            return
    
    # 检查 CDP 端口
    print("\n检查 CDP 端口...")
    for i in range(10):
        if check_cdp_port():
            print("✓ CDP 端口 9222 已就绪")
            break
        time.sleep(1)
    else:
        print("✗ CDP 端口未就绪，请检查 Chrome 是否正常运行")
        return
    
    # 步骤2: 登录平台
    print_step(2, "登录目标平台")
    print("请在 Chrome 中访问以下网站并登录:")
    print("  小红书: https://www.xiaohongshu.com")
    print("  抖音: https://www.douyin.com")
    print("  微博: https://weibo.com")
    print("  B站: https://www.bilibili.com")
    print("")
    print("登录完成后，按 Enter 继续...")
    input()
    
    # 步骤3: 运行爬虫
    print_step(3, "运行 MediaCrawler")
    
    platforms = {
        "1": ("xhs", "小红书"),
        "2": ("dy", "抖音"),
        "3": ("wb", "微博"),
        "4": ("bili", "B站"),
    }
    
    print("选择要测试的平台:")
    for key, (code, name) in platforms.items():
        print(f"  {key}. {name}")
    
    platform_choice = input("\n请选择 (1-4): ").strip()
    
    if platform_choice not in platforms:
        print("无效选择")
        return
    
    platform_code, platform_name = platforms[platform_choice]
    keyword = input(f"请输入搜索关键词 (默认: 美食探店): ").strip() or "美食探店"
    
    print(f"\n正在运行 {platform_name} 爬虫，关键词: {keyword}...")
    success = run_mediacrawler(platform_code, keyword)
    
    # 步骤4: 查看结果
    print_step(4, "查看抓取结果")
    
    if success:
        print("✓ 爬虫运行完成")
        show_results()
    else:
        print("✗ 爬虫运行失败")
        print("请检查日志了解详细错误信息")
    
    print_header("测试完成")
    print("数据保存在: /Users/zhijian/workspace/MediaCrawler-main/data/")
    print("\n提示:")
    print("- 如需重新抓取，请确保 Chrome 仍在运行且已登录")
    print("- 可以修改 config/base_config.py 调整抓取参数")
    print("- 使用 --headless True 可以在后台运行")

if __name__ == "__main__":
    main()
