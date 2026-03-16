# -*- coding: utf-8 -*-
"""
提高现有图标的分辨率（不改变样式）
作者: Kkwans
创建时间: 2026-03-16
"""

from PIL import Image
import os

def upscale_icon():
    """提高图标分辨率到 512x512"""
    
    png_path = 'assets/icon.png'
    
    if not os.path.exists(png_path):
        print(f"错误：找不到图标文件 {png_path}")
        return
    
    # 读取现有图标
    img = Image.open(png_path)
    print(f"当前图标尺寸: {img.size}")
    
    # 如果已经是高分辨率，跳过
    if img.size[0] >= 512:
        print("图标已经是高分辨率，无需处理")
        return
    
    # 使用 LANCZOS 算法放大到 512x512
    high_res_img = img.resize((512, 512), Image.Resampling.LANCZOS)
    
    # 保存高分辨率 PNG
    high_res_img.save(png_path, 'PNG')
    print(f"✓ 已将 PNG 图标提升到 512x512: {png_path}")
    
    # 生成多尺寸 ICO 文件
    ico_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    ico_images = []
    
    for ico_size in ico_sizes:
        ico_img = high_res_img.resize(ico_size, Image.Resampling.LANCZOS)
        ico_images.append(ico_img)
    
    ico_path = 'assets/icon.ico'
    ico_images[0].save(
        ico_path, 
        format='ICO', 
        sizes=[(img.width, img.height) for img in ico_images],
        append_images=ico_images[1:]
    )
    print(f"✓ 已生成多尺寸 ICO 图标: {ico_path}")
    print(f"  包含尺寸: {', '.join([f'{s[0]}x{s[1]}' for s in ico_sizes])}")

if __name__ == '__main__':
    upscale_icon()
    print("\n图标分辨率提升完成！")
