# -*- coding: utf-8 -*-
"""
设置对话框
作者: Kkwans
创建时间: 2026-03-16
"""

import flet as ft
from core.config_manager import ConfigManager
from utils.logger import Logger


class SettingsDialog:
    """设置对话框"""
    
    def __init__(self, page: ft.Page, config_manager: ConfigManager, on_save):
        """初始化设置对话框"""
        self.page = page
        self.config_manager = config_manager
        self.on_save = on_save
        
        # 加载当前配置
        self.config = config_manager.getAllConfig()
        
        # 创建输入控件
        self.port_field = ft.TextField(
            label="默认端口",
            value=str(self.config.get('default_port', 9000)),
            keyboard_type=ft.KeyboardType.NUMBER,
            width=200
        )
        
        self.html_field = ft.TextField(
            label="默认HTML文件",
            value=self.config.get('default_html', 'index.html'),
            width=300
        )
        
        self.auto_open_switch = ft.Switch(
            label="启动后自动打开浏览器",
            value=self.config.get('auto_open_browser', True)
        )
        
        # 创建对话框
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("设置"),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        self.port_field,
                        ft.Container(height=16),
                        self.html_field,
                        ft.Container(height=16),
                        self.auto_open_switch
                    ],
                    spacing=0,
                    tight=True
                ),
                width=400,
                padding=ft.padding.symmetric(vertical=20)
            ),
            actions=[
                ft.TextButton("取消", on_click=self._close),
                ft.FilledButton("保存", on_click=self._save)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
    
    def show(self):
        """显示对话框"""
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()
    
    def _close(self, e):
        """关闭对话框"""
        self.dialog.open = False
        self.page.update()
    
    def _save(self, e):
        """保存设置"""
        try:
            # 验证端口
            port = int(self.port_field.value)
            if port < 1024 or port > 65535:
                self._show_error("端口号必须在1024-65535范围内")
                return
            
            # 验证HTML文件名
            html_file = self.html_field.value.strip()
            if not html_file:
                self._show_error("HTML文件名不能为空")
                return
            
            # 保存配置
            self.config_manager.setConfig('default_port', port)
            self.config_manager.setConfig('default_html', html_file)
            self.config_manager.setConfig('auto_open_browser', self.auto_open_switch.value)
            
            Logger.info(f"配置已保存: 端口={port}, HTML={html_file}")
            
            # 关闭对话框
            self.dialog.open = False
            self.page.update()
            
            # 回调通知
            if self.on_save:
                self.on_save()
        
        except ValueError:
            self._show_error("端口号必须是数字")
        except Exception as ex:
            Logger.exception(f"保存配置失败: {ex}")
            self._show_error(f"保存失败: {str(ex)}")
    
    def _show_error(self, message: str):
        """显示错误提示"""
        snackbar = ft.SnackBar(
            content=ft.Text(message, color=ft.colors.WHITE),
            bgcolor=ft.colors.RED_600
        )
        self.page.snack_bar = snackbar
        snackbar.open = True
        self.page.update()
