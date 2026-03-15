# -*- coding: utf-8 -*-
"""
配置管理模块
负责配置文件的读取、保存和验证
作者: Kkwans
创建时间: 2026-03-15
"""

import json
import os
from typing import Dict, Any
from pathlib import Path


# 默认配置常量
DEFAULT_PORT = 9000  # 默认端口号（避免8888端口权限问题）
DEFAULT_DIRECTORY = ""  # 默认部署目录（空表示EXE所在目录）
DEFAULT_HTML = "index.html"  # 默认入口HTML文件
DEFAULT_THEME = "system"  # 默认主题（system/light/dark）
DEFAULT_AUTO_OPEN_BROWSER = True  # 是否自动打开浏览器
DEFAULT_LOG_LEVEL = "INFO"  # 日志级别

# 端口范围限制
MIN_PORT = 1024  # 最小端口号（避免系统保留端口）
MAX_PORT = 65535  # 最大端口号


class ConfigManager:
    """
    配置管理器类
    功能：
    - 加载配置文件
    - 保存配置文件
    - 验证配置有效性
    - 提供默认配置
    """
    
    def __init__(self, config_dir: str = "config"):
        """
        初始化配置管理器
        
        参数:
            config_dir: 配置文件目录路径
        """
        self.config_dir = Path(config_dir)
        self.config_file = self.config_dir / "settings.json"
        self._config: Dict[str, Any] = {}
        
        # 确保配置目录存在
        self._ensureConfigDirExists()
    
    def _ensureConfigDirExists(self) -> None:
        """
        确保配置目录存在，不存在则创建
        
        异常:
            OSError: 目录创建失败
        """
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"创建配置目录失败: {e}")
            raise
    
    def getDefaultConfig(self) -> Dict[str, Any]:
        """
        获取默认配置
        
        返回:
            默认配置字典
        """
        return {
            "default_port": DEFAULT_PORT,
            "default_directory": DEFAULT_DIRECTORY,
            "default_html": DEFAULT_HTML,
            "theme": DEFAULT_THEME,
            "auto_open_browser": DEFAULT_AUTO_OPEN_BROWSER,
            "log_level": DEFAULT_LOG_LEVEL
        }

    
    def loadConfig(self) -> Dict[str, Any]:
        """
        加载配置文件
        
        返回:
            配置字典
        
        异常处理:
            - 文件不存在: 创建默认配置文件
            - JSON格式错误: 使用默认配置并记录警告
        """
        # 如果配置文件不存在，创建默认配置
        if not self.config_file.exists():
            print(f"配置文件不存在，创建默认配置: {self.config_file}")
            default_config = self.getDefaultConfig()
            self.saveConfig(default_config)
            self._config = default_config
            return self._config
        
        # 读取配置文件
        try:
            with open(self.config_file, 'r', encoding='utf-8-sig') as f:
                self._config = json.load(f)
            
            # 验证配置有效性
            if not self._validateConfig(self._config):
                print("配置文件格式错误，使用默认配置")
                self._config = self.getDefaultConfig()
            
            return self._config
        
        except json.JSONDecodeError as e:
            print(f"配置文件JSON格式错误: {e}，使用默认配置")
            self._config = self.getDefaultConfig()
            return self._config
        
        except Exception as e:
            print(f"读取配置文件失败: {e}，使用默认配置")
            self._config = self.getDefaultConfig()
            return self._config
    
    def saveConfig(self, config: Dict[str, Any]) -> bool:
        """
        保存配置到文件
        
        参数:
            config: 配置字典
        
        返回:
            是否保存成功
        
        编码: UTF-8 with BOM
        """
        try:
            # 验证配置有效性
            if not self._validateConfig(config):
                print("配置验证失败，无法保存")
                return False
            
            # 写入配置文件（UTF-8 with BOM）
            with open(self.config_file, 'w', encoding='utf-8-sig') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
            
            self._config = config
            print(f"配置已保存: {self.config_file}")
            return True
        
        except Exception as e:
            print(f"保存配置文件失败: {e}")
            return False
    
    def _validateConfig(self, config: Dict[str, Any]) -> bool:
        """
        验证配置有效性
        
        参数:
            config: 配置字典
        
        返回:
            配置是否有效
        """
        # 检查必需字段
        required_fields = ["default_port", "default_directory", "default_html"]
        for field in required_fields:
            if field not in config:
                print(f"配置缺少必需字段: {field}")
                return False
        
        # 验证端口范围
        port = config.get("default_port")
        if not isinstance(port, int) or port < MIN_PORT or port > MAX_PORT:
            print(f"端口号无效: {port}，必须在{MIN_PORT}-{MAX_PORT}范围内")
            return False
        
        # 验证目录路径（如果不为空）
        directory = config.get("default_directory")
        if directory and not isinstance(directory, str):
            print(f"目录路径格式错误: {directory}")
            return False
        
        # 验证HTML文件名
        html_file = config.get("default_html")
        if not isinstance(html_file, str) or not html_file:
            print(f"HTML文件名无效: {html_file}")
            return False
        
        return True
    
    def getConfig(self, key: str, default: Any = None) -> Any:
        """
        获取配置项
        
        参数:
            key: 配置键
            default: 默认值
        
        返回:
            配置值
        """
        return self._config.get(key, default)
    
    def setConfig(self, key: str, value: Any) -> bool:
        """
        设置配置项
        
        参数:
            key: 配置键
            value: 配置值
        
        返回:
            是否设置成功
        """
        self._config[key] = value
        return self.saveConfig(self._config)
    
    def getAllConfig(self) -> Dict[str, Any]:
        """
        获取所有配置
        
        返回:
            配置字典
        """
        return self._config.copy()


# 测试代码
if __name__ == "__main__":
    # 创建配置管理器实例
    config_manager = ConfigManager()
    
    # 加载配置
    config = config_manager.loadConfig()
    print("当前配置:", config)
    
    # 修改配置
    config_manager.setConfig("default_port", 9000)
    print("修改后配置:", config_manager.getAllConfig())
