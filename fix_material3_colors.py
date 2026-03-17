# -*- coding: utf-8 -*-
"""
修复Material 3颜色常量
Flet 0.82使用不同的颜色命名
"""

import re

# 颜色映射（旧名称 -> 新名称）
COLOR_MAP = {
    'ft.Colors.SURFACE_VARIANT': 'ft.Colors.SURFACE_CONTAINER',
    'ft.Colors.BACKGROUND': 'ft.Colors.SURFACE',
    'ft.Colors.ON_SURFACE_VARIANT': 'ft.Colors.ON_SURFACE',
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
    print("修复Material 3颜色常量")
    print("=" * 60)
    print()
    
    files = [
        'ui/home_view.py',
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
