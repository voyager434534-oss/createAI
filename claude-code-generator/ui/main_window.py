"""
主窗口模块
应用的主界面
"""

import customtkinter as ctk

import config.constants as constants
from config.settings import get_settings_manager
from core.claude_api import ClaudeAPIClient
from core.code_generator import CodeGenerator
from ui.code_input_panel import CodeInputPanel
from ui.output_panel import OutputPanel
from ui.settings_dialog import SettingsDialog
from ui.styles import Styles
from utils.logger import get_logger


class MainWindow(ctk.CTk):
    """主窗口"""

    def __init__(self):
        """初始化主窗口"""
        super().__init__()

        self.logger = get_logger()
        self.settings = get_settings_manager()

        # API 客户端和代码生成器
        self.api_client = None
        self.code_generator = None

        # 设置窗口
        self._setup_window()

        # 创建 UI
        self._create_ui()

        # 初始化 API
        self._initialize_api()

        # 加载设置
        self._load_settings()

        self.logger.info("应用已启动")

    def _setup_window(self):
        """设置窗口"""
        self.title(f"{constants.APP_NAME} v{constants.APP_VERSION}")
        self.geometry(f"{constants.DEFAULT_WINDOW_WIDTH}x{constants.DEFAULT_WINDOW_HEIGHT}")
        self.minsize(constants.WINDOW_MIN_WIDTH, constants.WINDOW_MIN_HEIGHT)

        # 配置主题
        theme = self.settings.get(constants.CONFIG_THEME, constants.DEFAULT_THEME)
        Styles.configure_appearance(theme)

        # 配置网格
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

    def _create_ui(self):
        """创建用户界面"""
        # 创建菜单栏
        self._create_menu_bar()

        # 创建工具栏
        self._create_toolbar()

        # 创建主面板（输入和输出）
        self._create_main_panel()

        # 创建状态栏
        self._create_status_bar()

    def _create_menu_bar(self):
        """创建菜单栏"""
        menubar = ctk.CTkFrame(self, height=30)
        menubar.grid(row=0, column=0, sticky="ew")
        menubar.grid_columnconfigure(0, weight=1)

        # 文件菜单
        file_btn = ctk.CTkButton(
            menubar,
            text="文件",
            width=60,
            height=30,
            fg_color="transparent",
            command=self._show_file_menu
        )
        file_btn.grid(row=0, column=0, padx=Styles.SPACING["xs"])

        # 编辑菜单
        edit_btn = ctk.CTkButton(
            menubar,
            text="编辑",
            width=60,
            height=30,
            fg_color="transparent",
            command=self._show_edit_menu
        )
        edit_btn.grid(row=0, column=1, padx=Styles.SPACING["xs"])

        # 设置菜单
        settings_btn = ctk.CTkButton(
            menubar,
            text="设置",
            width=60,
            height=30,
            fg_color="transparent",
            command=self._show_settings
        )
        settings_btn.grid(row=0, column=2, padx=Styles.SPACING["xs"])

        # 帮助菜单
        help_btn = ctk.CTkButton(
            menubar,
            text="帮助",
            width=60,
            height=30,
            fg_color="transparent",
            command=self._show_help
        )
        help_btn.grid(row=0, column=3, padx=Styles.SPACING["xs"])

    def _create_toolbar(self):
        """创建工具栏"""
        toolbar = ctk.CTkFrame(self, height=50)
        toolbar.grid(row=1, column=0, sticky="ew")
        toolbar.grid_columnconfigure(0, weight=1)

        # 生成按钮
        self.generate_toolbar_btn = ctk.CTkButton(
            toolbar,
            text="生成代码",
            font=Styles.FONTS["body"],
            height=35,
            width=100,
            command=self._on_generate
        )
        self.generate_toolbar_btn.grid(row=0, column=0, padx=Styles.SPACING["md"], pady=Styles.SPACING["sm"])

    def _create_main_panel(self):
        """创建主面板"""
        # 使用 PanedFrame 分割输入和输出面板
        paned_frame = ctk.CTkFrame(self)
        paned_frame.grid(row=2, column=0, sticky="nsew", padx=Styles.SPACING["md"], pady=Styles.SPACING["md"])
        paned_frame.grid_columnconfigure(0, weight=1)
        paned_frame.grid_columnconfigure(1, weight=1)
        paned_frame.grid_rowconfigure(0, weight=1)

        # 输入面板
        self.input_panel = CodeInputPanel(paned_frame)
        self.input_panel.grid(row=0, column=0, sticky="nsew", padx=(0, Styles.SPACING["xs"]))

        # 输出面板
        self.output_panel = OutputPanel(paned_frame)
        self.output_panel.grid(row=0, column=1, sticky="nsew", padx=(Styles.SPACING["xs"], 0))

        # 设置回调
        self.input_panel.set_generate_command(self._on_generate)
        self.input_panel.set_clear_command(self._on_clear_input)

        self.output_panel.set_copy_command(self._on_copy_code)
        self.output_panel.set_save_command(self._on_save_code)
        self.output_panel.set_clear_command(self._on_clear_output)

    def _create_status_bar(self):
        """创建状态栏"""
        status_bar = ctk.CTkFrame(self, height=30)
        status_bar.grid(row=3, column=0, sticky="ew")
        status_bar.grid_columnconfigure(0, weight=1)

        # 状态标签
        self.status_label = ctk.CTkLabel(
            status_bar,
            text="就绪",
            anchor="w",
            font=Styles.FONTS["small"]
        )
        self.status_label.grid(row=0, column=0, sticky="ew", padx=Styles.SPACING["md"])

        # 模型标签
        self.model_label = ctk.CTkLabel(
            status_bar,
            text="",
            anchor="e",
            font=Styles.FONTS["small"]
        )
        self.model_label.grid(row=0, column=1, sticky="e", padx=Styles.SPACING["md"])

    def _initialize_api(self):
        """初始化 API 客户端"""
        api_key = self.settings.get(constants.CONFIG_API_KEY, "")
        if api_key:
            try:
                self.api_client = ClaudeAPIClient(api_key)
                model = self.settings.get(constants.CONFIG_MODEL, constants.DEFAULT_MODEL)
                self.api_client.set_model(model)
                self.code_generator = CodeGenerator(self.api_client)
                self._update_status("API 已连接")
            except Exception as e:
                self.logger.error(f"初始化 API 失败: {e}", exc_info=True)
                self._update_status("API 连接失败", is_error=True)
        else:
            self._update_status("未配置 API Key")

    def _load_settings(self):
        """加载设置"""
        # 更新模型标签
        model = self.settings.get(constants.CONFIG_MODEL, constants.DEFAULT_MODEL)
        model_name = self._get_model_display_name(model)
        if model_name:
            self.model_label.configure(text=f"模型: {model_name}")

    def _get_model_display_name(self, model_id: str) -> str | None:
        """获取模型显示名称"""
        for name, id_ in constants.CLAUDE_MODELS.items():
            if id_ == model_id:
                return name
        return None

    def _on_generate(self):
        """生成代码按钮回调"""
        # 检查 API 客户端
        if not self.api_client or not self.code_generator:
            self._show_error("未配置 API", "请先在设置中配置您的 Claude API Key")
            return

        # 获取输入
        description = self.input_panel.get_description()
        language = self.input_panel.get_language()
        template = self.input_panel.get_template()

        # 验证描述
        is_valid, error_msg = self.code_generator.validate_description(description)
        if not is_valid:
            self._show_error("输入错误", error_msg)
            return

        # 设置加载状态
        self.input_panel.set_loading(True)
        self._update_status("正在生成代码...")

        # 清空输出
        self.output_panel.clear()

        # 生成代码（使用线程避免阻塞 UI）
        import threading

        def generate_thread():
            try:
                # 获取生成参数
                temperature = self.settings.get(constants.CONFIG_TEMPERATURE, constants.DEFAULT_TEMPERATURE)
                max_tokens = self.settings.get(constants.CONFIG_MAX_TOKENS, constants.DEFAULT_MAX_TOKENS)

                # 生成代码
                code = self.code_generator.generate(
                    description=description,
                    language=language,
                    template_type=template,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    use_stream=True,
                    callback=lambda text: self.after(0, lambda: self._on_stream_data(text))
                )

                # 完成后更新 UI
                self.after(0, lambda: self._on_generate_complete(code))

            except Exception as e:
                self.after(0, lambda: self._on_generate_error(str(e)))

        thread = threading.Thread(target=generate_thread, daemon=True)
        thread.start()

    def _on_stream_data(self, text: str):
        """
        流式数据回调

        Args:
            text: 流式数据
        """
        self.output_panel.set_code(text, append=True)

    def _on_generate_complete(self, code: str):
        """
        生成完成回调

        Args:
            code: 生成的代码
        """
        self.input_panel.set_loading(False)
        self.output_panel.set_code(code)
        self._update_status("代码生成完成")
        self.logger.info("代码生成成功")

    def _on_generate_error(self, error_msg: str):
        """
        生成错误回调

        Args:
            error_msg: 错误消息
        """
        self.input_panel.set_loading(False)
        self.output_panel.set_status(f"生成失败: {error_msg}", is_error=True)
        self._update_status("生成失败", is_error=True)
        self.logger.error(f"代码生成失败: {error_msg}")

    def _on_clear_input(self):
        """清除输入回调"""
        self.input_panel.clear()

    def _on_clear_output(self):
        """清除输出回调"""
        self.output_panel.clear()

    def _on_copy_code(self):
        """复制代码回调"""
        self.output_panel.copy_to_clipboard()

    def _on_save_code(self):
        """保存代码回调"""
        self.output_panel.save_to_file(self)

    def _show_settings(self):
        """显示设置对话框"""
        dialog = SettingsDialog(self)
        dialog.set_on_save(self._on_settings_saved)

    def _on_settings_saved(self):
        """设置保存回调"""
        # 重新初始化 API
        self._initialize_api()

        # 更新主题
        theme = self.settings.get(constants.CONFIG_THEME, constants.DEFAULT_THEME)
        Styles.configure_appearance(theme)

        # 更新模型标签
        self._load_settings()

        self.logger.info("设置已更新")

    def _show_file_menu(self):
        """显示文件菜单（简化版）"""
        pass

    def _show_edit_menu(self):
        """显示编辑菜单（简化版）"""
        pass

    def _show_help(self):
        """显示帮助"""
        help_text = f"""{constants.APP_NAME} v{constants.APP_VERSION}

使用说明:
1. 在设置中配置您的 Claude API Key
2. 在输入框中描述您需要的代码
3. 选择目标编程语言
4. 点击"生成代码"按钮
5. 使用"复制"或"保存"按钮获取代码

获取 API Key: https://console.anthropic.com/"""

        dialog = ctk.CTkToplevel(self)
        dialog.title("帮助")
        dialog.geometry("500x300")
        dialog.grab_set()

        label = ctk.CTkLabel(dialog, text=help_text, justify="left")
        label.pack(expand=True, padx=Styles.SPACING["lg"], pady=Styles.SPACING["lg"])

        btn = ctk.CTkButton(dialog, text="确定", command=dialog.destroy, width=100)
        btn.pack(pady=Styles.SPACING["md"])

    def _update_status(self, message: str, is_error: bool = False):
        """
        更新状态栏

        Args:
            message: 状态消息
            is_error: 是否为错误
        """
        color = "#F44336" if is_error else "#4CAF50"
        self.status_label.configure(text=message, text_color=color)

    def _show_error(self, title: str, message: str):
        """
        显示错误对话框

        Args:
            title: 标题
            message: 错误消息
        """
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("400x200")
        dialog.grab_set()

        label = ctk.CTkLabel(dialog, text=message, wraplength=350)
        label.pack(expand=True, padx=Styles.SPACING["lg"], pady=Styles.SPACING["lg"])

        btn = ctk.CTkButton(dialog, text="确定", command=dialog.destroy, width=100)
        btn.pack(pady=Styles.SPACING["md"])

    def on_closing(self):
        """窗口关闭事件"""
        self.logger.info("应用正在关闭")
        self.destroy()
