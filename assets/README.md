# 资源文件目录

## 图标文件

将应用程序图标文件放置在此目录：

- `icon.ico` - Windows应用程序图标（推荐尺寸：256x256）

## 图标制作建议

1. 使用在线工具或专业软件创建图标
2. 推荐尺寸：256x256、128x128、64x64、48x48、32x32、16x16
3. 格式：ICO格式（Windows标准）
4. 设计风格：符合Windows 11 Fluent Design风格

## 使用方法

创建图标后，修改 `build.spec` 文件中的 `icon` 参数：

```python
exe = EXE(
    ...
    icon='assets/icon.ico',  # 指定图标路径
    ...
)
```
