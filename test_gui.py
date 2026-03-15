# -*- coding: utf-8 -*-
"""
GUI功能测试脚本
测试主窗口、配置对话框和系统托盘功能
作者: Kkwans
创建时间: 2026-03-15
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from utils.logger import Logger


def test_imports():
    """测试所有模块导入"""
    print("=" * 60)
    print("测试模块导入...")
    print("=" * 60)
    
    try:
        # 测试UI模块导入
        print("\n1. 测试UI模块导入...")
        from ui.main_window import MainWindow
        print("   ✓ MainWindow 导入成功")
        
        from ui.config_dialog import ConfigDialog
        print("   ✓ ConfigDialog 导入成功")
        
        from ui.tray_icon import TrayIcon
        print("   ✓ TrayIcon 导入成功")
        
        # 测试核心模块导入
        print("\n2. 测试核心模块导入...")
        from core.config_manager import ConfigManager
        print("   ✓ ConfigManager 导入成功")
        
        from core.http_server_manager import HTTPServerManager
        print("   ✓ HTTPServerManager 导入成功")
        
        from core.port_manager import PortManager
        print("   ✓ PortManager 导入成功")
        
        from core.resource_handler import ResourceHandler
        print("   ✓ ResourceHandler 导入成功")
        
        # 测试工具模块导入
        print("\n3. 测试工具模块导入...")
        from utils.logger import Logger
        print("   ✓ Logger 导入成功")
        
        from utils.network_utils import NetworkUtils
        print("   ✓ NetworkUtils 导入成功")
        
        print("\n" + "=" * 60)
        print("✓ 所有模块导入测试通过！")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n✗ 模块导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_config_manager():
    """测试配置管理器"""
    print("\n" + "=" * 60)
    print("测试配置管理器...")
    print("=" * 60)
    
    try:
        from core.config_manager import ConfigManager
        
        config_manager = ConfigManager()
        config = config_manager.loadConfig()
        
        print(f"\n当前配置:")
        print(f"  默认端口: {config.get('default_port', 8888)}")
        print(f"  默认目录: {config.get('default_directory', '当前目录')}")
        print(f"  默认HTML: {config.get('default_html', 'index.html')}")
        print(f"  自动打开浏览器: {config.get('auto_open_browser', True)}")
        
        print("\n✓ 配置管理器测试通过！")
        return True
        
    except Exception as e:
        print(f"\n✗ 配置管理器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_port_manager():
    """测试端口管理器"""
    print("\n" + "=" * 60)
    print("测试端口管理器...")
    print("=" * 60)
    
    try:
        from core.port_manager import PortManager
        
        # 测试端口可用性检测
        print("\n1. 测试端口可用性检测...")
        is_available = PortManager.isPortAvailable(8888)
        print(f"   端口 8888 可用: {is_available}")
        
        # 测试查找可用端口
        print("\n2. 测试查找可用端口...")
        available_port = PortManager.findAvailablePort(8888)
        print(f"   找到可用端口: {available_port}")
        
        print("\n✓ 端口管理器测试通过！")
        return True
        
    except Exception as e:
        print(f"\n✗ 端口管理器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_network_utils():
    """测试网络工具"""
    print("\n" + "=" * 60)
    print("测试网络工具...")
    print("=" * 60)
    
    try:
        from utils.network_utils import NetworkUtils
        
        # 测试获取本机IP
        print("\n1. 测试获取本机IP...")
        local_ip = NetworkUtils.getLocalIP()
        print(f"   本机IP: {local_ip}")
        
        # 测试生成URL
        print("\n2. 测试生成URL...")
        local_url = NetworkUtils.generateLocalURL(8888, "index.html")
        print(f"   本地URL: {local_url}")
        
        lan_url = NetworkUtils.generateLANURL(8888, "index.html")
        print(f"   局域网URL: {lan_url}")
        
        print("\n✓ 网络工具测试通过！")
        return True
        
    except Exception as e:
        print(f"\n✗ 网络工具测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "Prism Local Server" + " " * 25 + "║")
    print("║" + " " * 20 + "GUI功能测试" + " " * 26 + "║")
    print("╚" + "═" * 58 + "╝")
    
    # 初始化日志
    Logger.initialize()
    
    # 运行测试
    results = []
    results.append(("模块导入", test_imports()))
    results.append(("配置管理器", test_config_manager()))
    results.append(("端口管理器", test_port_manager()))
    results.append(("网络工具", test_network_utils()))
    
    # 显示测试结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name:20s} {status}")
    
    # 统计
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print("\n" + "=" * 60)
    print(f"总计: {passed}/{total} 测试通过")
    print("=" * 60)
    
    if passed == total:
        print("\n✓ 所有测试通过！可以启动GUI应用程序。")
        print("\n运行命令: python main.py")
    else:
        print("\n✗ 部分测试失败，请检查错误信息。")
    
    print()


if __name__ == "__main__":
    main()
