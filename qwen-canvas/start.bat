@echo off
setlocal
chcp 65001 >nul
cd /d %~dp0
title Qwen Canvas Launcher
if not exist .venv\Scripts\python.exe (echo [ERROR] 未安装，请先双击 install.bat & pause & exit /b 1)
if not exist frontend\node_modules (echo [ERROR] 前端依赖不存在，请重新运行 install.bat & pause & exit /b 1)
start "Qwen Canvas API - DO NOT CLOSE" cmd /k "cd /d %~dp0backend && ..\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000"
timeout /t 3 /nobreak >nul
start "Qwen Canvas UI - DO NOT CLOSE" cmd /k "cd /d %~dp0frontend && npm run dev"
timeout /t 3 /nobreak >nul
start "" http://127.0.0.1:7860
echo Qwen Canvas 已启动。请保留两个服务窗口。
timeout /t 2 >nul
