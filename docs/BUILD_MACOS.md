# macOS 版本构建指南（可选）

## 前置要求

在 macOS 系统上构建 Prism Local Server 需要以下工具：

### 安装 Xcode Command Line Tools
```bash
xcode-select --install
```

### 安装 Homebrew
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## 安装 Rust 和 Node.js

```bash
# 安装 Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 安装 Node.js
brew install node@20
```

## 构建步骤

```bash
# 1. 克隆仓库
git clone https://github.com/Kkwans/prism-local-server.git
cd prism-local-server

# 2. 切换到 tauri-v3 分支
git checkout tauri-v3

# 3. 安装前端依赖
npm install

# 4. 构建前端
npm run build

# 5. 构建 Tauri 应用
cd backend
cargo tauri build

# 6. 查看构建产物
ls -lh target/release/bundle/
```

## 构建产物

macOS 版本会生成以下文件：

- `target/release/prism-local-server-tauri` - 可执行文件
- `target/release/bundle/macos/Prism Local Server.app` - macOS 应用包
- `target/release/bundle/dmg/Prism Local Server_3.0.0_x64.dmg` - DMG 安装镜像

## 安装和运行

### 使用 DMG 安装
1. 双击 DMG 文件
2. 将应用拖拽到 Applications 文件夹
3. 从启动台或 Applications 文件夹启动

### 直接运行 .app
```bash
open "target/release/bundle/macos/Prism Local Server.app"
```

## 注意事项

1. macOS 版本不支持 Mica/Acrylic 毛玻璃效果（Windows 11 专属）
2. 首次运行可能需要在"系统偏好设置 > 安全性与隐私"中允许运行
3. 如果遇到"无法验证开发者"提示，右键点击应用选择"打开"
4. 系统托盘图标会显示在菜单栏右上角

## 代码签名（可选）

如果需要分发给其他用户，建议进行代码签名：

```bash
# 需要 Apple Developer 账号
codesign --force --deep --sign "Developer ID Application: Your Name" \
  "target/release/bundle/macos/Prism Local Server.app"
```

## 故障排除

### 构建失败：找不到 Xcode
```bash
# 确认 Xcode Command Line Tools 已安装
xcode-select -p
```

### 运行时错误：权限被拒绝
```bash
# 授予可执行权限
chmod +x target/release/prism-local-server-tauri
```

### 系统托盘不显示
macOS 系统托盘图标会自动显示在菜单栏，如果没有显示，检查"系统偏好设置 > 通知"中的应用权限。
