@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
title Qwen Canvas Installer
echo ========================================
echo Qwen Canvas Installer - Windows NVIDIA
echo ========================================
set "PYEXE="
where py >nul 2>nul
if not errorlevel 1 (
 py -3.11 -c "import sys;print(sys.executable)" >nul 2>nul
 if not errorlevel 1 set "PYEXE=py -3.11"
)
if not defined PYEXE (
 where python >nul 2>nul
 if not errorlevel 1 (
  python -c "import sys;exit(0 if sys.version_info[:2]==(3,11) else 1)" >nul 2>nul
  if not errorlevel 1 set "PYEXE=python"
 )
)
if not defined PYEXE goto :python_missing
where node >nul 2>nul
if errorlevel 1 goto :node_missing
where git >nul 2>nul
if errorlevel 1 goto :git_missing
if not exist ".venv\Scripts\python.exe" %PYEXE% -m venv ".venv"
if errorlevel 1 goto :fail
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
if errorlevel 1 goto :fail
echo [1/3] Installing NVIDIA CUDA PyTorch...
python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
if errorlevel 1 goto :fail
echo [2/3] Installing Qwen Canvas backend...
python -m pip install -r "backend\requirements.txt"
if errorlevel 1 goto :fail
echo [3/3] Installing frontend...
pushd "frontend"
call npm install
if errorlevel 1 (popd & goto :fail)
popd
if not exist "outputs" mkdir "outputs"
if not exist "projects" mkdir "projects"
echo ========================================
echo [OK] Installation finished.
echo Run check.bat, then start.bat.
echo ========================================
pause
exit /b 0
:python_missing
echo [ERROR] Python 3.11 was not found.
echo Install Python 3.11 x64, or verify with: py -3.11 --version
goto :stop
:node_missing
echo [ERROR] Node.js not found. Install Node.js 20 or newer.
goto :stop
:git_missing
echo [ERROR] Git not found. Install Git for Windows.
goto :stop
:fail
echo [ERROR] Installation failed. Run run-doctor.bat and keep the full output.
:stop
pause
exit /b 1
