"""
代码生成器模块
提供代码生成的业务逻辑
"""

from typing import Optional

from config.constants import (
    CODE_TEMPLATES,
    DEFAULT_MAX_TOKENS,
    DEFAULT_TEMPERATURE,
    PROGRAMMING_LANGUAGES,
)
from core.claude_api import ClaudeAPIClient


class CodeGenerator:
    """代码生成器"""

    def __init__(self, api_client: ClaudeAPIClient):
        """
        初始化代码生成器

        Args:
            api_client: Claude API 客户端
        """
        self.api_client = api_client

    def generate(
        self,
        description: str,
        language: str,
        template_type: Optional[str] = None,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        use_stream: bool = False,
        callback: Optional[callable] = None,
    ) -> str:
        """
        生成代码

        Args:
            description: 代码描述
            language: 编程语言
            template_type: 模板类型（可选）
            temperature: 温度参数
            max_tokens: 最大 token 数
            use_stream: 是否使用流式响应
            callback: 流式响应回调函数

        Returns:
            生成的代码
        """
        # 验证语言
        if language not in PROGRAMMING_LANGUAGES and language != "Other":
            language = "Python"

        # 构建提示词
        prompt = self._build_prompt(description, language, template_type)

        # 生成代码
        if use_stream and callback:
            return self.api_client.generate_code_stream(
                prompt=prompt,
                language=language,
                callback=callback,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        else:
            return self.api_client.generate_code(
                prompt=prompt,
                language=language,
                temperature=temperature,
                max_tokens=max_tokens,
            )

    def _build_prompt(
        self,
        description: str,
        language: str,
        template_type: Optional[str] = None
    ) -> str:
        """
        构建提示词

        Args:
            description: 代码描述
            language: 编程语言
            template_type: 模板类型

        Returns:
            完整的提示词
        """
        if template_type and template_type in CODE_TEMPLATES:
            # 使用模板
            template = CODE_TEMPLATES[template_type]
            prompt = template.format(
                language=language,
                description=description
            )
        else:
            # 直接使用描述
            prompt = description

        return prompt

    def validate_description(self, description: str) -> tuple[bool, str]:
        """
        验证代码描述

        Args:
            description: 代码描述

        Returns:
            (是否有效, 错误消息)
        """
        if not description or not description.strip():
            return False, "请输入代码描述"

        if len(description) < 10:
            return False, "代码描述太短，请提供更多细节"

        if len(description) > 5000:
            return False, "代码描述太长，请精简您的描述"

        return True, ""

    def get_template_types(self) -> list[str]:
        """
        获取可用的模板类型

        Returns:
            模板类型列表
        """
        return list(CODE_TEMPLATES.keys())

    def get_supported_languages(self) -> list[str]:
        """
        获取支持的编程语言

        Returns:
            语言列表
        """
        return PROGRAMMING_LANGUAGES
