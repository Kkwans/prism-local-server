# Linux 版本构建指南

## 前置要求

在 Linux 系统上构建 Prism Local Server 需要以下依赖：

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install -y \
  libwebkit2gtk-4.1-dev \
  build-essential \
  curl \
  wget \
  file \
  libssl-dev \
  libayatana-appindicator3-dev \
  librsvg2-dev
```

### Fedora/RHEL
```bash
sudo dnf install -y \
  webkit2gtk4.1-devel \
  openssl-devel \
  curl \
  wget \
  file \
  libappindicator-gtk3-devel \
  librsvg2-devel
```

### Arch Linux
```bash
sudo pacman -S --needed \
  webkit2gtk-4.1 \
  base-devel \
  curl \
  wget \
  file \
  openssl \
  libappindicator-gtk3 \
  librsvg
```

## 安装 Rust 和 Node.js

```bash
# 安装 Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 安装 Node.js (使用 nvm)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 20
nvm use 20
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

Linux 版本会生成以下文件：

- `target/release/prism-local-server-tauri` - 可执行文件
- `target/release/bundle/deb/prism-local-server_3.0.0_amd64.deb` - Debian 安装包
- `target/release/bundle/appimage/prism-local-server_3.0.0_amd64.AppImage` - AppImage 便携版

## 安装和运行

### 使用 DEB 包（Ubuntu/Debian）
```bash
sudo dpkg -i target/release/bundle/deb/prism-local-server_3.0.0_amd64.deb
prism-local-server-tauri
```

### 使用 AppImage（通用）
```bash
chmod +x target/release/bundle/appimage/prism-local-server_3.0.0_amd64.AppImage
./target/release/bundle/appimage/prism-local-server_3.0.0_amd64.AppImage
```

### 直接运行可执行文件
```bash
./target/release/prism-local-server-tauri
```

## 注意事项

1. Linux 版本不支持 Mica/Acrylic 毛玻璃效果（Windows 11 专属）
2. 系统托盘图标在不同桌面环境下显示效果可能不同
3. 确保系统已安装 WebKitGTK 4.1 运行时库
4. 首次运行可能需要授予网络权限

## 故障排除

### 构建失败：找不到 webkit2gtk
```bash
# 确认已安装 webkit2gtk-4.1
pkg-config --modversion webkit2gtk-4.1
```

### 运行时错误：libwebkit2gtk 找不到
```bash
# 安装运行时依赖
sudo apt install libwebkit2gtk-4.1-0
```

### 系统托盘不显示
某些桌面环境（如 GNOME）默认不显示系统托盘，需要安装扩展：
```bash
# GNOME 用户安装 AppIndicator 扩展
gnome-extensions install appindicatorsupport@rgcjonas.gmail.com
```
