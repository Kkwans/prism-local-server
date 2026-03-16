# Prism Local Server - 开发文档

## 开发环境

### 系统要求
- Windows 11 Professional/Enterprise
- Python 3.8+
- Git

### 依赖安装

```bash
pip install -r requirements.txt
```

### 主要依赖
- flet >= 0.24.0 (UI框架)
- requests >= 2.31.0 (HTTP客户端)
- pystray >= 0.19.5 (系统托盘)
- Pillow >= 10.0.0 (图像处理)

## 项目结构

```
prism-server-flet/
├── main.py                     # 应用入口
├── core/                       # 核心业务逻辑层
│   ├── config_manager.py       # 配置管理
│   ├── http_server_manager.py  # HTTP服务管理
│   ├── port_manager.py         # 端口管理
│   └── resource_handler.py     # 资源处理器
├── ui/                         # UI层
│   ├── home_view.py            # 主页视图
│   ├── settings_dialog.py      # 设置对话框
│   └── tray_manager.py         # 系统托盘
├── utils/                      # 工具层
│   ├── logger.py               # 日志工具
│   └── network_utils.py        # 网络工具
└── test_demo/                  # 测试资源
```

## 开发流程

### 1. 克隆项目

```bash
git clone <repository-url>
cd prism-server-flet
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行应用

```bash
python main.py
# 或使用快速启动脚本
run.bat
```

### 4. 运行测试

```bash
# 单元测试
python test_app.py

# 功能测试
python test_full_functionality.py

# 端到端测试
python test_e2e.py
```

### 5. 打包应用

```bash
# 使用打包脚本
build.bat

# 或手动打包
pyinstaller build.spec
```

## 代码规范

### 文件编码
- UTF-8 with BOM
- CRLF换行符（Windows标准）

### 注释规范
- 所有注释使用中文
- 类和函数必须有文档字符串
- 复杂逻辑添加行注释

### 命名规范
- 变量/函数: 驼峰命名 (camelCase)
- 常量: 全大写下划线分隔 (UPPER_SNAKE_CASE)
- 类名: 帕斯卡命名 (PascalCase)

### Git提交规范
- 提交信息使用中文
- 格式: `[类型] 功能描述 - 细节说明`
- 类型: feat/fix/opt/docs

## 核心模块说明

### ConfigManager (配置管理器)
- 配置文件位置: `C:\Users\{username}\.prism-server\settings.json`
- 支持配置验证和默认值
- 自动创建配置目录

### HTTPServerManager (HTTP服务管理器)
- 管理多个HTTP服务实例
- 自动检测HTML文件
- 支持服务启动/停止/状态查询

### PortManager (端口管理器)
- 端口可用性检测
- 自动查找可用端口
- 端口范围验证（1024-65535）

### ResourceHandler (资源处理器)
- 支持HTTP Range请求（视频拖动）
- 优化Content-Type设置
- TCP_NODELAY网络优化

## 测试说明

### 测试文件
- `test_app.py` - 单元测试
- `test_full_functionality.py` - 功能测试
- `test_e2e.py` - 端到端测试

### 测试覆盖
- ✅ 配置管理
- ✅ HTTP服务启动/停止
- ✅ 多服务并发
- ✅ 端口自动切换
- ✅ 资源加载（HTML/CSS/JS/图片）

### 运行所有测试

```bash
python test_app.py && python test_full_functionality.py && python test_e2e.py
```

## 打包说明

### 打包配置
- 配置文件: `build.spec`
- 打包脚本: `build.bat`
- 应用图标: `assets/icon.ico`

### 打包选项
- 单文件模式（所有依赖打包到一个EXE）
- 无控制台窗口
- UPX压缩
- 自定义图标

### 打包后测试
1. 复制EXE到其他目录
2. 双击运行
3. 验证配置文件在用户目录创建
4. 测试所有功能

## 性能优化

### 内存优化
- 懒加载非核心模块
- 及时释放无用对象
- 避免循环引用

### 启动优化
- 延迟初始化非必需组件
- 异步加载配置
- 减少导入模块数量

### 网络优化
- TCP_NODELAY减少延迟
- 文件缓冲读取（8KB）
- HTTP Range支持

## 常见问题

### Q: 如何调试Flet应用？
A: 在main.py中设置 `page.debug = True`

### Q: 如何修改应用图标？
A: 编辑 `create_icon.py` 重新生成图标

### Q: 如何添加新功能？
A: 
1. 在对应模块添加功能代码
2. 在UI层添加交互界面
3. 编写测试用例
4. 更新文档

### Q: 打包后EXE很大怎么办？
A: 
1. 启用UPX压缩（已启用）
2. 排除不必要的依赖
3. 使用虚拟环境打包

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交代码（遵循代码规范）
4. 运行所有测试
5. 提交Pull Request

## 技术支持

如有问题或建议，请提交Issue或联系作者。

## 作者

Kkwans

## 更新时间

2026-03-16
