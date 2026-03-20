# Prism Local Server - Release 构建脚本
# 用途：构建所有平台的发布版本并整理到 release 文件夹

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Prism Local Server v3.0.0 构建脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. 清理旧的构建产物
Write-Host "[1/5] 清理旧的构建产物..." -ForegroundColor Yellow
if (Test-Path "release") {
    Remove-Item -Path "release" -Recurse -Force
}
New-Item -ItemType Directory -Path "release" -Force | Out-Null

# 2. 构建前端
Write-Host "[2/5] 构建前端代码..." -ForegroundColor Yellow
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "前端构建失败！" -ForegroundColor Red
    exit 1
}

# 3. 构建 Windows 版本
Write-Host "[3/5] 构建 Windows 版本..." -ForegroundColor Yellow
Set-Location backend
cargo tauri build
if ($LASTEXITCODE -ne 0) {
    Write-Host "Windows 构建失败！" -ForegroundColor Red
    Set-Location ..
    exit 1
}
Set-Location ..

# 4. 复制 Windows 打包文件到 release 文件夹
Write-Host "[4/5] 整理打包文件..." -ForegroundColor Yellow

# 复制主 EXE
Copy-Item "backend\target\release\prism-local-server-tauri.exe" "release\Prism-Local-Server-v3.0.0.exe" -Force

# 复制 MSI 安装包
$msiPath = Get-ChildItem "backend\target\release\bundle\msi\*.msi" | Select-Object -First 1
if ($msiPath) {
    Copy-Item $msiPath.FullName "release\" -Force
    Write-Host "  ✓ MSI 安装包已复制" -ForegroundColor Green
}

# 复制 NSIS 安装包
$nsisPath = Get-ChildItem "backend\target\release\bundle\nsis\*-setup.exe" | Select-Object -First 1
if ($nsisPath) {
    Copy-Item $nsisPath.FullName "release\" -Force
    Write-Host "  ✓ NSIS 安装包已复制" -ForegroundColor Green
}

# 5. 显示构建结果
Write-Host "[5/5] 构建完成！" -ForegroundColor Green
Write-Host ""
Write-Host "打包文件列表：" -ForegroundColor Cyan
Get-ChildItem -Path "release" | ForEach-Object {
    $sizeMB = [math]::Round($_.Length / 1MB, 2)
    Write-Host "  - $($_.Name) ($sizeMB MB)" -ForegroundColor White
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  构建成功！文件位于 release 文件夹" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# 复制 NSIS 安装包
$nsisPath = Get-ChildItem "backend\target\release\bundle\nsis\*-setup.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
if ($nsisPath) {
    Copy-Item $nsisPath.FullName "release\" -Force
    Write-Host "  ✓ NSIS 安装包已复制" -ForegroundColor Green
}

# 5. 显示构建结果
Write-Host "[5/5] 构建完成！" -ForegroundColor Green
Write-Host ""
Write-Host "打包文件列表：" -ForegroundColor Cyan
Get-ChildItem -Path "release" | ForEach-Object {
    $sizeMB = [math]::Round($_.Length / 1MB, 2)
    Write-Host "  - $($_.Name) ($sizeMB MB)" -ForegroundColor White
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  所有文件已整理到 release 文件夹" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "提示：" -ForegroundColor Yellow
Write-Host "  - Windows 用户可以使用 .exe 或安装包" -ForegroundColor White
Write-Host "  - Linux/macOS 版本需要在对应系统上构建" -ForegroundColor White
Write-Host "  - 使用 'cargo tauri build' 在目标平台构建" -ForegroundColor White
