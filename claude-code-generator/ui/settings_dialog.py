"""
设置对话框模块
提供应用设置界面
"""

import customtkinter as ctk

import config.constants as constants
from config.settings import get_settings_manager
from ui.styles import Styles
from utils.validators import validate_api_key, validate_temperature, validate_max_tokens


class SettingsDialog(ctk.CTkToplevel):
    """设置对话框"""

    def __init__(self, parent, **kwargs):
        """
        初始化设置对话框

        Args:
            parent: 父窗口
        """
        super().__init__(parent, **kwargs)

        self.parent = parent
        self.settings = get_settings_manager()
        self.on_save_callback = None

        self.title("设置")
        self.geometry("500x600")
        self.resizable(False, False)

        # 设置为模态对话框
        self.grab_set()

        self._setup_ui()
        self._load_settings()

    def _setup_ui(self):
        """设置用户界面"""
        # 配置网格
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 创建滚动框架
        scroll_frame = ctk.CTkScrollableFrame(self)
        scroll_frame.grid(row=0, column=0, sticky="nsew", padx=Styles.SPACING["md"], pady=Styles.SPACING["md"])

        # API 配置部分
        self._create_api_section(scroll_frame)

        # 模型配置部分
        self._create_model_section(scroll_frame)

        # UI 配置部分
        self._create_ui_section(scroll_frame)

        # 按钮部分
        self._create_buttons(scroll_frame)

    def _create_api_section(self, parent):
        """创建 API 配置部分"""
        # 部分标题
        label = ctk.CTkLabel(
            parent,
            text="API 配置",
            font=Styles.FONTS["subheading"],
            anchor="w"
        )
        label.pack(fill="x", pady=(0, Styles.SPACING["xs"]))

        # 容器
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=(0, Styles.SPACING["lg"]))

        # API Key 输入
        api_key_label = ctk.CTkLabel(frame, text="API Key:", anchor="w")
        api_key_label.pack(fill="x", padx=Styles.SPACING["sm"], pady=(Styles.SPACING["sm"], Styles.SPACING["xs"]))

        self.api_key_entry = ctk.CTkEntry(
            frame,
            placeholder_text="sk-ant-...",
            show="•",
            font=Styles.FONTS["body"]
        )
        self.api_key_entry.pack(fill="x", padx=Styles.SPACING["sm"], pady=(0, Styles.SPACING["sm"]))

        # 显示/隐藏按钮
        self.show_key_btn = ctk.CTkButton(
            frame,
            text="显示",
            width=80,
            height=28,
            font=Styles.FONTS["small"],
            command=self._toggle_api_key_visibility
        )
        self.show_key_btn.pack(anchor="e", padx=Styles.SPACING["sm"], pady=(0, Styles.SPACING["sm"]))

    def _create_model_section(self, parent):
        """创建模型配置部分"""
        # 部分标题
        label = ctk.CTkLabel(
            parent,
            text="模型配置",
            font=Styles.FONTS["subheading"],
            anchor="w"
        )
        label.pack(fill="x", pady=(0, Styles.SPACING["xs"]))

        # 容器
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=(0, Styles.SPACING["lg"]))

        # 模型选择
        model_label = ctk.CTkLabel(frame, text="模型:", anchor="w")
        model_label.pack(fill="x", padx=Styles.SPACING["sm"], pady=(Styles.SPACING["sm"], Styles.SPACING["xs"]))

        model_values = list(constants.CLAUDE_MODELS.keys())
        self.model_combo = ctk.CTkOptionMenu(
            frame,
            values=model_values,
            font=Styles.FONTS["body"],
            dropdown_font=Styles.FONTS["body"]
        )
        self.model_combo.pack(fill="x", padx=Styles.SPACING["sm"], pady=(0, Styles.SPACING["sm"]))

        # 温度滑块
        temp_label = ctk.CTkLabel(frame, text="温度:", anchor="w")
        temp_label.pack(fill="x", padx=Styles.SPACING["sm"], pady=(Styles.SPACING["sm"], Styles.SPACING["xs"]))

        self.temp_slider = ctk.CTkSlider(
            frame,
            from_=0,
            to=2,
            number_of_steps=20,
            font=Styles.FONTS["body"]
        )
        self.temp_slider.pack(fill="x", padx=Styles.SPACING["sm"], pady=(0, Styles.SPACING["xs"]))

        self.temp_value_label = ctk.CTkLabel(frame, text="0.7", font=Styles.FONTS["small"])
        self.temp_value_label.pack(anchor="e", padx=Styles.SPACING["sm"], pady=(0, Styles.SPACING["sm"]))

        # 绑定滑块事件
        self.temp_slider.configure(command=self._on_temp_change)

        # 最大 token
        max_tokens_label = ctk.CTkLabel(frame, text="最大 Tokens:", anchor="w")
        max_tokens_label.pack(fill="x", padx=Styles.SPACING["sm"], pady=(Styles.SPACING["sm"], Styles.SPACING["xs"]))

        self.max_tokens_entry = ctk.CTkEntry(frame, font=Styles.FONTS["body"])
        self.max_tokens_entry.pack(fill="x", padx=Styles.SPACING["sm"], pady=(0, Styles.SPACING["sm"]))

    def _create_ui_section(self, parent):
        """创建 UI 配置部分"""
        # 部分标题
        label = ctk.CTkLabel(
            parent,
            text="界面配置",
            font=Styles.FONTS["subheading"],
            anchor="w"
        )
        label.pack(fill="x", pady=(0, Styles.SPACING["xs"]))

        # 容器
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=(0, Styles.SPACING["lg"]))

        # 主题选择
        theme_label = ctk.CTkLabel(frame, text="主题:", anchor="w")
        theme_label.pack(fill="x", padx=Styles.SPACING["sm"], pady=(Styles.SPACING["sm"], Styles.SPACING["xs"]))

        self.theme_combo = ctk.CTkOptionMenu(
            frame,
            values=constants.THEMES,
            font=Styles.FONTS["body"],
            dropdown_font=Styles.FONTS["body"]
        )
        self.theme_combo.pack(fill="x", padx=Styles.SPACING["sm"], pady=(0, Styles.SPACING["sm"]))

    def _create_buttons(self, parent):
        """创建按钮"""
        # 按钮容器
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill="x", pady=Styles.SPACING["md"])

        # 保存按钮
        save_btn = ctk.CTkButton(
            button_frame,
            text="保存",
            font=Styles.FONTS["body"],
            height=35,
            command=self._on_save
        )
        save_btn.pack(side="left", fill="x", expand=True, padx=(0, Styles.SPACING["xs"]))

        # 取消按钮
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="取消",
            font=Styles.FONTS["body"],
            height=35,
            fg_color="transparent",
            border_width=2,
            command=self._on_cancel
        )
        cancel_btn.pack(side="left", fill="x", expand=True, padx=(Styles.SPACING["xs"], 0))

    def _load_settings(self):
        """从设置管理器加载设置"""
        # API Key
        api_key = self.settings.get(constants.CONFIG_API_KEY, "")
        self.api_key_entry.insert(0, api_key)

        # 模型
        model = self.settings.get(constants.CONFIG_MODEL, constants.DEFAULT_MODEL)
        # 将模型 ID 转换为显示名称
        model_name = self._get_model_display_name(model)
        if model_name:
            self.model_combo.set(model_name)

        # 温度
        temperature = self.settings.get(constants.CONFIG_TEMPERATURE, constants.DEFAULT_TEMPERATURE)
        self.temp_slider.set(temperature)
        self._on_temp_change(temperature)

        # 最大 tokens
        max_tokens = self.settings.get(constants.CONFIG_MAX_TOKENS, constants.DEFAULT_MAX_TOKENS)
        self.max_tokens_entry.insert(0, str(max_tokens))

        # 主题
        theme = self.settings.get(constants.CONFIG_THEME, constants.DEFAULT_THEME)
        self.theme_combo.set(theme)

    def _get_model_display_name(self, model_id: str) -> str | None:
        """
        获取模型显示名称

        Args:
            model_id: 模型 ID

        Returns:
            模型显示名称或 None
        """
        for name, id_ in constants.CLAUDE_MODELS.items():
            if id_ == model_id:
                return name
        return None

    def _toggle_api_key_visibility(self):
        """切换 API Key 可见性"""
        if self.api_key_entry.cget("show") == "•":
            self.api_key_entry.configure(show="")
            self.show_key_btn.configure(text="隐藏")
        else:
            self.api_key_entry.configure(show="•")
            self.show_key_btn.configure(text="显示")

    def _on_temp_change(self, value):
        """
        温度滑块改变回调

        Args:
            value: 温度值
        """
        self.temp_value_label.configure(text=f"{value:.1f}")

    def _on_save(self):
        """保存设置"""
        # 验证 API Key
        api_key = self.api_key_entry.get().strip()
        if api_key:
            is_valid, error_msg = validate_api_key(api_key)
            if not is_valid:
                self._show_error("API Key 验证失败", error_msg)
                return

        # 验证温度
        temperature = self.temp_slider.get()
        is_valid, error_msg = validate_temperature(temperature)
        if not is_valid:
            self._show_error("温度验证失败", error_msg)
            return

        # 验证最大 token
        try:
            max_tokens = int(self.max_tokens_entry.get())
        except ValueError:
            self._show_error("输入错误", "最大 tokens 必须是数字")
            return

        is_valid, error_msg = validate_max_tokens(max_tokens)
        if not is_valid:
            self._show_error("最大 tokens 验证失败", error_msg)
            return

        # 保存设置
        self.settings.set(constants.CONFIG_API_KEY, api_key)
        model_name = self.model_combo.get()
        model_id = constants.CLAUDE_MODELS.get(model_name, constants.DEFAULT_MODEL)
        self.settings.set(constants.CONFIG_MODEL, model_id)
        self.settings.set(constants.CONFIG_TEMPERATURE, temperature)
        self.settings.set(constants.CONFIG_MAX_TOKENS, max_tokens)
        self.settings.set(constants.CONFIG_THEME, self.theme_combo.get())

        # 保存到文件
        try:
            self.settings.save_config()

            # 调用回调
            if self.on_save_callback:
                self.on_save_callback()

            self._show_info("设置已保存", "您的设置已成功保存")
            self.destroy()

        except Exception as e:
            self._show_error("保存失败", f"保存设置时出错: {str(e)}")

    def _on_cancel(self):
        """取消并关闭对话框"""
        self.destroy()

    def _show_error(self, title: str, message: str):
        """
        显示错误对话框

        Args:
            title: 标题
            message: 错误消息
        """
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("400x150")
        dialog.grab_set()

        label = ctk.CTkLabel(dialog, text=message, wraplength=350)
        label.pack(expand=True, padx=Styles.SPACING["lg"], pady=Styles.SPACING["lg"])

        btn = ctk.CTkButton(dialog, text="确定", command=dialog.destroy, width=100)
        btn.pack(pady=Styles.SPACING["md"])

    def _show_info(self, title: str, message: str):
        """
        显示信息对话框

        Args:
            title: 标题
            message: 信息消息
        """
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("400x150")
        dialog.grab_set()

        label = ctk.CTkLabel(dialog, text=message, wraplength=350)
        label.pack(expand=True, padx=Styles.SPACING["lg"], pady=Styles.SPACING["lg"])

        btn = ctk.CTkButton(dialog, text="确定", command=dialog.destroy, width=100)
        btn.pack(pady=Styles.SPACING["md"])

    def set_on_save(self, callback):
        """
        设置保存回调函数

        Args:
            callback: 回调函数
        """
        self.on_save_callback = callback
