# -*- coding: utf-8 -*-
"""
资源处理器模块
自定义HTTP请求处理器，优化资源加载性能
作者: Kkwans
创建时间: 2026-03-15
"""

import os
import socket
import urllib.parse
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from typing import Optional


# 文件读取缓冲区大小（8KB）
BUFFER_SIZE = 8192

# Content-Type映射表
CONTENT_TYPE_MAP = {
    '.html': 'text/html; charset=utf-8',
    '.htm': 'text/html; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.js': 'application/javascript; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.xml': 'application/xml; charset=utf-8',
    '.txt': 'text/plain; charset=utf-8',
    # 图片格式
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.bmp': 'image/bmp',
    '.ico': 'image/x-icon',
    '.svg': 'image/svg+xml',
    '.webp': 'image/webp',
    # 视频格式
    '.mp4': 'video/mp4',
    '.MP4': 'video/mp4',
    '.webm': 'video/webm',
    '.ogg': 'video/ogg',
    '.avi': 'video/x-msvideo',
    '.mov': 'video/quicktime',
    '.MOV': 'video/quicktime',
    '.wmv': 'video/x-ms-wmv',
    '.flv': 'video/x-flv',
    # 音频格式
    '.mp3': 'audio/mpeg',
    '.wav': 'audio/wav',
    '.ogg': 'audio/ogg',
    '.m4a': 'audio/mp4',
    # 其他格式
    '.pdf': 'application/pdf',
    '.zip': 'application/zip',
    '.rar': 'application/x-rar-compressed',
}


