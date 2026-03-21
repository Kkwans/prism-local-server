# 边界测试：无 HTML 文件测试脚本
# 功能：创建不包含 HTML 文件的测试目录

Write-Host "=== 无 HTML 文件边界测试 ===" -ForegroundColor Cyan
Write-Host ""

# 定义测试目录路径
$testDir = Join-Path $PSScriptRoot "test_resources\no_html_test"

# 清理旧的测试目录
if (Test-Path $testDir) {
    Write-Host "清理旧的测试目录..." -ForegroundColor Yellow
    Remove-Item -Path $testDir -Recurse -Force
}

# 创建测试目录
Write-Host "创建测试目录: $testDir" -ForegroundColor Green
New-Item -Path $testDir -ItemType Directory | Out-Null

# 创建各种非 HTML 文件
Write-Host "创建测试文件..." -ForegroundColor Yellow

# CSS 文件
$cssContent = @"
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}
"@
$cssContent | Out-File -FilePath "$testDir\style.css" -Encoding UTF8

# JavaScript 文件
$jsContent = @"
console.log('这是一个测试 JavaScript 文件');
console.log('目录中没有 HTML 文件');
"@
$jsContent | Out-File -FilePath "$testDir\script.js" -Encoding UTF8

# 文本文件
$txtContent = @"
这是一个测试目录
目录中不包含任何 HTML 文件
用于测试应用的错误处理机制
"@
$txtContent | Out-File -FilePath "$testDir\readme.txt" -Encoding UTF8

# JSON 文件
$jsonContent = @"
{
  "name": "no-html-test",
  "description": "测试目录，不包含 HTML 文件",
  "files": ["style.css", "script.js", "readme.txt"]
}
"@
$jsonContent | Out-File -FilePath "$testDir\config.json" -Encoding UTF8

# 创建子目录和文件
$subDir = Join-Path $testDir "assets"
New-Item -Path $subDir -ItemType Directory | Out-Null
"/* 子目录中的 CSS 文件 */" | Out-File -FilePath "$subDir\sub.css" -Encoding UTF8

Write-Host ""
Write-Host "✅ 测试目录创建完成" -ForegroundColor Green
Write-Host ""
Write-Host "目录路径: $testDir" -ForegroundColor Cyan
Write-Host ""
Write-Host "目录中包含以下文件:" -ForegroundColor Yellow
Get-ChildItem -Path $testDir -Recurse | ForEach-Object {
    $relativePath = $_.FullName.Replace($testDir, "").TrimStart("\")
    if ($_.PSIsContainer) {
        Write-Host "  📁 $relativePath" -ForegroundColor Blue
    } else {
        Write-Host "  📄 $relativePath" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "测试步骤:" -ForegroundColor Cyan
Write-Host "1. 启动 Prism Local Server 应用"
Write-Host "2. 选择此目录作为部署目录: $testDir"
Write-Host "3. 尝试启动服务"
Write-Host "4. 观察应用的警告提示和行为"
Write-Host ""
Write-Host "预期结果:" -ForegroundColor Yellow
Write-Host "- 应用检测到目录中没有 HTML 文件"
Write-Host "- 显示警告提示（但不阻止服务启动）"
Write-Host "- 服务仍然可以启动（允许访问其他资源）"
Write-Host "- 应用不崩溃"
Write-Host ""
Write-Host "测试完成后，可以尝试访问:" -ForegroundColor Magenta
Write-Host "  http://localhost:8888/style.css"
Write-Host "  http://localhost:8888/script.js"
Write-Host "  http://localhost:8888/readme.txt"
Write-Host ""
Write-Host "按任意键清理测试目录..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# 清理测试目录
Write-Host ""
Write-Host "是否清理测试目录? (Y/N)" -ForegroundColor Yellow
$response = Read-Host
if ($response -eq "Y" -or $response -eq "y") {
    Remove-Item -Path $testDir -Recurse -Force
    Write-Host "✅ 测试目录已清理" -ForegroundColor Green
} else {
    Write-Host "测试目录保留: $testDir" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "请在测试报告中记录测试结果" -ForegroundColor Cyan
