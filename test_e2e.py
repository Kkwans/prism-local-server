# -*- coding: utf-8 -*-
"""
端到端测试
测试完整的应用流程
作者: Kkwans
创建时间: 2026-03-16
"""

import os
import sys
import time
import requests
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from core.http_server_manager import HTTPServerManager
from core.config_manager import ConfigManager
from utils.logger import Logger


def test_scenario_1():
    """
    测试场景1: 单服务启动和停止
    """
    print("\n" + "=" * 60)
    print("测试场景1: 单服务启动和停止")
    print("=" * 60)
    
    manager = HTTPServerManager()
    test_dir = os.path.join(os.path.dirname(__file__), 'test_demo')
    
    try:
        # 启动服务
        print("\n[1/4] 启动服务...")
        service = manager.startService(
            directory=test_dir,
            port=9000,
            entry_html="index.html",
            auto_open_browser=False
        )
        print(f"✓ 服务启动成功: {service.id}, 端口{service.port}")
        
        # 验证服务可访问
        print("\n[2/4] 验证服务可访问...")
        time.sleep(1)
        response = requests.get(f"http://localhost:{service.port}/index.html", timeout=5)
        if response.status_code == 200:
            print(f"✓ 服务可访问")
        else:
            print(f"✗ 服务不可访问: {response.status_code}")
            return False
        
        # 检查运行时长
        print("\n[3/4] 检查运行时长...")
        time.sleep(2)
        uptime = service.getUptime()
        print(f"✓ 运行时长: {uptime}")
        
        # 停止服务
        print("\n[4/4] 停止服务...")
        success = manager.stopService(service.id)
        if success:
            print(f"✓ 服务停止成功")
        else:
            print(f"✗ 服务停止失败")
            return False
        
        print("\n✓ 测试场景1通过")
        return True
    
    except Exception as e:
        print(f"\n✗ 测试场景1失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_scenario_2():
    """
    测试场景2: 多服务并发运行
    """
    print("\n" + "=" * 60)
    print("测试场景2: 多服务并发运行")
    print("=" * 60)
    
    manager = HTTPServerManager()
    test_dir = os.path.join(os.path.dirname(__file__), 'test_demo')
    
    try:
        # 启动3个服务
        print("\n[1/4] 启动3个服务...")
        services = []
        for i in range(3):
            service = manager.startService(
                directory=test_dir,
                port=9000 + i,
                entry_html="index.html",
                auto_open_browser=False
            )
            services.append(service)
            print(f"✓ 服务{i+1}启动: {service.id}, 端口{service.port}")
        
        # 验证所有服务可访问
        print("\n[2/4] 验证所有服务可访问...")
        time.sleep(1)
        for service in services:
            response = requests.get(f"http://localhost:{service.port}/index.html", timeout=5)
            if response.status_code == 200:
                print(f"✓ 服务{service.id}可访问")
            else:
                print(f"✗ 服务{service.id}不可访问")
                return False
        
        # 检查服务数量
        print("\n[3/4] 检查服务数量...")
        count = manager.getServiceCount()
        if count == 3:
            print(f"✓ 服务数量正确: {count}")
        else:
            print(f"✗ 服务数量错误: {count}, 期望3")
            return False
        
        # 停止所有服务
        print("\n[4/4] 停止所有服务...")
        stopped = manager.stopAllServices()
        if stopped == 3:
            print(f"✓ 所有服务已停止: {stopped}")
        else:
            print(f"✗ 停止服务失败: {stopped}/3")
            return False
        
        print("\n✓ 测试场景2通过")
        return True
    
    except Exception as e:
        print(f"\n✗ 测试场景2失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_scenario_3():
    """
    测试场景3: 端口自动切换
    """
    print("\n" + "=" * 60)
    print("测试场景3: 端口自动切换")
    print("=" * 60)
    
    manager = HTTPServerManager()
    test_dir = os.path.join(os.path.dirname(__file__), 'test_demo')
    
    try:
        # 启动第一个服务占用9000端口
        print("\n[1/3] 启动服务占用9000端口...")
        service1 = manager.startService(
            directory=test_dir,
            port=9000,
            entry_html="index.html",
            auto_open_browser=False
        )
        print(f"✓ 服务1启动: 端口{service1.port}")
        
        # 再次请求9000端口，应该自动切换到9001
        print("\n[2/3] 再次请求9000端口，测试自动切换...")
        service2 = manager.startService(
            directory=test_dir,
            port=9000,
            entry_html="index.html",
            auto_open_browser=False
        )
        
        if service2.port == 9001:
            print(f"✓ 端口自动切换成功: {service2.port}")
        else:
            print(f"✗ 端口切换失败: {service2.port}, 期望9001")
            return False
        
        # 停止所有服务
        print("\n[3/3] 停止所有服务...")
        manager.stopAllServices()
        print(f"✓ 所有服务已停止")
        
        print("\n✓ 测试场景3通过")
        return True
    
    except Exception as e:
        print(f"\n✗ 测试场景3失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_scenario_4():
    """
    测试场景4: 配置管理
    """
    print("\n" + "=" * 60)
    print("测试场景4: 配置管理")
    print("=" * 60)
    
    config_manager = ConfigManager()
    
    try:
        # 加载配置
        print("\n[1/4] 加载配置...")
        config = config_manager.loadConfig()
        print(f"✓ 配置加载成功")
        print(f"  默认端口: {config.get('default_port')}")
        print(f"  默认HTML: {config.get('default_html')}")
        
        # 修改配置
        print("\n[2/4] 修改配置...")
        config_manager.setConfig('default_port', 9999)
        config_manager.setConfig('default_html', 'test.html')
        print(f"✓ 配置修改成功")
        
        # 重新加载验证
        print("\n[3/4] 重新加载验证...")
        config = config_manager.loadConfig()
        if config.get('default_port') == 9999 and config.get('default_html') == 'test.html':
            print(f"✓ 配置持久化成功")
        else:
            print(f"✗ 配置持久化失败")
            return False
        
        # 恢复默认配置
        print("\n[4/4] 恢复默认配置...")
        config_manager.setConfig('default_port', 9000)
        config_manager.setConfig('default_html', 'index.html')
        print(f"✓ 配置已恢复")
        
        print("\n✓ 测试场景4通过")
        return True
    
    except Exception as e:
        print(f"\n✗ 测试场景4失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("=" * 60)
    print("Prism Local Server - 端到端测试")
    print("=" * 60)
    
    # 初始化日志
    Logger.initialize()
    
    # 运行所有测试场景
    scenarios = [
        ("单服务启动和停止", test_scenario_1),
        ("多服务并发运行", test_scenario_2),
        ("端口自动切换", test_scenario_3),
        ("配置管理", test_scenario_4)
    ]
    
    passed = 0
    failed = 0
    
    for scenario_name, test_func in scenarios:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"\n✗ {scenario_name}测试异常: {e}")
            failed += 1
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print(f"测试完成: {passed}个通过, {failed}个失败")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
