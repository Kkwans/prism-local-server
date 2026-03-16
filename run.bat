@echo off
REM Prism Local Server 快速启动脚本
REM 作者: Kkwans
REM 创建时间: 2026-03-16

echo ========================================
echo Prism Local Server - 快速启动
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Python未安装或未添加到PATH
    echo 请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查依赖是否安装
python -c "import flet" 2>nul
if errorlevel 1 (
    echo [提示] 检测到依赖未安装
    echo 正在安装依赖...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 安装依赖失败
        pause
        exit /b 1
    )
    echo 依赖安装完成
    echo.
)

echo 正在启动应用...
python main.py

pause
