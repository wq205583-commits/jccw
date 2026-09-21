@echo off
chcp 65001 >nul
cd /d %~dp0
if not exist .venv\Scripts\python.exe (echo 请先运行 install.bat & pause & exit /b 1)
start "Qwen Canvas API" cmd /k "cd /d %~dp0backend && ..\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000"
timeout /t 2 >nul
start "Qwen Canvas UI" cmd /k "cd /d %~dp0frontend && npm run dev"
timeout /t 2 >nul
start http://127.0.0.1:7860
