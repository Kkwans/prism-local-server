@echo off
REM 清理旧目录脚本（CMD 版本）
REM 用于删除重命名后的旧目录（src-tauri）

echo === 清理旧目录 ===
echo.

if exist "src-tauri" (
    echo 发现旧目录: src-tauri
    echo 正在尝试删除...
    
    rmdir /s /q "src-tauri" 2>nul
    
    if exist "src-tauri" (
        echo X 删除失败
        echo.
        echo 可能的原因：
        echo   1. 文件资源管理器正在访问该目录
        echo   2. IDE（如 VS Code）正在打开该目录中的文件
        echo   3. Cargo 或其他进程正在使用该目录
        echo   4. Windows 索引服务正在扫描该目录
        echo.
        echo 解决方法：
        echo   1. 关闭所有可能访问该目录的程序（IDE、文件管理器等）
        echo   2. 等待几秒钟让文件锁释放
        echo   3. 重新运行此脚本
        echo   4. 如果仍然失败，重启计算机后再试
        echo.
        pause
        exit /b 1
    ) else (
        echo √ 成功删除 src-tauri 目录
    )
) else (
    echo √ src-tauri 目录不存在，无需清理
)

echo.
echo === 清理完成 ===
pause
