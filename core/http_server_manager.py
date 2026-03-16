# -*- coding: utf-8 -*-
"""
HTTP服务管理器模块
负责管理多个HTTP服务实例的生命周期
作者: Kkwans
创建时间: 2026-03-15
"""

import os
import webbrowser
import threading
import time
from datetime import datetime
from http.server import ThreadingHTTPServer
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from pathlib import Path

from .port_manager import PortManager, NoAvailablePortError
from .resource_handler import ResourceHandler


@dataclass
class ServiceInstance:
    """
    服务实例数据结构
    
    属性:
        id: 服务唯一标识
        port: 监听端口
        directory: 部署目录
        entry_html: 入口HTML文件
        start_time: 启动时间
        server: HTTP服务器对象
        thread: 服务线程
        status: 运行状态 (running/stopped)
    """
    id: str
    port: int
    directory: str
    entry_html: str
    start_time: datetime
    server: Optional[ThreadingHTTPServer] = None
    thread: Optional[threading.Thread] = None
    status: str = "stopped"
    
    def getUptime(self) -> str:
        """
        获取服务运行时长
        
        返回:
            格式化的运行时长 (HH:MM:SS)
        """
        if self.status != "running":
            return "00:00:00"
        
        elapsed = datetime.now() - self.start_time
        hours, remainder = divmod(int(elapsed.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


class DirectoryNotFoundError(Exception):
    """目录不存在异常"""
    pass


class NoHTMLFileError(Exception):
    """无HTML文件异常"""
    pass



class HTTPServerManager:
    """
    HTTP服务管理器类
    功能:
    - 管理多个HTTP服务实例
    - 启动和停止服务
    - 自动检测HTML文件
    - 打开浏览器
    """
    
    def __init__(self):
        """初始化服务管理器"""
        self.services: Dict[str, ServiceInstance] = {}
        self._next_id = 1
    
    def _generateServiceId(self) -> str:
        """
        生成服务唯一ID
        
        返回:
            服务ID字符串
        """
        service_id = f"service_{self._next_id}"
        self._next_id += 1
        return service_id
    
    def _validateDirectory(self, directory: str) -> bool:
        """
        验证部署目录是否存在
        
        参数:
            directory: 目录路径
        
        返回:
            是否存在
        
        异常:
            DirectoryNotFoundError: 目录不存在
        """
        if not os.path.exists(directory):
            raise DirectoryNotFoundError(f"部署目录不存在: {directory}")
        
        if not os.path.isdir(directory):
            raise DirectoryNotFoundError(f"路径不是目录: {directory}")
        
        return True
    
    def _detectHTMLFile(self, directory: str, preferred_name: str = "index.html") -> str:
        """
        自动检测目录下的HTML文件
        
        参数:
            directory: 目录路径
            preferred_name: 优先选择的文件名
        
        返回:
            HTML文件名
        
        异常:
            NoHTMLFileError: 未找到HTML文件
        
        检测策略:
        1. 优先选择preferred_name（如index.html）
        2. 其次选择messages.html
        3. 最后选择第一个.html文件
        """
        # 优先级列表
        priority_files = [preferred_name, "index.html", "messages.html"]
        
        # 检查优先级文件
        for filename in priority_files:
            file_path = os.path.join(directory, filename)
            if os.path.exists(file_path):
                print(f"找到HTML文件: {filename}")
                return filename
        
        # 扫描目录查找任意HTML文件
        try:
            for filename in os.listdir(directory):
                if filename.lower().endswith(('.html', '.htm')):
                    print(f"找到HTML文件: {filename}")
                    return filename
        except Exception as e:
            print(f"扫描目录失败: {e}")
        
        # 未找到HTML文件
        raise NoHTMLFileError(f"目录下未找到HTML文件: {directory}")
    
    def startService(self, directory: str, port: int = 9000, 
                    entry_html: str = "index.html", 
                    auto_open_browser: bool = True) -> ServiceInstance:
        """
        启动HTTP服务
        
        参数:
            directory: 部署目录路径
            port: 监听端口（默认8888）
            entry_html: 入口HTML文件名（默认index.html）
            auto_open_browser: 是否自动打开浏览器（默认True）
        
        返回:
            ServiceInstance对象
        
        异常:
            DirectoryNotFoundError: 目录不存在
            NoHTMLFileError: 未找到HTML文件
            NoAvailablePortError: 无可用端口
        """
        print(f"\n=== 启动HTTP服务 ===")
        print(f"部署目录: {directory}")
        print(f"请求端口: {port}")
        
        # 验证目录
        self._validateDirectory(directory)
        
        # 自动检测HTML文件
        try:
            entry_html = self._detectHTMLFile(directory, entry_html)
        except NoHTMLFileError as e:
            print(f"警告: {e}")
            # 允许继续启动，但不自动打开浏览器
            auto_open_browser = False
        
        # 查找可用端口
        try:
            available_port = PortManager.findAvailablePort(port)
            if available_port != port:
                print(f"端口{port}被占用，使用端口{available_port}")
        except NoAvailablePortError as e:
            print(f"错误: {e}")
            raise
        
        # 创建服务实例
        service_id = self._generateServiceId()
        service = ServiceInstance(
            id=service_id,
            port=available_port,
            directory=directory,
            entry_html=entry_html,
            start_time=datetime.now(),
            status="starting"
        )
        
        # 创建HTTP服务器
        try:
            server_address = ('0.0.0.0', available_port)
            
            # 设置ResourceHandler的部署目录（使用类变量）
            ResourceHandler.deployment_directory = directory
            
            httpd = ThreadingHTTPServer(server_address, ResourceHandler)
            httpd.allow_reuse_address = True
            service.server = httpd
            
            # 创建服务线程
            def serve():
                print(f"服务线程启动: 端口{available_port}")
                httpd.serve_forever()
            
            thread = threading.Thread(target=serve, daemon=True)
            thread.start()
            service.thread = thread
            service.status = "running"
            
            # 保存服务实例
            self.services[service_id] = service
            
            print(f"✓ 服务启动成功")
            print(f"  服务ID: {service_id}")
            print(f"  监听端口: {available_port}")
            print(f"  本地访问: http://localhost:{available_port}/{entry_html}")
            print(f"  局域网访问: http://<内网IP>:{available_port}/{entry_html}")
            
            # 自动打开浏览器
            if auto_open_browser and entry_html:
                url = f"http://localhost:{available_port}/{entry_html}"
                print(f"  正在打开浏览器: {url}")
                try:
                    webbrowser.open(url)
                except Exception as e:
                    print(f"  打开浏览器失败: {e}")
            
            return service
        
        except Exception as e:
            print(f"✗ 启动服务失败: {e}")
            raise

    
    def stopService(self, service_id: str) -> bool:
        """
        停止HTTP服务
        
        参数:
            service_id: 服务ID
        
        返回:
            是否成功停止
        """
        if service_id not in self.services:
            print(f"服务不存在: {service_id}")
            return False
        
        service = self.services[service_id]
        
        print(f"\n=== 停止HTTP服务 ===")
        print(f"服务ID: {service_id}")
        print(f"端口: {service.port}")
        
        try:
            # 关闭HTTP服务器
            if service.server:
                service.server.shutdown()
                service.server.server_close()
                print("✓ HTTP服务器已关闭")
            
            # 等待线程结束
            if service.thread and service.thread.is_alive():
                service.thread.join(timeout=5)
                print("✓ 服务线程已停止")
            
            # 更新状态
            service.status = "stopped"
            
            # 从服务列表中移除
            del self.services[service_id]
            
            print(f"✓ 服务已停止")
            return True
        
        except Exception as e:
            print(f"✗ 停止服务失败: {e}")
            return False
    
    def getAllServices(self) -> List[ServiceInstance]:
        """
        获取所有服务实例列表
        
        返回:
            服务实例列表
        """
        return list(self.services.values())
    
    def getService(self, service_id: str) -> Optional[ServiceInstance]:
        """
        获取指定服务实例
        
        参数:
            service_id: 服务ID
        
        返回:
            服务实例或None
        """
        return self.services.get(service_id)
    
    def getServiceCount(self) -> int:
        """
        获取运行中的服务数量
        
        返回:
            服务数量
        """
        return len(self.services)
    
    def stopAllServices(self) -> int:
        """
        停止所有服务
        
        返回:
            成功停止的服务数量
        """
        print("\n=== 停止所有服务 ===")
        service_ids = list(self.services.keys())
        success_count = 0
        
        for service_id in service_ids:
            if self.stopService(service_id):
                success_count += 1
        
        print(f"✓ 已停止 {success_count}/{len(service_ids)} 个服务")
        return success_count


# 测试代码
if __name__ == "__main__":
    print("=== HTTP服务管理器测试 ===\n")
    
    # 创建服务管理器
    manager = HTTPServerManager()
    
    # 测试1: 启动服务
    try:
        print("测试1: 启动服务")
        service = manager.startService(
            directory=os.getcwd(),
            port=8888,
            entry_html="index.html",
            auto_open_browser=False
        )
        print(f"服务状态: {service.status}")
        print(f"运行时长: {service.getUptime()}")
        
        # 等待几秒
        time.sleep(3)
        print(f"3秒后运行时长: {service.getUptime()}")
        
        # 测试2: 获取所有服务
        print("\n测试2: 获取所有服务")
        services = manager.getAllServices()
        print(f"运行中的服务数量: {len(services)}")
        for svc in services:
            print(f"  - {svc.id}: 端口{svc.port}, 状态{svc.status}")
        
        # 测试3: 停止服务
        print("\n测试3: 停止服务")
        manager.stopService(service.id)
        print(f"剩余服务数量: {manager.getServiceCount()}")
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
