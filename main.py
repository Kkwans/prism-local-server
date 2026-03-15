# -*- coding: utf-8 -*-
"""
Prism Local Server - 主程序入口
棱镜本地服务器 - 快速部署HTML静态文件到本地HTTP服务器
作者: Kkwans
创建时间: 2026-03-15
版本: 0.1.0
"""

import os
import sys
import time
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from core.config_manager import ConfigManager
from core.http_server_manager import HTTPServerManager
from utils.logger import Logger
from utils.network_utils import NetworkUtils


class PrismLocalServer:
    """
    Prism Local Server 主类
    功能:
    - 初始化各个模块
    - 管理服务生命周期
    - 提供命令行接口（临时）
    """
    
    def __init__(self):
        """初始化应用程序"""
        print("=" * 60)
        print("  Prism Local Server - 棱镜本地服务器")
        print("  版本: 0.1.0")
        print("=" * 60)
        print()
        
        # 初始化日志系统
        Logger.initialize()
        Logger.info("应用程序启动")
        
        # 初始化配置管理器
        self.config_manager = ConfigManager()
        self.config = self.config_manager.loadConfig()
        Logger.info(f"配置加载完成: {self.config}")
        
        # 初始化HTTP服务管理器
        self.server_manager = HTTPServerManager()
        Logger.info("HTTP服务管理器初始化完成")
    
    def run(self):
        """运行应用程序（命令行模式）"""
        try:
            # 获取当前目录作为默认部署目录
            default_directory = self.config.get('default_directory')
            if not default_directory:
                default_directory = os.getcwd()
            
            default_port = self.config.get('default_port', 8888)
            default_html = self.config.get('default_html', 'index.html')
            auto_open = self.config.get('auto_open_browser', True)
            
            print(f"\n默认配置:")
            print(f"  部署目录: {default_directory}")
            print(f"  监听端口: {default_port}")
            print(f"  入口文件: {default_html}")
            print(f"  自动打开浏览器: {'是' if auto_open else '否'}")
            print()
            
            # 启动服务
            Logger.info("准备启动HTTP服务")
            service = self.server_manager.startService(
                directory=default_directory,
                port=default_port,
                entry_html=default_html,
                auto_open_browser=auto_open
            )
            
            # 显示访问信息
            print(f"\n✓ 服务启动成功！")
            print(f"\n访问地址:")
            print(f"  本地访问: {NetworkUtils.generateLocalURL(service.port, service.entry_html)}")
            
            lan_url = NetworkUtils.generateLANURL(service.port, service.entry_html)
            if lan_url:
                print(f"  局域网访问: {lan_url}")
            
            all_lan_urls = NetworkUtils.generateAllLANURLs(service.port, service.entry_html)
            if len(all_lan_urls) > 1:
                print(f"\n  所有网卡地址:")
                for url in all_lan_urls:
                    print(f"    - {url}")
            
            print(f"\n按 Ctrl+C 停止服务")
            print()
            
            # 保持运行
            while True:
                time.sleep(1)
        
        except KeyboardInterrupt:
            print("\n\n正在停止服务...")
            Logger.info("收到停止信号")
            self.shutdown()
        
        except Exception as e:
            Logger.exception(f"运行时错误: {e}")
            print(f"\n错误: {e}")
            self.shutdown()
    
    def shutdown(self):
        """关闭应用程序"""
        Logger.info("开始关闭应用程序")
        
        # 停止所有服务
        count = self.server_manager.stopAllServices()
        Logger.info(f"已停止 {count} 个服务")
        
        Logger.info("应用程序已关闭")
        print("再见！")


def main():
    """主函数"""
    try:
        app = PrismLocalServer()
        app.run()
    except Exception as e:
        print(f"启动失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
