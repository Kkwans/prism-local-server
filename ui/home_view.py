# -*- coding: utf-8 -*-
"""
主页视图
实现Material Design 3风格的现代化界面
作者: Kkwans
创建时间: 2026-03-16
"""

import flet as ft
from flet import Colors
import os
import webbrowser
from typing import Dict, Optional
from datetime import datetime

from core.http_server_manager import HTTPServerManager, ServiceInstance
from core.config_manager import ConfigManager
from utils.logger import Logger
from utils.network_utils import NetworkUtils
from ui.settings_dialog import SettingsDialog


class ServiceCard(ft.Container):
    """服务卡片组件"""
    
    def __init__(self, service: ServiceInstance, on_stop, on_open):
        """初始化服务卡片"""
        self.service = service
        self.on_stop = on_stop
        self.on_open = on_open
        
        # 运行时长文本
        self.uptime_text = ft.Text(
            f"运行时长: {service.getUptime()}",
            size=12,
            color=Colors.GREY_600
        )
        
        # 创建卡片内容
        super().__init__(
            content=ft.Row(
                controls=[
                    # 左侧信息区域
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                # 状态和端口
                                ft.Row(
                                    controls=[
                                        ft.Icon(
                                            ft.icons.CIRCLE,
                                            color=Colors.GREEN_600,
                                            size=12
                                        ),
                                        ft.Text(
                                            "运行中",
                                            size=14,
                                            weight=ft.FontWeight.BOLD,
                                            color=Colors.GREEN_700
                                        ),
                                        ft.Container(width=10),
                                        ft.Text(
                                            f"端口 {service.port}",
                                            size=14,
                                            weight=ft.FontWeight.BOLD
                                        ),
                                        ft.Container(width=10),
                                        self.uptime_text
                                    ],
                                    spacing=5
                                ),
                                # 目录路径
                                ft.Row(
                                    controls=[
                                        ft.Icon(
                                            ft.icons.FOLDER_OUTLINED,
                                            size=16,
                                            color=Colors.GREY_600
                                        ),
                                        ft.Text(
                                            service.directory,
                                            size=12,
                                            color=Colors.GREY_700
                                        )
                                    ],
                                    spacing=5
                                ),
                                # 访问地址
                                ft.Row(
                                    controls=[
                                        ft.Icon(
                                            ft.icons.LANGUAGE,
                                            size=16,
                                            color=Colors.BLUE_600
                                        ),
                                        ft.Text(
                                            NetworkUtils.generateLocalURL(service.port, service.entry_html),
                                            size=12,
                                            color=Colors.BLUE_700
                                        )
                                    ],
                                    spacing=5
                                )
                            ],
                            spacing=8
                        ),
                        expand=True,
                        padding=ft.padding.only(left=20, top=15, bottom=15)
                    ),
                    # 右侧按钮区域
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.FilledTonalButton(
                                    "打开",
                                    icon=ft.icons.OPEN_IN_BROWSER,
                                    on_click=lambda _: self.on_open(service)
                                ),
                                ft.FilledButton(
                                    "停止",
                                    icon=ft.icons.STOP,
                                    on_click=lambda _: self.on_stop(service.id),
                                    style=ft.ButtonStyle(
                                        bgcolor=Colors.RED_600,
                                        color=Colors.WHITE
                                    )
                                )
                            ],
                            spacing=10
                        ),
                        padding=ft.padding.only(right=20, top=15, bottom=15)
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            bgcolor=Colors.SURFACE_VARIANT,
            border_radius=12,
            margin=ft.margin.only(bottom=12),
            animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT)
        )
    
    def update_uptime(self):
        """更新运行时长"""
        self.uptime_text.value = f"运行时长: {self.service.getUptime()}"
        self.uptime_text.update()


