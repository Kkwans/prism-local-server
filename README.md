# Prism Local Server (Flet版本)

基于Flet (Flutter) 的现代化前端静态文件部署工具

## 特性

- 🎨 **现代化UI**: Material Design 3风格，流畅动画，支持浅色/深色主题
- 🚀 **一键部署**: 快速将HTML静态文件部署到本地HTTP服务器
- 🌐 **局域网访问**: 支持局域网内其他设备访问
- 📦 **多服务管理**: 同时运行多个HTTP服务实例
- ⚙️ **灵活配置**: 自定义端口、HTML文件等
- 🔄 **自动端口**: 端口被占用时自动切换
- 📁 **独立配置**: 配置文件存储在用户目录，EXE可独立运行

## 技术栈

- **UI框架**: Flet 0.82+ (基于Flutter)
- **HTTP服务**: Python http.server
- **系统托盘**: pystray
- **打包工具**: PyInstaller

## 开发环境

- Python 3.8+
- Windows 11

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行

```bash
python main.py
```

## 打包为EXE

**推荐方法（Flet 官方）**：
```bash
pack.bat
```

**备用方法（PyInstaller，不推荐）**：
```bash
build.bat
```

打包后的EXE文件位于 `dist/PrismLocalServer.exe`

详细说明请查看：[docs/打包说明.md](docs/打包说明.md)

## 配置文件位置

配置文件存储在: `C:\Users\{username}\.prism-server\`

- `settings.json` - 应用配置
- `logs/` - 日志文件

## 使用说明

1. 点击"选择目录"选择要部署的HTML文件所在目录
2. 点击"启动服务"启动HTTP服务
3. 浏览器会自动打开访问地址
4. 可以同时启动多个服务（不同端口）
5. 点击"停止"按钮停止对应的服务

## 核心功能

### 资源加载优化
- 支持HTML相对路径资源（CSS/JS/图片/视频）
- 支持HTTP Range请求（视频拖动播放）
- 启用TCP_NODELAY优化网络性能

### 端口管理
- 默认端口: 9000
- 端口被占用时自动递增（9001/9002...）
- 支持手动配置默认端口

### 多服务管理
- 显示服务状态（运行中/已停止）
- 实时显示运行时长
- 显示部署目录和访问地址
- 一键打开浏览器访问

## 项目结构

```
prism-server-flet/
├── main.py                     # 应用入口
├── core/                       # 核心业务逻辑
│   ├── config_manager.py       # 配置管理（用户目录存储）
│   ├── http_server_manager.py  # HTTP服务管理（多实例）
│   ├── port_manager.py         # 端口管理（自动检测）
│   └── resource_handler.py     # 资源处理器（Range支持）
├── ui/                         # UI层
│   ├── home_view.py            # 主页视图（Material Design 3）
│   ├── settings_dialog.py      # 设置对话框
│   └── tray_manager.py         # 系统托盘管理
├── utils/                      # 工具模块
│   ├── logger.py               # 日志工具
│   └── network_utils.py        # 网络工具
├── assets/                     # 资源文件
│   ├── icon.ico                # 应用图标
│   └── icon.png                # 托盘图标
├── docs/                       # 项目文档
│   ├── 项目总结.md
│   ├── 用户指南.md
│   ├── 开发文档.md
│   └── ...
├── test_demo/                  # 测试资源
├── requirements.txt            # 依赖列表
├── build.spec                  # PyInstaller配置
├── build.bat                   # 打包脚本
└── README.md                   # 项目说明
```

## 作者

Kkwans

## 许可证

MIT License
