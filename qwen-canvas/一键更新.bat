@echo off
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0"
title Qwen Canvas One-Click Updater
echo ========================================
echo Qwen Canvas One-Click Updater
echo ========================================
echo Preserving models, .env, outputs, projects and .venv.
where powershell.exe >nul 2>nul
if errorlevel 1 goto :fail
set "TMP=%TEMP%\qwen-canvas-update-%RANDOM%%RANDOM%"
set "ZIP=%TMP%\main.zip"
set "SRC=%TMP%\src"
mkdir "%TMP%" >nul 2>nul
mkdir "%SRC%" >nul 2>nul
echo [1/4] Downloading latest source...
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "$ProgressPreference='SilentlyContinue'; Invoke-WebRequest -UseBasicParsing 'https://github.com/wq205583-commits/jccw/archive/refs/heads/main.zip' -OutFile '%ZIP%'"
if errorlevel 1 goto :fail
echo [2/4] Extracting...
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -LiteralPath '%ZIP%' -DestinationPath '%SRC%' -Force"
if errorlevel 1 goto :fail
set "NEW=%SRC%\jccw-main\qwen-canvas"
if not exist "%NEW%\start.bat" goto :fail
echo [3/4] Updating program files...
robocopy "%NEW%" "%~dp0" /E /R:2 /W:1 /XD models outputs projects .venv node_modules /XF .env >nul
set "RC=%ERRORLEVEL%"
if %RC% GEQ 8 goto :fail
echo [4/4] Refreshing dependencies...
if exist ".venv\Scripts\python.exe" ".venv\Scripts\python.exe" -m pip install -r "backend\requirements.txt" --disable-pip-version-check
if exist "frontend\package.json" (
 where npm >nul 2>nul
 if not errorlevel 1 (
  pushd "frontend"
  call npm install
  popd
 )
)
rmdir /s /q "%TMP%" >nul 2>nul
echo ========================================
echo [OK] Update completed. Starting Qwen Canvas...
echo ========================================
timeout /t 2 /nobreak >nul
call "%~dp0start.bat"
exit /b 0
:fail
echo [ERROR] Update failed. Existing local data was preserved.
if exist "%TMP%" rmdir /s /q "%TMP%" >nul 2>nul
pause
exit /b 1
