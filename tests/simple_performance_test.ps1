# Prism Local Server Tauri - 简化性能测试脚本
# 版本: v1.0.0

param(
    [string]$ExePath = "..\prism-local-server-v3.0.0.exe"
)

Write-Host "`n========================================"
Write-Host "  Prism Local Server 性能测试"
Write-Host "========================================`n"

# 检查 EXE 文件
Write-Host "[1/4] 检查 EXE 文件..." -ForegroundColor Yellow

if (-not (Test-Path $ExePath)) {
    Write-Host "错误: 找不到 EXE 文件: $ExePath" -ForegroundColor Red
    exit 1
}

Write-Host "EXE 文件存在" -ForegroundColor Green

# 测量 EXE 文件体积
Write-Host "`n[2/4] 测量 EXE 文件体积..." -ForegroundColor Yellow

$ExeFile = Get-Item $ExePath
$ExeSizeMB = [math]::Round($ExeFile.Length / 1MB, 2)

Write-Host "EXE 文件体积: $ExeSizeMB MB" -ForegroundColor Cyan

if ($ExeSizeMB -le 15) {
    Write-Host "达标 (目标 <= 15MB)" -ForegroundColor Green
} else {
    Write-Host "未达标 (目标 <= 15MB)" -ForegroundColor Red
}

# 测量冷启动时间
Write-Host "`n[3/4] 测量冷启动时间 (3次测试)..." -ForegroundColor Yellow

$StartupTimes = @()

for ($i = 1; $i -le 3; $i++) {
    Write-Host "  第 $i 次测试..." -ForegroundColor Gray
    
    # 关闭现有进程
    Get-Process -Name "prism-local-server-tauri" -ErrorAction SilentlyContinue | Stop-Process -Force
    Start-Sleep -Seconds 2
    
    # 测量启动时间
    $StartTime = Get-Date
    $Process = Start-Process -FilePath $ExePath -PassThru -WindowStyle Normal
    
    # 等待窗口出现
    $Timeout = 10
    $Elapsed = 0
    while ($Elapsed -lt $Timeout) {
        Start-Sleep -Milliseconds 100
        $Elapsed += 0.1
        
        $Process.Refresh()
        if ($Process.MainWindowHandle -ne 0) {
            break
        }
    }
    
    $EndTime = Get-Date
    $StartupTime = ($EndTime - $StartTime).TotalSeconds
    $StartupTimes += $StartupTime
    
    Write-Host "    启动时间: $([math]::Round($StartupTime, 2)) 秒" -ForegroundColor Cyan
    
    Start-Sleep -Seconds 2
}

$AvgStartupTime = [math]::Round(($StartupTimes | Measure-Object -Average).Average, 2)
Write-Host "`n平均冷启动时间: $AvgStartupTime 秒" -ForegroundColor Cyan

if ($AvgStartupTime -le 1.5) {
    Write-Host "达标 (目标 <= 1.5 秒)" -ForegroundColor Green
} else {
    Write-Host "未达标 (目标 <= 1.5 秒)" -ForegroundColor Red
}

# 测量空闲状态内存占用
Write-Host "`n[4/4] 测量空闲状态内存占用..." -ForegroundColor Yellow
Write-Host "  等待 30 秒让应用稳定..." -ForegroundColor Gray

Start-Sleep -Seconds 30

$Process = Get-Process -Name "prism-local-server-tauri" -ErrorAction SilentlyContinue
if ($Process) {
    $IdleMemoryMB = [math]::Round($Process.WorkingSet64 / 1MB, 2)
    
    Write-Host "空闲内存占用: $IdleMemoryMB MB" -ForegroundColor Cyan
    
    if ($IdleMemoryMB -le 40) {
        Write-Host "达标 (目标 <= 40MB)" -ForegroundColor Green
    } else {
        Write-Host "未达标 (目标 <= 40MB)" -ForegroundColor Red
    }
} else {
    Write-Host "错误: 找不到运行中的进程" -ForegroundColor Red
    $IdleMemoryMB = 0
}

# 生成简单报告
Write-Host "`n========================================"
Write-Host "  测试结果汇总"
Write-Host "========================================`n"

Write-Host "1. EXE 文件体积: $ExeSizeMB MB (目标 <= 15MB)"
Write-Host "2. 平均冷启动时间: $AvgStartupTime 秒 (目标 <= 1.5 秒)"
Write-Host "3. 空闲内存占用: $IdleMemoryMB MB (目标 <= 40MB)"

Write-Host "`n测试完成！" -ForegroundColor Green
Write-Host "请手动测试以下项目:" -ForegroundColor Yellow
Write-Host "- 运行 5 个服务时的内存占用 (目标 <= 150MB)"
Write-Host "- 小文件响应时间 (目标 <= 10ms)"
Write-Host "- 视频首帧加载时间 (目标 <= 100ms)"

Write-Host "`n是否关闭应用? (Y/N)" -ForegroundColor Yellow
$CloseApp = Read-Host

if ($CloseApp -eq "Y" -or $CloseApp -eq "y") {
    Get-Process -Name "prism-local-server-tauri" -ErrorAction SilentlyContinue | Stop-Process -Force
    Write-Host "应用已关闭" -ForegroundColor Green
}
