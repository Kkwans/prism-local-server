# ============================================================================
# Prism Local Server Tauri - 性能测试脚本
# 版本: v1.0.0
# 描述: 自动化性能测试脚本，测试冷启动时间、内存占用、文件响应时间等指标
# ============================================================================

param(
    [string]$ExePath = "..\prism-local-server-v3.0.0.exe",
    [string]$OutputFile = "TASK_10.2_PERFORMANCE_TEST_REPORT.md"
)

# 颜色输出函数
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

# 测试结果存储
$TestResults = @{
    ColdStartTime = @()
    IdleMemory = 0
    MultiServiceMemory = 0
    ExeSize = 0
    UIResponseTime = @{}
    PortCheckTime = 0
    SmallFileResponse = @{}
    VideoFirstFrame = 0
}

Write-ColorOutput "`n========================================" "Cyan"
Write-ColorOutput "  Prism Local Server 性能测试" "Cyan"
Write-ColorOutput "========================================`n" "Cyan"

# ============================================================================
# 测试 1: 检查 EXE 文件是否存在
# ============================================================================
Write-ColorOutput "[测试准备] 检查 EXE 文件..." "Yellow"

if (-not (Test-Path $ExePath)) {
    Write-ColorOutput "❌ 错误: 找不到 EXE 文件: $ExePath" "Red"
    Write-ColorOutput "请先构建 Release 版本: npm run tauri:build" "Red"
    exit 1
}

Write-ColorOutput "✅ EXE 文件存在: $ExePath" "Green"

# ============================================================================
# 测试 2: 测量 EXE 文件体积
# ============================================================================
Write-ColorOutput "`n[测试 1/6] 测量 EXE 文件体积..." "Yellow"

$ExeFile = Get-Item $ExePath
$ExeSizeMB = [math]::Round($ExeFile.Length / 1MB, 2)
$TestResults.ExeSize = $ExeSizeMB

Write-ColorOutput "📦 EXE 文件体积: $ExeSizeMB MB" "Cyan"

if ($ExeSizeMB -le 15) {
    Write-ColorOutput "✅ 达标 (目标 ≤ 15MB)" "Green"
} else {
    Write-ColorOutput "❌ 未达标 (目标 ≤ 15MB)" "Red"
}

# ============================================================================
# 测试 3: 测量冷启动时间
# ============================================================================
Write-ColorOutput "`n[测试 2/6] 测量冷启动时间 (3 次测试)..." "Yellow"

for ($i = 1; $i -le 3; $i++) {
    Write-ColorOutput "  第 $i 次测试..." "Gray"
    
    # 确保应用完全关闭
    Get-Process -Name "prism-local-server-tauri" -ErrorAction SilentlyContinue | Stop-Process -Force
    Start-Sleep -Seconds 2
    
    # 测量启动时间
    $StartTime = Get-Date
    $Process = Start-Process -FilePath $ExePath -PassThru -WindowStyle Normal
    
    # 等待窗口出现（检查进程是否有主窗口句柄）
    $Timeout = 10
    $Elapsed = 0
    while ($Elapsed -lt $Timeout) {
        Start-Sleep -Milliseconds 100
        $Elapsed += 0.1
        
        # 检查进程是否有主窗口
        $Process.Refresh()
        if ($Process.MainWindowHandle -ne 0) {
            break
        }
    }
    
    $EndTime = Get-Date
    $StartupTime = ($EndTime - $StartTime).TotalSeconds
    $TestResults.ColdStartTime += $StartupTime
    
    Write-ColorOutput "    启动时间: $([math]::Round($StartupTime, 2)) 秒" "Cyan"
    
    # 等待应用稳定
    Start-Sleep -Seconds 2
}

$AvgStartupTime = [math]::Round(($TestResults.ColdStartTime | Measure-Object -Average).Average, 2)
Write-ColorOutput "`n⏱️  平均冷启动时间: $AvgStartupTime 秒" "Cyan"

