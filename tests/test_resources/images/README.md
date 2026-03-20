# 测试图片资源说明

## 需要准备的测试图片

请在此目录下放置以下测试图片：

1. **test-image.png** - 普通测试图片（建议大小：500KB 左右）
2. **中文文件名图片.png** - 用于测试中文文件名支持

## 如何准备测试图片

### 方法 1：使用在线图片生成器
访问 https://placeholder.com/ 或 https://via.placeholder.com/
- 生成 800x600 的 PNG 图片
- 下载并重命名为 `test-image.png`
- 复制一份并重命名为 `中文文件名图片.png`

### 方法 2：使用现有图片
- 找任意 PNG 图片
- 重命名为 `test-image.png`
- 复制一份并重命名为 `中文文件名图片.png`

### 方法 3：使用 PowerShell 生成纯色图片
```powershell
# 需要安装 ImageMagick
magick -size 800x600 xc:blue test-image.png
magick -size 800x600 xc:green 中文文件名图片.png
```

## 测试目的

- **test-image.png**: 测试普通英文文件名的图片加载
- **中文文件名图片.png**: 测试 UTF-8 编码的中文文件名支持
