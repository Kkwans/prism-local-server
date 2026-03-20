# 任务 10.3 边界测试指南

## 📋 测试概述

边界测试旨在验证应用在各种异常和极端情况下的表现，确保错误处理和容错机制正常工作。

**测试目标**:
- 验证应用在异常情况下的稳定性
- 验证错误提示是否友好清晰
- 验证应用是否能优雅降级
- 发现潜在的崩溃和内存泄漏问题

---

## 🧪 测试用例列表

### 测试 1: 端口被占用的情况

**测试场景**: 所有可用端口都被占用

**测试步骤**:
1. 使用脚本占用端口 8888-8900（共 13 个端口）
2. 启动 Prism Local Server
3. 尝试启动服务
4. 观察应用的行为和错误提示

**预期结果**:
- ✅ 应用检测到端口范围内所有端口都被占用
- ✅ 显示友好的错误提示："无法找到可用端口（8888-8900 已被占用），请释放端口后重试"
- ✅ 应用不崩溃，可以继续操作
- ✅ 日志文件记录详细的端口检测信息

**测试脚本**: `boundary_test_port_occupied.ps1`

---

### 测试 2: 目录不存在的情况

**测试场景**: 用户指定的部署目录不存在

**测试步骤**:
1. 启动应用
2. 在设置中指定一个不存在的目录路径（如 `C:\NonExistentDirectory\`）
3. 尝试启动服务
4. 观察应用的行为和错误提示

**预期结果**:
- ✅ 应用检测到目录不存在
- ✅ 显示友好的错误提示："部署目录不存在：C:\NonExistentDirectory\"
- ✅ 阻止服务启动
- ✅ 应用不崩溃，可以继续操作
- ✅ 日志文件记录错误信息

**测试脚本**: 手动测试

---

### 测试 3: 无 HTML 文件的情况

**测试场景**: 部署目录中没有任何 HTML 文件

**测试步骤**:
1. 创建一个空目录或只包含非 HTML 文件的目录
2. 启动应用，选择该目录作为部署目录
3. 尝试启动服务
4. 观察应用的行为和错误提示

**预期结果**:
- ✅ 应用检测到目录中没有 HTML 文件
- ✅ 显示警告提示："部署目录中未找到 HTML 文件，服务已启动但可能无法正常访问"
- ✅ 服务仍然启动（允许用户访问其他资源）
- ✅ 应用不崩溃，可以继续操作

**测试脚本**: `boundary_test_no_html.ps1`

---

### 测试 4: 无权限目录的情况

**测试场景**: 用户指定的目录没有读取权限

**测试步骤**:
1. 创建一个测试目录
2. 使用 Windows 权限设置移除当前用户的读取权限
3. 启动应用，选择该目录作为部署目录
4. 尝试启动服务
5. 观察应用的行为和错误提示

**预期结果**:
- ✅ 应用检测到目录无读取权限
- ✅ 显示友好的错误提示："无法访问目录：权限不足"
- ✅ 阻止服务启动
- ✅ 应用不崩溃，可以继续操作
- ✅ 日志文件记录权限错误信息

**测试脚本**: `boundary_test_no_permission.ps1`

---

### 测试 5: 网络断开的情况

**测试场景**: 在服务运行时断开网络连接

**测试步骤**:
1. 启动应用并启动一个服务
2. 在浏览器中访问服务 URL，确认正常工作
3. 禁用网络适配器（或拔掉网线）
4. 刷新浏览器页面
5. 重新启用网络适配器
6. 再次刷新浏览器页面
7. 观察应用的行为

**预期结果**:
- ✅ 网络断开时，localhost 访问仍然正常（本地回环不受影响）
- ✅ 局域网访问失败（符合预期）
- ✅ 网络恢复后，局域网访问恢复正常
- ✅ 应用不崩溃，服务继续运行
- ✅ 服务卡片显示的 IP 地址自动更新（如果有变化）

**测试脚本**: 手动测试

---

### 测试 6: 同时启动 10+ 个服务

**测试场景**: 测试应用的并发处理能力

**测试步骤**:
1. 启动应用
2. 连续快速启动 15 个服务实例
3. 观察应用的响应和性能
4. 检查任务管理器中的资源占用
5. 在浏览器中访问所有服务的 URL
6. 逐个停止所有服务

**预期结果**:
- ✅ 所有 15 个服务都成功启动
- ✅ 端口号正确分配（8888-8902）
- ✅ 应用界面保持响应，无卡顿
- ✅ 内存占用 ≤ 250MB
- ✅ CPU 占用 ≤ 10%（空闲状态）
- ✅ 所有服务的 URL 都可以正常访问
- ✅ 停止服务时端口正确释放
- ✅ 应用不崩溃，无内存泄漏

**测试脚本**: `boundary_test_multiple_services.ps1`

---

### 测试 7: 超大文件（>1GB）的加载

**测试场景**: 测试服务处理超大文件的能力

**测试步骤**:
1. 准备一个 >1GB 的视频文件（如 1.5GB 的 MP4 文件）
2. 将文件放入测试目录
3. 启动服务，部署该目录
4. 在浏览器中访问该视频文件
5. 测试视频播放和拖拽功能
6. 观察内存占用和响应时间

**预期结果**:
- ✅ 服务能正确处理超大文件请求
- ✅ 视频能正常播放（不需要完全加载）
- ✅ Range Request 正常工作，支持拖拽播放
- ✅ 内存占用不会随文件大小线性增长（使用流式传输）
- ✅ 首帧加载时间 ≤ 200ms（允许大文件有更长的加载时间）
- ✅ 应用不崩溃，不出现内存溢出

**测试脚本**: 手动测试（需要准备大文件）

---

## 🛠️ 测试工具和脚本

### PowerShell 测试脚本

#### 1. 端口占用测试脚本

文件: `boundary_test_port_occupied.ps1`

```powershell
# 占用端口 8888-8900
$ports = 8888..8900
$jobs = @()