if ($AvgStartupTime -le 1.5) {
    Write-ColorOutput "✅ 达标 (目标 ≤ 1.5 秒)" "Green"
} else {
    Write-ColorOutput "❌ 未达标 (目标 ≤ 1.5 秒)" "Red"
}

# ============================================================================
# 测试 4: 测量空闲状态内存占用
# ============================================================================
Write-ColorOutput "`n[测试 3/6] 测量空闲状态内存占用..." "Yellow"
Write-ColorOutput "  等待 30 秒让应用稳定..." "Gray"

Start-Sleep -Seconds 30

$Process = Get-Process -Name "prism-local-server-tauri" -ErrorAction SilentlyContinue
if ($Process) {
    $IdleMemoryMB = [math]::Round($Process.WorkingSet64 / 1MB, 2)
    $TestResults.IdleMemory = $IdleMemoryMB
    
    Write-ColorOutput "💾 空闲内存占用: $IdleMemoryMB MB" "Cyan"
    
    if ($IdleMemoryMB -le 40) {
        Write-ColorOutput "✅ 达标 (目标 ≤ 40MB)" "Green"
    } else {
        Write-ColorOutput "❌ 未达标 (目标 ≤ 40MB)" "Red"
    }
} else {
    Write-ColorOutput "❌ 错误: 找不到运行中的进程" "Red"
}

# ============================================================================
# 测试 5: 测量运行 5 个服务时的内存占用
# ============================================================================
Write-ColorOutput "`n[测试 4/6] 测量运行 5 个服务时的内存占用..." "Yellow"
Write-ColorOutput "⚠️  此测试需要手动操作:" "Yellow"
Write-ColorOutput "  1. 在应用中启动 5 个服务" "Gray"
Write-ColorOutput "  2. 等待所有服务启动完成" "Gray"
Write-ColorOutput "  3. 按任意键继续测量内存..." "Gray"

$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

$Process = Get-Process -Name "prism-local-server-tauri" -ErrorAction SilentlyContinue
if ($Process) {
    $MultiServiceMemoryMB = [math]::Round($Process.WorkingSet64 / 1MB, 2)
    $TestResults.MultiServiceMemory = $MultiServiceMemoryMB
    
    Write-ColorOutput "💾 运行 5 个服务时内存占用: $MultiServiceMemoryMB MB" "Cyan"
    
    if ($MultiServiceMemoryMB -le 150) {
        Write-ColorOutput "✅ 达标 (目标 ≤ 150MB)" "Green"
    } else {
        Write-ColorOutput "❌ 未达标 (目标 ≤ 150MB)" "Red"
    }
} else {
    Write-ColorOutput "❌ 错误: 找不到运行中的进程" "Red"
}

# ============================================================================
# 测试 6: 测量小文件响应时间
# ============================================================================
Write-ColorOutput "`n[测试 5/6] 测量小文件 HTTP 响应时间..." "Yellow"
Write-ColorOutput "⚠️  此测试需要手动操作:" "Yellow"
Write-ColorOutput "  1. 确保至少有一个服务正在运行" "Gray"
Write-ColorOutput "  2. 记录服务的端口号（例如 8888）" "Gray"
Write-ColorOutput "  3. 按任意键继续..." "Gray"

$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

$Port = Read-Host "请输入服务端口号"

if ($Port) {
    Write-ColorOutput "  测试 index.html 响应时间..." "Gray"
    
    try {
        $StartTime = Get-Date
        $Response = Invoke-WebRequest -Uri "http://localhost:$Port/index.html" -UseBasicParsing -TimeoutSec 5
        $EndTime = Get-Date
        $ResponseTime = ($EndTime - $StartTime).TotalMilliseconds
        
        $TestResults.SmallFileResponse["index.html"] = [math]::Round($ResponseTime, 2)
        Write-ColorOutput "    index.html: $([math]::Round($ResponseTime, 2)) ms" "Cyan"
        
        if ($ResponseTime -le 10) {
            Write-ColorOutput "    ✅ 达标 (目标 ≤ 10ms)" "Green"
        } else {
            Write-ColorOutput "    ❌ 未达标 (目标 ≤ 10ms)" "Red"
        }
    } catch {
        Write-ColorOutput "    ❌ 请求失败: $_" "Red"
    }
} else {
    Write-ColorOutput "❌ 跳过小文件响应时间测试" "Yellow"
}

