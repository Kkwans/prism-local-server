# -*- coding: utf-8 -*-
"""
系统托盘管理器
作者: Kkwans
创建时间: 2026-03-16
"""

import pystray
from PIL import Image, ImageDraw
from typing import Callable, Optional
import threading


class TrayManager:
    """系统托盘管理器"""
    
    def __init__(self, on_show: Callable, on_quit: Callable):
        """
        初始化托盘管理器
        
        参数:
            on_show: 显示窗口回调
            on_quit: 退出应用回调
        """
        self.on_show = on_show
        self.on_quit = on_quit
        self.icon: Optional[pystray.Icon] = None
        self.thread: Optional[threading.Thread] = None
    
    def _create_icon_image(self) -> Image.Image:
        """
        创建托盘图标
        
        返回:
            PIL Image对象
        """
        # 创建64x64的图标
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        
        # 绘制蓝色六边形（Prism标志）
        points = [
            (32, 8),   # 顶部
            (52, 20),  # 右上
            (52, 44),  # 右下
            (32, 56),  # 底部
            (12, 44),  # 左下
            (12, 20)   # 左上
        ]
        draw.polygon(points, fill='#0078D4', outline='#005A9E')
        
        return image
    
    def start(self):
        """启动系统托盘"""
        if self.icon:
            return
        
        # 创建托盘图标
        icon_image = self._create_icon_image()
        
        # 创建菜单
        menu = pystray.Menu(
            pystray.MenuItem('显示窗口', self._on_show_clicked),
            pystray.MenuItem('退出', self._on_quit_clicked)
        )
        
        # 创建托盘图标对象
        self.icon = pystray.Icon(
            'Prism Local Server',
            icon_image,
            'Prism Local Server',
            menu
        )
        
        # 在后台线程运行托盘
        def run_tray():
            self.icon.run()
        
        self.thread = threading.Thread(target=run_tray, daemon=True)
        self.thread.start()
    
    def stop(self):
        """停止系统托盘"""
        if self.icon:
            self.icon.stop()
            self.icon = None
    
    def _on_show_clicked(self, icon, item):
        """显示窗口菜单项点击"""
        if self.on_show:
            self.on_show()
    
    def _on_quit_clicked(self, icon, item):
        """退出菜单项点击"""
        if self.on_quit:
            self.on_quit()
        self.stop()
