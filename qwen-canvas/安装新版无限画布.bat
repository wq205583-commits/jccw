@echo off
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0"
title Qwen Canvas - Infinite Canvas Bootstrap
echo ========================================
echo Qwen Canvas - Infinite Canvas Bootstrap
echo ========================================
where git >nul 2>nul
if errorlevel 1 (echo [ERROR] Git for Windows is required. & pause & exit /b 1)
if not exist "infinite-canvas\.git" (
 echo [1/3] Downloading upstream infinite-canvas...
 git clone --depth 1 https://github.com/basketikun/infinite-canvas.git infinite-canvas
 if errorlevel 1 goto :fail
) else (
 echo [1/3] Updating upstream infinite-canvas...
 pushd infinite-canvas
 git pull --ff-only
 popd
)
echo [2/3] Installing canvas frontend...
where bun >nul 2>nul
if not errorlevel 1 (
 pushd infinite-canvas\web
 call bun install
 popd
 goto :done
)
where npm >nul 2>nul
if errorlevel 1 (echo [ERROR] Bun or Node.js/npm is required. & pause & exit /b 1)
pushd infinite-canvas\web
call npm install
if errorlevel 1 (popd & goto :fail)
popd
:done
echo [3/3] Ready.
echo Existing Qwen model is untouched: models\Qwen-Image-2.1
echo Next integration target: local API http://127.0.0.1:8000/api/generate
pause
exit /b 0
:fail
echo [ERROR] Bootstrap failed. Existing Qwen model/data were not removed.
pause
exit /b 1
