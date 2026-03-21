# Prism Local Server Tauri - 开发文档

## 项目概述

**项目名称**: Prism Local Server Tauri（棱镜本地服务器 Tauri 版）

**版本**: v3.0.0

**技术栈**: Tauri v2 + Rust (Axum) + React 18 + TypeScript + Tailwind CSS

**项目描述**: 一个基于 Tauri v2 技术栈的 Windows 11 原生桌面应用程序，用于快速将 HTML 静态文件部署到本地 HTTP 服务器。采用 Rust 后端 + React 前端架构，提供高性能、低内存占用、现代化 UI 的本地文件服务解决方案。

**核心特性**:
- ⚡ 高性能：Rust 编译型语言，冷启动 ≤1.5 秒，内存占用 ≤40MB
- 🎨 现代化 UI：Windows 11 Fluent Design，毛玻璃效果，深色主题
- 🚀 一键部署：自动检测 HTML 文件，自动打开浏览器
- 📦 小体积：打包后仅 4.7MB（相比 Python/Electron 版本减少 80-90%）
- 🔄 多服务并发：支持同时运行 10+ 个服务实例
- 🌐 局域网访问：自动检测内网 IP，支持局域网设备访问
- 🎬 视频支持：HTTP Range Request，支持视频拖拽播放
- 🛡️ 类型安全：Rust + TypeScript 双重类型保障

---

## 目录

