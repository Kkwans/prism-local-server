# Prism Local Server 测试目录

## 📁 目录说明

本目录包含 Prism Local Server Tauri 版本的功能测试资源和脚本。

## 🚀 快速开始

### 运行功能测试（任务 10.1）

**PowerShell:**
```powershell
.\run_functional_tests.ps1
```

**CMD:**
```cmd
run_functional_tests.bat
```

### 运行性能测试（任务 10.2）

**简化版自动化测试（推荐）:**
```powershell
.\simple_performance_test.ps1
```

**完整版手动测试:**
参考 `TASK_10.2_MANUAL_PERFORMANCE_TEST_GUIDE.md`

### 运行边界测试（任务 10.3）

**PowerShell（推荐）:**
```powershell
.\run_boundary_tests.ps1
```

**CMD:**
```cmd
run_boundary_tests.bat
```

**运行特定测试:**
```powershell
# 端口占用测试
.\boundary_test_port_occupied.ps1

# 无 HTML 文件测试
.\boundary_test_no_html.ps1

# 无权限目录测试（需要管理员权限）
.\boundary_test_no_permission.ps1

# 多服务并发测试
.\boundary_test_multiple_services.ps1
```

### 查看测试指南

- 功能测试：`TESTING_GUIDE.md`
- 性能测试：`TASK_10.2_MANUAL_PERFORMANCE_TEST_GUIDE.md`
- 边界测试：`TASK_10.3_BOUNDARY_TEST_GUIDE.md`

## 📋 文件说明

### 测试脚本

**功能测试:**
- `run_functional_tests.ps1` - PowerShell 功能测试脚本
- `run_functional_tests.bat` - CMD 功能测试脚本

**性能测试:**
- `simple_performance_test.ps1` - 简化版性能测试脚本（推荐）
- `performance_test.ps1` - 完整版性能测试脚本
- `performance_test.bat` - CMD 性能测试启动器

**边界测试:**
- `run_boundary_tests.ps1` - PowerShell 边界测试主脚本（推荐）
- `run_boundary_tests.bat` - CMD 边界测试启动器
- `boundary_test_port_occupied.ps1` - 端口占用测试
- `boundary_test_no_html.ps1` - 无 HTML 文件测试
- `boundary_test_no_permission.ps1` - 无权限目录测试
- `boundary_test_multiple_services.ps1` - 多服务并发测试

### 测试文档

**功能测试（任务 10.1）:**
- `TESTING_GUIDE.md` - 完整的功能测试指南
- `TASK_10.1_FUNCTIONAL_TEST_REPORT.md` - 功能测试报告模板
- `TASK_10.1_PREPARATION_SUMMARY.md` - 测试准备工作总结

**性能测试（任务 10.2）:**
- `TASK_10.2_PERFORMANCE_TEST_REPORT.md` - 性能测试报告
- `TASK_10.2_MANUAL_PERFORMANCE_TEST_GUIDE.md` - 手动性能测试指南

**边界测试（任务 10.3）:**
- `TASK_10.3_BOUNDARY_TEST_GUIDE.md` - 边界测试指南
- `TASK_10.3_BOUNDARY_TEST_REPORT.md` - 边界测试报告模板

**集成测试:**
- `integration_test.md` - 集成测试用例（已有）

### 测试资源
- `test_resources/` - 测试资源目录
  - `index.html` - 测试页面
  - `css/style.css` - 样式表
  - `js/script.js` - JavaScript 脚本
  - `images/` - 图片资源（需要手动添加）
  - `videos/` - 视频资源（需要手动添加）

## ⚠️ 注意事项

### 需要手动添加的资源

以下资源需要手动添加才能完成完整测试：

1. **测试图片** (`test_resources/images/`)
   - `test-image.png`
   - `中文文件名图片.png`
   
2. **测试视频** (`test_resources/videos/`)
   - `test-video.mp4` (> 50MB)

详细说明请查看：
- `test_resources/images/README.md`
- `test_resources/videos/README.md`

## 📊 测试用例

### 功能测试（任务 10.1）

本次功能测试包含 10 项测试用例：

1. ✅ 一键启动服务（默认配置）
2. ✅ 端口自动递增（手动占用 8888 端口）
3. ✅ 多服务并发（启动 3-5 个服务实例）
4. ✅ 服务停止和重启
5. ✅ 相对路径资源加载（CSS、JS、图片）
6. ✅ 视频文件 Range Request（拖拽播放）
7. ✅ 局域网访问（从手机访问）
8. ✅ 中文文件名和路径
9. ✅ 系统托盘功能
10. ✅ 配置保存和加载

### 性能测试（任务 10.2）

本次性能测试包含 6 项性能指标：

1. ⚠️ 冷启动时间（目标 ≤ 1.5 秒）
2. ⚠️ 空闲状态内存占用（目标 ≤ 40MB）
3. ⚠️ 运行 5 个服务时内存占用（目标 ≤ 150MB）
4. ⚠️ 小文件响应时间（目标 ≤ 10ms）
5. ⚠️ 大视频首帧加载时间（目标 ≤ 100ms）
6. ⚠️ 打包体积（目标 ≤ 15MB）

**说明**: ⚠️ 表示待测试，✅ 表示已达标，❌ 表示未达标

### 边界测试（任务 10.3）

本次边界测试包含 7 项测试用例：

1. ⚠️ 端口被占用的情况
2. ⚠️ 目录不存在的情况
3. ⚠️ 无 HTML 文件的情况
4. ⚠️ 无权限目录的情况
5. ⚠️ 网络断开的情况
6. ⚠️ 同时启动 10+ 个服务
7. ⚠️ 超大文件（>1GB）的加载

**说明**: ⚠️ 表示待测试，✅ 表示已通过，❌ 表示未通过

## 📞 获取帮助

- 查看 `TESTING_GUIDE.md` 获取详细指南
- 查看 `TASK_10.1_PREPARATION_SUMMARY.md` 了解准备工作
- 运行 `.\run_functional_tests.ps1 -CheckOnly` 检查环境

---

**祝测试顺利！** 🎉
