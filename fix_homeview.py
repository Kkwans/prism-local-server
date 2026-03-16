# -*- coding: utf-8 -*-
"""
修复 HomeView 属性引用的脚本
"""

import re

file_path = 'ui/home_view.py'

print(f"处理文件: {file_path}")

# 读取文件
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 替换属性引用（只在 HomeView 类内部）
replacements = [
    ('self.page', 'self._page'),
    ('self.config_manager', 'self._config_manager'),
    ('self.server_manager', 'self._server_manager'),
    ('self.config', 'self._config'),
    ('self.current_directory', 'self._current_directory'),
    ('self.current_port', 'self._current_port'),
    ('self.current_html', 'self._current_html'),
    ('self.service_cards', 'self._service_cards'),
    ('self.service_count_text', 'self._service_count_text'),
    ('self.service_list', 'self._service_list'),
    ('self.empty_state', 'self._empty_state'),
]

for old, new in replacements:
    count = content.count(old)
    content = content.replace(old, new)
    print(f"  替换 {old} -> {new}: {count} 处")

# 写回文件
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"  ✓ 完成")
