"""
文件处理模块
提供文件读写功能
"""

import os
import tkinter as tk
from tkinter import filedialog
from typing import Optional

from utils.logger import get_logger
from utils.validators import sanitize_filename, validate_file_path


class FileHandler:
    """文件处理器"""

    def __init__(self, parent_window: Optional[tk.Tk] = None):
        """
        初始化文件处理器

        Args:
            parent_window: 父窗口（用于文件对话框）
        """
        self.parent_window = parent_window
        self.logger = get_logger()

    def save_code_dialog(
        self,
        code: str,
        default_name: str = "generated_code",
        file_types: Optional[list[tuple[str, str]]] = None
    ) -> tuple[bool, str]:
        """
        打开保存文件对话框并保存代码

        Args:
            code: 要保存的代码
            default_name: 默认文件名
            file_types: 文件类型列表

        Returns:
            (是否成功, 文件路径或错误消息)
        """
        if not code:
            return False, "没有可保存的代码"

        # 默认文件类型
        if file_types is None:
            file_types = [
                ("Python Files", "*.py"),
                ("All Files", "*.*"),
            ]

        try:
            # 打开保存对话框
            file_path = filedialog.asksaveasfilename(
                title="保存代码",
                defaultextension=".py",
                initialfile=sanitize_filename(default_name),
                filetypes=file_types,
                parent=self.parent_window
            )

            # 用户取消
            if not file_path:
                return False, ""

            # 保存文件
            return self.save_code(file_path, code)

        except Exception as e:
            error_msg = f"保存文件失败: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return False, error_msg

    def save_code(self, file_path: str, code: str) -> tuple[bool, str]:
        """
        保存代码到文件

        Args:
            file_path: 文件路径
            code: 代码内容

        Returns:
            (是否成功, 文件路径或错误消息)
        """
        # 验证文件路径
        is_valid, error_msg = validate_file_path(file_path)
        if not is_valid:
            return False, error_msg

        if not code:
            return False, "没有可保存的代码"

        try:
            # 确保目录存在
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code)

            self.logger.info(f"代码已保存到: {file_path}")
            return True, file_path

        except PermissionError:
            error_msg = "权限不足，无法保存文件"
            self.logger.error(error_msg)
            return False, error_msg

        except Exception as e:
            error_msg = f"保存文件失败: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return False, error_msg

    def read_file_dialog(
        self,
        file_types: Optional[list[tuple[str, str]]] = None
    ) -> tuple[bool, str, str]:
        """
        打开文件选择对话框并读取文件

        Args:
            file_types: 文件类型列表

        Returns:
            (是否成功, 文件内容, 文件路径)
        """
        # 默认文件类型
        if file_types is None:
            file_types = [
                ("Python Files", "*.py"),
                ("Text Files", "*.txt"),
                ("All Files", "*.*"),
            ]

        try:
            # 打开文件对话框
            file_path = filedialog.askopenfilename(
                title="打开文件",
                filetypes=file_types,
                parent=self.parent_window
            )

            # 用户取消
            if not file_path:
                return False, "", ""

            # 读取文件
            return self.read_file(file_path)

        except Exception as e:
            error_msg = f"读取文件失败: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return False, "", error_msg

    def read_file(self, file_path: str) -> tuple[bool, str, str]:
        """
        读取文件内容

        Args:
            file_path: 文件路径

        Returns:
            (是否成功, 文件内容, 文件路径或错误消息)
        """
        # 验证文件路径
        is_valid, error_msg = validate_file_path(file_path)
        if not is_valid:
            return False, "", error_msg

        if not os.path.exists(file_path):
            return False, "", "文件不存在"

        try:
            # 读取文件
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            self.logger.info(f"文件已读取: {file_path}")
            return True, content, file_path

        except PermissionError:
            error_msg = "权限不足，无法读取文件"
            self.logger.error(error_msg)
            return False, "", error_msg

        except Exception as e:
            error_msg = f"读取文件失败: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return False, "", error_msg
