# -*- coding: utf-8 -*-
"""
创建现代化的Prism图标
使用渐变色和Material Design风格
作者: Kkwans
创建时间: 2026-03-16
"""

from PIL import Image, ImageDraw
import os

def create_modern_icon():
    """创建现代化的Prism图标"""
    
    # 创建多个尺寸的图标
    sizes = [16, 32, 48, 64, 128, 256]
    images = []
    
    for size in sizes:
        # 创建透明背景
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # 计算尺寸
        padding = size // 8
        center_x = size // 2
        center_y = size // 2
        
        # 绘制六边形（棱镜形状）
        hex_size = size - padding * 2
        hex_radius = hex_size // 2
        
        # 六边形顶点
        import math
        points = []
        for i in range(6):
            angle = math.pi / 3 * i - math.pi / 6
            x = center_x + hex_radius * math.cos(angle)
            y = center_y + hex_radius * math.sin(angle)
            points.append((x, y))
        
        # 绘制渐变背景（模拟）
        # 使用蓝色到紫色的渐变
        colors = [
            (33, 150, 243, 255),   # 蓝色
            (103, 58, 183, 255),   # 紫色
        ]
        
        # 绘制六边形主体
        draw.polygon(points, fill=(63, 81, 181, 255), outline=(33, 150, 243, 255))
        
        # 绘制内部三角形（棱镜效果）
        triangle_size = hex_radius * 0.6
        triangle_points = [
            (center_x, center_y - triangle_size),
            (center_x - triangle_size * 0.866, center_y + triangle_size * 0.5),
            (center_x + triangle_size * 0.866, center_y + triangle_size * 0.5),
        ]
        draw.polygon(triangle_points, fill=(255, 255, 255, 200))
        
        # 绘制光线效果
        line_width = max(1, size // 32)
        for i in range(3):
            angle = math.pi * 2 / 3 * i
            start_x = center_x + triangle_size * 0.3 * math.cos(angle)
            start_y = center_y + triangle_size * 0.3 * math.sin(angle)
            end_x = center_x + hex_radius * 0.8 * math.cos(angle)
            end_y = center_y + hex_radius * 0.8 * math.sin(angle)
            draw.line([(start_x, start_y), (end_x, end_y)], 
                     fill=(255, 255, 255, 150), width=line_width)
        
        images.append(img)
    
    # 保存为PNG（用于Flet）
    images[-1].save('assets/icon.png', 'PNG')
    print(f"✓ 已创建 PNG 图标: assets/icon.png")
    
    # 保存为ICO（用于Windows）
    images[0].save('assets/icon.ico', format='ICO', 
                   sizes=[(s, s) for s in sizes])
    print(f"✓ 已创建 ICO 图标: assets/icon.ico")
    
    print("\n图标创建完成！")
    print("- PNG图标用于Flet打包")
    print("- ICO图标用于Windows应用")

if __name__ == '__main__':
    # 确保assets目录存在
    os.makedirs('assets', exist_ok=True)
    create_modern_icon()
