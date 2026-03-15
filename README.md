# Prism Local Server (棱镜本地服务器)

一个Windows 11桌面应用程序，用于快速将HTML静态文件部署到本地HTTP服务器，支持本地访问和局域网访问。

## 功能特性

- 🚀 一键启动HTTP服务，无需复杂配置
- 🎨 现代化UI界面，遵循Windows 11 Fluent Design
- 🔄 支持多服务并发运行（不同端口）
- 📱 支持局域网访问，手机/平板可访问
- ⚡ 高性能资源加载，速度接近本地磁盘访问
- 🎯 智能端口管理，自动处理端口占用
- 🌙 支持浅色/深色主题切换
- 📦 后台运行，系统托盘管理

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

1. 启动程序后，默认部署当前目录
2. 程序自动检测HTML文件（优先index.html或messages.html）
3. 自动在浏览器中打开访问地址
4. 按Ctrl+C停止服务

### 功能测试

运行功能测试脚本验证所有核心功能：
```bash
python test_functionality.py
```

测试覆盖：
- ✅ 配置管理器（读取、保存、验证）
- ✅ 端口管理器（可用性检测、自动递增）
- ✅ 网络工具（IP获取、URL生成）
- ✅ HTTP服务器（启动、停止、请求处理）
- ✅ 多服务管理（并发运行、批量停止）

## 技术栈

- Python 3.11+
- CustomTkinter (UI框架)
- http.server (HTTP服务)
- pystray (系统托盘)
- PyInstaller (打包工具)

## 项目结构

```
prism-local-server/
├── main.py                 # 程序入口
├── core/                   # 核心模块
├── ui/                     # UI模块
├── utils/                  # 工具模块
├── assets/                 # 资源文件
├── config/                 # 配置文件
└── logs/                   # 日志文件
```

## 开发规范

- 代码注释使用中文
- 遵循PEP 8编码规范
- Git提交信息使用中文，格式：`[类型] 功能描述 - 细节说明`

## 许可证

MIT License

## 作者

Kkwans

## 更新日志

### v0.1.0 (2026-03-15)
- ✅ 项目初始化和Git仓库配置
- ✅ 实现配置管理模块（读取、保存、验证）
- ✅ 实现端口管理模块（可用性检测、自动递增）
- ✅ 实现资源处理器（相对路径适配、Range请求、TCP_NODELAY优化）
- ✅ 实现HTTP服务管理器（多服务管理、自动检测HTML、浏览器打开）
- ✅ 实现日志工具（异步输出、文件滚动）
- ✅ 实现网络工具（IP获取、URL生成）
- ✅ 实现程序入口（命令行模式）
- ✅ 完成功能测试（所有核心功能验证通过）

### 测试结果
- 配置管理：✅ 通过
- 端口管理：✅ 通过
- 网络工具：✅ 通过
- HTTP服务器：✅ 通过（状态码200，响应正常）
- 多服务管理：✅ 通过（3个服务并发运行）
- 资源加载：✅ 通过（CSS/JS/HTML正常加载）
