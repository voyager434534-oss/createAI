"""
输出面板模块
显示生成的代码
"""

import customtkinter as ctk
import pyperclip

from ui.styles import Styles
from utils.file_handler import FileHandler


class OutputPanel(ctk.CTkFrame):
    """输出面板"""

    def __init__(self, master, **kwargs):
        """
        初始化输出面板

        Args:
            master: 父容器
        """
        super().__init__(master, **kwargs)

        self.current_code = ""
        self.file_handler = None

        self._setup_ui()

    def _setup_ui(self):
        """设置用户界面"""
        # 配置网格
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        # 标题栏
        self._create_header()

        # 代码显示区域
        self._create_code_display()

        # 按钮栏
        self._create_buttons()

    def _create_header(self):
        """创建标题"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=Styles.SPACING["md"], pady=(Styles.SPACING["md"], Styles.SPACING["xs"]))

        # 标题
        label = ctk.CTkLabel(
            header_frame,
            text="生成的代码",
            font=Styles.FONTS["subheading"],
            anchor="w"
        )
        label.grid(row=0, column=0, sticky="ew")

        # 状态指示器
        self.status_label = ctk.CTkLabel(
            header_frame,
            text="",
            font=Styles.FONTS["small"],
            text_color="gray"
        )
        self.status_label.grid(row=0, column=1, sticky="e")

        header_frame.grid_columnconfigure(0, weight=1)

    def _create_code_display(self):
        """创建代码显示区域"""
        # 文本框容器
        textbox_frame = ctk.CTkFrame(self)
        textbox_frame.grid(row=1, column=0, sticky="nsew", padx=Styles.SPACING["md"], pady=Styles.SPACING["sm"])
        textbox_frame.grid_columnconfigure(0, weight=1)
        textbox_frame.grid_rowconfigure(0, weight=1)

        # 代码文本框（使用滚动文本框）
        self.code_textbox = ctk.CTkTextbox(
            textbox_frame,
            font=Styles.FONTS["code"],
            wrap="none",
        )
        self.code_textbox.grid(row=0, column=0, sticky="nsew")

        # 滚动条
        scrollbar_y = ctk.CTkScrollbar(textbox_frame, command=self.code_textbox.yview)
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.code_textbox.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = ctk.CTkScrollbar(textbox_frame, command=self.code_textbox.xview, orientation="horizontal")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        self.code_textbox.configure(xscrollcommand=scrollbar_x.set)

    def _create_buttons(self):
        """创建按钮"""
        # 按钮容器
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=2, column=0, sticky="ew", padx=Styles.SPACING["md"], pady=Styles.SPACING["md"])

        # 复制按钮
        self.copy_btn = ctk.CTkButton(
            button_frame,
            text="复制",
            font=Styles.FONTS["body"],
            height=35,
            width=100,
        )
        self.copy_btn.grid(row=0, column=0, padx=(0, Styles.SPACING["xs"]))

        # 保存按钮
        self.save_btn = ctk.CTkButton(
            button_frame,
            text="保存",
            font=Styles.FONTS["body"],
            height=35,
            width=100,
        )
        self.save_btn.grid(row=0, column=1, padx=Styles.SPACING["xs"])

        # 清除按钮
        self.clear_btn = ctk.CTkButton(
            button_frame,
            text="清除",
            font=Styles.FONTS["body"],
            height=35,
            width=100,
            fg_color="transparent",
            border_width=2,
        )
        self.clear_btn.grid(row=0, column=2, padx=Styles.SPACING["xs"])

    def set_code(self, code: str, append: bool = False):
        """
        设置代码内容

        Args:
            code: 代码内容
            append: 是否追加
        """
        if append and self.current_code:
            self.code_textbox.insert("end", code)
            self.current_code += code
        else:
            self.code_textbox.delete("1.0", "end")
            self.code_textbox.insert("1.0", code)
            self.current_code = code

    def get_code(self) -> str:
        """
        获取当前代码

        Returns:
            代码内容
        """
        return self.code_textbox.get("1.0", "end").strip()

    def clear(self):
        """清除代码"""
        self.code_textbox.delete("1.0", "end")
        self.current_code = ""
        self.set_status("")

    def set_status(self, message: str, is_error: bool = False):
        """
        设置状态消息

        Args:
            message: 状态消息
            is_error: 是否为错误消息
        """
        color = "#F44336" if is_error else "#4CAF50"
        self.status_label.configure(text=message, text_color=color)

    def copy_to_clipboard(self):
        """复制代码到剪贴板"""
        code = self.get_code()
        if code:
            try:
                pyperclip.copy(code)
                self.set_status("已复制到剪贴板")
            except Exception as e:
                self.set_status(f"复制失败: {str(e)}", is_error=True)
        else:
            self.set_status("没有可复制的代码", is_error=True)

    def save_to_file(self, parent_window=None):
        """
        保存代码到文件

        Args:
            parent_window: 父窗口
        """
        code = self.get_code()
        if not code:
            self.set_status("没有可保存的代码", is_error=True)
            return

        # 创建文件处理器
        if self.file_handler is None:
            self.file_handler = FileHandler(parent_window)

        # 保存文件
        success, result = self.file_handler.save_code_dialog(code)

        if success:
            self.set_status(f"已保存: {result}")
        elif result:  # 有错误消息
            self.set_status(result, is_error=True)

    def set_copy_command(self, command):
        """
        设置复制按钮的回调函数

        Args:
            command: 回调函数
        """
        self.copy_btn.configure(command=command)

    def set_save_command(self, command):
        """
        设置保存按钮的回调函数

        Args:
            command: 回调函数
        """
        self.save_btn.configure(command=command)

    def set_clear_command(self, command):
        """
        设置清除按钮的回调函数

        Args:
            command: 回调函数
        """
        self.clear_btn.configure(command=command)
