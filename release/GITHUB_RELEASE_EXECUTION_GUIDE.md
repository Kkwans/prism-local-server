# GitHub Release 发布执行指南

## 📋 任务概览

本指南将指导您完成 Prism Local Server v3.0.0 的 GitHub Release 发布流程。

## ✅ 已完成的准备工作

- ✅ 所有打包文件已生成（3 个文件,总计 9.51 MB）
- ✅ v3.0.0 Tag 已推送到远程仓库
- ✅ RELEASE_NOTES.md 已准备完毕
- ✅ CREATE_GITHUB_RELEASE.md 指南已准备完毕

## 🎯 需要手动完成的任务

### 任务 2: 在 GitHub 上创建 Release

#### 2.1 访问 GitHub Releases 页面

1. 打开浏览器访问: `https://github.com/Kkwans/prism-local-server/releases`
2. 点击 **"Draft a new release"** 按钮

#### 2.2 配置 Release 基本信息

1. **选择 Tag**: 从下拉菜单选择 `v3.0.0`
2. **Release 标题**: 输入 `Prism Local Server v3.0.0 - Tauri v2 完全重写版本`
3. **发布选项**:
   - ✅ 勾选 "Set as the latest release"
   - ❌ 不勾选 "Set as a pre-release"

---

### 任务 3: 填写 Release 描述信息

#### 3.1 复制发布说明内容

从 `release/RELEASE_NOTES.md` 复制以下内容到 Release 描述框:

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

#### 3.2 确认内容完整性

确保描述包含:
- ✅ 重大更新说明
- ✅ 新特性列表（性能、UI、核心功能、技术架构）
- ✅ 下载说明（3 个 Windows 文件 + Linux/macOS 指南）
- ✅ 系统要求
- ✅ 快速开始指南
- ✅ 完整文档链接

---

### 任务 4: 上传 Windows 安装包文件

在 "Attach binaries" 区域，拖拽上传以下文件:

#### 4.1 上传 NSIS 安装包
- 文件: `Prism Local Server_3.0.0_x64-setup.exe`
- 大小: 1.74 MB
- 验证文件名和大小显示正确

#### 4.2 上传 MSI 安装包
- 文件: `Prism Local Server_3.0.0_x64_en-US.msi`
- 大小: 3.05 MB
- 验证文件名和大小显示正确

#### 4.3 上传独立可执行文件
- 文件: `Prism-Local-Server-v3.0.0.exe`
- 大小: 4.72 MB
- 验证文件名和大小显示正确

---

### 任务 5: 发布 Release

1. **最终检查**:
   - ✅ 标题正确
   - ✅ 描述完整
   - ✅ 3 个文件已上传
   - ✅ "Set as the latest release" 已勾选
   - ✅ "Set as a pre-release" 未勾选

2. **点击发布**: 点击 **"Publish release"** 按钮

3. **等待完成**: 等待 GitHub 处理完成

---

### 任务 6: 验证 Release 发布状态

#### 6.1 验证 Release 页面信息

访问: `https://github.com/Kkwans/prism-local-server/releases/tag/v3.0.0`

确认:
- ✅ 标题显示: "Prism Local Server v3.0.0 - Tauri v2 完全重写版本"
- ✅ 描述正确显示（包含所有章节）
- ✅ 显示 "Latest" 绿色标签
- ✅ 显示发布时间和 Git Tag 信息

#### 6.2 验证文件上传完整性

确认:
- ✅ 3 个安装包文件都已上传
- ✅ 文件名保持原始名称（未被重命名）
- ✅ 文件大小显示正确
- ✅ 自动生成了源代码压缩包（Source code (zip) 和 Source code (tar.gz)）

#### 6.3 测试下载链接

1. 点击每个安装包文件
2. 验证下载功能正常
3. 验证下载的文件可以正常打开/安装

---

### 任务 7: Checkpoint - 确认 Release 发布成功

如果所有验证项都通过，Release 发布成功！

如果发现问题:
- 可以点击 "Edit release" 修改描述或重新上传文件
- 如果需要标记为预发布版本，可以勾选 "Set as a pre-release"

---

## 📊 验证清单

完成发布后，请确认以下所有项:

- [ ] Release 已创建并发布
- [ ] 标题正确: "Prism Local Server v3.0.0 - Tauri v2 完全重写版本"
- [ ] 描述完整（包含所有必需章节）
- [ ] 3 个 Windows 安装包文件已上传
- [ ] 文件名和大小正确
- [ ] 标记为 "Latest" release
- [ ] 自动生成了源代码压缩包
- [ ] 所有下载链接可用
- [ ] 从项目主页可以看到 Latest release

---

## 🎉 完成后的后续步骤

Release 发布成功后，还需要:

1. **更新 README.md**: 添加 v3.0.0 下载链接（任务 8）
2. **验证文档一致性**: 确保 README.md 和 RELEASE_NOTES.md 内容一致（任务 8.2）
3. **最终验证**: 执行完整验证清单（任务 9）

---

## 📞 需要帮助？

如果在发布过程中遇到问题:
- 参考 `docs/CREATE_GITHUB_RELEASE.md` 获取详细指导
- 检查 GitHub 权限设置
- 确认网络连接稳定

---

**祝发布顺利！** 🚀
