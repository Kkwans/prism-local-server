# -*- coding: utf-8 -*-
"""
检查并修复图标分辨率问题
保持原有样式，只提高清晰度
"""

from PIL import Image
import os

print("=" * 60)
print("图标分辨率检查与修复")
print("=" * 60)

# 检查PNG
png_path = "assets/icon.png"
if os.path.exists(png_path):
    img = Image.open(png_path)
    print(f"\n当前PNG尺寸: {img.size[0]}x{img.size[1]}")
    print(f"图像模式: {img.mode}")
else:
    print(f"\n错误: 找不到 {png_path}")
    exit(1)

# 检查ICO
ico_path = "assets/icon.ico"
if os.path.exists(ico_path):
    ico = Image.open(ico_path)
    print(f"\n当前ICO信息:")
    print(f"  主尺寸: {ico.size[0]}x{ico.size[1]}")
    print(f"  图像模式: {ico.mode}")
else:
    print(f"\n错误: 找不到 {ico_path}")

# 问题分析
print("\n" + "=" * 60)
print("问题分析:")
print("=" * 60)
print("1. PNG是512x512，但如果是从低分辨率放大的，会模糊")
print("2. ICO需要包含多个尺寸才能在不同场景下清晰显示")
print("3. Windows任务栏通常使用32x32或48x48的图标")

# 生成高质量ICO
print("\n" + "=" * 60)
print("重新生成ICO（包含多个尺寸）")
print("=" * 60)

# 使用现有的512x512 PNG作为源
source_img = Image.open(png_path)

# 确保是RGBA模式
if source_img.mode != 'RGBA':
    source_img = source_img.convert('RGBA')

# 生成多个尺寸的图标
sizes = [
    (16, 16),   # 小图标
    (24, 24),   # 小图标
    (32, 32),   # 任务栏
    (48, 48),   # 任务栏（高DPI）
    (64, 64),   # 中等图标
    (128, 128), # 大图标
    (256, 256)  # 超大图标
]

# 使用高质量重采样
icon_images = []
for size in sizes:
    resized = source_img.resize(size, Image.Resampling.LANCZOS)
    icon_images.append(resized)
    print(f"  生成 {size[0]}x{size[1]} 尺寸")

# 保存为ICO（包含所有尺寸）
ico_output = "assets/icon.ico"
icon_images[0].save(
    ico_output,
    format='ICO',
    sizes=sizes,
    append_images=icon_images[1:]
)

print(f"\n✓ 已生成高质量ICO: {ico_output}")
print(f"  包含尺寸: {', '.join([f'{s[0]}x{s[1]}' for s in sizes])}")

print("\n" + "=" * 60)
print("完成！")
print("=" * 60)
print("\n建议:")
print("1. 清理构建缓存: 删除 build/ 和 dist/ 目录")
print("2. 重新打包: 运行 pack_improved.bat")
print("3. 如果图标仍然模糊，可能需要原始矢量图或更高分辨率的源文件")
