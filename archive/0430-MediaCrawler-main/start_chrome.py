#!/usr/bin/env python3
"""
MediaCrawler 启动助手 - 正确处理 Chrome 后台进程
"""

import subprocess
import os
import sys
import time
import json
import signal
import atexit

CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DEBUG_PORT = 9222

def is_chrome_running():
    """检查 Chrome 是否运行"""
    try:
        result = subprocess.run(["pgrep", "-x", "Google Chrome"], capture_output=True, text=True)
        return result.returncode == 0 and result.stdout.strip()
    except:
        return False

def check_cdp_port():
    """检查 CDP 端口"""
    try:
        import httpx
        response = httpx.get(f"http://localhost:{DEBUG_PORT}/json/version", timeout=2)
        return response.status_code == 200
    except:
        return False

def start_chrome_debug():
    """启动带调试的 Chrome"""
    if not os.path.isfile(CHROME_PATH):
        print(f"错误: 未找到 Chrome: {CHROME_PATH}")
        return False
    
    # 使用 nohup 和 setsid 确保进程在后台持续运行
    cmd = [
        "nohup",
        CHROME_PATH,
        f"--remote-debugging-port={DEBUG_PORT}",
        "--no-first-run",
        "--no-default-browser-check",
        "--user-data-dir=/tmp/chrome_dev_profile",
        "about:blank"
    ]
    
    try:
        # 使用 Popen 启动，不等待完成
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True  # 创建新会话，避免被终端关闭影响
        )
        
        print(f"Chrome 启动中，PID: {process.pid}")
        
        # 等待 Chrome 就绪
        for i in range(10):
            time.sleep(1)
            if check_cdp_port():
                print(f"✓ Chrome 远程调试端口 {DEBUG_PORT} 已就绪")
                return True
            print(f"等待 Chrome 启动... {i+1}/10")
        
        print("✗ Chrome 启动超时")
        return False
        
    except Exception as e:
        print(f"启动 Chrome 失败: {e}")
        return False

def main():
    print("=" * 60)
    print("MediaCrawler Chrome 启动助手")
    print("=" * 60)
    print()
    
    # 检查现有 Chrome
    if is_chrome_running():
        print("检测到 Chrome 正在运行")
        print()
        print("选项:")
        print("1. 关闭现有 Chrome，启动新的调试实例")
        print("2. 使用现有 Chrome（需要手动开启远程调试）")
        print("3. 退出")
        print()
        
        try:
            choice = input("请选择 (1/2/3): ").strip()
        except EOFError:
            # 非交互式环境，默认选择1
            choice = "1"
            print("非交互式环境，自动选择选项 1")
        
        if choice == "1":
            print("关闭现有 Chrome...")
            subprocess.run(["pkill", "-x", "Google Chrome"], check=False)
            time.sleep(3)
            
            if not start_chrome_debug():
                sys.exit(1)
                
        elif choice == "2":
            print("请在 Chrome 地址栏输入: chrome://inspect/#remote-debugging")
            print("然后勾选 'Allow remote debugging for this browser instance'")
            print()
            print("完成后按 Enter 继续...")
            try:
                input()
            except EOFError:
                pass
            
            if not check_cdp_port():
                print("✗ CDP 端口未就绪")
                sys.exit(1)
        else:
            print("退出")
            sys.exit(0)
    else:
        print("Chrome 未运行，启动带调试的 Chrome...")
        if not start_chrome_debug():
            sys.exit(1)
    
    print()
    print("=" * 60)
    print("Chrome 已就绪")
    print(f"远程调试端口: {DEBUG_PORT}")
    print()
    print("现在可以运行 MediaCrawler:")
    print(f"  cd /Users/zhijian/workspace/MediaCrawler-main")
    print(f"  python3 main.py --platform xhs --lt qrcode --crawler-type search --keywords \"美食探店\"")
    print("=" * 60)
    
    # 保持运行
    print()
    print("按 Ctrl+C 退出（Chrome 将继续运行）")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n已退出")

if __name__ == "__main__":
    main()
