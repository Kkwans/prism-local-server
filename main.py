# -*- coding: utf-8 -*-
"""
Prism Local Server - 主程序入口
棱镜本地服务器 - 快速部署HTML静态文件到本地HTTP服务器
作者: Kkwans
创建时间: 2026-03-15
版本: 0.1.0
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from ui.main_window import MainWindow
from utils.logger import Logger


def main():
    """
    主函数 - 启动GUI应用程序
    """
    try:
        # 初始化日志系统
        Logger.initialize()
        Logger.info("=" * 60)
        Logger.info("Prism Local Server 启动")
        Logger.info("版本: 0.1.0")
        Logger.info("=" * 60)
        
        # 创建并运行主窗口
        app = MainWindow()
        app.protocol("WM_DELETE_WINDOW", app.on_closing)
        app.mainloop()
        
    except Exception as e:
        Logger.exception(f"应用程序启动失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
