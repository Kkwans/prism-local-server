@echo off
chcp 65001 >nul
REM Prism Local Server - 改进的Flet打包脚本
REM 作者: Kkwans
REM 创建时间: 2026-03-16

echo ========================================
echo Prism Local Server - Flet官方打包
echo ========================================
echo.

REM 检查Flet是否安装
python -c "import flet" 2>nul
if errorlevel 1 (
    echo [错误] Flet未安装
    echo 正在安装Flet...
    pip install flet
    if errorlevel 1 (
        echo [错误] 安装Flet失败
        pause
        exit /b 1
    )
)

echo [1/4] 清理旧的构建文件...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
echo 完成

echo.
echo [2/4] 检查依赖...
pip install -r requirements.txt
echo 完成

echo.
echo [3/4] 开始打包（使用Flet官方工具）...
echo 这可能需要几分钟，请耐心等待...
echo.

REM 使用 flet pack 打包，包含所有必要的模块和资源
flet pack main.py ^
    --name "PrismLocalServer" ^
    --icon "assets\icon.ico" ^
    --add-data "core;core" ^
    --add-data "ui;ui" ^
    --add-data "utils;utils" ^
    --add-data "assets;assets" ^
    --add-data "config;config" ^
    --debug-console true

if errorlevel 1 (
    echo.
    echo [错误] 打包失败
    echo.
    echo 可能的原因
    echo 1. Flet版本过旧，请运行 pip install --upgrade flet
    echo 2. 缺少依赖，请运行 pip install -r requirements.txt
    echo 3. 图标文件不存在，请检查 assets\icon.ico
    echo.
    pause
    exit /b 1
)

echo.
echo [4/4] 打包完成
echo EXE文件位置 dist\PrismLocalServer.exe
echo.
echo 提示 首次运行可能需要下载Flet运行时组件
echo.

pause
