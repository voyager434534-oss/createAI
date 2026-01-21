"""
Claude API 客户端模块
负责与 Anthropic Claude API 的通信
"""

import time
from typing import Callable, Optional

import anthropic

from config.constants import (
    API_RETRY_ATTEMPTS,
    API_RETRY_DELAY,
    API_TIMEOUT,
    DEFAULT_MAX_TOKENS,
    DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    ERROR_MESSAGES,
)


class ClaudeAPIClient:
    """Claude API 客户端"""

    def __init__(self, api_key: str):
        """
        初始化 API 客户端

        Args:
            api_key: Claude API Key
        """
        if not api_key:
            raise ValueError(ERROR_MESSAGES["no_api_key"])

        self.api_key = api_key
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = DEFAULT_MODEL

    def set_model(self, model: str) -> None:
        """
        设置使用的模型

        Args:
            model: 模型名称或 ID
        """
        self.model = model

    def _build_system_prompt(self, language: str) -> str:
        """
        构建系统提示词

        Args:
            language: 编程语言

        Returns:
            系���提示词
        """
        return f"""You are an expert {language} programmer. Your task is to generate clean, efficient, and well-documented code.

Requirements:
- Follow {language} best practices and conventions
- Include proper error handling
- Add clear comments for complex logic
- Use meaningful variable and function names
- Consider edge cases and validation
- Structure the code in a readable and maintainable way

Respond ONLY with the code block. Do not include explanations or markdown formatting outside the code block.
Start your response directly with the code."""

    def generate_code(
        self,
        prompt: str,
        language: str,
        model: Optional[str] = None,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS,
    ) -> str:
        """
        生成代码（非流式）

        Args:
            prompt: 用户提示词
            language: 编程语言
            model: 模型名称（可选）
            temperature: 温度参数
            max_tokens: 最大 token 数

        Returns:
            生成的代码

        Raises:
            RuntimeError: API 调用失败
        """
        if not prompt.strip():
            raise ValueError(ERROR_MESSAGES["empty_input"])

        system_prompt = self._build_system_prompt(language)
        model_to_use = model or self.model

        for attempt in range(API_RETRY_ATTEMPTS):
            try:
                response = self.client.messages.create(
                    model=model_to_use,
                    system=system_prompt,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                )

                # 提取代码内容
                code = response.content[0].text
                return self._extract_code(code)

            except anthropic.AuthenticationError:
                raise RuntimeError(ERROR_MESSAGES["invalid_api_key"])

            except anthropic.RateLimitError:
                if attempt < API_RETRY_ATTEMPTS - 1:
                    time.sleep(API_RETRY_DELAY * (2 ** attempt))
                    continue
                else:
                    raise RuntimeError("API 请求过于频繁，请稍后再试")

            except anthropic.APITimeoutError:
                if attempt < API_RETRY_ATTEMPTS - 1:
                    time.sleep(API_RETRY_DELAY)
                    continue
                else:
                    raise RuntimeError(ERROR_MESSAGES["network_error"])

            except Exception as e:
                if attempt < API_RETRY_ATTEMPTS - 1:
                    time.sleep(API_RETRY_DELAY)
                    continue
                else:
                    raise RuntimeError(ERROR_MESSAGES["api_error"].format(error=str(e)))

        raise RuntimeError("代码生成失败")

    def generate_code_stream(
        self,
        prompt: str,
        language: str,
        callback: Callable[[str], None],
        model: Optional[str] = None,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS,
    ) -> str:
        """
        生成代码（流式）

        Args:
            prompt: 用户提示词
            language: 编程语言
            callback: 接收流式数据的回调函数
            model: 模型名称（可选）
            temperature: 温度参数
            max_tokens: 最大 token 数

        Returns:
            完整的生成代码

        Raises:
            RuntimeError: API 调用失败
        """
        if not prompt.strip():
            raise ValueError(ERROR_MESSAGES["empty_input"])

        system_prompt = self._build_system_prompt(language)
        model_to_use = model or self.model
        full_code = ""

        try:
            with self.client.messages.stream(
                model=model_to_use,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            ) as stream:
                for text in stream.text_stream:
                    full_code += text
                    callback(text)

            return self._extract_code(full_code)

        except anthropic.AuthenticationError:
            raise RuntimeError(ERROR_MESSAGES["invalid_api_key"])

        except anthropic.RateLimitError:
            raise RuntimeError("API 请求过于频繁，请稍后再试")

        except anthropic.APITimeoutError:
            raise RuntimeError(ERROR_MESSAGES["network_error"])

        except Exception as e:
            raise RuntimeError(ERROR_MESSAGES["api_error"].format(error=str(e)))

    def test_connection(self) -> bool:
        """
        测试 API 连接

        Returns:
            连接成功返回 True，否则返回 False
        """
        try:
            self.client.messages.create(
                model=self.model,
                max_tokens=10,
                messages=[{"role": "user", "content": "test"}]
            )
            return True
        except Exception:
            return False

    def _extract_code(self, text: str) -> str:
        """
        从响应中提取代码
        移除 markdown 代码块标记（如果存在）

        Args:
            text: 原始文本

        Returns:
            提取的代码
        """
        # 移除可能存在的 markdown 代码块标记
        lines = text.split('\n')

        # 检查是否有代码块开始
        start_idx = 0
        end_idx = len(lines)

        for i, line in enumerate(lines):
            if line.strip().startswith('```'):
                start_idx = i + 1
                break

        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip().startswith('```'):
                end_idx = i
                break

        # 提取代码
        code_lines = lines[start_idx:end_idx]
        code = '\n'.join(code_lines).strip()

        return code if code else text
