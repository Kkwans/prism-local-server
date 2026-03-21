# 边界测试 PowerShell 主脚本
# 用于运行所有自动化边界测试

param(
    [switch]$All,
    [switch]$Port,
    [switch]$NoHtml,
    [switch]$NoPermission,
    [switch]$Multiple,
    [switch]$Help
)

function Show-Header {
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  Prism Local Server 边界测试套件" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
}

function Show-Help {
    Show-Header
    Write-Host "用法: .\run_boundary_tests.ps1 [选项]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "选项:" -ForegroundColor Green
    Write-Host "  -All            运行所有测试" -ForegroundColor Gray
    Write-Host "  -Port           运行端口占用测试" -ForegroundColor Gray
    Write-Host "  -NoHtml         运行无 HTML 文件测试" -ForegroundColor Gray
    Write-Host "  -NoPermission   运行无权限目录测试 (需要管理员权限)" -ForegroundColor Gray
    Write-Host "  -Multiple       运行多服务并发测试" -ForegroundColor Gray
    Write-Host "  -Help           显示此帮助信息" -ForegroundColor Gray
    Write-Host ""
    Write-Host "示例:" -ForegroundColor Cyan
    Write-Host "  .\run_boundary_tests.ps1 -All" -ForegroundColor Gray
    Write-Host "  .\run_boundary_tests.ps1 -Port" -ForegroundColor Gray
    Write-Host "  .\run_boundary_tests.ps1 -NoHtml -Multiple" -ForegroundColor Gray
    Write-Host ""
}

function Show-Menu {
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  选择要运行的测试" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  1. 端口占用测试" -ForegroundColor Yellow
    Write-Host "  2. 无 HTML 文件测试" -ForegroundColor Yellow
    Write-Host "  3. 无权限目录测试 (需要管理员权限)" -ForegroundColor Yellow
    Write-Host "  4. 多服务并发测试" -ForegroundColor Yellow
    Write-Host "  5. 运行所有测试" -ForegroundColor Green
    Write-Host "  0. 退出" -ForegroundColor Red
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
}

function Run-PortTest {
    Write-Host ""
    Write-Host "[测试 1/4] 端口占用测试" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Gray
    & "$PSScriptRoot\boundary_test_port_occupied.ps1"
}

function Run-NoHtmlTest {
    Write-Host ""
    Write-Host "[测试 2/4] 无 HTML 文件测试" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Gray
    & "$PSScriptRoot\boundary_test_no_html.ps1"
}

function Run-NoPermissionTest {
    Write-Host ""
    Write-Host "[测试 3/4] 无权限目录测试" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Gray
    Write-Host "注意: 此测试需要管理员权限" -ForegroundColor Yellow
    & "$PSScriptRoot\boundary_test_no_permission.ps1"
}

function Run-MultipleTest {
    Write-Host ""
    Write-Host "[测试 4/4] 多服务并发测试" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Gray
    & "$PSScriptRoot\boundary_test_multiple_services.ps1"
}

function Run-AllTests {
    Write-Host ""
    Write-Host "运行所有边界测试..." -ForegroundColor Green
    Write-Host ""
    
    Run-PortTest
    Write-Host ""
    Write-Host "按任意键继续下一个测试..." -ForegroundColor Magenta
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    
    Run-NoHtmlTest
    Write-Host ""
    Write-Host "按任意键继续下一个测试..." -ForegroundColor Magenta
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    
    Run-NoPermissionTest
    Write-Host ""
    Write-Host "按任意键继续下一个测试..." -ForegroundColor Magenta
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    
    Run-MultipleTest
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  所有测试完成!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
}

# 主逻辑
Show-Header

if ($Help) {
    Show-Help
    exit 0
}

if ($All) {
    Run-AllTests
    exit 0
}

if ($Port) {
    Run-PortTest
}

if ($NoHtml) {
    Run-NoHtmlTest
}

if ($NoPermission) {
    Run-NoPermissionTest
}

if ($Multiple) {
    Run-MultipleTest
}

# 如果没有指定任何参数，显示交互式菜单
if (-not ($All -or $Port -or $NoHtml -or $NoPermission -or $Multiple)) {
    Write-Host "此脚本将运行边界测试" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "注意事项:" -ForegroundColor Cyan
    Write-Host "  - 某些测试需要管理员权限" -ForegroundColor Gray
    Write-Host "  - 测试过程中请勿关闭应用" -ForegroundColor Gray
    Write-Host "  - 请在测试报告中记录结果" -ForegroundColor Gray
    Write-Host ""
    Write-Host "按任意键继续..." -ForegroundColor Magenta
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    
    while ($true) {
        Clear-Host
        Show-Header
        Show-Menu
        
        $choice = Read-Host "请输入选项 (0-5)"
        
        switch ($choice) {
            "1" { Run-PortTest }
            "2" { Run-NoHtmlTest }
            "3" { Run-NoPermissionTest }
            "4" { Run-MultipleTest }
            "5" { Run-AllTests; break }
            "0" { 
                Write-Host ""
                Write-Host "测试结束" -ForegroundColor Green
                Write-Host "请查看测试报告: TASK_10.3_BOUNDARY_TEST_REPORT.md" -ForegroundColor Cyan
                Write-Host ""
                exit 0
            }
            default {
                Write-Host ""
                Write-Host "无效选项，请重新选择" -ForegroundColor Red
                Start-Sleep -Seconds 2
            }
        }
        
        if ($choice -ne "5") {
            Write-Host ""
            Write-Host "按任意键返回菜单..." -ForegroundColor Magenta
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
    }
}

Write-Host ""
Write-Host "测试完成，请查看测试报告: TASK_10.3_BOUNDARY_TEST_REPORT.md" -ForegroundColor Cyan
Write-Host ""
