# -*- coding: utf-8 -*-
"""
修复所有颜色引用 - 将 Colors.XXX 改为字符串形式
"""

files_to_fix = [
    'ui/home_view.py',
    'ui/settings_dialog.py'
]

# 颜色映射
color_mappings = {
    'Colors.GREY_600': '"grey600"',
    'Colors.GREEN_600': '"green600"',
    'Colors.GREEN_700': '"green700"',
    'Colors.GREY_700': '"grey700"',
    'Colors.BLUE_600': '"blue600"',
    'Colors.BLUE_700': '"blue700"',
    'Colors.RED_600': '"red600"',
    'Colors.WHITE': '"white"',
    'Colors.SURFACE_VARIANT': '"surfacevariant"',
    'Colors.GREY_400': '"grey400"',
    'Colors.GREY_500': '"grey500"',
    'Colors.BACKGROUND': '"background"',
    'Colors.SURFACE': '"surface"',
}

for file_path in files_to_fix:
    print(f"处理文件: {file_path}")
    
    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换所有颜色
    for old, new in color_mappings.items():
        count = content.count(old)
        if count > 0:
            content = content.replace(old, new)
            print(f"  替换 {old} -> {new}: {count} 处")
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✓ 完成\n")

print("所有文件处理完成！")
