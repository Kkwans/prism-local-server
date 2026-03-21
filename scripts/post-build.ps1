# 构建后脚本 - 复制 EXE 到根目录

$ErrorActionPreference = "Stop"

# 获取版本号
$cargoToml = Get-Content "backend/Cargo.toml" -Raw
if ($cargoToml -match 'version\s*=\s*"([^"]+)"') {
    $version = $matches[1]
} else {
    $version = "unknown"
}

# 源文件路径
$sourceExe = "backend/target/release/prism-local-server-tauri.exe"

# 目标文件路径
$targetExe = "prism-local-server-v$version.exe"

# 检查源文件是否存在
if (Test-Path $sourceExe) {
    Write-Host "正在复制 EXE 文件到根目录..." -ForegroundColor Green
    Copy-Item -Path $sourceExe -Destination $targetExe -Force
    Write-Host "✓ 已复制到: $targetExe" -ForegroundColor Green
    
    # 显示文件大小
    $fileSize = (Get-Item $targetExe).Length / 1MB
    Write-Host "文件大小: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Cyan
} else {
    Write-Host "错误: 找不到构建的 EXE 文件" -ForegroundColor Red
    Write-Host "路径: $sourceExe" -ForegroundColor Yellow
    exit 1
}
