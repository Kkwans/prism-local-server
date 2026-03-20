# Prism Local Server 功能测试辅助脚本
# 用途：帮助测试人员快速准备测试环境和执行测试

param(
    [switch]$PrepareOnly,
    [switch]$CheckOnly
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Prism Local Server 功能测试助手" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查 EXE 文件是否存在
$exePath = Join-Path $PSScriptRoot "..\prism-local-server-v3.0.0.exe"
if (-not (Test-Path $exePath)) {
    Write-Host "❌ 错误: 未找到 EXE 文件" -ForegroundColor Red
    Write-Host "   路径: $exePath" -ForegroundColor Yellow
    Write-Host "   请先运行 'npm run tauri:build' 构建应用" -ForegroundColor Yellow
    exit 1
}
Write-Host "✅ 找到 EXE 文件: $exePath" -ForegroundColor Green

# 检查测试资源
$testResourcesPath = Join-Path $PSScriptRoot "test_resources"
Write-Host ""
Write-Host "检查测试资源..." -ForegroundColor Cyan

$requiredFiles = @(
    "index.html",
    "css\style.css",
    "js\script.js"
)

$missingFiles = @()
foreach ($file in $requiredFiles) {
    $filePath = Join-Path $testResourcesPath $file
    if (Test-Path $filePath) {
        Write-Host "  ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file (缺失)" -ForegroundColor Red
        $missingFiles += $file
    }
}

# 检查可选资源（需要手动添加）
Write-Host ""
Write-Host "检查可选测试资源（需要手动添加）..." -ForegroundColor Cyan

$optionalFiles = @(
    @{Path="images\test-image.png"; Description="普通测试图片"},
    @{Path="images\中文文件名图片.png"; Description="中文文件名测试"},
    @{Path="videos\test-video.mp4"; Description="视频 Range Request 测试"}
)

$missingOptional = @()
foreach ($file in $optionalFiles) {
    $filePath = Join-Path $testResourcesPath $file.Path
    if (Test-Path $filePath) {
        $size = (Get-Item $filePath).Length / 1MB
        Write-Host "  ✅ $($file.Path) ($([math]::Round($size, 2)) MB)" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  $($file.Path) (缺失) - $($file.Description)" -ForegroundColor Yellow
        $missingOptional += $file
    }
}

if ($CheckOnly) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "检查完成" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    exit 0
}

# 如果有缺失的必需文件，退出
if ($missingFiles.Count -gt 0) {
    Write-Host ""
    Write-Host "❌ 错误: 缺少必需的测试文件" -ForegroundColor Red
    Write-Host "   请确保已创建所有测试资源文件" -ForegroundColor Yellow
    exit 1
}

# 提示用户添加可选资源
if ($missingOptional.Count -gt 0) {
    Write-Host ""
    Write-Host "⚠️  警告: 缺少以下可选测试资源" -ForegroundColor Yellow
    foreach ($file in $missingOptional) {
        Write-Host "   - $($file.Path): $($file.Description)" -ForegroundColor Yellow
    }
    Write-Host ""
    Write-Host "   这些资源对于完整测试是必需的。" -ForegroundColor Yellow
    Write-Host "   请参考 test_resources/images/README.md 和 test_resources/videos/README.md" -ForegroundColor Yellow
    Write-Host ""
    
    $continue = Read-Host "是否继续测试？(y/n)"
    if ($continue -ne "y") {
        Write-Host "测试已取消" -ForegroundColor Yellow
        exit 0
    }
}

if ($PrepareOnly) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "准备完成" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    exit 0
}

# 检查端口占用情况
Write-Host ""
Write-Host "检查端口占用情况..." -ForegroundColor Cyan

$portsToCheck = 8888..8892
$occupiedPorts = @()

foreach ($port in $portsToCheck) {
    $connection = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    if ($connection) {
        Write-Host "  ⚠️  端口 $port 被占用 (PID: $($connection.OwningProcess))" -ForegroundColor Yellow
        $occupiedPorts += $port
    } else {
        Write-Host "  ✅ 端口 $port 可用" -ForegroundColor Green
    }
}

if ($occupiedPorts.Count -gt 0) {
    Write-Host ""
    Write-Host "⚠️  警告: 以下端口被占用" -ForegroundColor Yellow
    foreach ($port in $occupiedPorts) {
        Write-Host "   - 端口 $port" -ForegroundColor Yellow
    }
    Write-Host ""
    Write-Host "   这可能影响端口自动递增测试。" -ForegroundColor Yellow
    Write-Host "   建议关闭占用这些端口的程序。" -ForegroundColor Yellow
    Write-Host ""
}

# 获取本机 IP 地址
Write-Host ""
Write-Host "获取本机 IP 地址..." -ForegroundColor Cyan

$ipAddresses = Get-NetIPAddress -AddressFamily IPv4 | 
    Where-Object { $_.IPAddress -notlike "127.*" -and $_.IPAddress -notlike "169.254.*" } |
    Select-Object -ExpandProperty IPAddress

if ($ipAddresses.Count -gt 0) {
    Write-Host "  本机 IP 地址:" -ForegroundColor Green
    foreach ($ip in $ipAddresses) {
        Write-Host "    - $ip" -ForegroundColor Green
    }
    Write-Host ""
    Write-Host "  局域网访问测试时，请使用以上 IP 地址" -ForegroundColor Cyan
} else {
    Write-Host "  ⚠️  未找到有效的局域网 IP 地址" -ForegroundColor Yellow
}

# 启动应用
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "准备启动应用进行测试" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "测试资源目录: $testResourcesPath" -ForegroundColor Cyan
Write-Host "测试报告模板: tests\TASK_10.1_FUNCTIONAL_TEST_REPORT.md" -ForegroundColor Cyan
Write-Host ""

$startApp = Read-Host "是否启动应用？(y/n)"
if ($startApp -eq "y") {
    Write-Host ""
    Write-Host "正在启动应用..." -ForegroundColor Green
    Start-Process $exePath
    
    Write-Host ""
    Write-Host "✅ 应用已启动" -ForegroundColor Green
    Write-Host ""
    Write-Host "请按照测试报告模板执行测试：" -ForegroundColor Cyan
    Write-Host "  tests\TASK_10.1_FUNCTIONAL_TEST_REPORT.md" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "测试步骤：" -ForegroundColor Cyan
    Write-Host "  1. 在应用中点击'启动服务'" -ForegroundColor White
    Write-Host "  2. 选择测试资源目录: $testResourcesPath" -ForegroundColor White
    Write-Host "  3. 在浏览器中访问: http://localhost:8888/index.html" -ForegroundColor White
    Write-Host "  4. 按照测试报告逐项测试" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "测试已取消" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "您可以手动启动应用进行测试：" -ForegroundColor Cyan
    Write-Host "  $exePath" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "测试助手运行完成" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
