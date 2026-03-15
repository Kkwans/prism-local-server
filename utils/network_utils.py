# -*- coding: utf-8 -*-
"""
网络工具模块
提供网络相关的辅助功能
作者: Kkwans
创建时间: 2026-03-15
"""

import socket
from typing import List, Optional


class NetworkUtils:
    """
    网络工具类
    功能:
    - 获取本机IP地址
    - 检测多网卡IP地址
    - 生成局域网访问URL
    """
    
    @staticmethod
    def getLocalIP() -> Optional[str]:
        """
        获取本机内网IP地址
        
        返回:
            IP地址字符串，失败返回None
        
        实现原理:
            通过连接外部地址获取本机使用的网卡IP
            不会真正发送数据，只是建立socket连接
        """
        try:
            # 创建UDP socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            # 连接到外部地址（不会真正发送数据）
            # 使用Google DNS服务器地址
            s.connect(('8.8.8.8', 80))
            
            # 获取socket绑定的本地IP
            local_ip = s.getsockname()[0]
            s.close()
            
            return local_ip
        
        except Exception as e:
            print(f"获取本机IP失败: {e}")
            return None
    
    @staticmethod
    def getAllLocalIPs() -> List[str]:
        """
        获取所有网卡的IP地址
        
        返回:
            IP地址列表
        """
        ip_list = []
        
        try:
            # 获取主机名
            hostname = socket.gethostname()
            
            # 获取所有IP地址
            addr_info = socket.getaddrinfo(hostname, None)
            
            for info in addr_info:
                # 只获取IPv4地址
                if info[0] == socket.AF_INET:
                    ip = info[4][0]
                    # 排除回环地址
                    if ip != '127.0.0.1' and not ip.startswith('127.'):
                        if ip not in ip_list:
                            ip_list.append(ip)
        
        except Exception as e:
            print(f"获取所有IP地址失败: {e}")
        
        return ip_list
    
    @staticmethod
    def generateLocalURL(port: int, path: str = "") -> str:
        """
        生成本地访问URL
        
        参数:
            port: 端口号
            path: 路径（可选）
        
        返回:
            本地访问URL
        """
        if path and not path.startswith('/'):
            path = '/' + path
        return f"http://localhost:{port}{path}"
    
    @staticmethod
    def generateLANURL(port: int, path: str = "") -> Optional[str]:
        """
        生成局域网访问URL
        
        参数:
            port: 端口号
            path: 路径（可选）
        
        返回:
            局域网访问URL，失败返回None
        """
        local_ip = NetworkUtils.getLocalIP()
        if not local_ip:
            return None
        
        if path and not path.startswith('/'):
            path = '/' + path
        return f"http://{local_ip}:{port}{path}"
    
    @staticmethod
    def generateAllLANURLs(port: int, path: str = "") -> List[str]:
        """
        生成所有网卡的局域网访问URL
        
        参数:
            port: 端口号
            path: 路径（可选）
        
        返回:
            URL列表
        """
        urls = []
        ip_list = NetworkUtils.getAllLocalIPs()
        
        if path and not path.startswith('/'):
            path = '/' + path
        
        for ip in ip_list:
            urls.append(f"http://{ip}:{port}{path}")
        
        return urls
    
    @staticmethod
    def isValidIP(ip: str) -> bool:
        """
        验证IP地址格式是否有效
        
        参数:
            ip: IP地址字符串
        
        返回:
            是否有效
        """
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False


# 测试代码
if __name__ == "__main__":
    print("=== 网络工具测试 ===\n")
    
    # 测试1: 获取本机IP
    print("测试1: 获取本机IP")
    local_ip = NetworkUtils.getLocalIP()
    print(f"本机IP: {local_ip}\n")
    
    # 测试2: 获取所有IP
    print("测试2: 获取所有网卡IP")
    all_ips = NetworkUtils.getAllLocalIPs()
    print(f"所有IP: {all_ips}\n")
    
    # 测试3: 生成URL
    print("测试3: 生成访问URL")
    port = 8888
    path = "index.html"
    
    local_url = NetworkUtils.generateLocalURL(port, path)
    print(f"本地URL: {local_url}")
    
    lan_url = NetworkUtils.generateLANURL(port, path)
    print(f"局域网URL: {lan_url}")
    
    all_lan_urls = NetworkUtils.generateAllLANURLs(port, path)
    print(f"所有局域网URL:")
    for url in all_lan_urls:
        print(f"  - {url}")
    
    # 测试4: IP验证
    print("\n测试4: IP地址验证")
    test_ips = ["192.168.1.1", "256.1.1.1", "invalid", "127.0.0.1"]
    for ip in test_ips:
        valid = NetworkUtils.isValidIP(ip)
        print(f"{ip}: {'有效' if valid else '无效'}")
