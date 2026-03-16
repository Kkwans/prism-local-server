@echo off
REM Prism Local Server 打包脚本
REM 作者: Kkwans
REM 创建时间: 2026-03-16

echo ========================================
echo Prism Local Server - 打包脚本
echo ========================================
echo.

REM 检查PyInstaller是否安装
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [错误] PyInstaller未安装
    echo 正在安装PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo [错误] 安装PyInstaller失败
        pause
        exit /b 1
    )
)

echo [1/3] 清理旧的构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo 完成

echo.
echo [2/3] 开始打包...
pyinstaller build.spec
if errorlevel 1 (
    echo [错误] 打包失败
    pause
    exit /b 1
)
echo 完成

echo.
echo [3/3] 打包完成！
echo EXE文件位置: dist\PrismLocalServer.exe
echo.

pause
