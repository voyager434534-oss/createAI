"""
Claude Code Generator
一个基于 Claude API 的 AI 代码生成器

主入口文件
"""

import sys

import customtkinter as ctk

import config.constants as constants
from ui.main_window import MainWindow
from ui.styles import Styles
from utils.logger import get_logger


def main():
    """应用主函数"""
    # 初始化日志
    logger = get_logger()
    logger.info("=" * 50)
    logger.info(f"启动 {constants.APP_NAME} v{constants.APP_VERSION}")
    logger.info("=" * 50)

    try:
        # 配置外观
        Styles.configure_appearance("System")

        # 创建应用
        app = MainWindow()

        # 设置关闭事件
        app.protocol("WM_DELETE_WINDOW", app.on_closing)

        # 运行应用
        logger.info("应用已成功启动")
        app.mainloop()

        logger.info("应用已正常关闭")
        return 0

    except KeyboardInterrupt:
        logger.info("应用被用户中断")
        return 0

    except Exception as e:
        logger.critical(f"应用崩溃: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
