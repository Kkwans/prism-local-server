# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller打包配置文件
用于将Flet应用打包为独立的Windows EXE
作者: Kkwans
创建时间: 2026-03-16
修改时间: 2026-03-16 (修复Flet打包问题)
"""

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Flet 需要的数据文件和子模块
flet_datas = collect_data_files('flet')
flet_hiddenimports = collect_submodules('flet')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=flet_datas,  # 添加 Flet 数据文件
    hiddenimports=[
        'flet',
        'flet.core',
        'flet.utils',
        'flet_core',
        'flet_runtime',
        'httpx',
        'oauthlib',
        'repath',
        'msgpack',
        'pystray',
        'PIL',
        'PIL._imaging',
    ] + flet_hiddenimports,  # 添加 Flet 所有子模块
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PrismLocalServer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 无控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',  # 应用图标
    version_file=None,
)
