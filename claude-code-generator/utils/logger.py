"""
日志记录模块
提供应用日志功能
"""

import logging
import os
from datetime import datetime
from typing import Optional

from config.constants import LOGS_DIR


class Logger:
    """应用日志记录器"""

    _instance = None
    _logger = None

    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化日志记录器"""
        if self._logger is None:
            self._setup_logger()

    def _setup_logger(self):
        """设置日志记录器"""
        # 创建日志目录
        os.makedirs(LOGS_DIR, exist_ok=True)

        # 创建日志记录器
        self._logger = logging.getLogger("ClaudeCodeGenerator")
        self._logger.setLevel(logging.DEBUG)

        # 防止重复添加处理器
        if self._logger.handlers:
            return

        # 创建文件处理器（按日期）
        log_file = os.path.join(
            LOGS_DIR,
            f"app_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # 创建格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 添加处理器
        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)

    def debug(self, message: str):
        """记录调试信息"""
        self._logger.debug(message)

    def info(self, message: str):
        """记录一般信息"""
        self._logger.info(message)

    def warning(self, message: str):
        """记录警告信息"""
        self._logger.warning(message)

    def error(self, message: str, exc_info: bool = False):
        """
        记录错误信息

        Args:
            message: 错误消息
            exc_info: 是否包含异常信息
        """
        self._logger.error(message, exc_info=exc_info)

    def critical(self, message: str, exc_info: bool = False):
        """
        记录严重错误信息

        Args:
            message: 错误消息
            exc_info: 是否包含异常信息
        """
        self._logger.critical(message, exc_info=exc_info)


# 全局日志实例
def get_logger() -> Logger:
    """
    获取全局日志记录器实例

    Returns:
        Logger 实例
    """
    return Logger()
