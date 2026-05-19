#!/bin/bash
# 启动 Chrome 并开启远程调试端口

CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DEBUG_PORT=9222

# 检查 Chrome 是否已运行
if pgrep -f "Google Chrome" > /dev/null; then
    echo "Chrome 已经在运行，请手动在 Chrome 地址栏输入: chrome://inspect/#remote-debugging"
    echo "然后勾选 'Allow remote debugging for this browser instance'"
    echo ""
    echo "或者关闭所有 Chrome 窗口后重新运行此脚本"
    exit 1
fi

# 启动 Chrome 并开启远程调试
echo "正在启动 Chrome 并开启远程调试端口 ${DEBUG_PORT}..."
"${CHROME_PATH}" \
    --remote-debugging-port=${DEBUG_PORT} \
    --no-first-run \
    --no-default-browser-check \
    --user-data-dir=/tmp/chrome_dev_profile \
    "https://www.xiaohongshu.com" &

CHROME_PID=$!
echo "Chrome 已启动，PID: ${CHROME_PID}"
echo "远程调试端口: ${DEBUG_PORT}"
echo ""
echo "请在小红书网站登录您的账号"
echo "登录完成后，按 Enter 键继续..."
read

echo "Chrome 正在运行，远程调试端口: ${DEBUG_PORT}"
echo "现在可以运行 MediaCrawler 了"
