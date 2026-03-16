# -*- coding: utf-8 -*-
"""
应用图标生成脚本
生成Windows应用图标（ICO格式）
作者: Kkwans
创建时间: 2026-03-16
"""

from PIL import Image, ImageDraw


def create_app_icon():
    """
    创建应用图标
    生成256x256的PNG图标，然后转换为ICO格式
    """
    # 创建256x256的图像
    size = 256
    image = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # 绘制渐变背景圆形
    center = size // 2
    radius = size // 2 - 20
    
    # 绘制蓝色圆形背景
    draw.ellipse(
        [center - radius, center - radius, center + radius, center + radius],
        fill='#0078D4',
        outline='#005A9E',
        width=4
    )
    
    # 绘制六边形（Prism标志）
    hex_radius = radius * 0.6
    points = []
    for i in range(6):
        angle = i * 60 - 30  # 从顶部开始
        import math
        x = center + hex_radius * math.cos(math.radians(angle))
        y = center + hex_radius * math.sin(math.radians(angle))
        points.append((x, y))
    
    draw.polygon(points, fill='white', outline='#E0E0E0', width=3)
    
    # 保存为PNG
    png_path = 'assets/icon.png'
    image.save(png_path, 'PNG')
    print(f"✓ PNG图标已生成: {png_path}")
    
    # 转换为ICO（多尺寸）
    ico_path = 'assets/icon.ico'
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    
    # 创建多尺寸图标
    images = []
    for icon_size in icon_sizes:
        resized = image.resize(icon_size, Image.Resampling.LANCZOS)
        images.append(resized)
    
    # 保存为ICO
    images[0].save(ico_path, format='ICO', sizes=icon_sizes, append_images=images[1:])
    print(f"✓ ICO图标已生成: {ico_path}")
    
    return ico_path


if __name__ == "__main__":
    print("=== 生成应用图标 ===\n")
    
    # 确保assets目录存在
    import os
    os.makedirs('assets', exist_ok=True)
    
    # 生成图标
    try:
        icon_path = create_app_icon()
        print(f"\n✓ 图标生成完成！")
        print(f"  PNG: assets/icon.png")
        print(f"  ICO: assets/icon.ico")
    except Exception as e:
        print(f"✗ 生成图标失败: {e}")
        import traceback
        traceback.print_exc()
