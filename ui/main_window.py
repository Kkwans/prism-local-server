# -*- coding: utf-8 -*-
"""
主窗口模块
实现Windows 11 Fluent Design风格的主界面
作者: Kkwans
创建时间: 2026-03-15
"""

import customtkinter as ctk
import os
import sys
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import Optional

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.http_server_manager import HTTPServerManager, ServiceInstance
from core.config_manager import ConfigManager
from utils.logger import Logger
from utils.network_utils import NetworkUtils
from ui.tray_icon import TrayIcon


# 设置CustomTkinter主题
ctk.set_appearance_mode("system")  # 跟随系统主题
ctk.set_default_color_theme("blue")  # 使用蓝色主题


class MainWindow(ctk.CTk):
    """
    主窗口类
    功能:
    - 显示服务列表
    - 启动/停止服务
    - 配置管理
    - 系统托盘集成
    """
    
    def __init__(self):
        """初始化主窗口"""
        super().__init__()
        
        # 窗口基本设置
        self.title("Prism Local Server - 棱镜本地服务器")
        self.geometry("1000x700")
        self.minsize(800, 600)
        
        # 初始化管理器
        Logger.initialize()
        self.config_manager = ConfigManager()
        self.config = self.config_manager.loadConfig()
        self.server_manager = HTTPServerManager()
        
        # 服务列表UI元素字典
        self.service_frames = {}
        
        # 当前主题
        self.current_theme = "system"
        
        # 初始化系统托盘
        self.tray_icon = TrayIcon(
            on_show=self._showWindow,
            on_hide=self._hideWindow,
            on_start_service=self._startServiceFromTray,
            on_quit=self._quitFromTray
        )
        self.tray_icon.start()
        
        # 创建UI
        self._createUI()
        
        # 加载配置
        self._loadConfig()
        
        Logger.info("主窗口初始化完成")
    
    def _createUI(self):
        """创建用户界面"""
        # 创建主容器
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 创建顶部区域
        self._createTopSection()
        
        # 创建服务列表区域
        self._createServiceListSection()
    
    def _createTopSection(self):
        """创建顶部快速启动区域"""
        top_frame = ctk.CTkFrame(self.main_container)
        top_frame.pack(fill="x", pady=(0, 20))
        
        # 标题
        title_label = ctk.CTkLabel(
            top_frame,
            text="快速启动",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(side="left", padx=20, pady=15)
        
        # 按钮容器
        button_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        button_frame.pack(side="right", padx=20, pady=15)
        
        # 选择目录按钮
        self.select_dir_btn = ctk.CTkButton(
            button_frame,
            text="📁 选择目录",
            width=120,
            height=36,
            corner_radius=8,
            command=self._selectDirectory
        )
        self.select_dir_btn.pack(side="left", padx=5)
        
        # 主题切换按钮
        self.theme_btn = ctk.CTkButton(
            button_frame,
            text="🌙",
            width=40,
            height=36,
            corner_radius=8,
            command=self._toggleTheme
        )
        self.theme_btn.pack(side="left", padx=5)
        
        # 配置按钮
        self.config_btn = ctk.CTkButton(
            button_frame,
            text="⚙️ 配置",
            width=100,
            height=36,
            corner_radius=8,
            command=self._openConfig
        )
        self.config_btn.pack(side="left", padx=5)
        
        # 启动服务按钮
        self.start_btn = ctk.CTkButton(
            button_frame,
            text="🚀 启动服务",
            width=120,
            height=36,
            corner_radius=8,
            fg_color="#0078D4",
            hover_color="#005A9E",
            command=self._startService
        )
        self.start_btn.pack(side="left", padx=5)
    
    def _createServiceListSection(self):
        """创建服务列表区域"""
        # 列表标题
        list_header = ctk.CTkFrame(self.main_container)
        list_header.pack(fill="x", pady=(0, 10))
        
        header_label = ctk.CTkLabel(
            list_header,
            text="运行中的服务",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        header_label.pack(side="left", padx=20, pady=10)
        
        self.service_count_label = ctk.CTkLabel(
            list_header,
            text="(0)",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.service_count_label.pack(side="left", padx=5, pady=10)
        
        # 服务列表容器（可滚动）
        self.service_list_frame = ctk.CTkScrollableFrame(
            self.main_container,
            fg_color="transparent"
        )
        self.service_list_frame.pack(fill="both", expand=True)
        
        # 空状态提示
        self.empty_label = ctk.CTkLabel(
            self.service_list_frame,
            text="暂无运行中的服务\n点击\"启动服务\"按钮开始",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.empty_label.pack(pady=50)

    
    def _loadConfig(self):
        """加载配置"""
        self.current_directory = self.config.get('default_directory', '')
        if not self.current_directory:
            self.current_directory = os.getcwd()
        
        self.current_port = self.config.get('default_port', 9000)
        self.current_html = self.config.get('default_html', 'index.html')
    
    def _selectDirectory(self):
        """选择部署目录"""
        directory = filedialog.askdirectory(
            title="选择部署目录",
            initialdir=self.current_directory
        )
        
        if directory:
            self.current_directory = directory
            Logger.info(f"选择目录: {directory}")
            messagebox.showinfo("成功", f"已选择目录:\n{directory}")
    
    def _toggleTheme(self):
        """切换主题"""
        if self.current_theme == "light":
            ctk.set_appearance_mode("dark")
            self.current_theme = "dark"
            self.theme_btn.configure(text="☀️")
            Logger.info("切换到深色主题")
        elif self.current_theme == "dark":
            ctk.set_appearance_mode("system")
            self.current_theme = "system"
            self.theme_btn.configure(text="🌓")
            Logger.info("切换到系统主题")
        else:
            ctk.set_appearance_mode("light")
            self.current_theme = "light"
            self.theme_btn.configure(text="🌙")
            Logger.info("切换到浅色主题")
    
    def _openConfig(self):
        """打开配置对话框"""
        from ui.config_dialog import ConfigDialog
        dialog = ConfigDialog(self, self.config_manager)
        dialog.wait_window()
        
        # 重新加载配置
        self._loadConfig()
    
    def _startService(self):
        """启动HTTP服务"""
        try:
            # 禁用启动按钮
            self.start_btn.configure(state="disabled", text="启动中...")
            self.update()
            
            # 启动服务
            service = self.server_manager.startService(
                directory=self.current_directory,
                port=self.current_port,
                entry_html=self.current_html,
                auto_open_browser=True
            )
            
            # 添加到服务列表
            self._addServiceToList(service)
            
            # 更新服务计数
            self._updateServiceCount()
            
            # 显示成功消息
            local_url = NetworkUtils.generateLocalURL(service.port, service.entry_html)
            lan_url = NetworkUtils.generateLANURL(service.port, service.entry_html)
            
            message = f"服务启动成功！\n\n"
            message += f"端口: {service.port}\n"
            message += f"本地访问: {local_url}\n"
            if lan_url:
                message += f"局域网访问: {lan_url}"
            
            messagebox.showinfo("成功", message)
            
            Logger.info(f"服务启动成功: 端口{service.port}")
        
        except Exception as e:
            Logger.exception(f"启动服务失败: {e}")
            messagebox.showerror("错误", f"启动服务失败:\n{str(e)}")
        
        finally:
            # 恢复启动按钮
            self.start_btn.configure(state="normal", text="🚀 启动服务")
    
    def _addServiceToList(self, service: ServiceInstance):
        """添加服务到列表"""
        # 隐藏空状态提示
        self.empty_label.pack_forget()
        
        # 创建服务卡片
        service_card = ctk.CTkFrame(
            self.service_list_frame,
            corner_radius=8
        )
        service_card.pack(fill="x", pady=8, padx=10)
        
        # 左侧信息区域
        info_frame = ctk.CTkFrame(service_card, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=20, pady=15)
        
        # 状态和端口
        status_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        status_frame.pack(fill="x", pady=(0, 8))
        
        status_label = ctk.CTkLabel(
            status_frame,
            text="🟢 运行中",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#107C10"
        )
        status_label.pack(side="left")
        
        port_label = ctk.CTkLabel(
            status_frame,
            text=f"端口 {service.port}",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        port_label.pack(side="left", padx=10)
        
        uptime_label = ctk.CTkLabel(
            status_frame,
            text=f"运行时长: {service.getUptime()}",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        uptime_label.pack(side="left", padx=10)
        
        # 目录路径
        dir_label = ctk.CTkLabel(
            info_frame,
            text=f"📂 {service.directory}",
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        dir_label.pack(fill="x", pady=(0, 5))
        
        # 访问地址
        local_url = NetworkUtils.generateLocalURL(service.port, service.entry_html)
        url_label = ctk.CTkLabel(
            info_frame,
            text=f"🌐 {local_url}",
            font=ctk.CTkFont(size=12),
            text_color="#0078D4",
            anchor="w"
        )
        url_label.pack(fill="x")
        
        # 右侧按钮区域
        button_frame = ctk.CTkFrame(service_card, fg_color="transparent")
        button_frame.pack(side="right", padx=20, pady=15)
        
        # 打开浏览器按钮
        open_btn = ctk.CTkButton(
            button_frame,
            text="🌍 打开",
            width=80,
            height=32,
            corner_radius=6,
            command=lambda: self._openBrowser(service)
        )
        open_btn.pack(side="left", padx=5)
        
        # 停止按钮
        stop_btn = ctk.CTkButton(
            button_frame,
            text="⏹️ 停止",
            width=80,
            height=32,
            corner_radius=6,
            fg_color="#D13438",
            hover_color="#A52A2A",
            command=lambda: self._stopService(service.id)
        )
        stop_btn.pack(side="left", padx=5)
        
        # 保存服务卡片引用
        self.service_frames[service.id] = {
            'card': service_card,
            'uptime_label': uptime_label
        }
        
        # 启动定时更新运行时长
        self._updateUptime(service.id)
    
    def _updateUptime(self, service_id: str):
        """更新服务运行时长"""
        if service_id not in self.service_frames:
            return
        
        service = self.server_manager.getService(service_id)
        if service and service.status == "running":
            uptime_label = self.service_frames[service_id]['uptime_label']
            uptime_label.configure(text=f"运行时长: {service.getUptime()}")
            
            # 1秒后再次更新
            self.after(1000, lambda: self._updateUptime(service_id))
    
    def _openBrowser(self, service: ServiceInstance):
        """打开浏览器"""
        import webbrowser
        url = NetworkUtils.generateLocalURL(service.port, service.entry_html)
        webbrowser.open(url)
        Logger.info(f"打开浏览器: {url}")
    
    def _stopService(self, service_id: str):
        """停止服务"""
        # 确认对话框
        result = messagebox.askyesno(
            "确认",
            "确定要停止这个服务吗？",
            icon='warning'
        )
        
        if not result:
            return
        
        try:
            # 停止服务
            success = self.server_manager.stopService(service_id)
            
            if success:
                # 从UI中移除
                if service_id in self.service_frames:
                    self.service_frames[service_id]['card'].destroy()
                    del self.service_frames[service_id]
                
                # 更新服务计数
                self._updateServiceCount()
                
                # 如果没有服务了，显示空状态
                if len(self.service_frames) == 0:
                    self.empty_label.pack(pady=50)
                
                messagebox.showinfo("成功", "服务已停止")
                Logger.info(f"服务已停止: {service_id}")
            else:
                messagebox.showerror("错误", "停止服务失败")
        
        except Exception as e:
            Logger.exception(f"停止服务失败: {e}")
            messagebox.showerror("错误", f"停止服务失败:\n{str(e)}")
    
    def _updateServiceCount(self):
        """更新服务计数"""
        count = len(self.service_frames)
        self.service_count_label.configure(text=f"({count})")
    
    def _showWindow(self):
        """显示主窗口"""
        self.deiconify()
        self.lift()
        self.focus_force()
    
    def _hideWindow(self):
        """隐藏主窗口"""
        self.withdraw()
    
    def _startServiceFromTray(self):
        """从托盘启动服务"""
        self._showWindow()
        self._startService()
    
    def _quitFromTray(self):
        """从托盘退出"""
        self.on_closing()
    
    def on_closing(self):
        """窗口关闭事件"""
        # 如果有服务运行，询问是最小化到托盘还是退出
        if len(self.service_frames) > 0:
            result = messagebox.askyesnocancel(
                "确认操作",
                f"当前有 {len(self.service_frames)} 个服务正在运行\n\n"
                "是 - 最小化到托盘（服务继续运行）\n"
                "否 - 停止所有服务并退出\n"
                "取消 - 返回",
                icon='question'
            )
            
            if result is None:  # 取消
                return
            elif result:  # 是 - 最小化到托盘
                self._hideWindow()
                return
            else:  # 否 - 停止服务并退出
                self.server_manager.stopAllServices()
        
        # 停止托盘图标
        self.tray_icon.stop()
        
        Logger.info("应用程序退出")
        self.destroy()


def main():
    """主函数"""
    app = MainWindow()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()


if __name__ == "__main__":
    main()
