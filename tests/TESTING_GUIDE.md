# Prism Local Server 功能测试指南

## 📋 测试概述

本指南将帮助您完成 Prism Local Server Tauri 版本的功能测试（任务 10.1）。

**测试目标**：验证应用的所有核心功能是否按照需求文档正常工作。

**预计测试时间**：30-45 分钟

---

## 🚀 快速开始

### 方法 1：使用自动化测试脚本（推荐）

**PowerShell:**
```powershell
cd prism-local-server-tauri/tests
.\run_functional_tests.ps1
```

**CMD:**
```cmd
cd prism-local-server-tauri\tests
run_functional_tests.bat
```

脚本会自动：
- ✅ 检查 EXE 文件是否存在
- ✅ 检查测试资源是否完整
- ✅ 检查端口占用情况
- ✅ 显示本机 IP 地址（用于局域网测试）
- ✅ 启动应用

### 方法 2：手动测试

1. 确保已构建 Release 版本：
   ```powershell
   npm run tauri:build
   ```

2. 准备测试资源（见下文）

3. 双击 `prism-local-server-v3.0.0.exe` 启动应用

4. 按照测试报告模板逐项测试

---

## 📁 测试资源准备

### 必需资源（已自动创建）

以下资源已通过测试脚本自动创建：

- ✅ `test_resources/index.html` - 测试页面
- ✅ `test_resources/css/style.css` - 样式表
- ✅ `test_resources/js/script.js` - JavaScript 脚本

### 可选资源（需要手动添加）

以下资源需要您手动添加，用于完整测试：

#### 1. 测试图片

**位置**: `test_resources/images/`

**需要的文件**:
- `test-image.png` - 普通测试图片（约 500KB）
- `中文文件名图片.png` - 中文文件名测试

**如何准备**:

**方法 A - 下载在线图片**:
1. 访问 https://via.placeholder.com/800x600.png
2. 下载并重命名为 `test-image.png`
3. 复制一份并重命名为 `中文文件名图片.png`

**方法 B - 使用现有图片**:
1. 找任意 PNG 图片
2. 复制到 `test_resources/images/` 目录
3. 重命名为上述文件名

**方法 C - 使用 PowerShell 创建纯色图片**:
```powershell
# 需要安装 ImageMagick
cd test_resources/images
magick -size 800x600 xc:blue test-image.png
magick -size 800x600 xc:green 中文文件名图片.png
```

#### 2. 测试视频

**位置**: `test_resources/videos/`

**需要的文件**:
- `test-video.mp4` - 测试视频（建议 > 50MB，时长 > 30 秒）

**如何准备**:

**方法 A - 下载免费测试视频**:
1. 访问 https://sample-videos.com/
2. 下载 "Big Buck Bunny" 或其他测试视频
3. 重命名为 `test-video.mp4`
4. 复制到 `test_resources/videos/` 目录

**方法 B - 使用现有视频**:
1. 找任意 MP4 视频（建议 > 50MB）
2. 复制到 `test_resources/videos/` 目录
3. 重命名为 `test-video.mp4`

**方法 C - 使用 FFmpeg 生成测试视频**:
```powershell
# 需要安装 FFmpeg
cd test_resources/videos
ffmpeg -f lavfi -i testsrc=duration=60:size=1920x1080:rate=30 -pix_fmt yuv420p test-video.mp4
```

---

## 📝 测试执行流程

### 第 1 步：环境检查

运行测试脚本或手动检查：

- [ ] EXE 文件存在
- [ ] 测试资源完整
- [ ] 端口 8888-8892 可用
- [ ] 已准备局域网测试设备（手机/平板）

### 第 2 步：启动应用

1. 双击 `prism-local-server-v3.0.0.exe`
2. 等待应用启动（应在 1.5 秒内完成）
3. 确认主界面正常显示

### 第 3 步：执行测试用例

打开测试报告模板：`tests/TASK_10.1_FUNCTIONAL_TEST_REPORT.md`

按顺序执行以下测试：

1. **一键启动服务** - 测试默认配置启动
2. **端口自动递增** - 测试端口占用处理
3. **多服务并发** - 测试同时运行多个服务
4. **服务停止和重启** - 测试服务管理
5. **相对路径资源加载** - 测试 CSS/JS/图片加载
6. **视频 Range Request** - 测试视频拖拽播放
7. **局域网访问** - 测试从手机访问
8. **中文文件名和路径** - 测试 UTF-8 支持
9. **系统托盘功能** - 测试后台运行
10. **配置保存和加载** - 测试配置持久化

### 第 4 步：记录测试结果

在测试报告模板中：

- ✅ 勾选测试结果（通过/失败）
- 📝 填写实际测试数据
- 📸 添加截图（如有问题）
- 🐛 记录发现的问题

### 第 5 步：生成测试报告

1. 完成所有测试用例
2. 统计通过率
3. 总结发现的问题
4. 提出改进建议

---

## 🔍 测试要点

### 测试 1：一键启动服务

**关键检查点**:
- 启动速度 ≤ 1.5 秒
- 自动打开浏览器
- Toast 提示显示
- 服务卡片信息正确

**常见问题**:
- 端口被占用 → 应自动递增
- 目录无权限 → 应显示错误提示
- 浏览器未打开 → 检查配置

