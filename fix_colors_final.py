# -*- coding: utf-8 -*-
"""
最终修复：将 ft.colors 改为 ft.Colors (大写C)
"""

import re
from pathlib import Path

def fix_file(file_path):
    """修复单个文件"""
    print(f"处理文件: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 替换 ft.colors 为 ft.Colors
    content = content.replace('ft.colors.', 'ft.Colors.')
    
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
    print("修复颜色API：ft.colors → ft.Colors")
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
