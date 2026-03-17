# -*- coding: utf-8 -*-
"""
修复Flet 0.80+的颜色API
将字符串颜色改为 ft.colors.XXX
"""

import re
from pathlib import Path

# 颜色映射表
COLOR_MAP = {
    '"grey400"': 'ft.colors.GREY_400',
    '"grey500"': 'ft.colors.GREY_500',
    '"grey600"': 'ft.colors.GREY_600',
    '"grey700"': 'ft.colors.GREY_700',
    '"blue600"': 'ft.colors.BLUE_600',
    '"blue700"': 'ft.colors.BLUE_700',
    '"green600"': 'ft.colors.GREEN_600',
    '"green700"': 'ft.colors.GREEN_700',
    '"red600"': 'ft.colors.RED_600',
    '"white"': 'ft.colors.WHITE',
    '"surfacevariant"': 'ft.colors.SURFACE_VARIANT',
    '"surface"': 'ft.colors.SURFACE',
    '"background"': 'ft.colors.BACKGROUND',
}

def fix_file(file_path):
    """修复单个文件"""
    print(f"处理文件: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 替换所有颜色
    for old_color, new_color in COLOR_MAP.items():
        content = content.replace(old_color, new_color)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ 已更新")
        return True
    else:
        print(f"  - 无需更新")
        return False

def main():
    print("=" * 60)
    print("修复Flet 0.80+颜色API")
    print("=" * 60)
    print()
    
    # 需要处理的文件
    files = [
        'ui/home_view.py',
        'ui/settings_dialog.py',
    ]
    
    updated_count = 0
    for file_path in files:
        if fix_file(file_path):
            updated_count += 1
    
    print()
    print("=" * 60)
    print(f"完成！共更新 {updated_count} 个文件")
    print("=" * 60)

if __name__ == "__main__":
    main()
