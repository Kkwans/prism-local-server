@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo   Prism Local Server 功能测试助手
echo ========================================
echo.

REM 检查 EXE 文件
set "EXE_PATH=%~dp0..\prism-local-server-v3.0.0.exe"
if not exist "%EXE_PATH%" (
    echo ❌ 错误: 未找到 EXE 文件
    echo    路径: %EXE_PATH%
    echo    请先运行 'npm run tauri:build' 构建应用
    pause
    exit /b 1
)
echo ✅ 找到 EXE 文件

REM 检查测试资源
set "TEST_RESOURCES=%~dp0test_resources"
echo.
echo 检查测试资源...

if exist "%TEST_RESOURCES%\index.html" (
    echo   ✅ index.html
) else (
    echo   ❌ index.html ^(缺失^)
    set "MISSING=1"
)

if exist "%TEST_RESOURCES%\css\style.css" (
    echo   ✅ css\style.css
) else (
    echo   ❌ css\style.css ^(缺失^)
    set "MISSING=1"
)

if exist "%TEST_RESOURCES%\js\script.js" (
    echo   ✅ js\script.js
) else (
    echo   ❌ js\script.js ^(缺失^)
    set "MISSING=1"
)

if defined MISSING (
    echo.
    echo ❌ 错误: 缺少必需的测试文件
    pause
    exit /b 1
)

REM 检查可选资源
echo.
echo 检查可选测试资源...

if exist "%TEST_RESOURCES%\images\test-image.png" (
    echo   ✅ images\test-image.png
) else (
    echo   ⚠️  images\test-image.png ^(缺失^)
    set "MISSING_OPTIONAL=1"
)

if exist "%TEST_RESOURCES%\images\中文文件名图片.png" (
    echo   ✅ images\中文文件名图片.png
) else (
    echo   ⚠️  images\中文文件名图片.png ^(缺失^)
    set "MISSING_OPTIONAL=1"
)

if exist "%TEST_RESOURCES%\videos\test-video.mp4" (
    echo   ✅ videos\test-video.mp4
) else (
    echo   ⚠️  videos\test-video.mp4 ^(缺失^)
    set "MISSING_OPTIONAL=1"
)

if defined MISSING_OPTIONAL (
    echo.
    echo ⚠️  警告: 缺少部分可选测试资源
    echo    请参考 test_resources\images\README.md 和 test_resources\videos\README.md
    echo.
)

REM 启动应用
echo.
echo ========================================
echo 准备启动应用进行测试
echo ========================================
echo.
echo 测试资源目录: %TEST_RESOURCES%
echo 测试报告模板: tests\TASK_10.1_FUNCTIONAL_TEST_REPORT.md
echo.

set /p START_APP="是否启动应用？(y/n): "
if /i "%START_APP%"=="y" (
    echo.
    echo 正在启动应用...
    start "" "%EXE_PATH%"
    
    echo.
    echo ✅ 应用已启动
    echo.
    echo 请按照测试报告模板执行测试：
    echo   tests\TASK_10.1_FUNCTIONAL_TEST_REPORT.md
    echo.
    echo 测试步骤：
    echo   1. 在应用中点击'启动服务'
    echo   2. 选择测试资源目录: %TEST_RESOURCES%
    echo   3. 在浏览器中访问: http://localhost:8888/index.html
    echo   4. 按照测试报告逐项测试
    echo.
) else (
    echo.
    echo 测试已取消
    echo.
    echo 您可以手动启动应用进行测试：
    echo   %EXE_PATH%
    echo.
)

echo ========================================
echo 测试助手运行完成
echo ========================================
pause
