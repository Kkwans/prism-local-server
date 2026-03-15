# -*- coding: utf-8 -*-
"""
测试自定义ResourceHandler
"""

import os
from http.server import ThreadingHTTPServer
from core.resource_handler import ResourceHandler

# 测试目录
test_dir = os.path.join(os.getcwd(), 'test_resources')
print(f"部署目录: {test_dir}")
print(f"目录内容: {os.listdir(test_dir)}")

# 设置ResourceHandler的部署目录
ResourceHandler.deployment_directory = test_dir

# 创建服务器
server_address = ('', 9000)
httpd = ThreadingHTTPServer(server_address, ResourceHandler)

print(f"\n服务器启动在端口 9000")
print(f"访问: http://localhost:9000/index.html")
print("按Ctrl+C停止\n")

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\n服务器已停止")
