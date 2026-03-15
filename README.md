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

1. 启动程序后，默认部署EXE所在目录
2. 点击"启动服务"按钮
3. 程序自动检测HTML文件并在浏览器中打开
4. 支持配置端口、目录、入口文件

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

### v0.1.0 (开发中)
- 项目初始化
- 基础架构搭建
