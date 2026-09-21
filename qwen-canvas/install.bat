@echo off
setlocal
chcp 65001 >nul
cd /d %~dp0
title Qwen Canvas Installer
where python >nul 2>nul || (echo [ERROR] 请安装 Python 3.11 x64 并勾选 Add Python to PATH & pause & exit /b 1)
where node >nul 2>nul || (echo [ERROR] 请安装 Node.js 20+ & pause & exit /b 1)
where git >nul 2>nul || (echo [ERROR] 请安装 Git for Windows & pause & exit /b 1)
if not exist .venv (python -m venv .venv || goto :fail)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip || goto :fail
pip install -r backend\requirements.txt || goto :fail
pushd frontend
call npm install || (popd & goto :fail)
popd
if not exist outputs mkdir outputs
if not exist projects mkdir projects
echo.
echo ========================================
echo [OK] Qwen Canvas 安装完成
echo 双击 start.bat 启动。首次生成会下载模型。
echo ========================================
pause
exit /b 0
:fail
echo.
echo [ERROR] 安装失败。请双击 run-doctor.bat 查看环境信息。
pause
exit /b 1
