# -*- coding: utf-8 -*-
"""
Flet应用功能测试
测试核心功能是否正常工作
作者: Kkwans
创建时间: 2026-03-16
"""

import os
import sys
import time
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from core.http_server_manager import HTTPServerManager
from core.config_manager import ConfigManager
from utils.logger import Logger


def test_config_manager():
    """测试配置管理器"""
    print("\n=== 测试配置管理器 ===")
    
    config_manager = ConfigManager()
    
    # 测试加载配置
    config = config_manager.loadConfig()
    print(f"✓ 配置加载成功")
    print(f"  默认端口: {config.get('default_port')}")
    print(f"  默认HTML: {config.get('default_html')}")
    print(f"  配置目录: {config_manager.config_dir}")
    
    # 测试保存配置
    config_manager.setConfig('test_key', 'test_value')
    print(f"✓ 配置保存成功")
    
    return True


def test_http_server():
    """测试HTTP服务管理器"""
    print("\n=== 测试HTTP服务管理器 ===")
    
    manager = HTTPServerManager()
    
    # 测试启动服务
    test_dir = os.path.join(os.path.dirname(__file__), '..', 'prism-local-server', 'test_resources')
    if not os.path.exists(test_dir):
        test_dir = os.getcwd()
    
    print(f"测试目录: {test_dir}")
    
    try:
        service = manager.startService(
            directory=test_dir,
            port=9000,
            entry_html="index.html",
            auto_open_browser=False
        )
        print(f"✓ 服务启动成功")
        print(f"  服务ID: {service.id}")
        print(f"  端口: {service.port}")
        print(f"  状态: {service.status}")
        
        # 等待3秒
        time.sleep(3)
        print(f"  运行时长: {service.getUptime()}")
        
        # 测试获取服务列表
        services = manager.getAllServices()
        print(f"✓ 服务列表获取成功，共{len(services)}个服务")
        
        # 测试停止服务
        success = manager.stopService(service.id)
        if success:
            print(f"✓ 服务停止成功")
        else:
            print(f"✗ 服务停止失败")
            return False
        
        return True
    
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("=" * 50)
    print("Prism Local Server - Flet版本功能测试")
    print("=" * 50)
    
    # 初始化日志
    Logger.initialize()
    
    # 运行测试
    tests = [
        ("配置管理器", test_config_manager),
        ("HTTP服务管理器", test_http_server)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"\n✗ {test_name}测试异常: {e}")
            failed += 1
    
    # 输出测试结果
    print("\n" + "=" * 50)
    print(f"测试完成: {passed}个通过, {failed}个失败")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
