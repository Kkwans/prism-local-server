# -*- coding: utf-8 -*-
"""
修复 ICO 文件 - 生成包含多种尺寸的高质量 ICO
作者: Kkwans
创建时间: 2026-03-16
"""

from PIL import Image
import os

def fix_ico():
    """生成包含多种尺寸的高质量 ICO 文件"""
    
    png_path = 'assets/icon.png'
    ico_path = 'assets/icon.ico'
    
    if not os.path.exists(png_path):
        print(f"错误：找不到 PNG 文件 {png_path}")
        return
    
    # 读取 PNG 图标
    img = Image.open(png_path)
    print(f"源 PNG 尺寸: {img.size}")
    
    # 定义需要的 ICO 尺寸（从小到大）
    sizes = [16, 24, 32, 48, 64, 128, 256]
    
    # 为每个尺寸创建图像
    images = []
    for size in sizes:
        resized = img.resize((size, size), Image.Resampling.LANCZOS)
        images.append(resized)
        print(f"  生成 {size}x{size} 尺寸")
    
    # 保存为 ICO（第一个图像作为主图像，其他作为附加图像）
    images[0].save(
        ico_path,
        format='ICO',
        sizes=[(size, size) for size in sizes],
        append_images=images[1:]
    )
    
    print(f"\n✓ 已生成多尺寸 ICO 文件: {ico_path}")
    print(f"  包含尺寸: {', '.join([f'{s}x{s}' for s in sizes])}")
    
    # 验证生成的 ICO
    ico_img = Image.open(ico_path)
    print(f"\n验证 ICO 文件:")
    print(f"  默认尺寸: {ico_img.size}")
    if 'sizes' in ico_img.info:
        print(f"  包含的所有尺寸: {ico_img.info['sizes']}")

if __name__ == '__main__':
    fix_ico()
    print("\nICO 文件修复完成！")
