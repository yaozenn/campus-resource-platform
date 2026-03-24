#!/bin/bash

# 校园资源共享平台一键启动脚本
echo "正在启动校园资源共享平台..."

# 启动后端服务器
echo "启动后端服务器..."
python3 manage.py runserver 8000 > backend.log 2>&1 &
BACKEND_PID=$!
echo "后端服务器已启动，PID: $BACKEND_PID"

# 等待后端服务器启动
sleep 3

# 启动前端服务器
echo "启动前端服务器..."
npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!
echo "前端服务器已启动，PID: $FRONTEND_PID"

# 显示访问地址
echo "系统启动完成！"
echo "后端地址: http://127.0.0.1:8000/"
echo "前端地址: http://localhost:5173/"
echo "如需停止服务，请运行: ./stop.sh"

# 保存进程ID到文件
echo $BACKEND_PID > backend.pid
echo $FRONTEND_PID > frontend.pid
