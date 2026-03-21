# 边界测试：无权限目录测试脚本
# 功能：创建无读取权限的测试目录
# 注意：需要管理员权限运行

Write-Host "=== 无权限目录边界测试 ===" -ForegroundColor Cyan
Write-Host ""

# 检查是否以管理员身份运行
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "❌ 错误: 此脚本需要管理员权限运行" -ForegroundColor Red
    Write-Host ""
    Write-Host "请右键点击 PowerShell 并选择'以管理员身份运行'" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "按任意键退出..." -ForegroundColor Cyan
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# 定义测试目录路径
$testDir = Join-Path $PSScriptRoot "test_resources\no_permission_test"

# 清理旧的测试目录
if (Test-Path $testDir) {
    Write-Host "清理旧的测试目录..." -ForegroundColor Yellow
    try {
        # 先恢复权限再删除
        $acl = Get-Acl $testDir
        $currentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
        $accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule(
            $currentUser,
            "FullControl",
            "Allow"
        )
        $acl.SetAccessRule($accessRule)
        Set-Acl -Path $testDir -AclObject $acl
        Remove-Item -Path $testDir -Recurse -Force
    } catch {
        Write-Host "清理失败: $_" -ForegroundColor Red
    }
}

# 创建测试目录
Write-Host "创建测试目录: $testDir" -ForegroundColor Green
New-Item -Path $testDir -ItemType Directory | Out-Null

# 创建测试文件
Write-Host "创建测试文件..." -ForegroundColor Yellow
$htmlContent = @"
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>无权限测试</title>
</head>
<body>
    <h1>这是一个测试页面</h1>
    <p>此目录将被设置为无读取权限</p>
</body>
</html>
"@
$htmlContent | Out-File -FilePath "$testDir\index.html" -Encoding UTF8

"body { background: red; }" | Out-File -FilePath "$testDir\style.css" -Encoding UTF8

Write-Host ""
Write-Host "✅ 测试目录和文件创建完成" -ForegroundColor Green
Write-Host ""

# 移除当前用户的读取权限
Write-Host "正在移除读取权限..." -ForegroundColor Yellow
try {
    $acl = Get-Acl $testDir
    $currentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
    
    # 禁用继承
    $acl.SetAccessRuleProtection($true, $false)
    
    # 移除所有现有规则
    $acl.Access | ForEach-Object { $acl.RemoveAccessRule($_) | Out-Null }
    
    # 添加拒绝读取的规则
    $denyRule = New-Object System.Security.AccessControl.FileSystemAccessRule(
        $currentUser,
        "Read",
        "ContainerInherit,ObjectInherit",
        "None",
        "Deny"
    )
    $acl.AddAccessRule($denyRule)
    
    # 应用权限
    Set-Acl -Path $testDir -AclObject $acl
    
    Write-Host "✅ 已移除读取权限" -ForegroundColor Green
    Write-Host ""
    Write-Host "目录路径: $testDir" -ForegroundColor Cyan
    Write-Host "当前用户: $currentUser" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "测试步骤:" -ForegroundColor Yellow
    Write-Host "1. 启动 Prism Local Server 应用"
    Write-Host "2. 尝试选择此目录作为部署目录"
    Write-Host "3. 或者手动输入路径: $testDir"
    Write-Host "4. 尝试启动服务"
    Write-Host "5. 观察应用的错误提示和行为"
    Write-Host ""
    Write-Host "预期结果:" -ForegroundColor Cyan
    Write-Host "- 应用检测到目录无读取权限"
    Write-Host "- 显示友好的错误提示: '无法访问目录：权限不足'"
    Write-Host "- 阻止服务启动"
    Write-Host "- 应用不崩溃"
    Write-Host ""
    Write-Host "测试完成后，按任意键恢复权限..." -ForegroundColor Magenta
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    
    # 恢复权限
    Write-Host ""
    Write-Host "正在恢复权限..." -ForegroundColor Yellow
    
    $acl = Get-Acl $testDir
    
    # 移除拒绝规则
    $acl.Access | Where-Object { $_.AccessControlType -eq "Deny" } | ForEach-Object {
        $acl.RemoveAccessRule($_) | Out-Null
    }
    
    # 启用继承
    $acl.SetAccessRuleProtection($false, $true)
    
    # 添加完全控制权限
    $allowRule = New-Object System.Security.AccessControl.FileSystemAccessRule(
        $currentUser,
        "FullControl",
        "ContainerInherit,ObjectInherit",
        "None",
        "Allow"
    )
    $acl.AddAccessRule($allowRule)
    
    Set-Acl -Path $testDir -AclObject $acl
    
    Write-Host "✅ 权限已恢复" -ForegroundColor Green
    
    # 询问是否清理
    Write-Host ""
    Write-Host "是否清理测试目录? (Y/N)" -ForegroundColor Yellow
    $response = Read-Host
    if ($response -eq "Y" -or $response -eq "y") {
        Remove-Item -Path $testDir -Recurse -Force
        Write-Host "✅ 测试目录已清理" -ForegroundColor Green
    } else {
        Write-Host "测试目录保留: $testDir" -ForegroundColor Cyan
    }
    
} catch {
    Write-Host "❌ 设置权限失败: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "可能的原因:" -ForegroundColor Yellow
    Write-Host "- 需要管理员权限"
    Write-Host "- 文件系统不支持 NTFS 权限"
    Write-Host "- 目录被其他程序占用"
}

Write-Host ""
Write-Host "请在测试报告中记录测试结果" -ForegroundColor Cyan
