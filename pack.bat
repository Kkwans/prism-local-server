@echo off
chcp 65001 >nul
REM Prism Local Server - Flet官方打包脚本
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

echo [1/3] 清理旧的构建文件...
if exist dist rmdir /s /q dist
echo 完成

echo.
echo [2/3] 开始打包（使用Flet官方工具）...
echo 这可能需要几分钟，请耐心等待...
echo.

flet pack main.py --name "PrismLocalServer" --icon assets/icon.png --add-data "assets;assets"

if errorlevel 1 (
    echo.
    echo [错误] 打包失败
    echo.
    echo 可能的原因：
    echo 1. Flet版本过旧，请运行: pip install --upgrade flet
    echo 2. 缺少依赖，请运行: pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo.
echo [3/3] 打包完成！
echo EXE文件位置: dist\PrismLocalServer.exe
echo.
echo 提示: 首次运行可能需要下载Flet运行时组件
echo.

pause
