# -*- coding: utf-8 -*-
"""
Prism Local Server - Flet版本
基于Flutter的现代化前端部署工具
作者: Kkwans
创建时间: 2026-03-16
"""

import flet as ft
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from core.http_server_manager import HTTPServerManager
from core.config_manager import ConfigManager
from utils.logger import Logger
from ui.home_view import HomeView


class PrismApp:
    """
    Prism应用主类
    """
    
    def __init__(self, page: ft.Page):
        """初始化应用"""
        self.page = page
        self.page.title = "Prism Local Server"
        self.page.window_width = 1100
        self.page.window_height = 750
        self.page.window_min_width = 900
        self.page.window_min_height = 650
        self.page.padding = 0
        self.page.theme_mode = ft.ThemeMode.SYSTEM
        
        # 设置Material 3主题
        self.page.theme = ft.Theme(
            color_scheme_seed=ft.colors.BLUE,
            use_material3=True
        )
        
        # 初始化管理器
        Logger.initialize()
        self.config_manager = ConfigManager()
        self.server_manager = HTTPServerManager()
        
        # 创建主视图
        self.home_view = HomeView(
            page=self.page,
            config_manager=self.config_manager,
            server_manager=self.server_manager
        )
        
        # 设置页面内容
        self.page.add(self.home_view)
        
        Logger.info("Prism应用启动成功")


def main(page: ft.Page):
    """应用入口"""
    PrismApp(page)


if __name__ == "__main__":
    # 使用Flet 0.80+的新API
    ft.app(main)
