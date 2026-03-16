# -*- coding: utf-8 -*-
"""
端口管理模块
负责端口可用性检测和自动分配
作者: Kkwans
创建时间: 2026-03-15
"""

import socket
from typing import Optional


# 端口范围常量
MIN_PORT = 1024  # 最小端口号（避免系统保留端口）
MAX_PORT = 65535  # 最大端口号
MAX_RETRY = 100  # 最大重试次数


class PortInUseError(Exception):
    """端口被占用异常"""
    pass


class NoAvailablePortError(Exception):
    """无可用端口异常"""
    pass


class PortManager:
    """
    端口管理器类
    功能:
    - 检查端口是否可用
    - 自动查找可用端口
    - 端口范围验证
    """
    
    @staticmethod
    def isPortAvailable(port: int) -> bool:
        """
        检查端口是否可用
        
        参数:
            port: 端口号
        
        返回:
            True表示可用，False表示被占用
        
        实现原理:
            尝试在指定端口上创建socket并绑定
            如果成功则端口可用，失败则被占用
        """
        # 验证端口范围
        if port < MIN_PORT or port > MAX_PORT:
            print(f"端口号超出有效范围: {port}，有效范围: {MIN_PORT}-{MAX_PORT}")
            return False
        
        try:
            # 创建TCP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 不使用SO_REUSEADDR，确保准确检测端口占用
            
            # 尝试绑定端口
            sock.bind(('0.0.0.0', port))
            sock.close()
            
            return True
        
        except OSError:
            # 端口被占用
            return False
        
        except Exception as e:
            print(f"检查端口可用性时发生异常: {e}")
            return False

    
    @staticmethod
    def findAvailablePort(start_port: int = 8888) -> int:
        """
        从指定端口开始查找可用端口
        
        参数:
            start_port: 起始端口号（默认8888）
        
        返回:
            可用端口号
        
        异常:
            NoAvailablePortError: 无可用端口
        
        策略:
            从start_port开始，逐个递增检查端口可用性
            最多尝试MAX_RETRY次
        """
        # 验证起始端口范围
        if start_port < MIN_PORT:
            start_port = MIN_PORT
            print(f"起始端口小于最小值，调整为: {MIN_PORT}")
        
        if start_port > MAX_PORT:
            raise NoAvailablePortError(f"起始端口{start_port}超出最大值{MAX_PORT}")
        
        # 逐个检查端口
        current_port = start_port
        retry_count = 0
        
        while retry_count < MAX_RETRY:
            # 检查当前端口是否可用
            if PortManager.isPortAvailable(current_port):
                print(f"找到可用端口: {current_port}")
                return current_port
            
            # 端口被占用，记录日志
            print(f"端口{current_port}被占用，尝试下一个端口")
            
            # 递增端口号
            current_port += 1
            retry_count += 1
            
            # 检查是否超出最大端口
            if current_port > MAX_PORT:
                raise NoAvailablePortError(
                    f"端口范围{start_port}-{MAX_PORT}内无可用端口"
                )
        
        # 达到最大重试次数
        raise NoAvailablePortError(
            f"尝试{MAX_RETRY}次后仍未找到可用端口（起始端口: {start_port}）"
        )
    
    @staticmethod
    def validatePortRange(port: int) -> bool:
        """
        验证端口是否在有效范围内
        
        参数:
            port: 端口号
        
        返回:
            是否在有效范围内
        """
        return MIN_PORT <= port <= MAX_PORT
    
    @staticmethod
    def getPortInfo(port: int) -> dict:
        """
        获取端口信息
        
        参数:
            port: 端口号
        
        返回:
            端口信息字典
        """
        return {
            "port": port,
            "available": PortManager.isPortAvailable(port),
            "valid_range": PortManager.validatePortRange(port),
            "min_port": MIN_PORT,
            "max_port": MAX_PORT
        }


# 测试代码
if __name__ == "__main__":
    print("=== 端口管理器测试 ===\n")
    
    # 测试1: 检查端口可用性
    test_port = 8888
    print(f"测试1: 检查端口{test_port}是否可用")
    is_available = PortManager.isPortAvailable(test_port)
    print(f"结果: {'可用' if is_available else '被占用'}\n")
    
    # 测试2: 查找可用端口
    print(f"测试2: 从端口{test_port}开始查找可用端口")
    try:
        available_port = PortManager.findAvailablePort(test_port)
        print(f"结果: 找到可用端口 {available_port}\n")
    except NoAvailablePortError as e:
        print(f"错误: {e}\n")
    
    # 测试3: 验证端口范围
    print("测试3: 验证端口范围")
    test_ports = [80, 1024, 8888, 65535, 70000]
    for p in test_ports:
        valid = PortManager.validatePortRange(p)
        print(f"端口{p}: {'有效' if valid else '无效'}")
    
    print("\n测试4: 获取端口信息")
    info = PortManager.getPortInfo(8888)
    print(f"端口信息: {info}")
