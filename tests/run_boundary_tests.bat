@echo off
REM 边界测试批处理脚本
REM 用于运行所有自动化边界测试

echo ========================================
echo   Prism Local Server 边界测试套件
echo ========================================
echo.

echo 此脚本将运行以下边界测试:
echo   1. 端口占用测试
echo   2. 无 HTML 文件测试
echo   3. 无权限目录测试 (需要管理员权限)
echo   4. 多服务并发测试
echo.

echo 注意: 某些测试需要管理员权限
echo.

pause

:MENU
echo.
echo ========================================
echo   选择要运行的测试
echo ========================================
echo   1. 端口占用测试
echo   2. 无 HTML 文件测试
echo   3. 无权限目录测试 (需要管理员权限)
echo   4. 多服务并发测试
echo   5. 运行所有测试
echo   0. 退出
echo ========================================
echo.

set /p choice="请输入选项 (0-5): "

if "%choice%"=="1" goto TEST1
if "%choice%"=="2" goto TEST2
if "%choice%"=="3" goto TEST3
if "%choice%"=="4" goto TEST4
if "%choice%"=="5" goto TESTALL
if "%choice%"=="0" goto END
goto MENU

:TEST1
echo.
echo 运行端口占用测试...
powershell -ExecutionPolicy Bypass -File "%~dp0boundary_test_port_occupied.ps1"
goto MENU

:TEST2
echo.
echo 运行无 HTML 文件测试...
powershell -ExecutionPolicy Bypass -File "%~dp0boundary_test_no_html.ps1"
goto MENU

:TEST3
echo.
echo 运行无权限目录测试...
echo 注意: 此测试需要管理员权限
powershell -ExecutionPolicy Bypass -File "%~dp0boundary_test_no_permission.ps1"
goto MENU

:TEST4
echo.
echo 运行多服务并发测试...
powershell -ExecutionPolicy Bypass -File "%~dp0boundary_test_multiple_services.ps1"
goto MENU

:TESTALL
echo.
echo 运行所有测试...
echo.
echo [1/4] 端口占用测试
powershell -ExecutionPolicy Bypass -File "%~dp0boundary_test_port_occupied.ps1"
echo.
echo [2/4] 无 HTML 文件测试
powershell -ExecutionPolicy Bypass -File "%~dp0boundary_test_no_html.ps1"
echo.
echo [3/4] 无权限目录测试
powershell -ExecutionPolicy Bypass -File "%~dp0boundary_test_no_permission.ps1"
echo.
echo [4/4] 多服务并发测试
powershell -ExecutionPolicy Bypass -File "%~dp0boundary_test_multiple_services.ps1"
echo.
echo 所有测试完成!
goto MENU

:END
echo.
echo 测试结束，请查看测试报告: TASK_10.3_BOUNDARY_TEST_REPORT.md
echo.
pause
