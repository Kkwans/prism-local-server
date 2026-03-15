@echo off
REM Prism Local Server 打包脚本
REM 使用PyInstaller将应用程序打包为EXE文件
REM 作者: Kkwans
REM 创建时间: 2026-03-15

echo ============================================================
echo   Prism Local Server - 打包脚本
echo ============================================================
echo.

REM 检查是否安装了PyInstaller
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [错误] 未安装PyInstaller
    echo 请运行: pip install pyinstaller
    pause
    exit /b 1
)

echo [1/4] 清理旧的构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo       完成

echo.
echo [2/4] 运行PyInstaller打包...
pyinstaller build.spec --clean --noconfirm
if errorlevel 1 (
    echo [错误] 打包失败
    pause
    exit /b 1
)
echo       完成

echo.
echo [3/4] 复制配置文件...
if not exist dist\PrismLocalServer\config mkdir dist\PrismLocalServer\config
if exist config\settings.json copy config\settings.json dist\PrismLocalServer\config\
echo       完成

echo.
echo [4/4] 创建日志目录...
if not exist dist\PrismLocalServer\logs mkdir dist\PrismLocalServer\logs
echo       完成

echo.
echo ============================================================
echo   打包完成！
echo ============================================================
echo.
echo   输出目录: dist\PrismLocalServer\
echo   可执行文件: dist\PrismLocalServer\PrismLocalServer.exe
echo.
echo ============================================================

pause
