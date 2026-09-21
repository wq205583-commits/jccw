@echo off
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0"
title Qwen Canvas Launcher
echo ========================================
echo Qwen Canvas + Infinite Canvas
echo ========================================
if not exist ".venv\Scripts\python.exe" goto :backend_missing
if not exist "infinite-canvas\web\package.json" goto :canvas_missing
if not exist "infinite-canvas\web\node_modules" goto :deps_missing

echo [0/3] Installing local Qwen provider into Infinite Canvas...
".venv\Scripts\python.exe" "%~dp0patch_infinite_qwen.py"
if errorlevel 1 (echo [ERROR] Failed to patch Infinite Canvas. & pause & exit /b 1)
echo [1/3] Starting Qwen-Image-2.1 backend...
start "Qwen Local API - DO NOT CLOSE" /D "%~dp0backend" "%ComSpec%" /k ""%~dp0.venv\Scripts\python.exe" -m uvicorn main:app --host 127.0.0.1 --port 8000"

echo [2/3] Starting Infinite Canvas...
start "Infinite Canvas - DO NOT CLOSE" /D "%~dp0infinite-canvas\web" "%ComSpec%" /k "npm run dev"

echo [3/3] Opening browser...
timeout /t 5 /nobreak >nul
start "" "http://127.0.0.1:3000"
echo [OK] Qwen API: http://127.0.0.1:8000
echo [OK] Canvas:   http://127.0.0.1:3000
exit /b 0

:backend_missing
echo [ERROR] Qwen Python environment is missing. Run install.bat first.
pause
exit /b 1
:canvas_missing
echo [ERROR] Infinite Canvas is missing. Run INSTALL-INFINITE-CANVAS.bat first.
pause
exit /b 1
:deps_missing
echo [ERROR] Infinite Canvas dependencies are missing. Run INSTALL-INFINITE-CANVAS.bat first.
pause
exit /b 1
