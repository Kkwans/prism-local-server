# 创建 GitHub Release 指南

## 前提条件

- 已推送 v3.0.0 tag 到 GitHub
- release 文件夹中包含所有打包文件
- 已登录 GitHub 账号

## 步骤

### 1. 访问 GitHub Releases 页面

打开浏览器访问：
```
https://github.com/Kkwans/prism-local-server/releases
```

### 2. 创建新 Release

1. 点击右上角的 "Draft a new release" 按钮
2. 或者点击 "Create a new release" 按钮

### 3. 填写 Release 信息

#### Tag 选择
- 选择现有 tag：`v3.0.0`
- 或者创建新 tag：输入 `v3.0.0` 并选择 target branch 为 `tauri-v3`

#### Release 标题
```
Prism Local Server v3.0.0 - Tauri v2 完全重写版本
```

#### Release 描述

复制以下内容（或使用 `release/RELEASE_NOTES.md` 的内容）：

```markdown
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

## 📦 下载说明

### Windows 用户（推荐）

1. **Prism Local Server_3.0.0_x64-setup.exe**（1.74 MB）⭐ 推荐
   - NSIS 安装程序，推荐大多数用户使用
   - 自动安装到 Program Files
   - 创建桌面快捷方式和开始菜单项

2. **Prism Local Server_3.0.0_x64_en-US.msi**（3.05 MB）
   - MSI 安装包，适合企业部署
   - 支持静默安装和组策略管理

3. **Prism-Local-Server-v3.0.0.exe**（4.72 MB）
   - 独立可执行文件，无需安装
   - 适合便携使用或测试

### Linux/macOS 用户

请下载源代码并参考构建指南：
- [Linux 构建指南](https://github.com/Kkwans/prism-local-server/blob/tauri-v3/docs/BUILD_LINUX.md)
- [macOS 构建指南](https://github.com/Kkwans/prism-local-server/blob/tauri-v3/docs/BUILD_MACOS.md)

## 🔧 系统要求

- Windows 10 1809+ 或 Windows 11（推荐）
- WebView2 运行时（Windows 11 自带）
- 64 位系统

## 📖 快速开始

1. 下载并安装 NSIS 安装包
2. 从开始菜单启动应用
3. 选择包含 HTML 文件的目录
4. 点击"启动服务"按钮
5. 浏览器会自动打开您的 HTML 页面

## 📝 完整文档

- [用户指南](https://github.com/Kkwans/prism-local-server/blob/tauri-v3/docs/USER_GUIDE.md)
- [开发文档](https://github.com/Kkwans/prism-local-server/blob/tauri-v3/docs/DEVELOPMENT.md)
- [更新日志](https://github.com/Kkwans/prism-local-server/blob/tauri-v3/CHANGELOG.md)

---

**项目地址**：https://github.com/Kkwans/prism-local-server  
**问题反馈**：https://github.com/Kkwans/prism-local-server/issues
```

### 4. 上传打包文件

在 "Attach binaries" 区域，上传以下文件：

从 `release/` 文件夹拖拽上传：
- ✅ `Prism Local Server_3.0.0_x64-setup.exe` (1.74 MB)
- ✅ `Prism Local Server_3.0.0_x64_en-US.msi` (3.05 MB)
- ✅ `Prism-Local-Server-v3.0.0.exe` (4.72 MB)

### 5. 发布设置

- ✅ 勾选 "Set as the latest release"
- ✅ 不勾选 "Set as a pre-release"（这是正式版本）
- ✅ 不勾选 "Create a discussion for this release"（可选）

### 6. 发布

点击 "Publish release" 按钮完成发布。

## 验证

发布后，访问以下链接验证：
```
https://github.com/Kkwans/prism-local-server/releases/tag/v3.0.0
```

确认：
- ✅ Release 标题和描述正确显示
- ✅ 三个打包文件都已上传
- ✅ 文件大小显示正确
- ✅ 标记为 "Latest" release

## 后续步骤

1. 在 README.md 中添加下载链接
2. 更新项目主页的版本号
3. 通知用户新版本发布
4. 收集用户反馈

## 注意事项

- GitHub Release 会自动生成 Source code (zip) 和 Source code (tar.gz)
- 这些源代码包是自动的，不需要手动上传
- 确保上传的二进制文件名称清晰，便于用户识别
- 建议在描述中标注推荐的下载文件（NSIS 安装包）
