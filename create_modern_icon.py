# -*- coding: utf-8 -*-
"""
创建现代化应用图标
生成高质量的多尺寸 ICO 文件
作者: Kkwans
创建时间: 2026-03-16
"""

from PIL import Image, ImageDraw
import os
import math

def create_modern_icon():
    """创建现代化的六边形图标（多尺寸）"""
    
    # 创建多个尺寸的图标
    sizes = [16, 24, 32, 48, 64, 128, 256]
    images = []
    
    for size in sizes:
        # 创建透明背景
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # 计算六边形顶点（棱镜形状）
        center_x, center_y = size // 2, size // 2
        radius = size * 0.4
        
        # 六边形的6个顶点
        points = []
        for i in range(6):
            angle = math.pi / 3 * i - math.pi / 6
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((x, y))
        
        # 绘制六边形外框（蓝紫色）
        main_color = (91, 127, 255, 255)
        draw.polygon(points, fill=main_color, outline=(70, 100, 230, 255))
        
        # 绘制内部三角形（光线效果）
        inner_radius = radius * 0.5
        inner_points = []
        for i in range(3):
            angle = math.pi * 2 / 3 * i
            x = center_x + inner_radius * math.cos(angle)
            y = center_y + inner_radius * math.sin(angle)
            inner_points.append((x, y))
        
        # 内部三角形使用浅色
        light_color = (150, 180, 255, 200)
        draw.polygon(inner_points, fill=light_color)
        
        images.append(img)
    
    # 保存为 PNG（最高分辨率）
    png_path = 'assets/icon.png'
    images[-1].save(png_path, 'PNG')
    print(f"✓ PNG 图标已保存: {png_path} (256x256)")
    
    # 保存为 ICO（包含所有尺寸）
    ico_path = 'assets/icon.ico'
    images[0].save(ico_path, format='ICO', sizes=[(img.width, img.height) for img in images])
    print(f"✓ ICO 图标已保存: {ico_path}")
    print(f"  包含尺寸: {', '.join(f'{s}x{s}' for s in sizes)}")
    
    print("\n图标创建完成！")
    print("- PNG 用于高分辨率显示（任务栏、窗口标题栏）")
    print("- ICO 包含多个尺寸，适配不同显示场景")

if __name__ == '__main__':
    # 确保 assets 目录存在
    os.makedirs('assets', exist_ok=True)
    
    create_modern_icon()