Write-Host "正在占用端口 8888-8900..." -ForegroundColor Yellow

foreach ($port in $ports) {
    $job = Start-Job -ScriptBlock {
        param($p)
        $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Any, $p)
        $listener.Start()
        Write-Host "端口 $p 已占用"
        Start-Sleep -Seconds 300  # 保持 5 分钟
        $listener.Stop()
    } -ArgumentList $port
    $jobs += $job
}

Write-Host "所有端口已占用，请在 5 分钟内完成测试" -ForegroundColor Green
Write-Host "按任意键停止占用端口..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# 停止所有任务
$jobs | Stop-Job
$jobs | Remove-Job

Write-Host "所有端口已释放" -ForegroundColor Green
```

#### 2. 无 HTML 文件测试脚本

文件: `boundary_test_no_html.ps1`

```powershell
# 创建无 HTML 文件的测试目录
$testDir = ".\test_resources\no_html_test"

if (Test-Path $testDir) {
    Remove-Item -Path $testDir -Recurse -Force
}

New-Item -Path $testDir -ItemType Directory | Out-Null

# 创建一些非 HTML 文件
"body { background: red; }" | Out-File -FilePath "$testDir\style.css" -Encoding UTF8
"console.log('test');" | Out-File -FilePath "$testDir\script.js" -Encoding UTF8
"This is a text file" | Out-File -FilePath "$testDir\readme.txt" -Encoding UTF8

Write-Host "测试目录已创建: $testDir" -ForegroundColor Green
Write-Host "目录中包含以下文件:" -ForegroundColor Cyan
Get-ChildItem -Path $testDir | ForEach-Object { Write-Host "  - $($_.Name)" }
Write-Host ""
Write-Host "请在应用中选择此目录并尝试启动服务" -ForegroundColor Yellow
```

#### 3. 无权限目录测试脚本

文件: `boundary_test_no_permission.ps1`

```powershell
# 创建无权限测试目录
$testDir = ".\test_resources\no_permission_test"

if (Test-Path $testDir) {
    Remove-Item -Path $testDir -Recurse -Force
}

New-Item -Path $testDir -ItemType Directory | Out-Null

# 创建测试文件
"<html><body>Test</body></html>" | Out-File -FilePath "$testDir\index.html" -Encoding UTF8

Write-Host "测试目录已创建: $testDir" -ForegroundColor Green

