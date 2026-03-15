# -*- coding: utf-8 -*-
"""
资源加载测试脚本
测试CSS/JS/图片是否能正常加载
"""

import os
import sys
import time
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.http_server_manager import HTTPServerManager
from utils.logger import Logger

def test_resource_loading():
    """测试资源加载"""
    print("=" * 60)
    print("  资源加载测试")
    print("=" * 60)
    print()
    
    # 初始化
    Logger.initialize()
    manager = HTTPServerManager()
    
    # 启动服务
    test_dir = os.path.join(os.getcwd(), 'test_resources')
    print(f"测试目录: {test_dir}")
    
    try:
        service = manager.startService(
            directory=test_dir,
            port=9000,
            entry_html='index.html',
            auto_open_browser=False
        )
        
        print(f"\n服务已启动，等待2秒...")
        time.sleep(2)
        
        # 测试HTML
        print("\n测试1: 加载HTML文件")
        response = requests.get(f'http://localhost:{service.port}/index.html')
        print(f"  状态码: {response.status_code}")
        print(f"  内容长度: {len(response.text)} 字节")
        if response.status_code == 200:
            print("  ✓ HTML加载成功")
        else:
            print("  ✗ HTML加载失败")
        
        # 测试CSS
        print("\n测试2: 加载CSS文件")
        response = requests.get(f'http://localhost:{service.port}/css/style.css')
        print(f"  状态码: {response.status_code}")
        print(f"  内容长度: {len(response.text)} 字节")
        if response.status_code == 200 and 'color: blue' in response.text:
            print("  ✓ CSS加载成功")
        else:
            print("  ✗ CSS加载失败")
        
        # 测试JS
        print("\n测试3: 加载JS文件")
        response = requests.get(f'http://localhost:{service.port}/js/script.js')
        print(f"  状态码: {response.status_code}")
        print(f"  内容长度: {len(response.text)} 字节")
        if response.status_code == 200 and 'JavaScript' in response.text:
            print("  ✓ JS加载成功")
        else:
            print("  ✗ JS加载失败")
        
        # 测试图片
        print("\n测试4: 加载图片文件")
        response = requests.get(f'http://localhost:{service.port}/images/test.png')
        print(f"  状态码: {response.status_code}")
        print(f"  内容长度: {len(response.content)} 字节")
        if response.status_code == 200:
            print("  ✓ 图片加载成功")
        else:
            print("  ✗ 图片加载失败")
        
        # 测试根路径
        print("\n测试5: 访问根路径 /")
        response = requests.get(f'http://localhost:{service.port}/')
        print(f"  状态码: {response.status_code}")
        print(f"  内容长度: {len(response.text)} 字节")
        if response.status_code == 200 and '<title>' in response.text:
            print("  ✓ 根路径自动加载HTML成功")
        else:
            print("  ✗ 根路径加载失败")
        
        print("\n" + "=" * 60)
        print("  ✓ 所有资源加载测试完成")
        print("=" * 60)
        print(f"\n请在浏览器中访问: http://localhost:{service.port}/")
        print("按Enter键停止服务...")
        input()
        
        # 停止服务
        manager.stopService(service.id)
        print("服务已停止")
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_resource_loading()
