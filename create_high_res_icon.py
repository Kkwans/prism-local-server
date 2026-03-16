# -*- coding: utf-8 -*-
"""
创建现代化应用图标（高分辨率版本）
生成 PNG 和 ICO 格式，支持多种尺寸
作者: Kkwans
创建时间: 2026-03-16
"""

from PIL import Image, ImageDraw
import os
import math

def create_modern_icon():
    """创建现代化的六边形图标（高分辨率）"""
    
    # 创建高分辨率图像 (512x512)
    size = 512
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 六边形坐标（居中）
    center_x, center_y = size // 2, size // 2
    radius = size // 2 - 40  # 留出边距
    
    # 计算六边形顶点
    hexagon = []
    for i in range(6):
        angle = math.pi / 3 * i - math.pi / 6
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        hexagon.append((x, y))
    
    # 绘制六边形背景（蓝紫色渐变效果，使用多层）
    for i in range(20):
        offset = i * 2
        temp_radius = radius - offset
        temp_hexagon = []
        for j in range(6):
            angle = math.pi / 3 * j - math.pi / 6
            x = center_x + temp_radius * math.cos(angle)
            y = center_y + temp_radius * math.sin(angle)
            temp_hexagon.append((x, y))
        
        # 渐变色（从蓝色到紫色）
        r = int(100 + i * 5)
        g = int(100 - i * 3)
        b = int(255 - i * 3)
        draw.polygon(temp_hexagon, fill=(r, g, b, 255))
    
    # 绘制内部三角形（光线效果）
    triangle_radius = radius * 0.4
    triangle = []
    for i in range(3):
        angle = math.pi * 2 / 3 * i - math.pi / 2
        x = center_x + triangle_radius * math.cos(angle)
        y = center_y + triangle_radius * math.sin(angle)
        triangle.append((x, y))
    
    draw.polygon(triangle, fill=(255, 255, 255, 200))

    
    # 保存 PNG（高分辨率）
    png_path = 'assets/icon.png'
    os.makedirs('assets', exist_ok=True)
    img.save(png_path, 'PNG')
    print(f"✓ 已生成高分辨率 PNG 图标: {png_path} (512x512)")
    
    # 生成多尺寸 ICO 文件
    ico_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    ico_images = []
    
    for ico_size in ico_sizes:
        ico_img = img.resize(ico_size, Image.Resampling.LANCZOS)
        ico_images.append(ico_img)
    
    ico_path = 'assets/icon.ico'
    ico_images[0].save(ico_path, format='ICO', sizes=[(img.width, img.height) for img in ico_images], append_images=ico_images[1:])
    print(f"✓ 已生成多尺寸 ICO 图标: {ico_path}")
    print(f"  包含尺寸: {', '.join([f'{s[0]}x{s[1]}' for s in ico_sizes])}")

if __name__ == '__main__':
    create_modern_icon()
    print("\n图标生成完成！")