class ResourceHandler(SimpleHTTPRequestHandler):
    """
    自定义HTTP资源处理器
    功能:
    - 适配HTML相对路径资源
    - 支持HTTP Range请求（视频拖动播放）
    - 优化Content-Type设置
    - 启用TCP_NODELAY优化
    - 文件缓冲读取
    """
    
    # 部署目录（由HTTPServerManager设置）
    deployment_directory = None
    
    def setup(self):
        """
        设置连接参数
        启用TCP_NODELAY优化，减少网络延迟
        """
        SimpleHTTPRequestHandler.setup(self)
        try:
            # 启用TCP_NODELAY，禁用Nagle算法
            self.request.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        except Exception as e:
            print(f"设置TCP_NODELAY失败: {e}")

    
    def translate_path(self, path: str) -> str:
        """
        将HTTP请求路径转换为本地文件系统路径
        
        参数:
            path: HTTP请求路径
        
        返回:
            本地文件系统路径
        
        关键点:
        - 禁用路径重定向
        - 保持相对路径一致性
        - 支持中文和特殊字符
        - 防止目录遍历攻击
        """
        # URL解码
        path = urllib.parse.unquote(path)
        
        # 移除查询参数
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        
        # 规范化路径，移除开头的斜杠
        path = path.lstrip('/')
        
        # 使用部署目录作为根目录
        if self.deployment_directory:
            base_dir = Path(self.deployment_directory).resolve()
        else:
            base_dir = Path.cwd()
        
        # 拼接完整路径
        full_path = base_dir / path
        
        # 安全检查：确保路径在部署目录内（防止目录遍历攻击）
        try:
            full_path = full_path.resolve()
            if not str(full_path).startswith(str(base_dir)):
                print(f"安全警告：尝试访问部署目录外的文件: {path}")
                return str(base_dir)
        except Exception as e:
            print(f"路径解析失败: {e}")
            return str(base_dir)
        
        return str(full_path)
    
    def guess_type(self, path: str) -> str:
        """
        根据文件扩展名猜测Content-Type
        
        参数:
            path: 文件路径
        
        返回:
            Content-Type字符串
        """
        # 获取文件扩展名
        ext = os.path.splitext(path)[1].lower()
        
        # 从映射表中查找
        content_type = CONTENT_TYPE_MAP.get(ext)
        
        if content_type:
            return content_type
        
        # 使用父类的默认方法
        return SimpleHTTPRequestHandler.guess_type(self, path)
    
    def do_GET(self):
        """
        处理GET请求
        支持HTTP Range请求（视频拖动播放）
        """
        # 获取文件路径
        file_path = self.translate_path(self.path)
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            self.send_error(404, "File not found")
            return
        
        # 如果是目录，尝试查找index.html
        if os.path.isdir(file_path):
            index_path = os.path.join(file_path, 'index.html')
            if os.path.exists(index_path):
                file_path = index_path
            else:
                # 返回目录列表
                SimpleHTTPRequestHandler.do_GET(self)
                return
        
        # 获取文件大小
        try:
            file_size = os.path.getsize(file_path)
        except OSError:
            self.send_error(404, "File not found")
            return
        
        # 检查是否有Range请求头
        range_header = self.headers.get('Range')
        
        if range_header:
            # 处理Range请求
            self._handleRangeRequest(file_path, file_size, range_header)
        else:
            # 处理普通请求
            self._handleNormalRequest(file_path, file_size)

    
    def _handleNormalRequest(self, file_path: str, file_size: int):
        """
        处理普通GET请求（无Range）
        
        参数:
            file_path: 文件路径
            file_size: 文件大小
        """
        try:
            # 打开文件
            with open(file_path, 'rb') as f:
                # 发送响应头
                self.send_response(200)
                self.send_header('Content-Type', self.guess_type(file_path))
                self.send_header('Content-Length', str(file_size))
                self.send_header('Accept-Ranges', 'bytes')
                self.end_headers()
                
                # 分块读取并发送文件内容
                while True:
                    chunk = f.read(BUFFER_SIZE)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
        
        except Exception as e:
            print(f"发送文件失败: {e}")
            self.send_error(500, "Internal server error")
    
    def _handleRangeRequest(self, file_path: str, file_size: int, range_header: str):
        """
        处理Range请求（支持视频拖动播放）
        
        参数:
            file_path: 文件路径
            file_size: 文件大小
            range_header: Range请求头内容
        """
        try:
            # 解析Range头（格式: bytes=start-end）
            range_match = range_header.replace('bytes=', '').split('-')
            start = int(range_match[0]) if range_match[0] else 0
            end = int(range_match[1]) if range_match[1] else file_size - 1
            
            # 验证范围
            if start >= file_size or end >= file_size or start > end:
                self.send_error(416, "Requested Range Not Satisfiable")
                return
            
            # 计算内容长度
            content_length = end - start + 1
            
            # 打开文件并定位到起始位置
            with open(file_path, 'rb') as f:
                f.seek(start)
                
                # 发送206 Partial Content响应
                self.send_response(206)
                self.send_header('Content-Type', self.guess_type(file_path))
                self.send_header('Content-Length', str(content_length))
                self.send_header('Content-Range', f'bytes {start}-{end}/{file_size}')
                self.send_header('Accept-Ranges', 'bytes')
                self.end_headers()
                
                # 分块读取并发送指定范围的内容
                remaining = content_length
                while remaining > 0:
                    chunk_size = min(BUFFER_SIZE, remaining)
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    remaining -= len(chunk)
        
        except Exception as e:
            print(f"处理Range请求失败: {e}")
            self.send_error(500, "Internal server error")
    
    def log_message(self, format, *args):
        """
        重写日志方法，自定义日志格式
        
        参数:
            format: 日志格式
            args: 日志参数
        """
        # 可以在这里集成到统一的日志系统
        # 暂时使用简单的打印
        print(f"[HTTP] {self.address_string()} - {format % args}")


# 测试代码
if __name__ == "__main__":
    from http.server import ThreadingHTTPServer
    
    print("=== 资源处理器测试 ===\n")
    
    # 设置部署目录为当前目录
    ResourceHandler.deployment_directory = os.getcwd()
    
    # 创建测试服务器
    port = 8888
    server_address = ('', port)
    
    try:
        httpd = ThreadingHTTPServer(server_address, ResourceHandler)
        print(f"测试服务器启动成功")
        print(f"访问地址: http://localhost:{port}")
        print(f"部署目录: {ResourceHandler.deployment_directory}")
        print("\n按Ctrl+C停止服务器\n")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"启动服务器失败: {e}")