# 移除当前用户的读取权限
try {
    $acl = Get-Acl $testDir
    $currentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
    $accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule(
        $currentUser,
        "Read",
        "Deny"
    )
    $acl.AddAccessRule($accessRule)
    Set-Acl -Path $testDir -AclObject $acl
    
    Write-Host "已移除读取权限" -ForegroundColor Yellow
    Write-Host "请在应用中选择此目录并尝试启动服务" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "测试完成后，按任意键恢复权限..." -ForegroundColor Magenta
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    
    # 恢复权限
    $acl.RemoveAccessRule($accessRule) | Out-Null
    Set-Acl -Path $testDir -AclObject $acl
    Write-Host "权限已恢复" -ForegroundColor Green
} catch {
    Write-Host "设置权限失败: $_" -ForegroundColor Red
    Write-Host "请以管理员身份运行此脚本" -ForegroundColor Yellow
}
```

#### 4. 多服务并发测试脚本

文件: `boundary_test_multiple_services.ps1`

```powershell
Write-Host "=== 多服务并发测试 ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "此测试将指导您启动 15 个服务实例" -ForegroundColor Yellow
Write-Host ""
Write-Host "测试步骤:" -ForegroundColor Green
Write-Host "1. 确保 Prism Local Server 应用已启动"
Write-Host "2. 连续快速点击 15 次'启动服务'按钮"
Write-Host "3. 观察所有服务是否都成功启动"
Write-Host "4. 检查任务管理器中的内存占用"
Write-Host "5. 在浏览器中访问几个服务的 URL"
Write-Host "6. 逐个停止所有服务"
Write-Host ""
Write-Host "预期结果:" -ForegroundColor Cyan
Write-Host "- 所有 15 个服务都成功启动"
Write-Host "- 端口号: 8888-8902"
Write-Host "- 内存占用 ≤ 250MB"
Write-Host "- 应用界面保持响应"
Write-Host "- 所有 URL 都可以访问"
Write-Host ""
Write-Host "按任意键开始测试..." -ForegroundColor Magenta
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# 打开任务管理器
Start-Process taskmgr

Write-Host ""
Write-Host "任务管理器已打开，请监控内存占用" -ForegroundColor Green
Write-Host "现在请在应用中启动 15 个服务..." -ForegroundColor Yellow
```

---

## 📊 测试报告模板

测试完成后，请填写 `TASK_10.3_BOUNDARY_TEST_REPORT.md` 报告。

---

## ⚠️ 注意事项

### 测试前准备

1. **备份数据**: 边界测试可能导致应用崩溃，请确保重要数据已备份
2. **管理员权限**: 某些测试（如权限测试）需要管理员权限
3. **测试环境**: 建议在测试环境或虚拟机中进行测试
4. **资源准备**: 准备好大文件（>1GB）用于测试

### 测试中注意

1. **观察日志**: 测试过程中注意查看日志文件（`logs/prism-server.log`）
2. **监控资源**: 使用任务管理器监控内存和 CPU 占用
3. **记录截图**: 对于错误提示和异常行为，及时截图记录
4. **详细记录**: 记录每个测试的详细结果和观察

### 测试后清理

1. **停止所有服务**: 确保所有测试服务都已停止
2. **释放端口**: 确保所有占用的端口都已释放
3. **删除测试文件**: 清理测试过程中创建的临时文件和目录
4. **恢复权限**: 恢复测试中修改的文件权限

---

## 🚀 快速开始

### 运行所有自动化测试

```powershell
# 1. 端口占用测试
.\boundary_test_port_occupied.ps1

# 2. 无 HTML 文件测试
.\boundary_test_no_html.ps1

# 3. 无权限目录测试（需要管理员权限）
.\boundary_test_no_permission.ps1

# 4. 多服务并发测试
.\boundary_test_multiple_services.ps1
```

### 手动测试项目

- 测试 2: 目录不存在
- 测试 5: 网络断开
- 测试 7: 超大文件加载

---

## 📞 获取帮助

如果在测试过程中遇到问题：

1. 查看日志文件：`logs/prism-server.log`
2. 查看测试报告模板：`TASK_10.3_BOUNDARY_TEST_REPORT.md`
3. 参考功能测试指南：`TESTING_GUIDE.md`

---

**祝测试顺利！** 🎉
