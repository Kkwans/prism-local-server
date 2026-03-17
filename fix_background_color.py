# -*- coding: utf-8 -*-
"""
修复BACKGROUND颜色问题
"""

# 读取文件
with open('ui/home_view.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 替换BACKGROUND为SURFACE
content = content.replace('bgcolor=ft.Colors.BACKGROUND', 'bgcolor=ft.Colors.SURFACE')

# 写回文件
with open('ui/home_view.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("修复完成！")
