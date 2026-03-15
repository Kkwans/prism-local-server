# -*- coding: utf-8 -*-
"""
基础服务器测试 - 使用原生SimpleHTTPRequestHandler
"""

import os
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial

# 测试目录
test_dir = os.path.join(os.getcwd(), 'test_resources')
print(f"部署目录: {test_dir}")
print(f"目录内容: {os.listdir(test_dir)}")

# 创建处理器类,绑定目录
handler = partial(SimpleHTTPRequestHandler, directory=test_dir)

# 创建服务器
server_address = ('', 8888)
httpd = ThreadingHTTPServer(server_address, handler)

print(f"\n服务器启动在端口 8888")
print(f"访问: http://localhost:8888/index.html")
print("按Ctrl+C停止\n")

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\n服务器已停止")
