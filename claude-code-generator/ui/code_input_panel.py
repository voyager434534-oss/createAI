"""
代码输入面板模块
提供用户输入代码描述的界面
"""

import customtkinter as ctk

import config.constants as constants
from ui.styles import Styles


class CodeInputPanel(ctk.CTkFrame):
    """代码输入面板"""

    def __init__(self, master, **kwargs):
        """
        初始化输入面板

        Args:
            master: 父容器
        """
        super().__init__(master, **kwargs)

        self.current_theme = "dark"
        self.selected_language = constants.DEFAULT_LANGUAGE
        self.selected_template = None

        self._setup_ui()

    def _setup_ui(self):
        """设置用户界面"""
        # 配置网格
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # 标题
        self._create_header()

        # 语言选择
        self._create_language_selector()

        # 文本输入框
        self._create_text_input()

        # 模板选择（可选）
        self._create_template_selector()

        # 按钮
        self._create_buttons()

    def _create_header(self):
        """创建标题"""
        header = ctk.CTkLabel(
            self,
            text="代码描述",
            font=Styles.FONTS["subheading"],
            anchor="w"
        )
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=Styles.SPACING["md"], pady=(Styles.SPACING["md"], Styles.SPACING["xs"]))

    def _create_language_selector(self):
        """创建语言选择器"""
        # 标签
        label = ctk.CTkLabel(
            self,
            text="语言:",
            font=Styles.FONTS["body"]
        )
        label.grid(row=1, column=0, sticky="w", padx=Styles.SPACING["md"])

        # 下拉菜单
        self.language_combo = ctk.CTkOptionMenu(
            self,
            values=constants.PROGRAMMING_LANGUAGES,
            command=self._on_language_change,
            font=Styles.FONTS["body"],
            dropdown_font=Styles.FONTS["body"],
            width=150,
        )
        self.language_combo.set(self.selected_language)
        self.language_combo.grid(row=1, column=1, sticky="e", padx=Styles.SPACING["md"])

    def _create_text_input(self):
        """创建文本输入框"""
        # 文本框容器
        textbox_frame = ctk.CTkFrame(self, fg_color="transparent")
        textbox_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=Styles.SPACING["md"], pady=Styles.SPACING["sm"])
        textbox_frame.grid_columnconfigure(0, weight=1)
        textbox_frame.grid_rowconfigure(0, weight=1)

        # 文本框
        self.textbox = ctk.CTkTextbox(
            textbox_frame,
            wrap="word",
            font=Styles.FONTS["body"],
        )
        self.textbox.grid(row=0, column=0, sticky="nsew")

        # 占位符提示
        self.textbox.insert("1.0", "请详细描述您需要生成的代码功能...\n\n例如：\n"
                                   "• 创建一个计算斐波那契数列的函数\n"
                                   "• 实现一个快速排序算法\n"
                                   "• 创建一个 RESTful API 端点")
        self.textbox.bind("<FocusIn>", self._on_textbox_focus)

    def _create_template_selector(self):
        """创建模板选择器"""
        # 模板按钮容器
        template_frame = ctk.CTkFrame(self, fg_color="transparent")
        template_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=Styles.SPACING["md"], pady=Styles.SPACING["xs"])

        # 模板按钮
        templates = ["函数", "类", "算法", "API", "数据处理"]
        for i, template in enumerate(templates):
            btn = ctk.CTkButton(
                template_frame,
                text=template,
                width=80,
                height=28,
                font=Styles.FONTS["small"],
                command=lambda t=template: self._on_template_click(t)
            )
            btn.grid(row=0, column=i, padx=2)

    def _create_buttons(self):
        """创建按钮"""
        # 按钮容器
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=Styles.SPACING["md"], pady=Styles.SPACING["md"])

        # 生成按钮
        self.generate_btn = ctk.CTkButton(
            button_frame,
            text="生成代码",
            font=Styles.FONTS["body"],
            height=40,
        )
        self.generate_btn.grid(row=0, column=0, sticky="ew", padx=(0, Styles.SPACING["xs"]))

        # 清除按钮
        self.clear_btn = ctk.CTkButton(
            button_frame,
            text="清除",
            font=Styles.FONTS["body"],
            height=40,
            fg_color="transparent",
            border_width=2,
        )
        self.clear_btn.grid(row=0, column=1, sticky="ew")

        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

    def _on_language_change(self, choice: str):
        """
        语言改变回调

        Args:
            choice: 选择的语言
        """
        self.selected_language = choice

    def _on_template_click(self, template: str):
        """
        模板按钮点击回调

        Args:
            template: 模板类型
        """
        self.selected_template = template

    def _on_textbox_focus(self, event):
        """文本框获得焦点时清除占位符"""
        current_text = self.textbox.get("1.0", "end").strip()
        if current_text.startswith("请详细描述"):
            self.textbox.delete("1.0", "end")

    def get_description(self) -> str:
        """
        获取用户输入的描述

        Returns:
            代码描述
        """
        return self.textbox.get("1.0", "end").strip()

    def get_language(self) -> str:
        """
        获取选择的语言

        Returns:
            编程语言
        """
        return self.language_combo.get()

    def get_template(self) -> str | None:
        """
        获取选择的模板

        Returns:
            模板类型或 None
        """
        return self.selected_template

    def clear(self):
        """清除输入"""
        self.textbox.delete("1.0", "end")
        self.selected_template = None

    def set_generate_command(self, command):
        """
        设置生成按钮的回调函数

        Args:
            command: 回调函数
        """
        self.generate_btn.configure(command=command)

    def set_clear_command(self, command):
        """
        设置清除按钮的回调函数

        Args:
            command: 回调函数
        """
        self.clear_btn.configure(command=command)

    def set_loading(self, loading: bool):
        """
        设置加载状态

        Args:
            loading: 是否加载中
        """
        if loading:
            self.generate_btn.configure(state="disabled", text="生成中...")
        else:
            self.generate_btn.configure(state="normal", text="生成代码")
