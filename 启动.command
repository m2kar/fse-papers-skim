#!/bin/bash
# FSE 论文略读 · 启动本地服务器并打开演示页面（macOS 双击即可）
cd "$(dirname "$0")" || exit 1

PORT=8931
while true; do
  # 该端口已能访问本页（上次启动的服务器还在）→ 直接打开
  if curl -s -m 1 -o /dev/null "http://localhost:$PORT/index.html"; then
    open "http://localhost:$PORT/index.html"
    exit 0
  fi
  # 端口被其他程序占用 → 换一个
  if lsof -i :"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
    PORT=$((PORT + 1))
    continue
  fi
  break
done

python3 -m http.server "$PORT" >/dev/null 2>&1 &
sleep 1

if curl -s -m 2 -o /dev/null "http://localhost:$PORT/index.html"; then
  echo "服务器已启动：http://localhost:$PORT/index.html"
  open "http://localhost:$PORT/index.html"
  echo "窗口可关闭，服务器继续运行；结束演示请在终端按 Ctrl+C 或关闭此窗口"
  wait $!
else
  echo "启动失败：请确认已安装 python3（终端执行 python3 --version 检查）"
  exit 1
fi
