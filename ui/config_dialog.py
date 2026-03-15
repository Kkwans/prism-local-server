# -*- coding: utf-8 -*-
"""
配置对话框模块
实现配置项的编辑和保存
作者: Kkwans
创建时间: 2026-03-15
"""

import customtkinter as ctk
import os
from tkinter import filedialog, messagebox
from pathlib import Path
from typing import Optional

from core.config_manager import ConfigManager
from utils.logger import Logger


class ConfigDialog(ctk.CTkToplevel):
    """
    配置对话框类
    功能:
    - 编辑默认端口
    - 选择默认目录
    - 选择默认HTML文件
    - 设置自动打开浏览器
    """
    
    def __init__(self, parent, config_manager: ConfigManager):
        """
        初始化配置对话框
        参数:
            parent: 父窗口
            config_manager: 配置管理器实例
        """
        super().__init__(parent)
        
        self.config_manager = config_manager
        self.config = config_manager.loadConfig()
        
        # 窗口设置
        self.title("配置")
        self.geometry("600x500")
        self.resizable(False, False)
        
        # 居中显示
        self._centerWindow()
        
        # 创建UI
        self._createUI()
        
        # 加载当前配置
        self._loadCurrentConfig()
        
        # 设置为模态对话框
        self.transient(parent)
        self.grab_set()
        
        Logger.info("配置对话框打开")
    
    def _centerWindow(self):
        """窗口居中显示"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def _createUI(self):
        """创建用户界面"""
        # 主容器
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 标题
        title_label = ctk.CTkLabel(
            main_frame,
            text="服务器配置",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # 配置项容器
        config_frame = ctk.CTkFrame(main_frame)
        config_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # 默认端口
        self._createPortSection(config_frame)
        
        # 默认目录
        self._createDirectorySection(config_frame)
        
        # 默认HTML文件
        self._createHTMLSection(config_frame)
        
        # 自动打开浏览器
        self._createAutoOpenSection(config_frame)
        
        # 按钮区域
        self._createButtonSection(main_frame)
    
    def _createPortSection(self, parent):
        """创建端口配置区域"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=10)
        
        label = ctk.CTkLabel(
            frame,
            text="默认端口:",
            font=ctk.CTkFont(size=14)
        )
        label.pack(side="left", padx=(0, 10))
        
        self.port_entry = ctk.CTkEntry(
            frame,
            width=150,
            placeholder_text="8888"
        )
        self.port_entry.pack(side="left")
        
        hint_label = ctk.CTkLabel(
            frame,
            text="(1024-65535)",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        hint_label.pack(side="left", padx=10)
    
    def _createDirectorySection(self, parent):
        """创建目录配置区域"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=10)
        
        label = ctk.CTkLabel(
            frame,
            text="默认目录:",
            font=ctk.CTkFont(size=14)
        )
        label.pack(side="left", padx=(0, 10))
        
        self.directory_entry = ctk.CTkEntry(
            frame,
            width=300,
            placeholder_text="选择部署目录"
        )
        self.directory_entry.pack(side="left", padx=(0, 10))
        
        browse_btn = ctk.CTkButton(
            frame,
            text="浏览...",
            width=80,
            command=self._browseDirectory
        )
        browse_btn.pack(side="left")
    
    def _createHTMLSection(self, parent):
        """创建HTML文件配置区域"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=10)
        
        label = ctk.CTkLabel(
            frame,
            text="入口HTML:",
            font=ctk.CTkFont(size=14)
        )
        label.pack(side="left", padx=(0, 10))
        
        self.html_entry = ctk.CTkEntry(
            frame,
            width=200,
            placeholder_text="index.html"
        )
        self.html_entry.pack(side="left")
        
        hint_label = ctk.CTkLabel(
            frame,
            text="(留空自动检测)",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        hint_label.pack(side="left", padx=10)
    
    def _createAutoOpenSection(self, parent):
        """创建自动打开浏览器配置区域"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=10)
        
        label = ctk.CTkLabel(
            frame,
            text="自动打开浏览器:",
            font=ctk.CTkFont(size=14)
        )
        label.pack(side="left", padx=(0, 10))
        
        self.auto_open_switch = ctk.CTkSwitch(
            frame,
            text="",
            onvalue=True,
            offvalue=False
        )
        self.auto_open_switch.pack(side="left")
    
    def _createButtonSection(self, parent):
        """创建按钮区域"""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill="x")
        
        # 取消按钮
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="取消",
            width=120,
            height=36,
            corner_radius=8,
            fg_color="gray",
            hover_color="darkgray",
            command=self._cancel
        )
        cancel_btn.pack(side="right", padx=5)
        
        # 保存按钮
        save_btn = ctk.CTkButton(
            button_frame,
            text="保存",
            width=120,
            height=36,
            corner_radius=8,
            fg_color="#0078D4",
            hover_color="#005A9E",
            command=self._save
        )
        save_btn.pack(side="right", padx=5)
        
        # 恢复默认按钮
        reset_btn = ctk.CTkButton(
            button_frame,
            text="恢复默认",
            width=120,
            height=36,
            corner_radius=8,
            command=self._resetToDefault
        )
        reset_btn.pack(side="left", padx=5)
    
    def _loadCurrentConfig(self):
        """加载当前配置"""
        # 端口
        port = self.config.get('default_port', 8888)
        self.port_entry.insert(0, str(port))
        
        # 目录
        directory = self.config.get('default_directory', '')
        if directory:
            self.directory_entry.insert(0, directory)
        
        # HTML文件
        html = self.config.get('default_html', 'index.html')
        self.html_entry.insert(0, html)
        
        # 自动打开浏览器
        auto_open = self.config.get('auto_open_browser', True)
        if auto_open:
            self.auto_open_switch.select()
        else:
            self.auto_open_switch.deselect()
    
    def _browseDirectory(self):
        """浏览选择目录"""
        current_dir = self.directory_entry.get()
        if not current_dir:
            current_dir = os.getcwd()
        
        directory = filedialog.askdirectory(
            title="选择默认部署目录",
            initialdir=current_dir
        )
        
        if directory:
            self.directory_entry.delete(0, "end")
            self.directory_entry.insert(0, directory)
    
    def _validatePort(self, port_str: str) -> Optional[int]:
        """
        验证端口号
        参数:
            port_str: 端口字符串
        返回:
            有效的端口号，或None
        """
        try:
            port = int(port_str)
            if 1024 <= port <= 65535:
                return port
            else:
                messagebox.showerror(
                    "错误",
                    "端口号必须在 1024-65535 之间",
                    parent=self
                )
                return None
        except ValueError:
            messagebox.showerror(
                "错误",
                "端口号必须是数字",
                parent=self
            )
            return None
    
    def _save(self):
        """保存配置"""
        # 验证端口
        port_str = self.port_entry.get().strip()
        if not port_str:
            messagebox.showerror("错误", "请输入端口号", parent=self)
            return
        
        port = self._validatePort(port_str)
        if port is None:
            return
        
        # 获取目录
        directory = self.directory_entry.get().strip()
        if directory and not os.path.isdir(directory):
            messagebox.showerror("错误", "目录不存在", parent=self)
            return
        
        # 获取HTML文件
        html = self.html_entry.get().strip()
        if not html:
            html = "index.html"
        
        # 获取自动打开浏览器
        auto_open = self.auto_open_switch.get()
        
        # 更新配置
        self.config['default_port'] = port
        self.config['default_directory'] = directory
        self.config['default_html'] = html
        self.config['auto_open_browser'] = auto_open
        
        # 保存配置
        try:
            self.config_manager.saveConfig(self.config)
            Logger.info(f"配置已保存: {self.config}")
            messagebox.showinfo("成功", "配置已保存", parent=self)
            self.destroy()
        except Exception as e:
            Logger.exception(f"保存配置失败: {e}")
            messagebox.showerror("错误", f"保存配置失败:\n{str(e)}", parent=self)
    
    def _resetToDefault(self):
        """恢复默认配置"""
        result = messagebox.askyesno(
            "确认",
            "确定要恢复默认配置吗？",
            parent=self
        )
        
        if result:
            # 清空输入
            self.port_entry.delete(0, "end")
            self.port_entry.insert(0, "8888")
            
            self.directory_entry.delete(0, "end")
            
            self.html_entry.delete(0, "end")
            self.html_entry.insert(0, "index.html")
            
            self.auto_open_switch.select()
            
            Logger.info("配置已恢复默认值")
    
    def _cancel(self):
        """取消"""
        self.destroy()