# ============================================================================
# 测试 7: 测量视频首帧加载时间
# ============================================================================
Write-ColorOutput "`n[测试 6/6] 测量视频首帧加载时间..." "Yellow"
Write-ColorOutput "⚠️  此测试需要手动操作:" "Yellow"
Write-ColorOutput "  1. 在浏览器中打开开发者工具 (F12)" "Gray"
Write-ColorOutput "  2. 切换到 Network 标签" "Gray"
Write-ColorOutput "  3. 访问视频文件 URL (例如 http://localhost:8888/videos/test-video.mp4)" "Gray"
Write-ColorOutput "  4. 查看第一个请求的 TTFB (Time To First Byte)" "Gray"
Write-ColorOutput "  5. 记录 TTFB 时间（毫秒）" "Gray"

$VideoTTFB = Read-Host "`n请输入视频首帧 TTFB 时间（毫秒，输入 0 跳过）"

if ($VideoTTFB -and $VideoTTFB -ne "0") {
    $TestResults.VideoFirstFrame = [int]$VideoTTFB
    Write-ColorOutput "🎬 视频首帧 TTFB: $VideoTTFB ms" "Cyan"
    
    if ([int]$VideoTTFB -le 100) {
        Write-ColorOutput "✅ 达标 (目标 ≤ 100ms)" "Green"
    } else {
        Write-ColorOutput "❌ 未达标 (目标 ≤ 100ms)" "Red"
    }
} else {
    Write-ColorOutput "⚠️  跳过视频首帧测试" "Yellow"
}

# ============================================================================
# 生成测试报告
# ============================================================================
Write-ColorOutput "`n[生成报告] 正在生成测试报告..." "Yellow"

$ReportContent = @"
# 任务 10.2 性能测试报告

## 测试信息

