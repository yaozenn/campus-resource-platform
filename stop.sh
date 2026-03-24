#!/bin/bash

# 校园资源共享平台一键停止脚本
echo "正在停止校园资源共享平台..."

# 停止前端服务器
if [ -f frontend.pid ]; then
    FRONTEND_PID=$(cat frontend.pid)
    echo "停止前端服务器，PID: $FRONTEND_PID"
    kill $FRONTEND_PID 2>/dev/null
    rm frontend.pid
else
    echo "前端服务器未运行"
fi

# 停止后端服务器
if [ -f backend.pid ]; then
    BACKEND_PID=$(cat backend.pid)
    echo "停止后端服务器，PID: $BACKEND_PID"
    kill $BACKEND_PID 2>/dev/null
    rm backend.pid
else
    echo "后端服务器未运行"
fi

# 清理日志文件
echo "清理日志文件..."
rm -f backend.log frontend.log

echo "系统已停止！"