1. [项目结构](#项目结构)
2. [开发环境配置](#开发环境配置)
3. [构建和调试](#构建和调试)
4. [技术架构](#技术架构)
5. [API 文档](#api-文档)
6. [前端组件](#前端组件)
7. [状态管理](#状态管理)
8. [性能优化](#性能优化)
9. [常见问题](#常见问题)

---

## 项目结构

### 完整目录树

```
prism-local-server-tauri/
├── backend/                          # Rust 后端代码
│   ├── src/
│   │   ├── commands/                 # Tauri IPC 命令实现
│   │   │   ├── config_commands.rs    # 配置管理命令
│   │   │   ├── fs_commands.rs        # 文件系统命令
│   │   │   ├── mod.rs                # 命令模块导出
│   │   │   ├── network_commands.rs   # 网络工具命令
│   │   │   └── server_commands.rs    # 服务管理命令
│   │   ├── config/                   # 配置管理模块
│   │   │   ├── manager.rs            # 配置管理器
│   │   │   └── mod.rs                # 配置模块导出
│   │   ├── server/                   # HTTP 服务器实现
│   │   │   ├── handler.rs            # 静态文件处理器
│   │   │   ├── manager.rs            # 服务管理器
│   │   │   ├── mime.rs               # MIME 类型检测
│   │   │   ├── mod.rs                # 服务模块导出
│   │   │   └── range.rs              # Range Request 处理
│   │   ├── utils/                    # 工具模块
│   │   │   ├── mod.rs                # 工具模块导出
│   │   │   ├── network.rs            # 网络工具
│   │   │   └── port.rs               # 端口管理工具
│   │   ├── errors.rs                 # 错误类型定义
│   │   ├── lib.rs                    # 库入口
│   │   ├── main.rs                   # 应用入口
│   │   └── models.rs                 # 数据模型定义
│   ├── icons/                        # 应用图标资源
│   ├── Cargo.toml                    # Rust 依赖配置
│   ├── build.rs                      # 构建脚本
│   └── tauri.conf.json               # Tauri 配置文件
├── frontend/                         # React 前端代码
│   ├── components/                   # UI 组件
│   │   ├── ui/                       # Shadcn/ui 基础组件
│   │   │   ├── button.tsx            # 按钮组件
│   │   │   ├── card.tsx              # 卡片组件
│   │   │   ├── dialog.tsx            # 对话框组件
│   │   │   ├── input.tsx             # 输入框组件
│   │   │   ├── switch.tsx            # 开关组件
│   │   │   └── toaster.tsx           # Toast 提示组件
│   │   ├── Dashboard.tsx             # 主仪表盘组件
│   │   ├── ServerCard.tsx            # 服务卡片组件
│   │   └── SettingsDialog.tsx        # 设置对话框组件
│   ├── hooks/                        # React Hooks
│   │   └── use-toast.ts              # Toast Hook
│   ├── lib/                          # 工具库
│   │   └── utils.ts                  # 工具函数
│   ├── stores/                       # Zustand 状态管理
│   │   ├── useConfigStore.ts         # 配置状态管理
│   │   └── useServerStore.ts         # 服务状态管理
│   ├── types/                        # TypeScript 类型定义
│   │   └── index.ts                  # 类型导出
│   ├── App.tsx                       # 应用根组件
│   ├── index.css                     # 全局样式
│   └── main.tsx                      # 前端入口
├── tests/                            # 测试脚本和资源
│   ├── test_resources/               # 测试资源文件
│   ├── run_functional_tests.ps1      # 功能测试脚本
│   ├── performance_test.ps1          # 性能测试脚本
│   └── run_boundary_tests.ps1        # 边界测试脚本
├── dist/                             # 前端构建产物（自动生成）
├── node_modules/                     # Node.js 依赖（自动生成）
├── package.json                      # 前端依赖配置
├── tsconfig.json                     # TypeScript 配置
├── vite.config.ts                    # Vite 构建配置
├── tailwind.config.js                # Tailwind CSS 配置
├── postcss.config.js                 # PostCSS 配置
├── components.json                   # Shadcn/ui 配置
├── index.html                        # HTML 入口
├── README.md                         # 项目说明
├── USER_GUIDE.md                     # 用户指南
├── DEVELOPMENT.md                    # 开发文档（本文件）
└── prism-local-server-v3.0.0.exe     # 打包的可执行文件
```

### 核心模块说明

#### 后端模块（Rust）

| 模块 | 文件 | 职责 |
|------|------|------|
| **命令层** | `commands/` | 处理前端 IPC 调用，协调业务逻辑 |
| **服务层** | `server/` | HTTP 服务器实现，静态文件处理 |
| **配置层** | `config/` | 配置文件的加载、保存和验证 |
| **工具层** | `utils/` | 端口检测、网络工具等通用功能 |
| **数据层** | `models.rs` | 数据结构定义（ServerInfo, AppConfig 等） |
| **错误层** | `errors.rs` | 自定义错误类型和错误处理 |

#### 前端模块（React + TypeScript）

| 模块 | 文件 | 职责 |
|------|------|------|
| **组件层** | `components/` | UI 组件，负责渲染和用户交互 |
| **状态层** | `stores/` | Zustand 状态管理，管理全局状态 |
| **类型层** | `types/` | TypeScript 类型定义 |
| **工具层** | `lib/` | 工具函数（如 `cn()` 样式合并） |
| **Hooks** | `hooks/` | 自定义 React Hooks |

---

## 开发环境配置

### 系统要求

- **操作系统**: Windows 11 Professional/Enterprise
- **内存**: 至少 8GB RAM（推荐 16GB）
- **磁盘空间**: 至少 5GB 可用空间
- **网络**: 需要互联网连接以下载依赖

### 必需工具

#### 1. Rust 工具链

**安装 Rust**:

```powershell
# 下载并运行 rustup-init.exe
# 访问: https://rustup.rs/

# 或使用 winget 安装
winget install Rustlang.Rustup
```

**验证安装**:

```powershell
rustc --version  # 应显示 rustc 1.77.2 或更高版本
cargo --version  # 应显示 cargo 1.77.2 或更高版本
```

**配置 Rust 工具链**:

```powershell
# 安装 Stable 工具链
rustup default stable

# 更新工具链
rustup update
```

#### 2. Node.js 和 npm

**安装 Node.js**:

```powershell
# 使用 winget 安装 Node.js LTS
winget install OpenJS.NodeJS.LTS

# 或下载安装包
# 访问: https://nodejs.org/
```

**验证安装**:

```powershell
node --version  # 应显示 v20.x.x 或更高版本
npm --version   # 应显示 10.x.x 或更高版本
```

#### 3. Tauri CLI

**安装 Tauri CLI**:

```powershell
# 方式 1: 通过 npm 安装（推荐）
npm install -g @tauri-apps/cli

# 方式 2: 通过 Cargo 安装
cargo install tauri-cli
```

**验证安装**:

```powershell
npm run tauri --version  # 应显示 2.10.1 或更高版本
```

#### 4. WebView2 运行时

Windows 11 系统自带 WebView2 运行时，无需额外安装。如果需要手动安装：

```powershell
# 下载 WebView2 运行时
# 访问: https://developer.microsoft.com/microsoft-edge/webview2/
```

#### 5. Visual Studio Build Tools（可选但推荐）

某些 Rust crate 需要 C++ 编译器：

```powershell
# 使用 winget 安装
winget install Microsoft.VisualStudio.2022.BuildTools

# 或下载安装包
# 访问: https://visualstudio.microsoft.com/downloads/
# 选择 "Desktop development with C++" 工作负载
```

### 开发工具推荐

#### 代码编辑器

**Visual Studio Code**（推荐）:

```powershell
winget install Microsoft.VisualStudioCode
```

**推荐扩展**:
- `rust-analyzer` - Rust 语言支持
- `Tauri` - Tauri 开发支持
- `ES7+ React/Redux/React-Native snippets` - React 代码片段
- `Tailwind CSS IntelliSense` - Tailwind CSS 智能提示
- `Error Lens` - 错误高亮显示
- `Better Comments` - 注释增强

#### 其他工具

- **Git**: 版本控制
  ```powershell
  winget install Git.Git
  ```

- **Windows Terminal**: 现代化终端
  ```powershell
  winget install Microsoft.WindowsTerminal
  ```

### 项目初始化

#### 1. 克隆项目

```powershell
# 克隆仓库
git clone https://github.com/Kkwans/prism-local-server.git
cd prism-local-server/prism-local-server-tauri
```

#### 2. 安装前端依赖

```powershell
# 使用 npm
npm install

# 或使用 yarn
yarn install

# 或使用 pnpm（推荐，更快）
pnpm install
```

#### 3. 安装 Rust 依赖

```powershell
# 进入后端目录
cd backend

# 检查依赖并下载
cargo check

# 返回项目根目录
cd ..
```

#### 4. 验证环境

```powershell
# 检查 Rust 编译
cargo check --manifest-path backend/Cargo.toml

# 检查 TypeScript 类型
npm run lint

# 如果以上命令都成功，环境配置完成！
```

### 环境变量配置（可选）

#### Rust 编译加速

```powershell
# 设置 Cargo 镜像（中国大陆用户）
# 编辑 %USERPROFILE%\.cargo\config.toml

[source.crates-io]
replace-with = 'ustc'

[source.ustc]
registry = "https://mirrors.ustc.edu.cn/crates.io-index"
```

#### Node.js 镜像加速

```powershell
# 设置 npm 镜像（中国大陆用户）
npm config set registry https://registry.npmmirror.com
```

---

## 构建和调试

### 开发模式

#### 启动开发服务器

**方式 1: 使用 npm 脚本（推荐）**

```powershell
# 启动 Tauri 开发模式（前端 + 后端热重载）
npm run tauri:dev
```

**方式 2: 分步启动**

```powershell
# 终端 1: 启动前端开发服务器
npm run dev

# 终端 2: 启动 Tauri 应用
cd backend
cargo tauri dev
```

#### 开发模式特性

- ✅ **前端热重载**: 修改 React 组件后自动刷新
- ✅ **后端热重载**: 修改 Rust 代码后自动重新编译
- ✅ **开发者工具**: 按 `F12` 打开 Chrome DevTools
- ✅ **日志输出**: 终端显示 Rust 日志和前端日志

#### 调试技巧

**前端调试**:

```typescript
// 在代码中添加断点
console.log('调试信息:', data);

// 使用 Chrome DevTools
// 1. 按 F12 打开开发者工具
// 2. 切换到 Sources 标签
// 3. 设置断点并刷新页面
```

**后端调试**:

```rust
// 在代码中添加日志
log::info!("服务启动成功: {}", server_info.id);
log::error!("端口 {} 不可用", port);

// 使用 dbg! 宏快速调试
dbg!(&server_config);
```

**Rust 调试器（VS Code）**:

1. 安装 `CodeLLDB` 扩展
2. 在 `.vscode/launch.json` 中配置：

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "lldb",
      "request": "launch",
      "name": "Tauri Development Debug",
      "cargo": {
        "args": [
          "build",
          "--manifest-path=backend/Cargo.toml",
          "--no-default-features"
        ]
      },
      "cwd": "${workspaceFolder}"
    }
  ]
}
```

### 生产构建

#### 构建可执行文件

**完整构建命令**:

```powershell
# 构建生产版本（包含前端构建 + Rust 编译 + 打包）
npm run tauri:build
```

**构建过程**:

1. **前端构建**: `npm run build` → 生成 `dist/` 目录
2. **Rust 编译**: `cargo build --release` → 生成优化的二进制文件
3. **打包**: Tauri CLI 打包成 `.exe` 和 `.msi` 安装包
4. **后处理**: 执行 `scripts/post-build.ps1` 复制文件

**构建产物位置**:

```
backend/target/release/
├── prism-local-server-tauri.exe     # 可执行文件
└── bundle/
    └── msi/
        └── Prism Local Server_3.0.0_x64_en-US.msi  # 安装包
```

#### 构建优化配置

在 `backend/Cargo.toml` 中已配置：

```toml
[profile.release]
opt-level = "z"        # 优化体积（最小化）
lto = true             # 启用链接时优化
codegen-units = 1      # 单个代码生成单元（更好的优化）
strip = true           # 移除调试符号
panic = "abort"        # Panic 时直接终止（减小体积）
```

**优化效果**:
- 体积: 从 ~15MB 减少到 4.7MB
- 启动速度: 冷启动 < 1.5 秒
- 内存占用: 空闲状态 < 40MB

#### 仅构建前端

```powershell
# 仅构建前端（用于测试前端构建）
npm run build

# 预览前端构建产物
npm run preview
```

#### 仅编译 Rust 后端

```powershell
# 开发模式编译（快速，包含调试信息）
cargo build --manifest-path backend/Cargo.toml

# 生产模式编译（优化，体积小）
cargo build --release --manifest-path backend/Cargo.toml
```

### 代码检查

#### TypeScript 类型检查

```powershell
# 检查 TypeScript 类型错误
npm run lint

# 等同于
tsc --noEmit
```

#### Rust 代码检查

```powershell
# 检查 Rust 代码（不生成二进制文件，速度快）
cargo check --manifest-path backend/Cargo.toml

# 运行 Clippy（Rust 代码质量检查工具）
cargo clippy --manifest-path backend/Cargo.toml

# 格式化 Rust 代码
cargo fmt --manifest-path backend/Cargo.toml
```

#### 前端代码格式化

```powershell
# 如果配置了 Prettier
npx prettier --write "frontend/**/*.{ts,tsx,css}"
```

### 测试

#### 功能测试

```powershell
# 运行功能测试脚本
cd tests
.\run_functional_tests.ps1

# 或使用 CMD
.\run_functional_tests.bat
```

#### 性能测试

```powershell
# 运行性能测试脚本
cd tests
.\simple_performance_test.ps1

# 或运行完整性能测试
.\performance_test.ps1
```

#### 边界测试

```powershell
# 运行边界测试脚本
cd tests
.\run_boundary_tests.ps1
```

#### Rust 单元测试

```powershell
# 运行 Rust 单元测试
cargo test --manifest-path backend/Cargo.toml

# 运行特定测试
cargo test --manifest-path backend/Cargo.toml test_port_availability
```

### 常用命令速查

| 命令 | 说明 |
|------|------|
| `npm run dev` | 启动前端开发服务器 |
| `npm run tauri:dev` | 启动 Tauri 开发模式（推荐） |
| `npm run build` | 构建前端 |
| `npm run tauri:build` | 构建生产版本 |
| `npm run lint` | TypeScript 类型检查 |
| `cargo check` | Rust 代码检查 |
| `cargo clippy` | Rust 代码质量检查 |
| `cargo fmt` | Rust 代码格式化 |
| `cargo test` | 运行 Rust 测试 |

---

## 技术架构

### 整体架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                         用户界面层                                │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  React 18 + TypeScript + Tailwind CSS + Shadcn/ui       │   │
│  │  - Dashboard.tsx (主仪表盘)                              │   │
│  │  - ServerCard.tsx (服务卡片)                             │   │
│  │  - SettingsDialog.tsx (设置对话框)                       │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↕ (Tauri IPC)
┌─────────────────────────────────────────────────────────────────┐
│                      状态管理层 (Zustand)                         │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  useServerStore (服务状态)                                │   │
│  │  useConfigStore (配置状态)                                │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↕ (invoke/emit)
┌─────────────────────────────────────────────────────────────────┐
│                      Tauri IPC 通信层                             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Commands (IPC 命令处理器)                                │   │
│  │  - start_server, stop_server, restart_server             │   │
│  │  - load_config, save_config                              │   │
│  │  - scan_html_files, select_directory                     │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                      Rust 业务逻辑层                              │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  ServerManager (服务管理器)                               │   │
│  │  - 管理多个 HTTP 服务实例                                 │   │
│  │  - 使用 Arc<Mutex<HashMap>> 存储服务                      │   │
│  │                                                            │   │
│  │  ConfigManager (配置管理器)                               │   │
│  │  - 加载/保存配置文件                                       │   │
│  │  - 配置验证                                                │   │
│  │                                                            │   │
│  │  PortManager (端口管理器)                                 │   │
│  │  - 端口可用性检测                                          │   │
│  │  - 端口自动递增                                            │   │
│  │                                                            │   │
│  │  NetworkUtils (网络工具)                                  │   │
│  │  - 获取本机 IP 地址                                        │   │
│  │  - 局域网地址生成                                          │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                   HTTP 服务层 (Axum + Tokio)                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Axum Router                                              │   │
│  │  - 静态文件路由                                            │   │
│  │  - CORS 中间件                                             │   │
│  │  - Trace 中间件                                            │   │
│  │                                                            │   │
│  │  StaticFileHandler (静态文件处理器)                       │   │
│  │  - 文件路径解析                                            │   │
│  │  - MIME 类型检测                                           │   │
│  │  - Range Request 处理                                      │   │
│  │  - 零拷贝文件流传输                                        │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                         系统层                                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  文件系统 (tokio::fs)                                      │   │
│  │  网络接口 (TcpListener, TcpStream)                        │   │
│  │  系统托盘 (Tauri tray-icon)                                │   │
│  │  默认浏览器 (Tauri Shell 插件)                             │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 前后端通信流程

#### 启动服务流程

```
用户点击"启动服务"按钮
    ↓
Dashboard.tsx 调用 useServerStore.startServer()
    ↓
Zustand Store 调用 invoke('start_server', { config })
    ↓
Tauri IPC 传递到 Rust 后端
    ↓
server_commands.rs 处理 start_server 命令
    ↓
ServerManager.start_server()
    ↓
1. PortManager 检查端口可用性
2. 如果端口被占用，自动递增端口号
3. 创建 Axum Router 和静态文件处理器
4. 使用 tokio::spawn 启动异步服务
5. 保存服务实例到 HashMap
6. 生成 ServerInfo（包含本地和局域网地址）
    ↓
返回 ServerInfo 到前端
    ↓
Zustand Store 更新 servers 数组
    ↓
Dashboard 重新渲染，显示新服务卡片
    ↓
如果配置了自动打开浏览器，调用 Tauri Shell 插件打开浏览器
```

#### HTTP 请求处理流程

```
浏览器请求 http://localhost:8888/css/style.css
    ↓
Axum Router 接收请求
    ↓
StaticFileHandler.handle_static_file()
    ↓
1. 解析 URI，提取文件路径 "/css/style.css"
2. URL 解码（处理中文文件名和空格）
3. 拼接完整路径: {root_dir}/css/style.css
4. 安全检查：防止目录遍历攻击
5. 检查文件是否存在
6. 检测 MIME 类型: "text/css"
7. 检查是否有 Range 请求头
    ↓
如果有 Range 头:
    ↓
    RangeHandler.handle_range_request()
    ↓
    1. 解析 Range 头（如 "bytes=0-1023"）
    2. 打开文件，seek 到指定位置
    3. 读取指定范围的数据
    4. 返回 206 Partial Content 响应
    ↓
如果没有 Range 头:
    ↓
    1. 使用 tokio::fs::File 打开文件
    2. 使用 ReaderStream 创建零拷贝流
    3. 设置响应头（Content-Type, Content-Length）
    4. 返回 200 OK 响应
    ↓
浏览器接收响应，渲染 CSS 样式
```

### 并发模型

#### Tokio 异步运行时

```rust
// 主线程运行 Tauri 事件循环
fn main() {
    tauri::Builder::default()
        .setup(|app| {
            // 初始化 ServerManager（包含 Tokio Runtime）
            let server_manager = ServerManager::new();
            app.manage(server_manager);
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

// 每个服务实例运行在独立的 Tokio 任务中
pub async fn start_server(&self, config: ServerConfig) -> Result<ServerInfo> {
    // ...
    
    // 启动 Axum 服务器（异步任务）
    let server_handle = tokio::spawn(async move {
        axum::serve(listener, app)
            .await
            .expect("服务器运行失败");
    });
    
    // 保存服务实例
    let instance = ServerInstance {
        info: server_info.clone(),
        abort_handle: server_handle.abort_handle(),
        server_handle,
    };
    
    // ...
}
```

#### 多服务并发管理

```rust
// 使用 Arc<Mutex<HashMap>> 管理多个服务实例
pub struct ServerManager {
    servers: Arc<Mutex<HashMap<String, ServerInstance>>>,
}

// 每个服务实例包含：
pub struct ServerInstance {
    pub info: ServerInfo,              // 服务信息
    pub abort_handle: AbortHandle,     // 用于停止服务
    pub server_handle: JoinHandle<()>, // 异步任务句柄
}
```

**并发特性**:
- ✅ 每个服务实例独立运行，互不干扰
- ✅ 使用 Tokio 异步 IO，高效处理并发请求
- ✅ 支持同时运行 10+ 个服务实例
- ✅ 停止服务时自动释放资源（RAII）

### 数据流转

#### 配置数据流

```
用户修改设置
    ↓
SettingsDialog.tsx 调用 useConfigStore.saveConfig()
    ↓
invoke('save_app_config', { config })
    ↓
config_commands.rs 处理 save_app_config 命令
    ↓
ConfigManager.save_config()
    ↓
1. 验证配置（端口范围、目录存在性）
2. 序列化为 JSON
3. 写入配置文件（使用 Tauri FS 插件）
    ↓
返回成功/失败到前端
    ↓
Zustand Store 更新 config 状态
    ↓
SettingsDialog 显示保存成功提示
```

#### 服务状态同步

```
后端服务状态变化
    ↓
ServerManager 更新内部状态
    ↓
前端定期调用 invoke('list_servers')
    ↓
返回最新的服务列表
    ↓
Zustand Store 更新 servers 数组
    ↓
Dashboard 重新渲染，显示最新状态
```

**注意**: 当前版本使用轮询方式同步状态。未来可以使用 Tauri Events 实现推送式更新。

---

## API 文档

### Tauri IPC 命令

所有 IPC 命令通过 `invoke()` 调用，返回 `Promise`。

#### 服务管理命令

##### `start_server`

启动一个新的 HTTP 服务实例。

**TypeScript 签名**:
```typescript
invoke<ServerInfo>('start_server', { config: ServerConfig }): Promise<ServerInfo>
```

**参数**:
```typescript
interface ServerConfig {
  port?: number;        // 端口号（可选，默认 8888）
  directory?: string;   // 部署目录（可选，默认当前目录）
  entryFile?: string;   // 入口文件（可选，默认 index.html）
}
```

**返回值**:
```typescript
interface ServerInfo {
  id: string;           // 服务唯一标识符（UUID）
  name: string;         // 服务名称（从目录提取）
  port: number;         // 实际使用的端口号
  directory: string;    // 部署目录路径
  entryFile: string;    // 入口 HTML 文件名
  status: 'running' | 'stopped';  // 运行状态
  startTime: number;    // 启动时间戳（毫秒）
  localUrl: string;     // 本地访问地址
  lanUrls: string[];    // 局域网访问地址列表
}
```

**错误**:
- `"端口 {port} 不可用"` - 端口被占用且无法找到可用端口
- `"目录不存在: {directory}"` - 指定的目录不存在
- `"入口文件不存在: {entry_file}"` - 指定的入口文件不存在
- `"端口 {port} 超出有效范围 (1024-65535)"` - 端口号无效

**示例**:
```typescript
try {
  const serverInfo = await invoke<ServerInfo>('start_server', {
    config: {
      port: 8888,
      directory: 'C:\\Users\\User\\Documents\\my-site',
      entryFile: 'index.html'
    }
  });
  console.log('服务启动成功:', serverInfo);
} catch (error) {
  console.error('启动失败:', error);
}
```

---

##### `stop_server`

停止指定的 HTTP 服务实例。

**TypeScript 签名**:
```typescript
invoke<void>('stop_server', { serverId: string }): Promise<void>
```

**参数**:
- `serverId`: 服务唯一标识符（从 `ServerInfo.id` 获取）

**返回值**: 无（成功时返回 `undefined`）

**错误**:
- `"服务 {server_id} 未找到"` - 指定的服务不存在

**示例**:
```typescript
try {
  await invoke('stop_server', { serverId: 'abc-123-def-456' });
  console.log('服务停止成功');
} catch (error) {
  console.error('停止失败:', error);
}
```

---

##### `restart_server`

重启指定的 HTTP 服务实例。

**TypeScript 签名**:
```typescript
invoke<ServerInfo>('restart_server', { serverId: string }): Promise<ServerInfo>
```

**参数**:
- `serverId`: 服务唯一标识符

**返回值**: 新的 `ServerInfo`（包含新的启动时间和可能变化的端口）

**错误**:
- `"服务 {server_id} 未找到"` - 指定的服务不存在
- 其他错误同 `start_server`

**示例**:
```typescript
try {
  const newServerInfo = await invoke<ServerInfo>('restart_server', {
    serverId: 'abc-123-def-456'
  });
  console.log('服务重启成功:', newServerInfo);
} catch (error) {
  console.error('重启失败:', error);
}
```

---

##### `list_servers`

获取所有运行中的服务实例列表。

**TypeScript 签名**:
```typescript
invoke<ServerInfo[]>('list_servers'): Promise<ServerInfo[]>
```

**参数**: 无

**返回值**: `ServerInfo[]` 数组

**错误**: 无（总是返回数组，可能为空）

**示例**:
```typescript
const servers = await invoke<ServerInfo[]>('list_servers');
console.log('当前运行的服务:', servers);
```

---

#### 配置管理命令

##### `load_app_config`

加载应用配置。

**TypeScript 签名**:
```typescript
invoke<AppConfig>('load_app_config'): Promise<AppConfig>
```

**参数**: 无

**返回值**:
```typescript
interface AppConfig {
  defaultPort: number;           // 默认端口号
  defaultDirectory: string;      // 默认部署目录
  defaultEntryFile: string;      // 默认入口文件
  theme: 'system' | 'dark' | 'light';  // 主题设置
  autoOpenBrowser: boolean;      // 是否自动打开浏览器
  minimizeToTray: boolean;       // 是否最小化到托盘
  isDirectoryUserSet: boolean;   // 目录是否由用户手动设置
}
```

**错误**: 无（如果配置文件不存在，返回默认配置）

**示例**:
```typescript
const config = await invoke<AppConfig>('load_app_config');
console.log('当前配置:', config);
```

---

##### `save_app_config`

保存应用配置。

**TypeScript 签名**:
```typescript
invoke<void>('save_app_config', { config: AppConfig }): Promise<void>
```

**参数**:
- `config`: 完整的 `AppConfig` 对象

**返回值**: 无

**错误**:
- `"配置验证失败: {reason}"` - 配置验证失败
- `"IO 错误: {error}"` - 文件写入失败

**示例**:
```typescript
try {
  await invoke('save_app_config', {
    config: {
      defaultPort: 8888,
      defaultDirectory: 'C:\\Users\\User\\Documents',
      defaultEntryFile: 'index.html',
      theme: 'dark',
      autoOpenBrowser: true,
      minimizeToTray: true,
      isDirectoryUserSet: true
    }
  });
  console.log('配置保存成功');
} catch (error) {
  console.error('保存失败:', error);
}
```

---

#### 网络工具命令

##### `check_port_availability`

检查指定端口是否可用。

**TypeScript 签名**:
```typescript
invoke<boolean>('check_port_availability', { port: number }): Promise<boolean>
```

**参数**:
- `port`: 要检查的端口号（1024-65535）

**返回值**: `true` 表示端口可用，`false` 表示端口被占用

**错误**:
- `"端口 {port} 超出有效范围 (1024-65535)"` - 端口号无效

**示例**:
```typescript
const isAvailable = await invoke<boolean>('check_port_availability', {
  port: 8888
});
console.log('端口 8888 可用:', isAvailable);
```

---

##### `get_lan_ip`

获取本机局域网 IP 地址列表。

**TypeScript 签名**:
```typescript
invoke<string[]>('get_lan_ip'): Promise<string[]>
```

**参数**: 无

**返回值**: IP 地址字符串数组（如 `["192.168.1.100", "10.0.0.50"]`）

**错误**: 无（如果无法获取 IP，返回空数组）

**示例**:
```typescript
const lanIps = await invoke<string[]>('get_lan_ip');
console.log('局域网 IP:', lanIps);
```

---

#### 文件系统命令

##### `select_directory`

打开目录选择对话框。

**TypeScript 签名**:
```typescript
invoke<string | null>('select_directory'): Promise<string | null>
```

**参数**: 无

**返回值**: 
- 用户选择的目录路径（字符串）
- 如果用户取消选择，返回 `null`

**错误**: 无

**示例**:
```typescript
const directory = await invoke<string | null>('select_directory');
if (directory) {
  console.log('用户选择的目录:', directory);
} else {
  console.log('用户取消了选择');
}
```

---

##### `scan_html_files`

扫描指定目录下的 HTML 文件。

**TypeScript 签名**:
```typescript
invoke<string[]>('scan_html_files', { directory: string }): Promise<string[]>
```

**参数**:
- `directory`: 要扫描的目录路径

**返回值**: HTML 文件名数组（如 `["index.html", "messages.html", "about.html"]`）

**错误**:
- `"目录不存在: {directory}"` - 指定的目录不存在

**示例**:
```typescript
try {
  const htmlFiles = await invoke<string[]>('scan_html_files', {
    directory: 'C:\\Users\\User\\Documents\\my-site'
  });
  console.log('找到的 HTML 文件:', htmlFiles);
} catch (error) {
  console.error('扫描失败:', error);
}
```

---

### HTTP API（静态文件服务器）

#### 获取静态文件

**请求**:
```
GET http://localhost:{port}/{file_path}
```

**示例**:
```
GET http://localhost:8888/index.html
GET http://localhost:8888/css/style.css
GET http://localhost:8888/images/photo.jpg
GET http://localhost:8888/videos/movie.mp4
```

**响应头**:
- `Content-Type`: 根据文件扩展名自动检测（如 `text/html`, `text/css`, `image/jpeg`）
- `Content-Length`: 文件大小（字节）
- `Accept-Ranges`: `bytes`（表示支持 Range Request）

**状态码**:
- `200 OK`: 文件成功返回
- `206 Partial Content`: Range Request 成功返回部分内容
- `404 Not Found`: 文件不存在
- `403 Forbidden`: 目录遍历攻击被阻止
- `500 Internal Server Error`: 服务器内部错误

---

#### Range Request（视频拖拽播放）

**请求**:
```
GET http://localhost:{port}/{file_path}
Range: bytes={start}-{end}
```

**示例**:
```
# 请求前 1024 字节
GET http://localhost:8888/videos/movie.mp4
Range: bytes=0-1023

# 请求从 1024 字节到文件末尾
GET http://localhost:8888/videos/movie.mp4
Range: bytes=1024-

# 请求最后 500 字节
GET http://localhost:8888/videos/movie.mp4
Range: bytes=-500
```

**响应头**:
- `Content-Type`: 文件 MIME 类型
- `Content-Length`: 返回的字节数
- `Content-Range`: `bytes {start}-{end}/{total_size}`
- `Accept-Ranges`: `bytes`

**状态码**:
- `206 Partial Content`: Range Request 成功
- `416 Range Not Satisfiable`: Range 超出文件大小

---

### 支持的 MIME 类型

| 文件扩展名 | MIME 类型 | 说明 |
|-----------|-----------|------|
| `.html` | `text/html` | HTML 文档 |
| `.css` | `text/css` | CSS 样式表 |
| `.js` | `application/javascript` | JavaScript 脚本 |
| `.json` | `application/json` | JSON 数据 |
| `.png` | `image/png` | PNG 图片 |
| `.jpg`, `.jpeg` | `image/jpeg` | JPEG 图片 |
| `.gif` | `image/gif` | GIF 图片 |
| `.svg` | `image/svg+xml` | SVG 矢量图 |
| `.webp` | `image/webp` | WebP 图片 |
| `.mp4` | `video/mp4` | MP4 视频 |
| `.webm` | `video/webm` | WebM 视频 |
| `.mov` | `video/quicktime` | QuickTime 视频 |
| `.mp3` | `audio/mpeg` | MP3 音频 |
| `.wav` | `audio/wav` | WAV 音频 |
| `.pdf` | `application/pdf` | PDF 文档 |
| `.txt` | `text/plain` | 纯文本 |
| `.woff`, `.woff2` | `font/woff`, `font/woff2` | Web 字体 |

**注意**: 
- 大小写混合的扩展名（如 `.MP4`, `.MOV`）也会被正确识别
- 未知扩展名默认使用 `application/octet-stream`

---

## 前端组件

### 组件层次结构

```
App.tsx (根组件)
├── Dashboard.tsx (主仪表盘)
│   ├── ServerCard.tsx (服务卡片) × N
│   └── SettingsDialog.tsx (设置对话框)
└── Toaster (Toast 提示组件)
```

### 核心组件详解

#### Dashboard.tsx

**职责**: 主仪表盘，显示服务列表和操作按钮

**Props**: 无

**State**:
```typescript
// 从 Zustand Store 获取
const { servers, isLoading, startServer, refreshServerList } = useServerStore();
const { config } = useConfigStore();
```

**主要功能**:
1. 显示"启动服务"按钮
2. 显示所有运行中的服务卡片
3. 处理启动服务逻辑（目录选择、端口检测、HTML 文件扫描）
4. 显示 Toast 提示信息

**关键代码片段**:
```typescript
const handleStartServer = async () => {
  // 1. 选择目录
  const directory = await invoke<string | null>('select_directory');
  if (!directory) return;

  // 2. 扫描 HTML 文件
  const htmlFiles = await invoke<string[]>('scan_html_files', { directory });
  
  // 3. 确定入口文件
  const entryFile = htmlFiles.find(f => 
    f === 'index.html' || f === 'messages.html'
  ) || htmlFiles[0] || 'index.html';

  // 4. 启动服务
  const serverInfo = await startServer({
    port: config?.defaultPort || 8888,
    directory,
    entryFile
  });

  // 5. 显示成功提示
  toast({
    title: '服务启动成功',
    description: `端口: ${serverInfo.port}`
  });
};
```

**样式特点**:
- 使用 Framer Motion 实现卡片进入动画
- 毛玻璃效果背景（`glass` 类）
- 响应式 Grid 布局（`grid-cols-1 md:grid-cols-2 lg:grid-cols-3`）

---

#### ServerCard.tsx

**职责**: 显示单个服务实例的信息和操作按钮

**Props**:
```typescript
interface ServerCardProps {
  server: ServerInfo;
  onStop: (serverId: string) => void;
  onRestart: (serverId: string) => void;
}
```

**主要功能**:
1. 显示服务基本信息（名称、端口、目录）
2. 显示运行时长（实时更新）
3. 显示本地和局域网访问地址
4. 提供停止、重启、复制链接按钮

**运行时长计算**:
```typescript
const [uptime, setUptime] = useState('00:00:00');

useEffect(() => {
  const timer = setInterval(() => {
    const now = Date.now();
    const diff = now - server.startTime;
    const hours = Math.floor(diff / 3600000);
    const minutes = Math.floor((diff % 3600000) / 60000);
    const seconds = Math.floor((diff % 60000) / 1000);
    setUptime(`${pad(hours)}:${pad(minutes)}:${pad(seconds)}`);
  }, 1000);

  return () => clearInterval(timer);
}, [server.startTime]);
```

**样式特点**:
- 卡片悬停效果（`hover:shadow-xl transition-all`）
- 状态指示器（绿色圆点表示运行中）
- 按钮组布局（停止、重启、复制）

---

#### SettingsDialog.tsx

**职责**: 设置对话框，配置默认参数

**Props**:
```typescript
interface SettingsDialogProps {
  isOpen: boolean;
  onClose: () => void;
}
```

**主要功能**:
1. 修改默认端口号
2. 修改默认部署目录
3. 修改默认入口文件名
4. 切换主题（系统/深色/浅色）
5. 切换自动打开浏览器
6. 切换最小化到托盘

**表单验证**:
```typescript
const handleSave = async () => {
  // 验证端口范围
  if (port < 1024 || port > 65535) {
    toast({
      title: '端口号无效',
      description: '端口号必须在 1024-65535 范围内',
      variant: 'destructive'
    });
    return;
  }

  // 保存配置
  await saveConfig({
    defaultPort: port,
    defaultDirectory: directory,
    defaultEntryFile: entryFile,
    theme,
    autoOpenBrowser,
    minimizeToTray,
    isDirectoryUserSet: true
  });

  toast({
    title: '设置已保存',
    description: '配置已成功保存'
  });
};
```

**样式特点**:
- 使用 Radix UI Dialog 组件
- 表单布局清晰，标签和输入框对齐
- 保存和取消按钮分离

---

### Shadcn/ui 基础组件

#### Button

**用法**:
```typescript
import { Button } from '@/components/ui/button';

<Button variant="default" size="default" onClick={handleClick}>
  启动服务
</Button>
```

**变体**:
- `default`: 默认样式（蓝色背景）
- `destructive`: 危险操作（红色背景）
- `outline`: 轮廓样式（透明背景，边框）
- `ghost`: 幽灵样式（透明背景，无边框）
- `link`: 链接样式（无背景，下划线）

**尺寸**:
- `default`: 默认尺寸
- `sm`: 小尺寸
- `lg`: 大尺寸
- `icon`: 图标按钮（正方形）

---

#### Card

**用法**:
```typescript
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

<Card>
  <CardHeader>
    <CardTitle>服务名称</CardTitle>
  </CardHeader>
  <CardContent>
    <p>服务内容</p>
  </CardContent>
</Card>
```

---

#### Dialog

**用法**:
```typescript
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';

<Dialog open={isOpen} onOpenChange={setIsOpen}>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>设置</DialogTitle>
    </DialogHeader>
    <div>对话框内容</div>
  </DialogContent>
</Dialog>
```

---

#### Input

**用法**:
```typescript
import { Input } from '@/components/ui/input';

<Input
  type="number"
  value={port}
  onChange={(e) => setPort(Number(e.target.value))}
  placeholder="8888"
/>
```

---

#### Switch

**用法**:
```typescript
import { Switch } from '@/components/ui/switch';

<Switch
  checked={autoOpenBrowser}
  onCheckedChange={setAutoOpenBrowser}
/>
```

---

#### Toast

**用法**:
```typescript
import { useToast } from '@/hooks/use-toast';

const { toast } = useToast();

toast({
  title: '操作成功',
  description: '服务已启动',
  variant: 'default' // 或 'destructive'
});
```

---

### 样式系统

#### Tailwind CSS 配置

**主题色**:
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        primary: 'hsl(var(--primary))',
        secondary: 'hsl(var(--secondary))',
        // ...
      }
    }
  }
}
```

**自定义类**:
```css
/* index.css */
.glass {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.card-shadow {
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}
```

#### 响应式设计

**断点**:
- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px
- `2xl`: 1536px

**示例**:
```typescript
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {/* 移动端 1 列，平板 2 列，桌面 3 列 */}
</div>
```

---

## 状态管理

### Zustand Store

项目使用 Zustand 进行轻量级状态管理，相比 Redux 更简洁易用。

#### useServerStore

**职责**: 管理服务实例的状态和操作

**State**:
```typescript
interface ServerStore {
  servers: ServerInfo[];      // 服务列表
  isLoading: boolean;         // 加载状态
  error: string | null;       // 错误信息
}
```

**Actions**:
```typescript
interface ServerStore {
  fetchServers: () => Promise<void>;                    // 获取服务列表
  startServer: (config: ServerConfig) => Promise<ServerInfo>;  // 启动服务
  stopServer: (serverId: string) => Promise<void>;      // 停止服务
  restartServer: (serverId: string) => Promise<void>;   // 重启服务
  refreshServerList: () => Promise<void>;               // 刷新服务列表
  setError: (error: string | null) => void;             // 设置错误
}
```

**实现细节**:
```typescript
export const useServerStore = create<ServerStore>((set, get) => ({
  servers: [],
  isLoading: false,
  error: null,

  startServer: async (config: ServerConfig) => {
    set({ isLoading: true, error: null });
    try {
      const serverInfo = await invoke<ServerInfo>('start_server', { config });
      set((state) => ({
        servers: [...state.servers, serverInfo],
        isLoading: false,
      }));
      return serverInfo;
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      set({ error: errorMsg, isLoading: false });
      throw error;
    }
  },

  // ... 其他 actions
}));
```

**使用示例**:
```typescript
// 在组件中使用
const { servers, isLoading, startServer, stopServer } = useServerStore();

// 启动服务
const handleStart = async () => {
  try {
    await startServer({ port: 8888, directory: '/path/to/dir' });
  } catch (error) {
    console.error('启动失败:', error);
  }
};

// 停止服务
const handleStop = async (serverId: string) => {
  try {
    await stopServer(serverId);
  } catch (error) {
    console.error('停止失败:', error);
  }
};
```

---

#### useConfigStore

**职责**: 管理应用配置的状态和操作

**State**:
```typescript
interface ConfigStore {
  config: AppConfig | null;   // 应用配置
  isLoading: boolean;         // 加载状态
  error: string | null;       // 错误信息
}
```

**Actions**:
```typescript
interface ConfigStore {
  loadConfig: () => Promise<void>;                  // 加载配置
  saveConfig: (config: AppConfig) => Promise<void>; // 保存配置
  updateConfig: (partial: Partial<AppConfig>) => void;  // 更新部分配置
  setError: (error: string | null) => void;         // 设置错误
}
```

**实现细节**:
```typescript
export const useConfigStore = create<ConfigStore>((set, get) => ({
  config: null,
  isLoading: false,
  error: null,

  loadConfig: async () => {
    set({ isLoading: true, error: null });
    try {
      const config = await invoke<AppConfig>('load_app_config');
      set({ config, isLoading: false });
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      set({ error: errorMsg, isLoading: false });
    }
  },

  saveConfig: async (config: AppConfig) => {
    set({ isLoading: true, error: null });
    try {
      await invoke('save_app_config', { config });
      set({ config, isLoading: false });
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      set({ error: errorMsg, isLoading: false });
      throw error;
    }
  },

  updateConfig: (partial: Partial<AppConfig>) => {
    set((state) => ({
      config: state.config ? { ...state.config, ...partial } : null
    }));
  },
}));
```

**使用示例**:
```typescript
// 在组件中使用
const { config, loadConfig, saveConfig } = useConfigStore();

// 加载配置
useEffect(() => {
  loadConfig();
}, []);

// 保存配置
const handleSave = async () => {
  try {
    await saveConfig({
      ...config!,
      defaultPort: 9000
    });
  } catch (error) {
    console.error('保存失败:', error);
  }
};
```

---

### 状态持久化

#### 配置持久化

配置通过 Rust 后端保存到本地 JSON 文件：

**配置文件位置**:
```
Windows: C:\Users\{用户名}\AppData\Roaming\com.kkwans.prism-local-server\config.json
```

**配置文件格式**:
```json
{
  "defaultPort": 8888,
  "defaultDirectory": "C:\\Users\\User\\Documents",
  "defaultEntryFile": "index.html",
  "theme": "dark",
  "autoOpenBrowser": true,
  "minimizeToTray": true,
  "isDirectoryUserSet": true
}
```

#### 服务状态持久化

服务状态**不持久化**，应用关闭后所有服务自动停止。这是设计决策，原因：
1. 避免端口占用冲突
2. 确保资源正确释放
3. 简化状态管理逻辑

---

### 状态同步策略

#### 轮询同步（当前实现）

```typescript
// Dashboard.tsx
useEffect(() => {
  // 初始加载
  refreshServerList();

  // 定期刷新（可选）
  const interval = setInterval(() => {
    refreshServerList();
  }, 5000); // 每 5 秒刷新一次

  return () => clearInterval(interval);
}, []);
```

**优点**:
- 实现简单
- 状态一致性高

**缺点**:
- 有轮询开销
- 实时性稍差

#### 事件驱动同步（未来优化）

使用 Tauri Events 实现推送式更新：

```typescript
// 后端推送事件
app.emit_all("server-started", &server_info)?;
app.emit_all("server-stopped", &server_id)?;

// 前端监听事件
import { listen } from '@tauri-apps/api/event';

useEffect(() => {
  const unlisten1 = listen<ServerInfo>('server-started', (event) => {
    // 添加新服务到列表
    set((state) => ({
      servers: [...state.servers, event.payload]
    }));
  });

  const unlisten2 = listen<string>('server-stopped', (event) => {
    // 从列表中移除服务
    set((state) => ({
      servers: state.servers.filter(s => s.id !== event.payload)
    }));
  });

  return () => {
    unlisten1.then(fn => fn());
    unlisten2.then(fn => fn());
  };
}, []);
```

**优点**:
- 实时性高
- 无轮询开销

**缺点**:
- 实现复杂
- 需要处理事件丢失

---

## 性能优化

### Rust 后端优化

#### 1. 编译优化

**Release 配置** (`backend/Cargo.toml`):
```toml
[profile.release]
opt-level = "z"        # 优化体积（最小化）
lto = true             # 启用链接时优化（Link Time Optimization）
codegen-units = 1      # 单个代码生成单元（更好的优化）
strip = true           # 移除调试符号
panic = "abort"        # Panic 时直接终止（减小体积）
```

**优化效果**:
- 体积: 从 ~15MB 减少到 4.7MB（减少 68%）
- 启动速度: 冷启动 < 1.5 秒
- 内存占用: 空闲状态 < 40MB

#### 2. 零拷贝文件传输

使用 `tokio::fs` 和 `ReaderStream` 实现零拷贝：

```rust
use tokio::fs::File;
use tokio_util::io::ReaderStream;

// 打开文件
let file = File::open(&file_path).await?;

// 创建零拷贝流
let stream = ReaderStream::new(file);

// 直接返回流，无需加载到内存
let body = Body::from_stream(stream);
```

**优点**:
- 大文件不占用内存
- 传输速度快
- 支持并发请求

#### 3. 异步并发

使用 Tokio 异步运行时：

```rust
// 每个服务实例运行在独立的异步任务中
let server_handle = tokio::spawn(async move {
    axum::serve(listener, app)
        .await
        .expect("服务器运行失败");
});
```

**优点**:
- 支持 10+ 并发服务实例
- 单线程处理多个请求
- 资源占用低

#### 4. 端口检测优化

使用超时机制避免阻塞：

```rust
use tokio::time::{timeout, Duration};

pub async fn check_port_available(&self, port: u16) -> bool {
    let addr = format!("127.0.0.1:{}", port);
    
    // 50ms 超时
    let result = timeout(
        Duration::from_millis(50),
        TcpStream::connect(&addr),
    ).await;
    
    match result {
        Ok(Ok(_)) => false,  // 端口被占用
        Ok(Err(_)) => true,  // 端口可用
        Err(_) => true,      // 超时，端口可用
    }
}
```

**优点**:
- 快速检测（50ms）
- 不阻塞主线程
- 支持并发检测

---

### 前端优化

#### 1. 代码分割

Vite 自动进行代码分割：

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom'],
          'tauri-vendor': ['@tauri-apps/api'],
          'ui-vendor': ['@radix-ui/react-dialog', '@radix-ui/react-switch']
        }
      }
    }
  }
});
```

**优化效果**:
- 初始加载体积减少
- 按需加载组件
- 缓存利用率提高

#### 2. 组件优化

使用 React.memo 避免不必要的重渲染：

```typescript
import { memo } from 'react';

export const ServerCard = memo(({ server, onStop, onRestart }: ServerCardProps) => {
  // 组件实现
}, (prevProps, nextProps) => {
  // 自定义比较函数
  return prevProps.server.id === nextProps.server.id &&
         prevProps.server.status === nextProps.server.status;
});
```

#### 3. 状态更新优化

使用 Zustand 的选择器避免不必要的订阅：

```typescript
// ❌ 不推荐：订阅整个 store
const store = useServerStore();

// ✅ 推荐：只订阅需要的状态
const servers = useServerStore(state => state.servers);
const startServer = useServerStore(state => state.startServer);
```

#### 4. 动画性能优化

使用 Framer Motion 的 `layoutId` 优化动画：

```typescript
import { motion } from 'framer-motion';

<motion.div
  layoutId={server.id}
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, y: -20 }}
  transition={{ duration: 0.3 }}
>
  {/* 服务卡片内容 */}
</motion.div>
```

---

### 打包优化

#### 1. Tauri 配置优化

**最小化权限** (`backend/tauri.conf.json`):
```json
{
  "app": {
    "security": {
      "csp": null
    }
  },
  "bundle": {
    "active": true,
    "targets": "all"
  }
}
```

#### 2. 依赖优化

**移除未使用的依赖**:
```powershell
# 检查未使用的依赖
npm run depcheck

# 移除未使用的依赖
npm uninstall <package-name>
```

**使用轻量级替代品**:
- ✅ Zustand（轻量级状态管理）代替 Redux
- ✅ Tailwind CSS（按需生成）代替完整 CSS 框架
- ✅ Radix UI（无样式组件）代替完整 UI 库

#### 3. 资源优化

**图标优化**:
- 使用 PNG 格式（Windows 推荐）
- 提供多种尺寸（32x32, 128x128, 256x256）
- 压缩图标文件

**字体优化**:
- 使用系统字体（无需打包字体文件）
- 如需自定义字体，使用 WOFF2 格式

---

### 性能监控

#### 1. Rust 性能分析

使用 `cargo-flamegraph` 生成火焰图：

```powershell
# 安装 cargo-flamegraph
cargo install flamegraph

# 生成火焰图
cargo flamegraph --manifest-path backend/Cargo.toml
```

#### 2. 前端性能分析

使用 Chrome DevTools：

1. 按 `F12` 打开开发者工具
2. 切换到 `Performance` 标签
3. 点击 `Record` 开始录制
4. 执行操作（如启动服务）
5. 点击 `Stop` 停止录制
6. 分析性能瓶颈

#### 3. 内存监控

**Windows 任务管理器**:
1. 按 `Ctrl+Shift+Esc` 打开任务管理器
2. 找到 `Prism Local Server` 进程
3. 查看内存占用

**预期值**:
- 空闲状态: < 40MB
- 运行 1 个服务: < 80MB
- 运行 5 个服务: < 150MB

---

### 性能基准测试

#### 启动速度测试

```powershell
# 测量冷启动时间
Measure-Command { Start-Process "prism-local-server-v3.0.0.exe" }
```

**目标**: < 1.5 秒

#### 文件响应速度测试

```powershell
# 使用 curl 测量响应时间
Measure-Command { curl http://localhost:8888/index.html }
```

**目标**:
- 小文件（< 1MB）: < 10ms
- 大文件（> 100MB）: 首帧 < 100ms

#### 并发性能测试

```powershell
# 使用 Apache Bench 测试并发性能
ab -n 1000 -c 10 http://localhost:8888/index.html
```

**目标**:
- 支持 10+ 并发连接
- 无明显性能下降

---

### 性能优化清单

#### 后端优化

- [x] 启用 Release 优化配置
- [x] 使用零拷贝文件传输
- [x] 使用 Tokio 异步运行时
- [x] 端口检测超时机制
- [x] 移除调试符号
- [x] 启用 LTO（链接时优化）

#### 前端优化

- [x] 代码分割（Vendor Chunks）
- [x] 组件 Memo 化
- [x] 状态选择器优化
- [x] 动画性能优化
- [x] 移除未使用的依赖
- [x] 使用轻量级库

#### 打包优化

- [x] 最小化 Tauri 权限
- [x] 压缩图标资源
- [x] 使用系统字体
- [x] 移除开发依赖

---

## 常见问题

### 开发环境问题

#### Q1: Rust 编译失败，提示 "linker 'link.exe' not found"

**原因**: 缺少 C++ 编译器

**解决方案**:
```powershell
# 安装 Visual Studio Build Tools
winget install Microsoft.VisualStudio.2022.BuildTools

# 或下载安装包
# https://visualstudio.microsoft.com/downloads/
# 选择 "Desktop development with C++" 工作负载
```

---

#### Q2: npm install 失败，提示网络错误

**原因**: npm 默认源速度慢或被墙

**解决方案**:
```powershell
# 切换到国内镜像源
npm config set registry https://registry.npmmirror.com

# 重新安装
npm install
```

---

#### Q3: Tauri 开发模式启动失败

**原因**: 端口被占用或 WebView2 未安装

**解决方案**:
```powershell
# 检查端口占用
netstat -ano | findstr :1420

# 如果被占用，修改 backend/tauri.conf.json 中的 devUrl 端口

# 检查 WebView2 是否安装
# Windows 11 自带，无需安装
# 如需手动安装: https://developer.microsoft.com/microsoft-edge/webview2/
```

---

#### Q4: TypeScript 类型错误

**原因**: 类型定义不匹配或缺失

**解决方案**:
```powershell
# 重新安装依赖
rm -rf node_modules package-lock.json
npm install

# 检查 TypeScript 版本
npm list typescript

# 运行类型检查
npm run lint
```

---

### 运行时问题

#### Q5: 服务启动失败，提示 "端口不可用"

**原因**: 端口被其他程序占用

**解决方案**:
```powershell
# 查看端口占用
netstat -ano | findstr :8888

# 找到占用端口的进程 PID，然后结束进程
taskkill /PID <PID> /F

# 或在设置中修改默认端口
```

---

#### Q6: 浏览器无法访问服务

**原因**: 防火墙阻止或服务未启动

**解决方案**:
```powershell
# 检查服务是否运行
netstat -ano | findstr :8888

# 检查防火墙设置
# 控制面板 > 系统和安全 > Windows Defender 防火墙 > 允许应用通过防火墙

# 添加 Prism Local Server 到允许列表
```

---

#### Q7: 视频无法拖拽播放

**原因**: Range Request 未正确处理

**解决方案**:
1. 检查视频文件格式（支持 MP4, WebM, MOV）
2. 检查浏览器控制台是否有错误
3. 使用 Chrome DevTools Network 标签查看请求头
4. 确认响应头包含 `Accept-Ranges: bytes`

---

#### Q8: 中文文件名无法访问

**原因**: URL 编码问题

**解决方案**:
- 后端已实现 URL 解码，应该能正确处理中文文件名
- 如果仍有问题，检查文件系统编码是否为 UTF-8
- 避免使用特殊字符（如 `<>:"|?*`）

---

### 构建和打包问题

#### Q9: 构建失败，提示 "out of memory"

**原因**: 内存不足

**解决方案**:
```powershell
# 增加 Node.js 内存限制
$env:NODE_OPTIONS="--max-old-space-size=4096"

# 重新构建
npm run tauri:build
```

---

#### Q10: 打包后的 EXE 无法运行

**原因**: 缺少依赖或权限问题

**解决方案**:
1. 检查是否安装了 WebView2 运行时
2. 以管理员身份运行
3. 检查 Windows Defender 是否阻止
4. 查看日志文件（`%APPDATA%\com.kkwans.prism-local-server\logs\`）

---

#### Q11: 打包后体积过大

**原因**: 未启用优化或包含了不必要的文件

**解决方案**:
1. 检查 `backend/Cargo.toml` 中的 `[profile.release]` 配置
2. 移除未使用的依赖
3. 检查 `.gitignore` 和 `.taurignore` 配置
4. 使用 `cargo bloat` 分析体积占用

---

### 性能问题

#### Q12: 应用启动慢

**原因**: 未使用 Release 模式或磁盘 IO 慢

**解决方案**:
```powershell
# 确保使用 Release 模式构建
npm run tauri:build

# 检查磁盘性能
# 使用 SSD 而非 HDD
```

---

#### Q13: 内存占用过高

**原因**: 服务实例过多或内存泄漏

**解决方案**:
1. 减少同时运行的服务实例数量
2. 停止不需要的服务
3. 检查是否有内存泄漏（使用 Chrome DevTools Memory Profiler）
4. 重启应用

---

#### Q14: 文件加载慢

**原因**: 文件过大或网络问题

**解决方案**:
1. 检查文件大小（大文件加载慢是正常的）
2. 使用局域网访问时，检查网络速度
3. 检查是否启用了 Range Request（视频文件）
4. 优化文件（压缩图片、视频）

---

### 调试技巧

#### 查看 Rust 日志

**开发模式**:
```powershell
# 日志会输出到终端
npm run tauri:dev
```

**生产模式**:
```powershell
# 日志保存在文件中
# 位置: %APPDATA%\com.kkwans.prism-local-server\logs\prism-server.log

# 查看日志
Get-Content "$env:APPDATA\com.kkwans.prism-local-server\logs\prism-server.log" -Tail 50
```

---

#### 查看前端日志

**开发模式**:
```powershell
# 按 F12 打开 Chrome DevTools
# 切换到 Console 标签
```

**生产模式**:
```powershell
# 按 F12 打开 Chrome DevTools（如果启用了）
# 或在代码中添加 console.log
```

---

#### 网络请求调试

**使用 Chrome DevTools**:
1. 按 `F12` 打开开发者工具
2. 切换到 `Network` 标签
3. 刷新页面或执行操作
4. 查看请求和响应详情

**使用 curl**:
```powershell
# 测试 HTTP 请求
curl -v http://localhost:8888/index.html

# 测试 Range Request
curl -v -H "Range: bytes=0-1023" http://localhost:8888/video.mp4
```

---

### 获取帮助

#### 官方文档

- **Tauri 文档**: https://v2.tauri.app/
- **Rust 文档**: https://doc.rust-lang.org/
- **React 文档**: https://react.dev/
- **Tailwind CSS 文档**: https://tailwindcss.com/docs

#### 社区支持

- **GitHub Issues**: https://github.com/Kkwans/prism-local-server/issues
- **Tauri Discord**: https://discord.com/invite/tauri
- **Rust 论坛**: https://users.rust-lang.org/

#### 报告 Bug

提交 Issue 时请包含：
1. 操作系统版本（Windows 11 版本号）
2. 应用版本（v3.0.0）
3. 详细的错误描述和复现步骤
4. 错误截图或日志文件
5. 预期行为和实际行为

---

## 附录

### 项目依赖清单

#### Rust 依赖（backend/Cargo.toml）

**核心依赖**:
- `tauri` (2.10.3) - Tauri 框架
- `axum` (0.7) - HTTP 服务器框架
- `tokio` (1.x) - 异步运行时
- `serde` (1.0) - 序列化/反序列化
- `serde_json` (1.0) - JSON 支持

**插件依赖**:
- `tauri-plugin-log` (2.x) - 日志插件
- `tauri-plugin-shell` (2.x) - Shell 插件
- `tauri-plugin-dialog` (2.x) - 对话框插件
- `tauri-plugin-fs` (2.x) - 文件系统插件
- `tauri-plugin-opener` (2.5.3) - 浏览器打开插件

**工具依赖**:
- `uuid` (1.0) - UUID 生成
- `chrono` (0.4) - 时间处理
- `thiserror` (1.0) - 错误处理
- `local-ip-address` (0.6) - IP 地址获取
- `mime_guess` (2.0) - MIME 类型检测
- `urlencoding` (2.1) - URL 编码/解码

#### 前端依赖（package.json）

**核心依赖**:
- `react` (19.2.4) - React 框架
- `react-dom` (19.2.4) - React DOM
- `@tauri-apps/api` (2.10.1) - Tauri API
- `zustand` (5.0.12) - 状态管理
- `framer-motion` (12.38.0) - 动画库

**UI 依赖**:
- `@radix-ui/react-dialog` (1.1.15) - 对话框组件
- `@radix-ui/react-switch` (1.2.6) - 开关组件
- `@radix-ui/react-toast` (1.2.15) - Toast 组件
- `tailwindcss` (4.2.1) - CSS 框架
- `clsx` (2.1.1) - 类名合并
- `tailwind-merge` (3.5.0) - Tailwind 类名合并

**开发依赖**:
- `typescript` (5.9.3) - TypeScript
- `vite` (8.0.0) - 构建工具
- `@vitejs/plugin-react` (6.0.1) - React 插件
- `@tauri-apps/cli` (2.10.1) - Tauri CLI

---

### 版本历史

#### v3.0.0 (2026-03-20)

**重大变更**:
- 🎉 使用 Tauri v2 完全重写，替代 Python + Flet 版本
- 🚀 性能提升 50-70%，体积减少 80-90%
- 🎨 全新 Windows 11 Fluent Design UI

**新功能**:
- ✅ 多服务实例并发管理
- ✅ HTTP Range Request 支持
- ✅ 局域网访问支持
- ✅ 系统托盘后台运行
- ✅ 配置持久化
- ✅ 端口自动递增
- ✅ 中文文件名支持

**技术栈**:
- Rust 1.77.2 + Axum 0.7
- React 18 + TypeScript 5.9
- Tailwind CSS 4.2 + Shadcn/ui
- Tauri v2.10.3

---

### 许可证

MIT License

Copyright (c) 2026 Kkwans

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

**文档版本**: v3.0.0  
**最后更新**: 2026年3月20日  
**维护者**: Kkwans

---

**感谢使用 Prism Local Server Tauri！** 🎉
