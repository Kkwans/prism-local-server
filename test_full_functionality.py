# -*- coding: utf-8 -*-
"""
完整功能测试
测试HTTP服务和资源加载
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
from utils.logger import Logger


def test_resource_loading():
    """测试资源加载"""
    print("\n=== 测试资源加载 ===")
    
    manager = HTTPServerManager()
    
    # 使用test_demo目录
    test_dir = os.path.join(os.path.dirname(__file__), 'test_demo')
    
    try:
        # 启动服务
        service = manager.startService(
            directory=test_dir,
            port=9000,
            entry_html="index.html",
            auto_open_browser=False
        )
        
        print(f"✓ 服务启动成功，端口: {service.port}")
        
        # 等待服务完全启动
        time.sleep(1)
        
        # 测试资源加载
        base_url = f"http://localhost:{service.port}"
        
        # 测试HTML
        print("\n测试HTML加载...")
        response = requests.get(f"{base_url}/index.html", timeout=5)
        if response.status_code == 200 and 'Prism Local Server' in response.text:
            print(f"✓ HTML加载成功 ({len(response.content)} bytes)")
        else:
            print(f"✗ HTML加载失败: {response.status_code}")
            return False
        
        # 测试CSS
        print("\n测试CSS加载...")
        response = requests.get(f"{base_url}/css/style.css", timeout=5)
        if response.status_code == 200 and 'Prism Local Server' in response.text:
            print(f"✓ CSS加载成功 ({len(response.content)} bytes)")
        else:
            print(f"✗ CSS加载失败: {response.status_code}")
            return False
        
        # 测试JS
        print("\n测试JS加载...")
        response = requests.get(f"{base_url}/js/script.js", timeout=5)
        if response.status_code == 200 and 'Prism Local Server' in response.text:
            print(f"✓ JS加载成功 ({len(response.content)} bytes)")
        else:
            print(f"✗ JS加载失败: {response.status_code}")
            return False
        
        # 测试图片
        print("\n测试图片加载...")
        response = requests.get(f"{base_url}/images/test.png", timeout=5)
        if response.status_code == 200:
            print(f"✓ 图片加载成功 ({len(response.content)} bytes)")
        else:
            print(f"✗ 图片加载失败: {response.status_code}")
            return False
        
        print("\n✓ 所有资源加载测试通过！")
        
        # 停止服务
        manager.stopService(service.id)
        print(f"✓ 服务已停止")
        
        return True
    
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("=" * 60)
    print("Prism Local Server - 完整功能测试")
    print("=" * 60)
    
    # 初始化日志
    Logger.initialize()
    
    # 运行测试
    success = test_resource_loading()
    
    # 输出结果
    print("\n" + "=" * 60)
    if success:
        print("✓ 测试通过")
    else:
        print("✗ 测试失败")
    print("=" * 60)
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
