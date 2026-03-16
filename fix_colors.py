# -*- coding: utf-8 -*-
"""
修复 colors 为 Colors 的脚本
"""

import os

files_to_fix = [
    'ui/home_view.py',
    'ui/settings_dialog.py'
]

for file_path in files_to_fix:
    print(f"处理文件: {file_path}")
    
    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换 colors. 为 Colors.
    content = content.replace('colors.', 'Colors.')
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✓ 完成")

print("\n所有文件处理完成！")
