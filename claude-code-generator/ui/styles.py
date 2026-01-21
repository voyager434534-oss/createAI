"""
UI 样式定义模块
定义应用的颜色、字体和其他样式
"""

import customtkinter as ctk


class Styles:
    """UI 样式配置"""

    # 颜色主题
    COLORS = {
        # 浅色主题
        "light": {
            "background": "#FFFFFF",
            "surface": "#F0F0F0",
            "primary": "#3B8ED0",
            "primary_hover": "#3672A8",
            "text": "#000000",
            "text_dim": "#666666",
            "border": "#CCCCCC",
            "success": "#4CAF50",
            "error": "#F44336",
            "warning": "#FF9800",
        },
        # 深色主题
        "dark": {
            "background": "#1A1A1A",
            "surface": "#2B2B2B",
            "primary": "#3B8ED0",
            "primary_hover": "#5BA3D9",
            "text": "#FFFFFF",
            "text_dim": "#AAAAAA",
            "border": "#404040",
            "success": "#4CAF50",
            "error": "#F44336",
            "warning": "#FF9800",
        },
    }

    # 字体配置
    FONTS = {
        "title": ("Microsoft YaHei UI", 24, "bold"),
        "heading": ("Microsoft YaHei UI", 18, "bold"),
        "subheading": ("Microsoft YaHei UI", 14, "bold"),
        "body": ("Microsoft YaHei UI", 12),
        "small": ("Microsoft YaHei UI", 10),
        "code": ("Consolas", 11),
        "code_large": ("Consolas", 13),
    }

    # 间距
    SPACING = {
        "xs": 5,
        "sm": 10,
        "md": 15,
        "lg": 20,
        "xl": 30,
    }

    # 圆角
    CORNER_RADIUS = {
        "sm": 5,
        "md": 10,
        "lg": 15,
    }

    @staticmethod
    def get_colors(theme: str = "dark") -> dict:
        """
        获取指定主题的颜色

        Args:
            theme: 主题名称（"light" 或 "dark"）

        Returns:
            颜色字典
        """
        return Styles.COLORS.get(theme, Styles.COLORS["dark"])

    @staticmethod
    def configure_appearance(theme: str = "System") -> None:
        """
        配置应用外观

        Args:
            theme: 主题（"System", "Dark", "Light"）
        """
        ctk.set_appearance_mode(theme)

        # 配置默认颜色主题
        ctk.set_default_color_theme("blue")

    @staticmethod
    def get_button_style(
        theme: str = "dark",
        fg_color: str = None,
        hover_color: str = None,
        text_color: str = None,
    ) -> dict:
        """
        获取按钮样式

        Args:
            theme: 主题名称
            fg_color: 前景色
            hover_color: 悬停色
            text_color: 文字颜色

        Returns:
            样式字典
        """
        colors = Styles.get_colors(theme)

        return {
            "fg_color": fg_color or colors["primary"],
            "hover_color": hover_color or colors["primary_hover"],
            "text_color": text_color or ("#FFFFFF" if theme == "dark" else "#FFFFFF"),
            "corner_radius": Styles.CORNER_RADIUS["md"],
            "font": Styles.FONTS["body"],
            "height": 35,
        }

    @staticmethod
    def get_input_style(theme: str = "dark") -> dict:
        """
        获取输入框样式

        Args:
            theme: 主题名称

        Returns:
            样式字典
        """
        colors = Styles.get_colors(theme)

        return {
            "fg_color": colors["surface"],
            "border_color": colors["border"],
            "text_color": colors["text"],
            "placeholder_text_color": colors["text_dim"],
            "corner_radius": Styles.CORNER_RADIUS["sm"],
            "font": Styles.FONTS["body"],
            "height": 100,
        }

    @staticmethod
    def get_textbox_style(theme: str = "dark") -> dict:
        """
        获取文本框样式

        Args:
            theme: 主题名称

        Returns:
            样式字典
        """
        colors = Styles.get_colors(theme)

        return {
            "fg_color": colors["surface"],
            "border_color": colors["border"],
            "text_color": colors["text"],
            "font": Styles.FONTS["code"],
            "corner_radius": Styles.CORNER_RADIUS["sm"],
        }
