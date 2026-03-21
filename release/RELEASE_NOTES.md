# Prism Local Server v3.0.0 发布说明

## 🎉 重大更新：Tauri v2 完全重写

Prism Local Server v3.0.0 是一个里程碑版本，我们使用 Tauri v2 技术栈完全重写了整个应用，带来了显著的性能提升和更好的用户体验。

## ✨ 新特性

### 🚀 性能大幅提升
- **启动速度**：冷启动时间 ≤ 1.5 秒（相比 v2.x 提升 60%）
- **内存占用**：空闲状态仅 40MB，运行状态 ≤ 80MB（相比 v2.x 降低 70%）
- **包体积**：NSIS 安装包仅 1.74MB，主程序 4.72MB（相比 v2.x 减小 85%）

### 💎 全新 UI 设计
- 采用 Windows 11 Fluent Design 设计语言
- 支持 Mica 毛玻璃效果（Windows 11 专属）
- 使用 Framer Motion 实现流畅动画
- 深色主题默认，完美适配 Windows 11

### 🎯 核心功能
- ✅ 一键启动本地 HTTP 服务器
- ✅ 智能端口自动递增（8888 → 8889 → ...）
- ✅ 多服务实例并发管理（支持 10+ 服务同时运行）
- ✅ HTTP Range Request 支持（视频拖拽播放）
- ✅ 局域网访问支持（显示所有网络接口 IP）
- ✅ 系统托盘后台运行
- ✅ 配置持久化保存
- ✅ 中文文件名和路径完美支持
- ✅ TCP_NODELAY 优化网络传输

### 🛠️ 技术架构
- **后端**：Rust + Axum + Tokio（高性能异步 HTTP 服务器）
- **前端**：React 18 + TypeScript + Tailwind CSS + Shadcn/ui
- **框架**：Tauri v2（原生性能 + Web 技术）

## 📦 下载文件说明

### Windows 用户（推荐）

1. **Prism Local Server_3.0.0_x64-setup.exe**（1.74 MB）⭐ 推荐
   - NSIS 安装程序，推荐大多数用户使用
   - 自动安装到 Program Files
   - 创建桌面快捷方式和开始菜单项
   - 支持一键卸载

2. **Prism Local Server_3.0.0_x64_en-US.msi**（3.05 MB）
   - MSI 安装包，适合企业部署
   - 支持静默安装和组策略管理
   - 更好的企业环境兼容性

3. **Prism-Local-Server-v3.0.0.exe**（4.72 MB）
   - 独立可执行文件，无需安装
   - 适合便携使用或测试
   - 解压即用，无需管理员权限

### Linux 用户

请参考 [Linux 构建指南](../docs/BUILD_LINUX.md) 在您的系统上构建。

构建后会生成：
- `.deb` 包（Ubuntu/Debian）
- `.AppImage` 便携版（通用）

### macOS 用户（可选）

请参考 [macOS 构建指南](../docs/BUILD_MACOS.md) 在您的系统上构建。

构建后会生成：
- `.app` 应用包
- `.dmg` 安装镜像

## 🔧 系统要求

### Windows
- Windows 10 1809+ 或 Windows 11（推荐）
- WebView2 运行时（Windows 11 自带，Windows 10 会自动下载）
- 64 位系统
- 建议内存：4GB+

### Linux
- 64 位系统
- WebKitGTK 4.1+
- GTK 3.24+

### macOS
- macOS 10.15+
- 64 位系统

## 📖 快速开始

1. **下载并安装**：下载 NSIS 安装包并运行
2. **启动应用**：从开始菜单或桌面快捷方式启动
3. **选择目录**：点击"浏览"按钮选择包含 HTML 文件的目录
4. **启动服务**：点击"启动服务"按钮
5. **自动打开**：浏览器会自动打开并显示您的 HTML 页面
6. **局域网访问**：使用显示的局域网地址在其他设备上访问

## 🎨 界面预览

应用采用 Windows 11 Fluent Design 风格，支持：
- Mica 毛玻璃背景效果
- 流畅的动画过渡
- 深色主题
- 响应式布局

## 🐛 已知问题

- 无

## 💡 使用技巧

1. **多服务管理**：可以同时启动多个服务，每个服务使用不同端口
2. **端口自动分配**：如果默认端口被占用，程序会自动寻找可用端口
3. **后台运行**：关闭窗口后程序会最小化到系统托盘，服务继续运行
4. **局域网访问**：在服务卡片上可以看到所有网络接口的访问地址

## 🔄 从旧版本升级

如果您之前使用 Python 版本（v2.x），建议：
1. 卸载旧版本
2. 安装 v3.0.0
3. 重新配置您的默认设置

配置文件不兼容，需要重新设置。

## 🙏 致谢

感谢所有测试用户的反馈和建议！

## 📝 完整更新日志

请查看 [CHANGELOG.md](../CHANGELOG.md)

---

**项目地址**：https://github.com/Kkwans/prism-local-server  
**问题反馈**：https://github.com/Kkwans/prism-local-server/issues  
**许可证**：MIT License
