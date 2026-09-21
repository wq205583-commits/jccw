@echo off
chcp 65001 >nul
cd /d %~dp0
echo === Qwen Canvas 环境自检 ===
where python >nul 2>nul && echo [OK] Python || echo [X] Python 未安装
where node >nul 2>nul && echo [OK] Node.js || echo [X] Node.js 未安装
where git >nul 2>nul && echo [OK] Git || echo [X] Git 未安装
if exist .venv\Scripts\python.exe (echo [OK] Python 虚拟环境) else echo [X] 请运行 install.bat
if exist frontend\node_modules (echo [OK] 前端依赖) else echo [X] 前端依赖未安装
if exist .env (echo [OK] .env 已创建) else echo [i] GPT/Gemini 可选：复制 .env.example 为 .env
if exist .venv\Scripts\python.exe .venv\Scripts\python.exe -c "import torch;print('[OK] CUDA:',torch.cuda.is_available(),torch.cuda.get_device_name(0) if torch.cuda.is_available() else '不可用')"
pause