class HomeView(ft.Container):
    """主页视图"""
    
    def __init__(self, page: ft.Page, config_manager: ConfigManager, server_manager: HTTPServerManager):
        """初始化主页视图"""
        # 先保存引用到私有变量
        self._page = page
        self._config_manager = config_manager
        self._server_manager = server_manager
        
        # 加载配置
        self._config = config_manager.loadConfig()
        self._current_directory = self._config.get('default_directory', '') or os.getcwd()
        self._current_port = self._config.get('default_port', 9000)
        self._current_html = self._config.get('default_html', 'index.html')
        
        # 服务卡片字典
        self._service_cards: Dict[str, ServiceCard] = {}
        
        # 服务计数文本
        self._service_count_text = ft.Text(
            "(0)",
            size=14,
            color=Colors.GREY_600
        )
        
        # 服务列表容器
        self._service_list = ft.Column(
            controls=[],
            spacing=0,
            scroll=ft.ScrollMode.AUTO
        )
        
        # 空状态提示
        self._empty_state = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(
                        ft.icons.CLOUD_QUEUE_OUTLINED,
                        size=80,
                        color=Colors.GREY_400
                    ),
                    ft.Text(
                        "暂无运行中的服务",
                        size=18,
                        color=Colors.GREY_600,
                        weight=ft.FontWeight.W_500
                    ),
                    ft.Text(
                        "点击\"启动服务\"按钮开始",
                        size=14,
                        color=Colors.GREY_500
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            ),
            padding=ft.padding.only(top=80),
            alignment=ft.alignment.center
        )
        
        # 创建UI
        super().__init__(
            content=ft.Column(
                controls=[
                    # 顶部应用栏
                    self._create_app_bar(),
                    # 快速启动区域
                    self._create_quick_start_section(),
                    # 服务列表区域
                    self._create_service_list_section()
                ],
                spacing=0,
                expand=True
            ),
            expand=True,
            bgcolor=Colors.BACKGROUND
        )
        
        # 启动定时器更新运行时长
        self._start_uptime_timer()
    
    def _create_app_bar(self):
        """创建顶部应用栏"""
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        ft.icons.HEXAGON,
                        size=32,
                        color=Colors.BLUE_600
                    ),
                    ft.Text(
                        "Prism Local Server",
                        size=24,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon=ft.icons.SETTINGS_OUTLINED,
                        tooltip="设置",
                        on_click=self._open_settings
                    ),
                    ft.IconButton(
                        icon=ft.icons.INFO_OUTLINE,
                        tooltip="关于",
                        on_click=self._show_about
                    )
                ],
                alignment=ft.MainAxisAlignment.START
            ),
            bgcolor=Colors.SURFACE_VARIANT,
            padding=ft.padding.symmetric(horizontal=24, vertical=16)
        )
    
    def _create_quick_start_section(self):
        """创建快速启动区域"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "快速启动",
                        size=20,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Container(height=16),
                    ft.Row(
                        controls=[
                            ft.FilledTonalButton(
                                "选择目录",
                                icon=ft.icons.FOLDER_OPEN,
                                on_click=self._select_directory,
                                height=48
                            ),
                            ft.FilledButton(
                                "启动服务",
                                icon=ft.icons.ROCKET_LAUNCH,
                                on_click=self._start_service,
                                height=48
                            )
                        ],
                        spacing=12
                    )
                ],
                spacing=0
            ),
            padding=ft.padding.all(24),
            bgcolor=Colors.SURFACE,
            border_radius=16,
            margin=ft.margin.all(24)
        )
    
    def _create_service_list_section(self):
        """创建服务列表区域"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    # 列表标题
                    ft.Row(
                        controls=[
                            ft.Text(
                                "运行中的服务",
                                size=18,
                                weight=ft.FontWeight.BOLD
                            ),
                            self._service_count_text
                        ],
                        spacing=8
                    ),
                    ft.Container(height=16),
                    # 服务列表
                    ft.Container(
                        content=ft.Stack(
                            controls=[
                                self._service_list,
                                self._empty_state
                            ]
                        ),
                        expand=True
                    )
                ],
                spacing=0,
                expand=True
            ),
            padding=ft.padding.all(24),
            expand=True
        )
    
    def _select_directory(self, e):
        """选择部署目录"""
        def on_result(result: ft.FilePickerResultEvent):
            if result.path:
                self._current_directory = result.path
                Logger.info(f"选择目录: {result.path}")
                self._show_snackbar(f"已选择目录: {result.path}", Colors.GREEN_600)
        
        file_picker = ft.FilePicker(on_result=on_result)
        self._page.overlay.append(file_picker)
        self._page.update()
        file_picker.get_directory_path(initial_directory=self._current_directory)
    
    def _start_service(self, e):
        """启动HTTP服务"""
        try:
            # 启动服务
            service = self._server_manager.startService(
                directory=self._current_directory,
                port=self._current_port,
                entry_html=self._current_html,
                auto_open_browser=True
            )
            
            # 添加到服务列表
            self._add_service_card(service)
            
            # 显示成功消息
            local_url = NetworkUtils.generateLocalURL(service.port, service.entry_html)
            self._show_snackbar(f"服务启动成功！端口: {service.port}", Colors.GREEN_600)
            
            Logger.info(f"服务启动成功: 端口{service.port}")
        
        except Exception as ex:
            Logger.exception(f"启动服务失败: {ex}")
            self._show_snackbar(f"启动服务失败: {str(ex)}", Colors.RED_600)
    
    def _add_service_card(self, service: ServiceInstance):
        """添加服务卡片"""
        # 隐藏空状态
        self._empty_state.visible = False
        
        # 创建服务卡片
        card = ServiceCard(
            service=service,
            on_stop=self._stop_service,
            on_open=self._open_browser
        )
        
        # 添加到列表
        self._service_list.controls.append(card)
        self._service_cards[service.id] = card
        
        # 更新服务计数
        self._update_service_count()
        
        # 更新UI
        self._page.update()
    
    def _stop_service(self, service_id: str):
        """停止服务"""
        def confirm_stop(e):
            dialog.open = False
            self._page.update()
            
            try:
                # 停止服务
                success = self._server_manager.stopService(service_id)
                
                if success:
                    # 从UI中移除
                    if service_id in self._service_cards:
                        card = self._service_cards[service_id]
                        self._service_list.controls.remove(card)
                        del self._service_cards[service_id]
                    
                    # 更新服务计数
                    self._update_service_count()
                    
                    # 如果没有服务了，显示空状态
                    if len(self._service_cards) == 0:
                        self._empty_state.visible = True
                    
                    self._show_snackbar("服务已停止", Colors.GREEN_600)
                    Logger.info(f"服务已停止: {service_id}")
                    self._page.update()
                else:
                    self._show_snackbar("停止服务失败", Colors.RED_600)
            
            except Exception as ex:
                Logger.exception(f"停止服务失败: {ex}")
                self._show_snackbar(f"停止服务失败: {str(ex)}", Colors.RED_600)
        
        def cancel_stop(e):
            dialog.open = False
            self._page.update()
        
        # 确认对话框
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("确认操作"),
            content=ft.Text("确定要停止这个服务吗？"),
            actions=[
                ft.TextButton("取消", on_click=cancel_stop),
                ft.FilledButton("停止", on_click=confirm_stop)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self._page.dialog = dialog
        dialog.open = True
        self._page.update()
    
    def _open_browser(self, service: ServiceInstance):
        """打开浏览器"""
        url = NetworkUtils.generateLocalURL(service.port, service.entry_html)
        webbrowser.open(url)
        Logger.info(f"打开浏览器: {url}")
        self._show_snackbar(f"已打开浏览器", Colors.BLUE_600)
    
    def _update_service_count(self):
        """更新服务计数"""
        count = len(self._service_cards)
        self._service_count_text.value = f"({count})"
        self._service_count_text.update()
    
    def _start_uptime_timer(self):
        """启动运行时长定时器"""
        import time
        import threading
        
        def update_loop():
            while True:
                time.sleep(1)
                try:
                    for card in self._service_cards.values():
                        card.update_uptime()
                except Exception as e:
                    Logger.exception(f"更新运行时长失败: {e}")
        
        # 启动后台线程
        timer_thread = threading.Thread(target=update_loop, daemon=True)
        timer_thread.start()
    
    def _open_settings(self, e):
        """打开设置对话框"""
        def on_save():
            # 重新加载配置
            self._config = self._config_manager.loadConfig()
            self._current_port = self._config.get('default_port', 9000)
            self._current_html = self._config.get('default_html', 'index.html')
            self._show_snackbar("设置已保存", Colors.GREEN_600)
        
        dialog = SettingsDialog(self._page, self._config_manager, on_save)
        dialog.show()
    
    def _show_about(self, e):
        """显示关于对话框"""
        def close_dialog(e):
            dialog.open = False
            self._page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("关于 Prism Local Server"),
            content=ft.Column(
                controls=[
                    ft.Text("版本: 2.0.0", size=14),
                    ft.Text("基于 Flet (Flutter) 构建", size=14),
                    ft.Text("作者: Kkwans", size=14),
                    ft.Text("", size=14),
                    ft.Text("一个现代化的前端静态文件部署工具", size=12, color=Colors.GREY_600)
                ],
                spacing=8,
                tight=True
            ),
            actions=[
                ft.FilledButton("关闭", on_click=close_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self._page.dialog = dialog
        dialog.open = True
        self._page.update()
    
    def _show_snackbar(self, message: str, bgcolor: str):
        """显示Snackbar提示"""
        snackbar = ft.SnackBar(
            content=ft.Text(message, color=Colors.WHITE),
            bgcolor=bgcolor,
            duration=3000
        )
        self._page.snack_bar = snackbar
        snackbar.open = True
        self._page.update()
