# 清理旧目录脚本
# 用于删除重命名后的旧目录（src-tauri）

Write-Host "=== 清理旧目录 ===" -ForegroundColor Cyan
Write-Host ""

# 检查 src-tauri 目录是否存在
if (Test-Path "src-tauri") {
    Write-Host "发现旧目录: src-tauri" -ForegroundColor Yellow
    Write-Host "正在尝试删除..." -ForegroundColor Yellow
    
    try {
        # 尝试删除
        Remove-Item -Path "src-tauri" -Recurse -Force -ErrorAction Stop
        Write-Host "✓ 成功删除 src-tauri 目录" -ForegroundColor Green
    }
    catch {
        Write-Host "✗ 删除失败: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host ""
        Write-Host "可能的原因：" -ForegroundColor Yellow
        Write-Host "  1. 文件资源管理器正在访问该目录" -ForegroundColor White
        Write-Host "  2. IDE（如 VS Code）正在打开该目录中的文件" -ForegroundColor White
        Write-Host "  3. Cargo 或其他进程正在使用该目录" -ForegroundColor White
        Write-Host "  4. Windows 索引服务正在扫描该目录" -ForegroundColor White
        Write-Host ""
        Write-Host "解决方法：" -ForegroundColor Yellow
        Write-Host "  1. 关闭所有可能访问该目录的程序（IDE、文件管理器等）" -ForegroundColor White
        Write-Host "  2. 等待几秒钟让文件锁释放" -ForegroundColor White
        Write-Host "  3. 重新运行此脚本" -ForegroundColor White
        Write-Host "  4. 如果仍然失败，重启计算机后再试" -ForegroundColor White
        Write-Host ""
        exit 1
    }
}
else {
    Write-Host "✓ src-tauri 目录不存在，无需清理" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== 清理完成 ===" -ForegroundColor Cyan
