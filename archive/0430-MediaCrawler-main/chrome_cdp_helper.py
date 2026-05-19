#!/usr/bin/env python3
"""
MediaCrawler Chrome CDP 启动助手
用于启动 Chrome 并开启远程调试，以便 MediaCrawler 复用登录状态
"""

import subprocess
import os
import sys
import time
import signal
import atexit

def find_chrome():
    """查找 Chrome 浏览器路径"""
    possible_paths = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chrome.app/Contents/MacOS/Google Chrome",
    ]
    
    for path in possible_paths:
        if os.path.isfile(path):
            return path
    
    try:
        result = subprocess.run(["which", "google-chrome"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    
    return None

def is_chrome_running():
    """检查 Chrome 是否正在运行"""
    try:
        result = subprocess.run(["pgrep", "-x", "Google Chrome"], capture_output=True, text=True)
        return result.returncode == 0 and result.stdout.strip()
    except:
        return False

def kill_chrome():
    """关闭所有 Chrome 进程"""
    print("正在关闭现有 Chrome 进程...")
    try:
        subprocess.run(["pkill", "-x", "Google Chrome"], check=False)
        time.sleep(2)
        print("Chrome 已关闭")
    except Exception as e:
        print(f"关闭 Chrome 时出错: {e}")

def start_chrome_debug():
    """启动 Chrome 并开启远程调试"""
    chrome_path = find_chrome()
    
    if not chrome_path:
        print("错误: 未找到 Chrome 浏览器")
        print("请确保 Chrome 已安装在 /Applications/Google Chrome.app")
        return None
    
    print(f"找到 Chrome: {chrome_path}")
    
    # 如果 Chrome 在运行，询问是否关闭
    if is_chrome_running():
        print("\n检测到 Chrome 正在运行")
        print("选项:")
        print("1. 关闭现有 Chrome，启动新的调试 Chrome")
        print("2. 在现有 Chrome 中手动开启远程调试")
        print("3. 取消操作")
        
        choice = input("\n请选择 (1/2/3): ").strip()
        
        if choice == "1":
            kill_chrome()
        elif choice == "2":
            print("\n请在 Chrome 地址栏输入: chrome://inspect/#remote-debugging")
            print("然后勾选 'Allow remote debugging for this browser instance'")
            print("完成后按 Enter 继续...")
            input()
            return 9222  # 返回默认端口
        else:
            print("操作已取消")
            return None
    
    debug_port = 9222
    user_data_dir = os.path.expanduser("~/tmp/chrome_dev_profile")
    os.makedirs(user_data_dir, exist_ok=True)
    
    print(f"\n正在启动 Chrome 并开启远程调试端口 {debug_port}...")
    print(f"用户数据目录: {user_data_dir}")
    
    cmd = [
        chrome_path,
        f"--remote-debugging-port={debug_port}",
        "--no-first-run",
        "--no-default-browser-check",
        f"--user-data-dir={user_data_dir}",
        "https://www.xiaohongshu.com"
    ]
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid if hasattr(os, 'setsid') else None
        )
        
        print(f"Chrome 已启动，PID: {process.pid}")
        print(f"远程调试端口: {debug_port}")
        print("")
        print("=" * 50)
        print("请在小红书网站登录您的账号")
        print("登录完成后，按 Enter 键继续...")
        print("=" * 50)
        input()
        
        return debug_port
        
    except Exception as e:
        print(f"启动 Chrome 失败: {e}")
        return None

def main():
    print("=" * 50)
    print("MediaCrawler Chrome CDP 启动助手")
    print("=" * 50)
    print("")
    
    port = start_chrome_debug()
    
    if port:
        print("")
        print("=" * 50)
        print("Chrome 远程调试已就绪")
        print(f"调试端口: {port}")
        print("")
        print("现在可以运行 MediaCrawler:")
        print(f"  cd /Users/zhijian/workspace/MediaCrawler-main")
        print(f"  python3 main.py --platform xhs --lt cookie --crawler-type search --keywords \"美食探店\"")
        print("=" * 50)
        
        # 保持脚本运行，防止 Chrome 被关闭
        print("")
        print("按 Ctrl+C 关闭 Chrome 并退出")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n正在关闭 Chrome...")
            kill_chrome()
            print("已退出")

if __name__ == "__main__":
    main()
