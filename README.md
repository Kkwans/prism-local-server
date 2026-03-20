# Prism Local Server (棱镜本地服务器)

> **⚠️ 版本声明：v1 版本 - 已废弃，不再开发**
> 
> 本分支为 v1 历史版本归档（基于 Python + CustomTkinter），已停止维护和功能开发。
> 
> 请使用最新的 v3 版本（基于 Tauri v2 + Rust + React），获得更好的性能和用户体验。
> 
> - **v3 版本仓库**：[prism-local-server-tauri](https://github.com/Kkwans/prism-local-server)（main 分支）
> - **技术栈升级**：Python → Rust（后端）+ React（前端）
> - **性能提升**：内存占用减少 70%，启动速度提升 3 倍，包体积减少 80%

---

一个Windows 11桌面应用程序，用于快速将HTML静态文件部署到本地HTTP服务器，支持本地访问和局域网访问。

## 功能特性

- 🚀 一键启动HTTP服务，无需复杂配置
- 🎨 现代化GUI界面，遵循Windows 11 Fluent Design
- 🔄 支持多服务并发运行（不同端口）
- 📱 支持局域网访问，手机/平板可访问
- ⚡ 高性能资源加载，速度接近本地磁盘访问
- 🎯 智能端口管理，自动处理端口占用
- 🌙 支持浅色/深色/系统主题切换
- 📦 后台运行，系统托盘管理
- ⚙️ 可视化配置界面，简单易用

## 系统要求

- Windows 11 (22H2或更高版本)
- Python 3.11+ (开发环境)

## 快速开始

### 开发环境

1. 克隆仓库
```bash
git clone git@github.com:Kkwans/prism-local-server.git
cd prism-local-server
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行程序
```bash
python main.py
```

### 使用说明

1. 启动程序后，显示现代化GUI界面
2. 点击"选择目录"按钮选择要部署的目录（默认当前目录）
3. 点击"启动服务"按钮启动HTTP服务
4. 程序自动检测HTML文件并在浏览器中打开
5. 服务列表实时显示运行状态、运行时长、访问地址
6. 支持多个服务同时运行（不同端口）
7. 关闭窗口可选择最小化到托盘或退出程序

### 功能测试

运行GUI功能测试脚本：
```bash
python test_gui.py
```

测试覆盖：
- ✅ 模块导入（UI、核心、工具模块）
- ✅ 配置管理器（读取、保存、验证）
- ✅ 端口管理器（可用性检测、自动递增）
- ✅ 网络工具（IP获取、URL生成）

运行核心功能测试脚本：
```bash
python test_functionality.py
```

测试覆盖：
- ✅ HTTP服务器（启动、停止、请求处理）
- ✅ 多服务管理（并发运行、批量停止）
- ✅ 资源加载（CSS/JS/HTML/图片/视频）

## 打包为EXE

### 方法1：使用打包脚本（推荐）

```bash
build.bat
```

### 方法2：手动打包

```bash
pyinstaller build.spec --clean --noconfirm
```

打包完成后，EXE文件位于 `dist/PrismLocalServer/` 目录。

## 技术栈

- Python 3.11+
- CustomTkinter (现代化UI框架)
- http.server (HTTP服务)
- pystray (系统托盘)
- Pillow (图像处理)
- psutil (系统信息)
- PyInstaller (打包工具)

## 项目结构

```
prism-local-server/
├── main.py                 # 程序入口（GUI模式）
├── core/                   # 核心模块
│   ├── config_manager.py   # 配置管理
│   ├── http_server_manager.py  # HTTP服务管理
│   ├── port_manager.py     # 端口管理
│   └── resource_handler.py # 资源处理
├── ui/                     # UI模块
│   ├── main_window.py      # 主窗口
│   ├── config_dialog.py    # 配置对话框
│   └── tray_icon.py        # 系统托盘
├── utils/                  # 工具模块
│   ├── logger.py           # 日志工具
│   └── network_utils.py    # 网络工具
├── assets/                 # 资源文件
├── config/                 # 配置文件
├── logs/                   # 日志文件
├── test_gui.py             # GUI功能测试
├── test_functionality.py   # 核心功能测试
├── build.spec              # PyInstaller配置
└── build.bat               # 打包脚本
```

## 开发规范

- 代码注释使用中文
- 遵循PEP 8编码规范
- Git提交信息使用中文，格式：`[类型] 功能描述 - 细节说明`
- UI设计遵循Windows 11 Fluent Design System

## 许可证

MIT License

## 作者

Kkwans

## 更新日志

### v0.1.0 (2026-03-15)

#### 核心功能
- ✅ 项目初始化和Git仓库配置
- ✅ 实现配置管理模块（读取、保存、验证）
- ✅ 实现端口管理模块（可用性检测、自动递增）
- ✅ 实现资源处理器（相对路径适配、Range请求、TCP_NODELAY优化）
- ✅ 实现HTTP服务管理器（多服务管理、自动检测HTML、浏览器打开）
- ✅ 实现日志工具（异步输出、文件滚动）
- ✅ 实现网络工具（IP获取、URL生成）

#### GUI界面
- ✅ 实现主窗口（服务列表、快速启动、实时状态更新）
- ✅ 实现配置对话框（端口、目录、HTML文件、自动打开浏览器）
- ✅ 实现系统托盘（显示/隐藏、快速启动、退出）
- ✅ 实现主题切换（浅色/深色/系统主题）
- ✅ 实现后台运行（最小化到托盘）

#### 测试与打包
- ✅ 完成核心功能测试（所有测试通过）
- ✅ 完成GUI功能测试（所有模块导入成功）
- ✅ 创建PyInstaller打包配置
- ✅ 创建自动化打包脚本

### 测试结果
- 模块导入：✅ 通过
- 配置管理：✅ 通过
- 端口管理：✅ 通过
- 网络工具：✅ 通过
- HTTP服务器：✅ 通过（状态码200，响应正常）
- 多服务管理：✅ 通过（3个服务并发运行）
- 资源加载：✅ 通过（CSS/JS/HTML/图片/视频正常加载）
