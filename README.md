# 棱镜本地服务器 (Prism Local Server) - Tauri 版本

<div align="center">

![Prism Local Server](https://img.shields.io/badge/version-3.0.0-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%2011-0078D4.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**高性能 HTML 静态文件部署工具**

一键启动本地 HTTP 服务器，支持局域网访问、多服务并发管理、视频拖拽播放

---

### 📥 下载 v3.0.0

<table>
<tr>
<td align="center" width="33%">
<h4>⭐ NSIS 安装包（推荐）</h4>
<a href="https://github.com/Kkwans/prism-local-server/releases/download/v3.0.0/Prism%20Local%20Server_3.0.0_x64-setup.exe">
<img src="https://img.shields.io/badge/下载-NSIS%20安装包-blue?style=for-the-badge&logo=windows" alt="下载 NSIS 安装包"/>
</a>
<br/>
<small>1.74 MB | 推荐大多数用户使用</small>
</td>
<td align="center" width="33%">
<h4>MSI 安装包</h4>
<a href="https://github.com/Kkwans/prism-local-server/releases/download/v3.0.0/Prism%20Local%20Server_3.0.0_x64_en-US.msi">
<img src="https://img.shields.io/badge/下载-MSI%20安装包-green?style=for-the-badge&logo=windows" alt="下载 MSI 安装包"/>
</a>
<br/>
<small>3.05 MB | 适合企业部署</small>
</td>
<td align="center" width="33%">
<h4>便携版</h4>
<a href="https://github.com/Kkwans/prism-local-server/releases/download/v3.0.0/Prism-Local-Server-v3.0.0.exe">
<img src="https://img.shields.io/badge/下载-便携版-orange?style=for-the-badge&logo=windows" alt="下载便携版"/>
</a>
<br/>
<small>4.72 MB | 无需安装</small>
</td>
</tr>
</table>

[📋 查看完整 Release 说明](https://github.com/Kkwans/prism-local-server/releases/tag/v3.0.0) | [📚 所有版本](https://github.com/Kkwans/prism-local-server/releases)

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
- **操作系统**: Windows 10 1809+ 或 Windows 11（推荐）
- **WebView2**: 系统自带（Win11 预装，Win10 会自动下载）
- **系统架构**: 64 位系统
- **磁盘空间**: ≥ 50 MB
- **建议内存**: 4GB+

### 下载安装

#### 方式 1: NSIS 安装包（⭐ 推荐）
1. [下载 NSIS 安装包](https://github.com/Kkwans/prism-local-server/releases/download/v3.0.0/Prism%20Local%20Server_3.0.0_x64-setup.exe) (1.74 MB)
2. 双击运行安装程序
3. 按照向导完成安装
4. 从开始菜单或桌面快捷方式启动应用

**特点**:
- ✅ 自动安装到 Program Files
- ✅ 创建桌面快捷方式和开始菜单项
- ✅ 支持一键卸载

#### 方式 2: MSI 安装包（企业部署）
1. [下载 MSI 安装包](https://github.com/Kkwans/prism-local-server/releases/download/v3.0.0/Prism%20Local%20Server_3.0.0_x64_en-US.msi) (3.05 MB)
2. 双击运行 MSI 安装程序
3. 完成安装后启动应用

**特点**:
- ✅ 支持静默安装和组策略管理
- ✅ 更好的企业环境兼容性

#### 方式 3: 便携版（无需安装）
1. [下载便携版](https://github.com/Kkwans/prism-local-server/releases/download/v3.0.0/Prism-Local-Server-v3.0.0.exe) (4.72 MB)
2. 放置到任意目录
3. 双击运行（无需安装，无需管理员权限）

**特点**:
- ✅ 解压即用
- ✅ 适合便携使用或测试
- ✅ 无需管理员权限

### Linux/macOS 用户

请下载源代码并参考构建指南：
- [Linux 构建指南](./docs/BUILD_LINUX.md)
- [macOS 构建指南](./docs/BUILD_MACOS.md)

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
│    React 前端层 (frontend/)                   │
│    职责: UI 渲染 + 状态管理              │
│    禁止: 文件 IO + 网络操作 + 业务逻辑   │
│  ┌─────────────────────────────────┐   │
│  │  Dashboard  │  ServerCard       │   │
│  │  Settings   │  Toast/Dialog     │   │
│  └─────────────────────────────────┘   │
└──────────────┬──────────────────────────┘
               │ IPC (Tauri Commands)
┌──────────────▼──────────────────────────┐
│    Rust 后端层 (backend/frontend/)         │
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
- 📁 `frontend/` - **React 前端代码**（UI 组件、状态管理、用户交互）
- 📁 `backend/` - **Rust 后端代码**（业务逻辑、文件 IO、网络操作、系统调用）

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
# - EXE: backend/target/release/prism-local-server-tauri.exe
# - MSI: backend/target/release/bundle/msi/
# - NSIS: backend/target/release/bundle/nsis/
```

### 代码检查

```bash
# 检查 Rust 代码
cd backend
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

### v3.0.0 (2026-03-21) - 最新版本 ✨

**🎉 重大更新：Tauri v2 完全重写**

[📥 下载 v3.0.0](https://github.com/Kkwans/prism-local-server/releases/tag/v3.0.0) | [📋 完整 Release 说明](https://github.com/Kkwans/prism-local-server/releases/tag/v3.0.0)

#### 新特性
- 🎉 完全重写为 Tauri v2 架构
- ⚡ 使用 Rust + Axum 实现高性能后端
- 🎨 全新 React + Tailwind CSS 现代化 UI
- 🌈 深色主题 + Windows 11 Fluent Design
- 📦 体积减小 85%，性能提升 300%
- 🔧 完整支持 HTTP Range Request（视频拖拽播放）
- 🌐 优化局域网访问体验
- 🎯 系统托盘 + 自动打开浏览器
- 🏷️ 智能服务命名（使用目录名）
- 🔄 端口变更 Toast 提示
- 🎭 流畅动画和响应式布局优化
- 💾 配置持久化和自动填充
- 🛡️ 目录唯一性保护

#### 性能提升
- **启动速度**: 冷启动时间 ≤ 1.5 秒（相比 v2.x 提升 60%）
- **内存占用**: 空闲状态仅 40MB，运行状态 ≤ 80MB（相比 v2.x 降低 70%）
- **包体积**: NSIS 安装包仅 1.74MB，主程序 4.72MB（相比 v2.x 减小 85%）

#### 下载文件
- [Prism Local Server_3.0.0_x64-setup.exe](https://github.com/Kkwans/prism-local-server/releases/download/v3.0.0/Prism%20Local%20Server_3.0.0_x64-setup.exe) (1.74 MB) ⭐ 推荐
- [Prism Local Server_3.0.0_x64_en-US.msi](https://github.com/Kkwans/prism-local-server/releases/download/v3.0.0/Prism%20Local%20Server_3.0.0_x64_en-US.msi) (3.05 MB)
- [Prism-Local-Server-v3.0.0.exe](https://github.com/Kkwans/prism-local-server/releases/download/v3.0.0/Prism-Local-Server-v3.0.0.exe) (4.72 MB)

### v2.x (Python + Flet)
- 基于 Python + Flet 的原始版本
- 已废弃，建议升级到 v3.0.0

[📚 查看所有版本](https://github.com/Kkwans/prism-local-server/releases)

---

## 🌿 分支管理策略

本项目采用多分支策略管理不同技术栈版本和开发流程：

### 分支说明

| 分支 | 类型 | 技术栈 | 状态 | 说明 |
|------|------|--------|------|------|
| `main` | 稳定发布分支 | Tauri v2 + Rust + React | ✅ 活跃 | 仅包含稳定发布版本，每次发布时打 Release Tag |
| `tauri-v3` | 日常开发分支 | Tauri v2 + Rust + React | ✅ 活跃 | 所有新功能开发、Bug 修复、性能优化在此分支进行 |
| `customtkinter` | 历史归档分支 | Python + CustomTkinter | 🔒 已归档 | v1 版本代码归档，不再开发和维护（Tag: v1.0.0-archived） |
| `flet-v2` | 历史归档分支 | Python + Flet | 🔒 已归档 | v2 版本代码归档，不再开发和维护（Tag: v2.0.0-archived） |

### 分支关系图

```
main (稳定发布)
  ├── v3.0.0 (Release Tag)
  ├── v3.1.0 (Release Tag)
  └── v3.2.0 (Release Tag)
  ↑
  └── 合并自 tauri-v3 (仅在发布时)

tauri-v3 (日常开发)
  ├── [feat] 新功能开发
  ├── [fix] Bug 修复
  ├── [perf] 性能优化
  └── [chore] 构建配置更新

customtkinter (v1 归档)
  └── Tag: v1.0.0-archived
  └── 状态: 已废弃，不再开发

flet-v2 (v2 归档)
  └── Tag: v2.0.0-archived
  └── 状态: 已废弃，不再开发
```

### 开发流程

#### 日常开发
1. **所有开发工作在 `tauri-v3` 分支进行**
   ```bash
   git checkout tauri-v3
   git pull origin tauri-v3
   # 进行开发...
   git add .
   git commit -m "[feat] 添加某个功能"
   git push origin tauri-v3
   ```

2. **功能完成并测试通过后提交到 `tauri-v3`**
   - 运行代码检查：`cargo clippy` 和 `npm run lint`
   - 运行测试：`cargo test` 和 `npm run test`
   - 确保所有测试通过后再提交

#### 版本发布流程

当准备发布新版本时，按以下步骤操作：

1. **在 `tauri-v3` 分支完成所有功能和测试**
   ```bash
   # 确保在 tauri-v3 分支
   git checkout tauri-v3
   
   # 更新版本号
   # - package.json
   # - backend/Cargo.toml
   # - backend/tauri.conf.json
   
   # 提交版本号更新
   git commit -m "[chore] 更新版本号到 v3.x.x"
   git push origin tauri-v3
   ```

2. **合并到 `main` 分支**
   ```bash
   git checkout main
   git pull origin main
   git merge tauri-v3
   git push origin main
   ```

3. **创建 Release Tag**
   ```bash
   # 创建带注释的 Tag
   git tag -a v3.x.x -m "Release v3.x.x - 功能描述"
   
   # 推送 Tag 到远程
   git push origin v3.x.x
   ```

4. **在 GitHub 创建 Release**
   - 访问 GitHub 仓库的 Releases 页面
   - 点击 "Draft a new release"
   - 选择刚创建的 Tag (v3.x.x)
   - 填写 Release 标题和说明（包含功能更新、Bug 修复、性能改进）
   - 上传构建产物（EXE、MSI、NSIS 安装包）
   - 发布 Release

5. **切回开发分支继续开发**
   ```bash
   git checkout tauri-v3
   ```

### 分支使用规则

#### ✅ 允许的操作
- 在 `tauri-v3` 分支进行所有开发工作
- 从 `tauri-v3` 合并到 `main`（仅在发布时）
- 在 `main` 分支创建 Release Tag
- 查看 `customtkinter` 和 `flet-v2` 分支的历史代码

#### ❌ 禁止的操作
- 直接在 `main` 分支进行开发
- 在 `customtkinter` 或 `flet-v2` 分支进行任何修改
- 从 `main` 合并回 `tauri-v3`（应该始终是单向合并）
- 删除历史归档分支

### 历史版本说明

#### v1 版本 (CustomTkinter)
- **分支**: `customtkinter`
- **技术栈**: Python + CustomTkinter
- **状态**: 已归档，不再维护
- **Tag**: v1.0.0-archived
- **说明**: 这是项目的第一个版本，使用 Python 和 CustomTkinter 构建。由于性能和打包体积问题，已被 v3 版本替代。

#### v2 版本 (Flet)
- **分支**: `flet-v2`
- **技术栈**: Python + Flet
- **状态**: 已归档，不再维护
- **Tag**: v2.0.0-archived
- **说明**: 这是项目的第二个版本，使用 Python 和 Flet 框架。虽然改进了 UI，但仍存在性能问题，已被 v3 版本替代。

#### v3 版本 (Tauri)
- **分支**: `tauri-v3` (开发) / `main` (发布)
- **技术栈**: Tauri v2 + Rust + React
- **状态**: 当前活跃版本
- **说明**: 完全重写的版本，使用 Rust 后端和 React 前端，性能提升 300%，体积减小 80%。

### 版本迁移建议

如果你正在使用 v1 或 v2 版本，强烈建议升级到 v3 版本：

| 对比项 | v1 (CustomTkinter) | v2 (Flet) | v3 (Tauri) |
|--------|-------------------|-----------|------------|
| 启动速度 | ~5 秒 | ~3 秒 | ~1.2 秒 ✅ |
| 内存占用 | ~150 MB | ~120 MB | ~35 MB ✅ |
| 打包体积 | ~80 MB | ~60 MB | ~5 MB ✅ |
| UI 性能 | 一般 | 良好 | 优秀 ✅ |
| 跨平台 | ❌ | ❌ | ✅ |

**升级步骤**:
1. 备份 v1/v2 版本的配置文件
2. 卸载旧版本
3. 安装 v3 版本
4. 重新配置（v3 配置文件格式不兼容）

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
