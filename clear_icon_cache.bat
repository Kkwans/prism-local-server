@echo off
chcp 65001 >nul
REM 清理 Windows 图标缓存
REM 作者: Kkwans
REM 创建时间: 2026-03-16

echo ========================================
echo 清理 Windows 图标缓存
echo ========================================
echo.

echo [1/3] 停止 Windows 资源管理器...
taskkill /f /im explorer.exe >nul 2>&1

echo [2/3] 删除图标缓存文件...
del /f /q "%localappdata%\IconCache.db" >nul 2>&1
del /f /q "%localappdata%\Microsoft\Windows\Explorer\iconcache_*.db" >nul 2>&1
del /f /q "%localappdata%\Microsoft\Windows\Explorer\thumbcache_*.db" >nul 2>&1

echo [3/3] 重启 Windows 资源管理器...
start explorer.exe

echo.
echo 完成！图标缓存已清理
echo 请检查 EXE 文件图标是否已更新
echo.

pause
