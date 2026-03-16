# -*- coding: utf-8 -*-
"""
修复所有图标引用 - 将 ft.icons.XXX 改为字符串形式
"""

import re

file_path = 'ui/home_view.py'

# 图标映射（ft.icons.XXX -> 字符串）
icon_mappings = {
    'ft.icons.CIRCLE': '"circle"',
    'ft.icons.FOLDER_OUTLINED': '"folder_outlined"',
    'ft.icons.LANGUAGE': '"language"',
    'ft.icons.OPEN_IN_BROWSER': '"open_in_browser"',
    'ft.icons.STOP': '"stop"',
    'ft.icons.SETTINGS_OUTLINED': '"settings_outlined"',
    'ft.icons.INFO_OUTLINE': '"info_outline"',
    'ft.icons.FOLDER_OPEN': '"folder_open"',
    'ft.icons.ROCKET_LAUNCH': '"rocket_launch"',
}

print(f"处理文件: {file_path}")

# 读取文件
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 替换所有图标
for old, new in icon_mappings.items():
    count = content.count(old)
    if count > 0:
        content = content.replace(old, new)
        print(f"  替换 {old} -> {new}: {count} 处")

# 写回文件
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"  ✓ 完成")
