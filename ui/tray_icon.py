# -*- coding: utf-8 -*-
"""
系统托盘模块
实现后台运行和托盘菜单
作者: Kkwans
创建时间: 2026-03-15
"""

import pystray
from PIL import Image, ImageDraw
from typing import Callable
import threading

from utils.logger import Logger


class TrayIcon:
    """
    系统托盘类
    功能:
    - 显示托盘图标
    - 托盘右键菜单
    - 显示/隐藏主窗口
    - 快速启动服务
    - 退出程序
    """
    
    def __init__(self, 
                 on_show: Callable,
                 on_hide: Callable,
                 on_start_service: Callable,
                 on_quit: Callable):
        """
        初始化系统托盘
        参数:
            on_show: 显示主窗口回调
            on_hide: 隐藏主窗口回调
            on_start_service: 启动服务回调
            on_quit: 退出程序回调
        """
        self.on_show = on_show
        self.on_hide = on_hide
        self.on_start_service = on_start_service
        self.on_quit = on_quit
        
        self.icon = None
        self.is_visible = True
        
        Logger.info("系统托盘初始化")
    
    def _createImage(self):
        """
        创建托盘图标
        返回:
            PIL Image对象
        """
        # 创建一个简单的图标（蓝色圆形）
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), (255, 255, 255))
        dc = ImageDraw.Draw(image)
        
        # 绘制蓝色圆形
        dc.ellipse([8, 8, 56, 56], fill='#0078D4', outline='#005A9E', width=2)
        
        # 绘制字母P
        dc.text((22, 18), 'P', fill='white')
        
        return image
    
    def _toggleWindow(self, icon, item):
        """切换窗口显示/隐藏"""
        if self.is_visible:
            self.on_hide()
            self.is_visible = False
            Logger.info("主窗口已隐藏")
        else:
            self.on_show()
            self.is_visible = True
            Logger.info("主窗口已显示")
    
    def _startService(self, icon, item):
        """启动服务"""
        self.on_start_service()
        Logger.info("从托盘启动服务")
    
    def _quit(self, icon, item):
        """退出程序"""
        Logger.info("从托盘退出程序")
        self.stop()
        self.on_quit()
    
    def _createMenu(self):
        """
        创建托盘菜单
        返回:
            pystray.Menu对象
        """
        return pystray.Menu(
            pystray.MenuItem(
                '显示/隐藏',
                self._toggleWindow,
                default=True
            ),
            pystray.MenuItem(
                '快速启动服务',
                self._startService
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                '退出',
                self._quit
            )
        )
    
    def start(self):
        """启动托盘图标（在新线程中）"""
        def run_icon():
            self.icon = pystray.Icon(
                'Prism Local Server',
                self._createImage(),
                'Prism Local Server',
                self._createMenu()
            )
            self.icon.run()
        
        # 在新线程中运行托盘图标
        thread = threading.Thread(target=run_icon, daemon=True)
        thread.start()
        
        Logger.info("系统托盘已启动")
    
    def stop(self):
        """停止托盘图标"""
        if self.icon:
            self.icon.stop()
            Logger.info("系统托盘已停止")
    
    def updateTitle(self, title: str):
        """
        更新托盘图标标题
        参数:
            title: 新标题
        """
        if self.icon:
            self.icon.title = title