- **测试日期**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
- **测试工具**: PowerShell 自动化脚本
- **应用版本**: v3.0.0
- **操作系统**: $([System.Environment]::OSVersion.VersionString)
- **测试环境**: 
  - CPU: $((Get-WmiObject Win32_Processor).Name)
  - 内存: $([math]::Round((Get-WmiObject Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 2)) GB
  - PowerShell 版本: $($PSVersionTable.PSVersion)

---

## 性能测试结果

### 测试 1: 冷启动时间（目标 ≤ 1.5 秒）

**测试方法**: 使用 PowerShell 脚本自动启动应用并测量时间

**测试结果**:
- 第 1 次启动: $([math]::Round($TestResults.ColdStartTime[0], 2)) 秒
- 第 2 次启动: $([math]::Round($TestResults.ColdStartTime[1], 2)) 秒
- 第 3 次启动: $([math]::Round($TestResults.ColdStartTime[2], 2)) 秒
- **平均时间: $AvgStartupTime 秒**
- **是否达标: $(if ($AvgStartupTime -le 1.5) { "✅ 是" } else { "❌ 否" })**

**分析**: 
$(if ($AvgStartupTime -le 1.5) {
    "冷启动时间符合预期，Tauri 应用启动速度优秀。"
} else {
    "冷启动时间超出目标，建议优化启动流程，减少初始化操作。"
})

---

### 测试 2: 空闲状态内存占用（目标 ≤ 40MB）

**测试方法**: 启动应用后等待 30 秒稳定，使用任务管理器测量内存占用

**测试结果**:
- **空闲内存占用: $($TestResults.IdleMemory) MB**
- **是否达标: $(if ($TestResults.IdleMemory -le 40) { "✅ 是" } else { "❌ 否" })**

**分析**: 
$(if ($TestResults.IdleMemory -le 40) {
    "空闲内存占用符合预期，Tauri 应用内存效率优秀。"
} else {
    "空闲内存占用超出目标，建议检查是否有内存泄漏或不必要的缓存。"
})

---

### 测试 3: 运行 5 个服务时内存占用（目标 ≤ 150MB）

**测试方法**: 启动 5 个服务实例后测量内存占用

**测试结果**:
- **运行 5 个服务时内存占用: $($TestResults.MultiServiceMemory) MB**
- **是否达标: $(if ($TestResults.MultiServiceMemory -le 150) { "✅ 是" } else { "❌ 否" })**

**分析**: 
$(if ($TestResults.MultiServiceMemory -le 150) {
    "多服务内存占用符合预期，Tokio 异步运行时效率优秀。"
} else {
    "多服务内存占用超出目标，建议优化服务管理器的资源使用。"
})

---

### 测试 4: 小文件响应时间（目标 ≤ 10ms）

**测试方法**: 使用 Invoke-WebRequest 测量 HTTP 响应时间

**测试结果**:
$(if ($TestResults.SmallFileResponse.Count -gt 0) {
    "- index.html TTFB: $($TestResults.SmallFileResponse['index.html']) ms`n"
    "- **是否达标: $(if ($TestResults.SmallFileResponse['index.html'] -le 10) { '✅ 是' } else { '❌ 否' })**"
} else {
    "- ⚠️ 未执行测试"
})

**分析**: 
$(if ($TestResults.SmallFileResponse.Count -gt 0) {
    if ($TestResults.SmallFileResponse['index.html'] -le 10) {
        "小文件响应时间符合预期，Axum 服务器性能优秀。"
    } else {
        "小文件响应时间超出目标，建议优化静态文件处理器。"
    }
} else {
    "未执行测试，无法评估。"
})

---

### 测试 5: 大视频首帧加载时间（目标 ≤ 100ms）

**测试方法**: 在浏览器开发者工具中测量视频文件的 TTFB

**测试结果**:
$(if ($TestResults.VideoFirstFrame -gt 0) {
    "- 视频首帧 TTFB: $($TestResults.VideoFirstFrame) ms`n"
    "- **是否达标: $(if ($TestResults.VideoFirstFrame -le 100) { '✅ 是' } else { '❌ 否' })**"
} else {
    "- ⚠️ 未执行测试"
})

**分析**: 
$(if ($TestResults.VideoFirstFrame -gt 0) {
    if ($TestResults.VideoFirstFrame -le 100) {
        "视频首帧加载时间符合预期，Range Request 实现优秀。"
    } else {
        "视频首帧加载时间超出目标，建议优化 Range Request 处理器。"
    }
} else {
    "未执行测试，无法评估。"
})

---

### 测试 6: 打包体积（目标 ≤ 15MB）

**测试方法**: 测量 Release 版本 EXE 文件大小

**测试结果**:
- **EXE 文件体积: $($TestResults.ExeSize) MB**
- **是否达标: $(if ($TestResults.ExeSize -le 15) { "✅ 是" } else { "❌ 否" })**

**分析**: 
$(if ($TestResults.ExeSize -le 15) {
    "打包体积符合预期，Tauri 应用体积优化优秀。"
} else {
    "打包体积超出目标，建议进一步优化 Cargo.toml 的 release profile。"
})

---

## 性能指标汇总

| 测试项目 | 目标值 | 实际值 | 是否达标 |
|---------|--------|--------|---------|
| 冷启动时间 | ≤ 1.5s | $AvgStartupTime s | $(if ($AvgStartupTime -le 1.5) { "✅" } else { "❌" }) |
| 空闲内存 | ≤ 40MB | $($TestResults.IdleMemory) MB | $(if ($TestResults.IdleMemory -le 40) { "✅" } else { "❌" }) |
| 5 服务内存 | ≤ 150MB | $($TestResults.MultiServiceMemory) MB | $(if ($TestResults.MultiServiceMemory -le 150) { "✅" } else { "❌" }) |
| EXE 体积 | ≤ 15MB | $($TestResults.ExeSize) MB | $(if ($TestResults.ExeSize -le 15) { "✅" } else { "❌" }) |
| 小文件响应 | ≤ 10ms | $(if ($TestResults.SmallFileResponse.Count -gt 0) { "$($TestResults.SmallFileResponse['index.html']) ms" } else { "未测试" }) | $(if ($TestResults.SmallFileResponse.Count -gt 0 -and $TestResults.SmallFileResponse['index.html'] -le 10) { "✅" } elseif ($TestResults.SmallFileResponse.Count -gt 0) { "❌" } else { "⚠️" }) |
| 视频首帧 | ≤ 100ms | $(if ($TestResults.VideoFirstFrame -gt 0) { "$($TestResults.VideoFirstFrame) ms" } else { "未测试" }) | $(if ($TestResults.VideoFirstFrame -gt 0 -and $TestResults.VideoFirstFrame -le 100) { "✅" } elseif ($TestResults.VideoFirstFrame -gt 0) { "❌" } else { "⚠️" }) |

---

## 达标率统计

$(
$TotalTests = 6
$PassedTests = 0

if ($AvgStartupTime -le 1.5) { $PassedTests++ }
if ($TestResults.IdleMemory -le 40) { $PassedTests++ }
if ($TestResults.MultiServiceMemory -le 150) { $PassedTests++ }
if ($TestResults.ExeSize -le 15) { $PassedTests++ }
if ($TestResults.SmallFileResponse.Count -gt 0 -and $TestResults.SmallFileResponse['index.html'] -le 10) { $PassedTests++ }
if ($TestResults.VideoFirstFrame -gt 0 -and $TestResults.VideoFirstFrame -le 100) { $PassedTests++ }

$PassRate = [math]::Round(($PassedTests / $TotalTests) * 100, 2)

"- 总测试项: $TotalTests 项`n"
"- 达标项: $PassedTests 项`n"
"- 达标率: $PassRate %"
)

---

## 性能优化建议

### 已达标项目
$(
$Suggestions = @()

if ($AvgStartupTime -le 1.5) {
    $Suggestions += "- ✅ 冷启动时间优秀，无需优化"
}
if ($TestResults.IdleMemory -le 40) {
    $Suggestions += "- ✅ 空闲内存占用优秀，无需优化"
}
if ($TestResults.MultiServiceMemory -le 150) {
    $Suggestions += "- ✅ 多服务内存占用优秀，无需优化"
}
if ($TestResults.ExeSize -le 15) {
    $Suggestions += "- ✅ 打包体积优秀，无需优化"
}
if ($TestResults.SmallFileResponse.Count -gt 0 -and $TestResults.SmallFileResponse['index.html'] -le 10) {
    $Suggestions += "- ✅ 小文件响应时间优秀，无需优化"
}
if ($TestResults.VideoFirstFrame -gt 0 -and $TestResults.VideoFirstFrame -le 100) {
    $Suggestions += "- ✅ 视频首帧加载时间优秀，无需优化"
}

if ($Suggestions.Count -gt 0) {
    $Suggestions -join "`n"
} else {
    "无"
}
)

### 需要优化的项目
$(
$OptimizationSuggestions = @()

if ($AvgStartupTime -gt 1.5) {
    $OptimizationSuggestions += @"
#### 冷启动时间优化
- 减少应用启动时的初始化操作
- 延迟加载非关键模块
- 优化 Rust 依赖项编译
- 使用 lazy_static 延迟初始化全局变量
"@
}

if ($TestResults.IdleMemory -gt 40) {
    $OptimizationSuggestions += @"
#### 空闲内存占用优化
- 检查是否有内存泄漏（使用 valgrind 或 heaptrack）
- 优化 Tokio 运行时配置
- 减少不必要的数据缓存
- 使用 Arc 和 Weak 引用避免循环引用
"@
}

if ($TestResults.MultiServiceMemory -gt 150) {
    $OptimizationSuggestions += @"
#### 多服务内存占用优化
- 优化服务管理器的资源使用
- 使用对象池复用资源
- 减少每个服务实例的内存占用
- 考虑使用更轻量的异步运行时配置
"@
}

if ($TestResults.ExeSize -gt 15) {
    $OptimizationSuggestions += @"
#### 打包体积优化
- 进一步优化 Cargo.toml 的 release profile
- 移除未使用的依赖项
- 使用 strip 移除调试符号
- 考虑使用 UPX 压缩 EXE（可选）
"@
}

if ($TestResults.SmallFileResponse.Count -gt 0 -and $TestResults.SmallFileResponse['index.html'] -gt 10) {
    $OptimizationSuggestions += @"
#### 小文件响应时间优化
- 优化静态文件处理器
- 使用零拷贝技术
- 启用 TCP_NODELAY
- 优化文件读取缓冲区大小
"@
}

if ($TestResults.VideoFirstFrame -gt 0 -and $TestResults.VideoFirstFrame -gt 100) {
    $OptimizationSuggestions += @"
#### 视频首帧加载时间优化
- 优化 Range Request 处理器
- 使用异步文件读取
- 优化文件定位算法
- 考虑使用 mmap 映射大文件
"@
}

if ($OptimizationSuggestions.Count -gt 0) {
    $OptimizationSuggestions -join "`n`n"
} else {
    "无需优化，所有指标均已达标！"
}
)

---

## 测试结论

**整体评价**: $(
if ($PassRate -ge 90) { "✅ 优秀" }
elseif ($PassRate -ge 75) { "✅ 良好" }
elseif ($PassRate -ge 60) { "⚠️ 一般" }
else { "❌ 需改进" }
)

**是否满足性能要求**: $(if ($PassRate -ge 80) { "✅ 是" } else { "❌ 否" })

**是否可以进入下一阶段**: $(if ($PassRate -ge 80) { "✅ 是" } else { "❌ 否，需要先优化性能" })

**总结**:
$(
if ($PassRate -ge 90) {
    "性能测试结果优秀，所有关键指标均达标。Tauri v2 架构的性能优势明显，相比 Python + Flet 版本有显著提升。应用已具备发布条件。"
} elseif ($PassRate -ge 75) {
    "性能测试结果良好，大部分指标达标。少数指标需要优化，但不影响基本使用。建议在后续版本中持续优化。"
} elseif ($PassRate -ge 60) {
    "性能测试结果一般，部分关键指标未达标。建议优先优化未达标项目后再进行发布。"
} else {
    "性能测试结果不理想，多个关键指标未达标。需要进行全面的性能优化后再进行测试。"
}
)

---

## 后续行动

- [ ] 修复所有未达标的性能指标
- [ ] 进行边界测试（任务 10.3）
- [ ] 更新用户文档
- [ ] 准备发布版本

---

**测试完成日期**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

**测试工具**: PowerShell 自动化脚本 v1.0.0

**报告生成**: 自动生成

"@

# 保存报告
$ReportPath = Join-Path $PSScriptRoot $OutputFile
$ReportContent | Out-File -FilePath $ReportPath -Encoding UTF8

Write-ColorOutput "`n✅ 测试报告已生成: $ReportPath" "Green"

# ============================================================================
# 清理
# ============================================================================
Write-ColorOutput "`n[清理] 是否关闭应用？(Y/N)" "Yellow"
$CloseApp = Read-Host

if ($CloseApp -eq "Y" -or $CloseApp -eq "y") {
    Get-Process -Name "prism-local-server-tauri" -ErrorAction SilentlyContinue | Stop-Process -Force
    Write-ColorOutput "✅ 应用已关闭" "Green"
}

Write-ColorOutput "`n========================================" "Cyan"
Write-ColorOutput "  性能测试完成！" "Cyan"
Write-ColorOutput "========================================`n" "Cyan"