### 测试 2：端口自动递增

**关键检查点**:
- 检测到端口占用
- 自动切换到下一个端口
- Toast 提示显示端口变更

**如何占用端口**:
```powershell
# PowerShell
python -m http.server 8888

# 或使用 netcat
nc -l -p 8888
```

### 测试 3：多服务并发

**关键检查点**:
- 所有服务都成功启动
- 端口号依次递增
- 内存占用 ≤ 150MB

**如何检查内存**:
1. 打开任务管理器（Ctrl+Shift+Esc）
2. 找到 `prism-local-server-tauri.exe`
3. 查看"内存"列

### 测试 6：视频 Range Request

**关键检查点**:
- 请求头包含 `Range: bytes=xxx-xxx`
- 响应状态码为 `206 Partial Content`
- 响应头包含 `Content-Range`
- 拖拽后立即播放

**如何验证**:
1. 打开浏览器开发者工具（F12）
2. 切换到 Network 标签
3. 播放视频并拖拽进度条
4. 查看网络请求详情

### 测试 7：局域网访问

**关键检查点**:
- 服务卡片显示局域网 IP
- 手机能访问该 IP
- 页面和资源正常加载

**如何获取局域网 IP**:
```powershell
# PowerShell
Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notlike "127.*" }

# CMD
ipconfig | findstr IPv4
```

### 测试 9：系统托盘功能

**关键检查点**:
- 关闭窗口后进程继续运行
- 托盘图标显示
- 托盘菜单功能正常
- 退出后端口释放

**如何验证进程继续运行**:
1. 关闭主窗口
2. 在浏览器中访问服务 URL
3. 页面应仍然可访问

---

## 🐛 常见问题排查

### 问题 1：应用无法启动

**可能原因**:
- WebView2 未安装
- 缺少运行时依赖

**解决方法**:
1. 安装 WebView2 Runtime
2. 检查 Windows 更新

### 问题 2：端口被占用

**可能原因**:
- 其他程序占用端口
- 之前的服务未正确停止

**解决方法**:
```powershell
# 查找占用端口的进程
netstat -ano | findstr :8888

# 结束进程（替换 PID）
taskkill /PID <PID> /F
```

### 问题 3：资源加载失败（404）

**可能原因**:
- 文件路径错误
- 文件不存在
- 权限问题

**解决方法**:
1. 检查文件是否存在
2. 检查文件路径大小写
3. 检查目录权限

### 问题 4：视频无法拖拽

**可能原因**:
- 服务器未实现 Range Request
- 视频格式不支持
- 浏览器兼容性问题

**解决方法**:
1. 检查响应头是否包含 `Accept-Ranges: bytes`
2. 使用标准 MP4 格式视频
3. 尝试不同浏览器

### 问题 5：局域网无法访问

**可能原因**:
- 防火墙阻止
- 设备不在同一网络
- IP 地址错误

**解决方法**:
1. 关闭防火墙或添加例外
2. 确认设备在同一 WiFi
3. 使用 `ipconfig` 确认 IP

---

## 📊 测试报告示例

### 优秀测试报告示例

```markdown
## 测试总结

### 测试统计
- 通过: 10 / 10
- 失败: 0 / 10
- 通过率: 100%

### 测试亮点
- 所有功能正常工作
- 性能指标全部达标
- 用户体验流畅

### 发现的问题
无

### 测试结论
应用完全满足需求文档要求，可以进入下一阶段。
```

### 需改进测试报告示例

```markdown
## 测试总结

### 测试统计
- 通过: 8 / 10
- 失败: 2 / 10
- 通过率: 80%

### 发现的问题

#### 问题 1：视频拖拽卡顿
- 严重程度: 中等
- 问题描述: 拖拽大视频文件时偶尔卡顿
- 复现步骤: 加载 > 100MB 视频，快速拖拽进度条
- 建议: 优化 Range Request 处理逻辑

#### 问题 2：中文路径显示乱码
- 严重程度: 轻微
- 问题描述: 包含特殊中文字符的路径显示异常
- 复现步骤: 使用包含 emoji 的目录名
- 建议: 增强 UTF-8 编码处理

### 测试结论
应用基本满足需求，但需修复中等及以上问题后再发布。
```

---

## ✅ 测试完成检查清单

测试完成后，请确认：

- [ ] 所有 10 项测试用例已执行
- [ ] 测试结果已记录在报告中
- [ ] 发现的问题已详细描述
- [ ] 已添加必要的截图和日志
- [ ] 已统计通过率
- [ ] 已给出测试结论和建议
- [ ] 测试报告已保存

---

## 📞 获取帮助

如果在测试过程中遇到问题：

1. 查看应用日志：`%APPDATA%/prism-local-server/logs/`
2. 查看浏览器控制台（F12）
3. 查看本指南的"常见问题排查"部分
4. 在 GitHub Issues 中报告问题

---

## 📚 相关文档

- [需求文档](../.kiro/specs/prism-local-server-tauri/requirements.md)
- [设计文档](../.kiro/specs/prism-local-server-tauri/design.md)
- [用户指南](../USER_GUIDE.md)
- [性能测试指南](../PERFORMANCE_TEST.md)

---

**祝测试顺利！** 🎉
