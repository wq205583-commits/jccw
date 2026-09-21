@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
echo ========================================
echo Qwen Canvas Environment Check
echo ========================================
where python >nul 2>nul
if errorlevel 1 (echo [X] Python not found) else (echo [OK] Python)
where node >nul 2>nul
if errorlevel 1 (echo [X] Node.js not found) else (echo [OK] Node.js)
where git >nul 2>nul
if errorlevel 1 (echo [X] Git not found) else (echo [OK] Git)
if exist ".venv\Scripts\python.exe" (echo [OK] Python venv) else (echo [X] Python venv missing - run install.bat)
if exist "frontend\node_modules" (echo [OK] Frontend dependencies) else (echo [X] Frontend dependencies missing - run install.bat)
if exist ".env" (echo [OK] Optional API config found) else (echo [INFO] OpenAI/Gemini API config is optional)
if exist ".venv\Scripts\python.exe" (
 echo Checking CUDA and GPU...
 ".venv\Scripts\python.exe" -c "import torch; print('[OK] CUDA:', torch.cuda.is_available()); print('[GPU]', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CUDA unavailable')"
)
echo ========================================
echo Check finished.
pause
endlocal
