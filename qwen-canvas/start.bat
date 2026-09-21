@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
title Qwen Canvas Launcher
if not exist ".venv\Scripts\python.exe" goto :not_installed
if not exist "frontend\node_modules" goto :not_installed
start "Qwen Canvas API - DO NOT CLOSE" cmd /k "cd /d ""%~dp0backend"" && ""%~dp0.venv\Scripts\python.exe"" -m uvicorn main:app --host 127.0.0.1 --port 8000"
timeout /t 4 /nobreak >nul
start "Qwen Canvas UI - DO NOT CLOSE" cmd /k "cd /d ""%~dp0frontend"" && npm run dev"
timeout /t 4 /nobreak >nul
start "" "http://127.0.0.1:7860"
exit /b 0
:not_installed
echo [ERROR] Dependencies are missing. Run install.bat first.
pause
exit /b 1
