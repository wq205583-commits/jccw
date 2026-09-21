@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (echo [ERROR] Run install.bat first. & pause & exit /b 1)
if not exist "models" mkdir "models"
echo Qwen-Image-2.1 model downloader
echo Destination: %~dp0models\Qwen-Image-2.1
echo Existing files will be reused. Interrupted downloads can be resumed.
".venv\Scripts\python.exe" download_model.py
if errorlevel 1 (echo [ERROR] Download failed. Run this file again to resume. & pause & exit /b 1)
echo [OK] Model download completed.
pause
