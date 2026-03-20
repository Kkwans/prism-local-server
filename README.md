# 棱镜本地服务器 (Prism Local Server) - Tauri 版本

<div align="center">

![Prism Local Server](https://img.shields.io/badge/version-3.0.0-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%2011-0078D4.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**高性能 HTML 静态文件部署工具**

一键启动本地 HTTP 服务器，支持局域网访问、多服务并发管理、视频拖拽播放

</div>

---

## ✨ 核心特性

### 🚀 极致性能
- **冷启动时间**: ≤ 1.5 秒（Rust 原生性能）
- **内存占用**: 空闲 ≤ 40MB，运行 5 个服务 ≤ 150MB
- **打包体积**: EXE 仅 4.67 MB，安装包 < 2.5 MB

### 🎯 核心功能
- ✅ **一键部署**: 选择目录 → 点击启动 → 自动打开浏览器
- ✅ **智能命名**: 自动使用目录名作为服务名称，支持中文和特殊字符
- ✅ **智能端口**: 默认 8888，占用时自动递增查找可用端口，并显示 Toast 提示
- ✅ **多服务管理**: 同时运行多个服务实例，独立控制，目录唯一性保护
- ✅ **局域网访问**: 自动显示局域网 IP，手机/平板可直接访问
- ✅ **视频支持**: 完整支持 HTTP Range Request，视频可拖拽播放
- ✅ **配置持久化**: 自动保存用户设置，下次启动自动填充
- ✅ **系统托盘**: 后台运行，关闭窗口不退出程序
- ✅ **中文支持**: 完美支持中文文件名和路径

### 🎨 现代化 UI
- Windows 11 Fluent Design 风格
- 深色主题 + 三层阴影系统
- 流畅动画 (Framer Motion)，所有动画 150-300ms
- 响应式布局，大屏幕支持双列显示
- 防抖优化，避免刷新闪烁和位置跳动

---

## 📦 安装说明

### 系统要求
- **操作系统**: Windows 11 (21H2 或更高版本)
- **WebView2**: 系统自带（Win11 预装）
- **磁盘空间**: ≥ 50 MB

### 安装方式

#### 方式 1: 使用安装包（推荐）
1. 下载 `Prism Local Server_3.0.0_x64-setup.exe`
2. 双击运行安装程序
3. 按照向导完成安装
4. 从开始菜单启动应用

#### 方式 2: 使用 MSI 安装包
1. 下载 `Prism Local Server_3.0.0_x64_en-US.msi`
2. 双击运行 MSI 安装程序
3. 完成安装后启动应用

#### 方式 3: 使用便携版
1. 下载 `prism-local-server-tauri.exe`
2. 放置到任意目录
3. 双击运行（无需安装）

---

## 🎮 使用指南

### 快速开始

1. **启动应用**
   - 双击桌面图标或从开始菜单启动

2. **部署第一个服务**
   - 点击"浏览"按钮选择包含 HTML 文件的目录
   - 设置端口号（默认 8888）
   - 点击"启动服务"按钮
   - 浏览器自动打开访问地址

3. **管理服务**
   - 查看运行状态、访问地址、运行时长
   - 点击"停止"按钮停止服务
   - 点击"重启"按钮重启服务
   - 点击"复制链接"快速复制访问地址
   - 点击"在浏览器中打开"直接访问

### 局域网访问

1. 启动服务后，在服务卡片中找到"局域网地址"
2. 在同一局域网的其他设备（手机/平板/电脑）浏览器中输入该地址
3. 即可访问部署的网页

**示例**:
```
本地地址: http://localhost:8888
局域网地址: http://192.168.1.100:8888
```

### 视频播放支持

本工具完整支持 HTTP Range Request，可以：
- ✅ 拖拽视频进度条快速跳转
- ✅ 断点续传，节省流量
- ✅ 支持 MP4、MOV、WebM 等格式

### 系统托盘

- 点击窗口关闭按钮 → 最小化到系统托盘（服务继续运行）
- 右键托盘图标 → 显示主窗口 / 退出程序
- 退出程序时自动停止所有运行中的服务

---

## ⚙️ 应用设置

点击右上角"设置"按钮，可配置：

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| 默认端口号 | 启动服务时的默认端口 | 8888 |
| 默认部署目录 | 启动服务时的默认目录 | EXE 所在目录 |
| 默认入口文件 | 服务的入口 HTML 文件名 | index.html |
| 自动打开浏览器 | 启动服务后自动打开浏览器 | 开启 |
| 最小化到托盘 | 关闭窗口时最小化到托盘 | 开启 |

---

## 🛠️ 技术架构

### 技术栈
- **框架**: Tauri v2
- **后端**: Rust + Axum + Tokio
- **前端**: React 18 + TypeScript + Vite
- **UI 库**: Tailwind CSS + Shadcn/ui + Framer Motion
- **状态管理**: Zustand

### 架构设计

**前后端职责分离原则**:

```
┌─────────────────────────────────────────┐
│    React 前端层 (src/)                   │
│    职责: UI 渲染 + 状态管理              │
│    禁止: 文件 IO + 网络操作 + 业务逻辑   │
│  ┌─────────────────────────────────┐   │
│  │  Dashboard  │  ServerCard       │   │
│  │  Settings   │  Toast/Dialog     │   │
│  └─────────────────────────────────┘   │
└──────────────┬──────────────────────────┘
               │ IPC (Tauri Commands)
┌──────────────▼──────────────────────────┐
│    Rust 后端层 (src-tauri/src/)         │
│    职责: 业务逻辑 + 文件 IO + 网络操作   │
│  ┌─────────────────────────────────┐   │
│  │  ServerManager (Axum + Tokio)   │   │
│  │  ConfigManager (JSON)           │   │
│  │  PortManager (TCP Check)        │   │
│  │  NetworkUtils (LAN IP)          │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

**目录结构说明**:
- 📁 `src/` - **React 前端代码**（UI 组件、状态管理、用户交互）
- 📁 `src-tauri/` - **Rust 后端代码**（业务逻辑、文件 IO、网络操作、系统调用）

**关键设计原则**:
- ✅ **前端**: 纯 UI 渲染与状态管理，通过 Tauri IPC 调用后端
- ✅ **后端**: 所有业务逻辑、文件操作、网络操作在 Rust 中实现
- ✅ **通信**: 前端通过 `invoke()` 调用后端 Commands，后端通过 `emit()` 通知前端
- ✅ **类型安全**: TypeScript + Rust 双重类型检查，确保接口一致性

### 核心模块

#### Rust 后端
- `server/manager.rs`: 服务管理器，负责启动/停止/重启服务
- `server/handler.rs`: 静态文件处理器，支持 Range Request
- `server/mime.rs`: MIME 类型检测器
- `config/manager.rs`: 配置管理器，持久化用户设置
- `utils/port.rs`: 端口管理工具
- `utils/network.rs`: 网络工具，获取局域网 IP

#### React 前端
- `components/Dashboard.tsx`: 主界面，服务列表和启动区域
- `components/ServerCard.tsx`: 服务卡片，显示服务信息和操作按钮
- `components/SettingsDialog.tsx`: 设置对话框
- `stores/useServerStore.ts`: 服务状态管理
- `stores/useConfigStore.ts`: 配置状态管理

---

## 📚 文档

| 文档 | 说明 |
|------|------|
| [用户指南 (USER_GUIDE.md)](./USER_GUIDE.md) | 详细的使用说明、功能介绍、常见问题解答 |
| [构建指南 (BUILD_GUIDE.md)](./BUILD_GUIDE.md) | 开发环境配置、构建流程、部署方法 |
| [性能测试指南 (PERFORMANCE_TEST.md)](./PERFORMANCE_TEST.md) | 性能基准测试方法和指标说明 |
| [集成测试文档 (tests/integration_test.md)](./tests/integration_test.md) | 端到端测试用例和测试流程 |

---

## 🔧 开发指南

### 环境准备

1. **安装 Rust**
   ```bash
   # 访问 https://rustup.rs/ 下载安装
   rustup default stable
   ```

2. **安装 Node.js**
   ```bash
   # 推荐使用 Node.js 18+ 或 20+
   # 访问 https://nodejs.org/ 下载安装
   ```

3. **克隆项目**
   ```bash
   git clone git@github.com:Kkwans/prism-local-server.git
   cd prism-local-server-tauri
   ```

4. **安装依赖**
   ```bash
   # 安装前端依赖
   npm install
   
   # Rust 依赖会在构建时自动下载
   ```

### 开发模式

```bash
# 启动开发服务器（热重载）
npm run tauri dev
```

### 构建生产版本

```bash
# 构建 Release 版本
npm run tauri build

# 生成文件位置:
# - EXE: src-tauri/target/release/prism-local-server-tauri.exe
# - MSI: src-tauri/target/release/bundle/msi/
# - NSIS: src-tauri/target/release/bundle/nsis/
```

### 代码检查

```bash
# 检查 Rust 代码
cd src-tauri
cargo check
cargo clippy

# 检查 TypeScript 代码
npm run lint
```

---

## 📝 常见问题

### Q: 启动服务时提示"端口被占用"？
A: 应用会自动递增端口号查找可用端口。如果仍然失败，请检查防火墙设置或手动指定其他端口。

### Q: 局域网无法访问？
A: 请检查：
1. 防火墙是否允许该端口的入站连接
2. 设备是否在同一局域网
3. 使用服务卡片中显示的"局域网地址"

### Q: 视频无法拖拽播放？
A: 本工具完整支持 HTTP Range Request。如果仍有问题，请检查：
1. 视频文件格式是否为 MP4/WebM
2. 浏览器是否支持该视频编码

### Q: 如何完全退出程序？
A: 右键系统托盘图标 → 选择"退出"。直接关闭窗口只会最小化到托盘。

### Q: 配置文件保存在哪里？
A: 配置文件保存在用户目录下：
```
C:\Users\[用户名]\AppData\Roaming\com.prism.local-server\config.json
```

---

## 🐛 故障排除

### 应用无法启动
1. 确认系统版本为 Windows 11
2. 检查 WebView2 是否已安装（Win11 预装）
3. 以管理员身份运行
4. 检查是否被杀毒软件拦截

### 服务启动失败
1. **目录问题**:
   - 检查目录是否包含 HTML 文件（默认 index.html）
   - 检查目录权限是否可读
   - 确认目录路径不包含特殊字符（除中文外）

2. **端口问题**:
   - 检查端口范围是否正确（1024-65535）
   - 如果端口被占用，应用会自动递增并显示 Toast 提示
   - 使用 `netstat -ano | findstr :8888` 检查端口占用情况

3. **目录唯一性**:
   - 同一目录只能启动一个服务
   - 如果提示"目录已被使用"，请先停止已有服务或选择其他目录

### 局域网无法访问
1. **防火墙设置**:
   - 打开 Windows 防火墙 → 高级设置 → 入站规则
   - 添加新规则，允许端口 8888-8988 的 TCP 连接
   - 或临时关闭防火墙测试

2. **网络检查**:
   - 确认设备在同一局域网（相同 WiFi 或有线网络）
   - 使用 `ipconfig` 检查本机 IP 地址
   - 在其他设备上 ping 本机 IP 测试连通性

3. **浏览器问题**:
   - 某些浏览器可能阻止局域网访问
   - 尝试使用 Chrome 或 Edge 浏览器
   - 检查浏览器是否启用了隐私保护功能

### 视频播放问题
1. **无法拖拽播放**:
   - 本工具完整支持 HTTP Range Request
   - 检查视频文件格式（推荐 MP4）
   - 使用浏览器开发者工具 → Network 标签，确认返回 206 状态码

2. **视频加载慢**:
   - 检查文件大小（建议 < 500MB）
   - 检查磁盘读取速度
   - 尝试使用 SSD 存储视频文件

### 性能问题
1. **内存占用过高**:
   - 关闭不需要的服务实例
   - 检查是否有内存泄漏（长时间运行后重启应用）
   - 检查系统其他程序的资源占用

2. **响应速度慢**:
   - 检查 CPU 占用情况
   - 关闭不必要的后台程序
   - 检查磁盘 I/O 性能

3. **UI 卡顿**:
   - 检查是否同时运行过多服务（建议 ≤ 10 个）
   - 更新显卡驱动
   - 检查 WebView2 版本

### 配置问题
1. **配置丢失**:
   - 配置文件位置：`%APPDATA%\prism-local-server\config.json`
   - 如果文件损坏，应用会自动恢复默认配置
   - 可以手动删除配置文件重置所有设置

2. **默认目录不正确**:
   - 首次启动时自动识别 EXE 所在目录
   - 可以在设置中手动修改默认目录
   - 修改后会持久化保存，不会被自动覆盖

### 构建问题
1. **Rust 编译错误**:
   - 运行 `rustup update` 更新 Rust 工具链
   - 运行 `cargo clean` 清理缓存
   - 检查 Cargo.toml 依赖版本

2. **前端构建错误**:
   - 删除 `node_modules` 和 `package-lock.json`
   - 重新运行 `npm install`
   - 检查 Node.js 版本（推荐 18+ 或 20+）

3. **Tauri 构建失败**:
   - 运行 `cargo update` 更新依赖
   - 检查 tauri.conf.json 配置是否正确
   - 查看详细错误日志：`npm run tauri build -- --verbose`

---

## 📊 性能指标

| 指标 | 目标值 | 实际值 |
|------|--------|--------|
| 冷启动时间 | ≤ 1.5 秒 | ~1.2 秒 ✅ |
| 空闲内存占用 | ≤ 40 MB | ~35 MB ✅ |
| 运行 5 个服务内存 | ≤ 150 MB | ~120 MB ✅ |
| EXE 体积 | ≤ 15 MB | 4.67 MB ✅ |
| 小文件响应时间 | ≤ 10 ms | ~5 ms ✅ |
| 视频首帧加载 | ≤ 100 ms | ~50 ms ✅ |

---

## 🔄 版本历史

### v3.0.0 (2026-03-20)
- 🎉 完全重写为 Tauri v2 架构
- ⚡ 使用 Rust + Axum 实现高性能后端
- 🎨 全新 React + Tailwind CSS 现代化 UI
- 🌈 深色主题 + Windows 11 Fluent Design
- 📦 体积减小 80%，性能提升 300%
- 🔧 完整支持 HTTP Range Request
- 🌐 优化局域网访问体验
- 🎯 系统托盘 + 自动打开浏览器
- 🏷️ 智能服务命名（使用目录名）
- 🔄 端口变更 Toast 提示
- 🎭 流畅动画和响应式布局优化
- 💾 配置持久化和自动填充
- 🛡️ 目录唯一性保护

### v2.x (Python + Flet)
- 基于 Python + Flet 的原始版本
- 已废弃，建议升级到 v3.0.0

---

## 🌿 分支策略

本项目采用以下分支管理策略：

| 分支 | 用途 | 说明 |
|------|------|------|
| `tauri-v3` | 日常开发分支 | Bug 修复、小优化、功能迭代 |
| `main` | 稳定发布分支 | 仅在发布新版本时从 tauri-v3 合并 |
| `flet` | 历史版本分支 | 保留 Python/Flet 版本代码（v2.x） |

**开发流程**:
1. 所有开发工作在 `tauri-v3` 分支进行
2. 功能完成并测试通过后，提交到 `tauri-v3`
3. 准备发布时，将 `tauri-v3` 合并到 `main` 并打 Tag
4. 从 `main` 分支创建 GitHub Release

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发流程
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m '[feat] 添加某个功能'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 提交信息规范
```
[类型] 功能描述 - 细节说明

类型:
- feat: 新增功能
- fix: 修复 Bug
- perf: 性能优化
- chore: 构建配置/依赖更新
```

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- [Tauri](https://tauri.app/) - 跨平台桌面应用框架
- [Axum](https://github.com/tokio-rs/axum) - Rust Web 框架
- [Shadcn/ui](https://ui.shadcn.com/) - React 组件库
- [Tailwind CSS](https://tailwindcss.com/) - CSS 框架

---

## 📧 联系方式

- GitHub: [@Kkwans](https://github.com/Kkwans)
- 项目地址: [prism-local-server](https://github.com/Kkwans/prism-local-server)

---

<div align="center">

**如果这个项目对你有帮助，请给个 ⭐ Star 支持一下！**

Made with ❤️ by Kkwans

</div>
