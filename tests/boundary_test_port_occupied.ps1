# 边界测试：端口占用测试脚本
# 功能：占用端口 8888-8900，测试应用的端口检测和错误处理

Write-Host "=== 端口占用边界测试 ===" -ForegroundColor Cyan
Write-Host ""

# 检查是否以管理员身份运行
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "警告: 建议以管理员身份运行此脚本以获得更好的端口控制" -ForegroundColor Yellow
    Write-Host ""
}

# 定义要占用的端口范围
$ports = 8888..8900
$jobs = @()

Write-Host "正在占用端口 8888-8900 (共 13 个端口)..." -ForegroundColor Yellow
Write-Host ""

# 启动后台任务占用端口
foreach ($port in $ports) {
    try {
        $job = Start-Job -ScriptBlock {
            param($p)
            try {
                $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Any, $p)
                $listener.Start()
                Write-Output "端口 $p 已占用"
                Start-Sleep -Seconds 600  # 保持 10 分钟
                $listener.Stop()
            } catch {
                Write-Output "端口 $p 占用失败: $_"
            }
        } -ArgumentList $port
        
        $jobs += $job
        Start-Sleep -Milliseconds 100  # 短暂延迟，确保端口绑定成功
    } catch {
        Write-Host "启动端口 $port 占用任务失败: $_" -ForegroundColor Red
    }
}

# 等待所有任务启动
Start-Sleep -Seconds 2

# 检查任务状态
Write-Host "端口占用状态:" -ForegroundColor Green
$jobs | ForEach-Object {
    $output = Receive-Job -Job $_ -ErrorAction SilentlyContinue
    if ($output) {
        Write-Host "  $output" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "✅ 所有端口已占用，测试环境准备完成" -ForegroundColor Green
Write-Host ""
Write-Host "测试步骤:" -ForegroundColor Cyan
Write-Host "1. 启动 Prism Local Server 应用"
Write-Host "2. 尝试启动服务（使用默认端口 8888）"
Write-Host "3. 观察应用的错误提示和行为"
Write-Host ""
Write-Host "预期结果:" -ForegroundColor Yellow
Write-Host "- 应用检测到端口 8888-8900 都被占用"
Write-Host "- 显示友好的错误提示"
Write-Host "- 应用不崩溃，可以继续操作"
Write-Host ""
Write-Host "按任意键停止占用端口并结束测试..." -ForegroundColor Magenta
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# 停止所有任务
Write-Host ""
Write-Host "正在释放所有端口..." -ForegroundColor Yellow
$jobs | Stop-Job -ErrorAction SilentlyContinue
$jobs | Remove-Job -ErrorAction SilentlyContinue

Write-Host "✅ 所有端口已释放，测试完成" -ForegroundColor Green
Write-Host ""
Write-Host "请在测试报告中记录测试结果" -ForegroundColor Cyan
