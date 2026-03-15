# -*- coding: utf-8 -*-
"""
调试测试脚本
"""

import os
import sys
import time
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.http_server_manager import HTTPServerManager
from utils.logger import Logger

def test_debug():
    """调试测试"""
    Logger.initialize()
    manager = HTTPServerManager()
    
    test_dir = os.path.join(os.getcwd(), 'test_resources')
    print(f"测试目录: {test_dir}")
    print(f"目录存在: {os.path.exists(test_dir)}")
    print(f"目录内容: {os.listdir(test_dir)}")
    
    service = manager.startService(
        directory=test_dir,
        port=8888,
        entry_html='index.html',
        auto_open_browser=False
    )
    
    time.sleep(2)
    
    # 测试HTML
    print("\n测试HTML:")
    response = requests.get(f'http://localhost:{service.port}/index.html')
    print(f"状态码: {response.status_code}")
    print(f"响应内容:\n{response.text[:500]}")
    
    input("\n按Enter停止...")
    manager.stopService(service.id)

if __name__ == "__main__":
    test_debug()
