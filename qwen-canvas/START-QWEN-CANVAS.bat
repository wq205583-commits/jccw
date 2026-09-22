@echo off
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0"
title Qwen Canvas - KEEP THIS WINDOW OPEN
echo ========================================
echo Qwen Canvas + Infinite Canvas
echo ========================================
if not exist ".venv\Scripts\python.exe" goto :backend_missing
if not exist "infinite-canvas\web\package.json" goto :canvas_missing
if not exist "infinite-canvas\web\node_modules" goto :deps_missing

echo [0/3] Installing local Qwen provider...
".venv\Scripts\python.exe" "%~dp0patch_infinite_qwen.py"
if errorlevel 1 goto :fail

echo [1/3] Cleaning stale local services...
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "$ports=8000,3000; foreach($port in $ports){$ids=(Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue).OwningProcess | Select-Object -Unique; foreach($id in $ids){if($id){Stop-Process -Id $id -Force -ErrorAction SilentlyContinue}}}"
timeout /t 1 /nobreak >nul

echo [2/3] Starting Qwen API in background...
start "" /b cmd /c "cd /d ""%~dp0backend"" && ""%~dp0.venv\Scripts\python.exe"" -m uvicorn main:app --host 127.0.0.1 --port 8000"

echo [3/3] Starting Infinite Canvas in background...
pushd "%~dp0infinite-canvas\web"
start "" /b cmd /c "npm run dev"
popd

echo Waiting for services...
timeout /t 5 /nobreak >nul
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "try{$r=Invoke-RestMethod -Uri 'http://127.0.0.1:8000/openapi.json' -TimeoutSec 5; $paths=@($r.paths.PSObject.Properties.Name); if($paths -notcontains '/v1/images/edits'){Write-Host '[ERROR] Loaded routes:' ($paths -join ', '); exit 2}}catch{Write-Host '[ERROR] API check:' $_.Exception.Message; exit 1}"
if errorlevel 1 goto :api_fail
start "" "http://127.0.0.1:3000"
echo.
echo ========================================
echo [OK] Qwen API: http://127.0.0.1:8000
echo [OK] Canvas:   http://127.0.0.1:3000
echo Keep this ONE window open while using Qwen Canvas.
echo Press Ctrl+C to stop services.
echo ========================================
:hold
timeout /t 3600 /nobreak >nul
goto :hold

:backend_missing
echo [ERROR] Python environment missing. Run install.bat first.
pause
exit /b 1
:canvas_missing
echo [ERROR] Infinite Canvas missing. Run INSTALL-INFINITE-CANVAS.bat first.
pause
exit /b 1
:deps_missing
echo [ERROR] Infinite Canvas dependencies missing. Run INSTALL-INFINITE-CANVAS.bat first.
pause
exit /b 1
:api_fail
echo [ERROR] Updated Qwen API failed to start.
pause
exit /b 1
:fail
echo [ERROR] Startup preparation failed.
pause
exit /b 1
