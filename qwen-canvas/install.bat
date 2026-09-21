@echo off
chcp 65001 >nul
cd /d %~dp0
where python >nul 2>nul || (echo 请先安装 Python 3.11 x64 & pause & exit /b 1)
where node >nul 2>nul || (echo 请先安装 Node.js 20+ & pause & exit /b 1)
python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r backend\requirements.txt
cd frontend
call npm install
cd ..
echo.
echo 安装完成。现在双击 start.bat
pause
