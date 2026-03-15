# -*- coding: utf-8 -*-
"""
功能测试脚本
测试Prism Local Server的核心功能
作者: Kkwans
创建时间: 2026-03-15
"""

import os
import sys
import time
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.config_manager import ConfigManager
from core.port_manager import PortManager
from core.http_server_manager import HTTPServerManager
from utils.logger import Logger
from utils.network_utils import NetworkUtils


def test_config_manager():
    """测试配置管理器"""
    print("\n" + "=" * 60)
    print("测试1: 配置管理器")
    print("=" * 60)
    
    config_manager = ConfigManager()
    
    # 测试加载配置
    config = config_manager.loadConfig()
    print(f"✓ 配置加载成功: {config}")
    
    # 测试修改配置
    config_manager.setConfig("default_port", 9000)
    new_config = config_manager.getAllConfig()
    assert new_config["default_port"] == 9000, "配置修改失败"
    print(f"✓ 配置修改成功: 端口 {new_config['default_port']}")
    
    # 恢复默认配置
    config_manager.setConfig("default_port", 8888)
    print("✓ 配置管理器测试通过")


def test_port_manager():
    """测试端口管理器"""
    print("\n" + "=" * 60)
    print("测试2: 端口管理器")
    print("=" * 60)
    
    # 测试端口可用性检测
    port = 8888
    is_available = PortManager.isPortAvailable(port)
    print(f"✓ 端口{port}可用性检测: {'可用' if is_available else '被占用'}")
    
    # 测试查找可用端口
    available_port = PortManager.findAvailablePort(8888)
    print(f"✓ 找到可用端口: {available_port}")
    
    # 测试端口范围验证
    assert PortManager.validatePortRange(8888) == True
    assert PortManager.validatePortRange(80) == False
    print("✓ 端口范围验证正常")
    
    print("✓ 端口管理器测试通过")


def test_network_utils():
    """测试网络工具"""
    print("\n" + "=" * 60)
    print("测试3: 网络工具")
    print("=" * 60)
    
    # 测试获取本机IP
    local_ip = NetworkUtils.getLocalIP()
    print(f"✓ 本机IP: {local_ip}")
    
    # 测试获取所有IP
    all_ips = NetworkUtils.getAllLocalIPs()
    print(f"✓ 所有网卡IP: {all_ips}")
    
    # 测试生成URL
    local_url = NetworkUtils.generateLocalURL(8888, "index.html")
    print(f"✓ 本地URL: {local_url}")
    
    lan_url = NetworkUtils.generateLANURL(8888, "index.html")
    print(f"✓ 局域网URL: {lan_url}")
    
    print("✓ 网络工具测试通过")


def test_http_server():
    """测试HTTP服务器"""
    print("\n" + "=" * 60)
    print("测试4: HTTP服务器")
    print("=" * 60)
    
    manager = HTTPServerManager()
    
    # 测试启动服务
    print("启动HTTP服务...")
    service = manager.startService(
        directory=os.getcwd(),
        port=8888,
        entry_html="test_index.html",
        auto_open_browser=False
    )
    print(f"✓ 服务启动成功: 端口{service.port}")
    
    # 等待服务完全启动
    time.sleep(2)
    
    # 测试HTTP请求
    try:
        url = f"http://localhost:{service.port}/test_index.html"
        response = requests.get(url, timeout=5)
        assert response.status_code == 200, f"HTTP请求失败: {response.status_code}"
        print(f"✓ HTTP请求成功: 状态码{response.status_code}")
        print(f"✓ 响应内容长度: {len(response.text)} 字节")
    except Exception as e:
        print(f"✗ HTTP请求失败: {e}")
    
    # 测试服务运行时长
    time.sleep(1)
    uptime = service.getUptime()
    print(f"✓ 服务运行时长: {uptime}")
    
    # 测试获取所有服务
    services = manager.getAllServices()
    print(f"✓ 运行中的服务数量: {len(services)}")
    
    # 测试停止服务
    print("停止HTTP服务...")
    success = manager.stopService(service.id)
    assert success, "停止服务失败"
    print(f"✓ 服务停止成功")
    
    print("✓ HTTP服务器测试通过")


def test_multi_services():
    """测试多服务管理"""
    print("\n" + "=" * 60)
    print("测试5: 多服务管理")
    print("=" * 60)
    
    manager = HTTPServerManager()
    
    # 启动多个服务
    services = []
    for i in range(3):
        port = 8888 + i
        print(f"启动服务{i+1}...")
        service = manager.startService(
            directory=os.getcwd(),
            port=port,
            entry_html="test_index.html",
            auto_open_browser=False
        )
        services.append(service)
        print(f"✓ 服务{i+1}启动成功: 端口{service.port}")
    
    time.sleep(2)
    
    # 验证所有服务都在运行
    all_services = manager.getAllServices()
    assert len(all_services) == 3, f"服务数量不正确: {len(all_services)}"
    print(f"✓ 所有服务运行正常: {len(all_services)}个")
    
    # 停止所有服务
    print("停止所有服务...")
    count = manager.stopAllServices()
    assert count == 3, f"停止服务数量不正确: {count}"
    print(f"✓ 已停止{count}个服务")
    
    print("✓ 多服务管理测试通过")


def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("  Prism Local Server - 功能测试")
    print("=" * 60)
    
    # 初始化日志
    Logger.initialize()
    
    try:
        # 运行所有测试
        test_config_manager()
        test_port_manager()
        test_network_utils()
        test_http_server()
        test_multi_services()
        
        print("\n" + "=" * 60)
        print("  ✓ 所有测试通过！")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n✗ 测试失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ 测试异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
