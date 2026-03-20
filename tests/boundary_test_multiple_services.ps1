# 边界测试：多服务并发测试脚本
# 功能：指导用户测试同时启动 15 个服务实例

Write-Host "=== 多服务并发边界测试 ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "测试目标: 验证应用能够稳定管理 15 个并发服务实例" -ForegroundColor Yellow
Write-Host ""

# 检查应用是否正在运行
$processName = "prism-local-server-v3.0.0"
$process = Get-Process -Name $processName -ErrorAction SilentlyContinue

if (-not $process) {
    Write-Host "⚠️  警告: 未检测到应用进程" -ForegroundColor Yellow
    Write-Host "请先启动 Prism Local Server 应用" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "按任意键继续..." -ForegroundColor Magenta
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

Write-Host "测试步骤:" -ForegroundColor Green
Write-Host ""
Write-Host "第 1 步: 打开任务管理器监控资源" -ForegroundColor Cyan
Write-Host "  - 按 Ctrl+Shift+Esc 打开任务管理器"
Write-Host "  - 切换到'详细信息'标签"
Write-Host "  - 找到 prism-local-server-v3.0.0.exe 进程"
Write-Host "  - 记录初始内存占用"
Write-Host ""

# 打开任务管理器
try {
    Start-Process taskmgr
    Write-Host "✅ 任务管理器已启动" -ForegroundColor Green
} catch {
    Write-Host "⚠️  无法自动启动任务管理器，请手动打开" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "按任意键继续到第 2 步..." -ForegroundColor Magenta
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host ""
Write-Host "第 2 步: 连续启动 15 个服务实例" -ForegroundColor Cyan
Write-Host "  - 在应用中连续快速点击 15 次'启动服务'按钮"
Write-Host "  - 可以使用相同的部署目录"
Write-Host "  - 观察每个服务的启动情况"
Write-Host "  - 记录启动过程中的任何错误或延迟"
Write-Host ""
Write-Host "预期结果:" -ForegroundColor Yellow
Write-Host "  ✅ 所有 15 个服务都成功启动"
Write-Host "  ✅ 端口号依次分配: 8888-8902"
Write-Host "  ✅ 应用界面保持响应，无明显卡顿"
Write-Host "  ✅ 每个服务卡片正确显示信息"
Write-Host ""

Write-Host "按任意键继续到第 3 步..." -ForegroundColor Magenta
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host ""
Write-Host "第 3 步: 检查资源占用" -ForegroundColor Cyan
Write-Host "  - 在任务管理器中查看内存占用"
Write-Host "  - 记录当前内存占用值"
Write-Host "  - 检查 CPU 占用（应该很低）"
Write-Host ""
Write-Host "性能目标:" -ForegroundColor Yellow
Write-Host "  ✅ 内存占用 ≤ 250MB"
Write-Host "  ✅ CPU 占用 ≤ 10% (空闲状态)"
Write-Host "  ✅ 应用响应时间 < 100ms"
Write-Host ""

Write-Host "按任意键继续到第 4 步..." -ForegroundColor Magenta
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host ""
Write-Host "第 4 步: 测试服务访问" -ForegroundColor Cyan
Write-Host "  - 在浏览器中打开多个标签页"
Write-Host "  - 访问不同服务的 URL (例如前 5 个服务)"
Write-Host "  - 验证所有服务都能正常响应"
Write-Host ""
Write-Host "测试 URL 示例:" -ForegroundColor Yellow
for ($i = 8888; $i -le 8892; $i++) {
    Write-Host "  http://localhost:$i/" -ForegroundColor Gray
}
Write-Host ""

Write-Host "按任意键继续到第 5 步..." -ForegroundColor Magenta
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host ""
Write-Host "第 5 步: 测试服务停止" -ForegroundColor Cyan
Write-Host "  - 逐个停止所有 15 个服务"
Write-Host "  - 观察停止过程是否流畅"
Write-Host "  - 检查端口是否正确释放"
Write-Host "  - 观察内存是否正确释放"
Write-Host ""
Write-Host "预期结果:" -ForegroundColor Yellow
Write-Host "  ✅ 所有服务都能正常停止"
Write-Host "  ✅ 停止响应时间 < 500ms"
Write-Host "  ✅ 端口正确释放（可以被重新使用）"
Write-Host "  ✅ 内存占用恢复到初始水平"
Write-Host ""

Write-Host "按任意键继续到第 6 步..." -ForegroundColor Magenta
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host ""
Write-Host "第 6 步: 验证端口释放" -ForegroundColor Cyan
Write-Host "  - 检查端口 8888-8902 是否都已释放"
Write-Host ""

Write-Host "正在检查端口状态..." -ForegroundColor Yellow
Write-Host ""

$portsInUse = @()
for ($port = 8888; $port -le 8902; $port++) {
    try {
        $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Any, $port)
        $listener.Start()
        $listener.Stop()
        Write-Host "  端口 $port : ✅ 已释放" -ForegroundColor Green
    } catch {
        Write-Host "  端口 $port : ❌ 仍被占用" -ForegroundColor Red
        $portsInUse += $port
    }
}

Write-Host ""
if ($portsInUse.Count -eq 0) {
    Write-Host "✅ 所有端口都已正确释放" -ForegroundColor Green
} else {
    Write-Host "⚠️  以下端口仍被占用: $($portsInUse -join ', ')" -ForegroundColor Yellow
    Write-Host "这可能表示服务未正确停止或存在资源泄漏" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== 测试总结 ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "请在测试报告中记录以下信息:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. 成功启动的服务数量: ___ / 15" -ForegroundColor Gray
Write-Host "2. 初始内存占用: ___ MB" -ForegroundColor Gray
Write-Host "3. 运行 15 个服务时的内存占用: ___ MB" -ForegroundColor Gray
Write-Host "4. CPU 占用: ___ %" -ForegroundColor Gray
Write-Host "5. 是否所有服务都能正常访问: [ ] 是 [ ] 否" -ForegroundColor Gray
Write-Host "6. 是否所有服务都能正常停止: [ ] 是 [ ] 否" -ForegroundColor Gray
Write-Host "7. 是否所有端口都正确释放: [ ] 是 [ ] 否" -ForegroundColor Gray
Write-Host "8. 是否出现崩溃或错误: [ ] 是 [ ] 否" -ForegroundColor Gray
Write-Host "9. 应用响应是否流畅: [ ] 是 [ ] 否" -ForegroundColor Gray
Write-Host ""
Write-Host "发现的问题:" -ForegroundColor Red
Write-Host "  - _______________" -ForegroundColor Gray
Write-Host "  - _______________" -ForegroundColor Gray
Write-Host ""
Write-Host "测试结论: [ ] 通过 [ ] 失败" -ForegroundColor Magenta
Write-Host ""
Write-Host "测试完成！请将结果记录到 TASK_10.3_BOUNDARY_TEST_REPORT.md" -ForegroundColor Cyan
