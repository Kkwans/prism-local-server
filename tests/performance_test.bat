@echo off
REM ============================================================================
REM Prism Local Server Tauri - 性能测试脚本 (CMD 版本)
REM 版本: v1.0.0
REM 描述: 调用 PowerShell 脚本执行性能测试
REM ============================================================================

echo.
echo ========================================
echo   Prism Local Server 性能测试
echo ========================================
echo.

REM 检查 PowerShell 是否可用
where powershell >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 找不到 PowerShell，请确保 PowerShell 已安装
    pause
    exit /b 1
)

REM 执行 PowerShell 脚本
echo [信息] 正在启动 PowerShell 性能测试脚本...
echo.

powershell -ExecutionPolicy Bypass -File "%~dp0performance_test.ps1"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [错误] 性能测试执行失败
    pause
    exit /b 1
)

echo.
echo [完成] 性能测试已完成，请查看生成的报告文件
pause
