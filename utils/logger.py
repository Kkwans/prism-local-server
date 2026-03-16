# -*- coding: utf-8 -*-
"""
日志工具模块
提供异步日志记录功能
作者: Kkwans
创建时间: 2026-03-15
"""

import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime


# 日志目录（使用用户目录）
USER_HOME = Path.home()
CONFIG_DIR_NAME = ".prism-server"
LOG_DIR = USER_HOME / CONFIG_DIR_NAME / "logs"
LOG_FILE = "prism-server.log"

# 日志格式
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# 日志级别
LOG_LEVEL = logging.INFO

# 日志文件大小限制（10MB）
MAX_LOG_SIZE = 10 * 1024 * 1024

# 保留的日志文件数量
BACKUP_COUNT = 5


class Logger:
    """
    日志工具类
    功能:
    - 配置日志格式和级别
    - 异步日志输出
    - 日志文件滚动
    - 自动创建日志目录
    """
    
    _initialized = False
    _logger = None
    
    @classmethod
    def initialize(cls, log_dir: Path = LOG_DIR, log_file: str = LOG_FILE, 
                  log_level: int = LOG_LEVEL) -> logging.Logger:
        """
        初始化日志系统
        
        参数:
            log_dir: 日志目录（Path对象）
            log_file: 日志文件名
            log_level: 日志级别
        
        返回:
            Logger对象
        """
        if cls._initialized:
            return cls._logger
        
        # 创建日志目录
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
        
        # 完整日志文件路径
        log_file_path = log_path / log_file
        
        # 创建logger
        logger = logging.getLogger("PrismServer")
        logger.setLevel(log_level)
        
        # 避免重复添加handler
        if logger.handlers:
            logger.handlers.clear()
        
        # 创建文件handler（带滚动）
        file_handler = RotatingFileHandler(
            log_file_path,
            maxBytes=MAX_LOG_SIZE,
            backupCount=BACKUP_COUNT,
            encoding='utf-8'
        )
        file_handler.setLevel(log_level)
        
        # 创建控制台handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        
        # 设置格式
        formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加handler
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        cls._logger = logger
        cls._initialized = True
        
        logger.info("=" * 60)
        logger.info("日志系统初始化完成")
        logger.info(f"日志文件: {log_file_path}")
        logger.info(f"日志级别: {logging.getLevelName(log_level)}")
        logger.info("=" * 60)
        
        return logger
    
    @classmethod
    def getLogger(cls) -> logging.Logger:
        """
        获取Logger对象
        
        返回:
            Logger对象
        """
        if not cls._initialized:
            return cls.initialize()
        return cls._logger
    
    @classmethod
    def debug(cls, message: str):
        """记录DEBUG级别日志"""
        cls.getLogger().debug(message)
    
    @classmethod
    def info(cls, message: str):
        """记录INFO级别日志"""
        cls.getLogger().info(message)
    
    @classmethod
    def warning(cls, message: str):
        """记录WARNING级别日志"""
        cls.getLogger().warning(message)
    
    @classmethod
    def error(cls, message: str):
        """记录ERROR级别日志"""
        cls.getLogger().error(message)
    
    @classmethod
    def critical(cls, message: str):
        """记录CRITICAL级别日志"""
        cls.getLogger().critical(message)
    
    @classmethod
    def exception(cls, message: str):
        """
        记录异常信息（包含堆栈跟踪）
        
        参数:
            message: 异常描述
        """
        cls.getLogger().exception(message)


# 测试代码
if __name__ == "__main__":
    print("=== 日志工具测试 ===\n")
    
    # 初始化日志系统
    Logger.initialize()
    
    # 测试不同级别的日志
    Logger.debug("这是DEBUG级别日志")
    Logger.info("这是INFO级别日志")
    Logger.warning("这是WARNING级别日志")
    Logger.error("这是ERROR级别日志")
    Logger.critical("这是CRITICAL级别日志")
    
    # 测试异常日志
    try:
        1 / 0
    except Exception:
        Logger.exception("捕获到异常")
    
    print("\n日志已写入文件: logs/prism-server.log")
