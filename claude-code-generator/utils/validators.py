"""
输入验证模块
提供各种输入验证功能
"""

import re


def validate_api_key(api_key: str) -> tuple[bool, str]:
    """
    验证 Claude API Key 格式

    Args:
        api_key: API Key

    Returns:
        (是否有效, 错误消息)
    """
    if not api_key or not api_key.strip():
        return False, "API Key 不能为空"

    api_key = api_key.strip()

    # Claude API Key 通常以 sk-ant- 开头
    if not api_key.startswith('sk-ant-'):
        return False, "无效的 Claude API Key 格式（应以 sk-ant- 开头）"

    # 检查长度（Claude API Key 通常很长）
    if len(api_key) < 20:
        return False, "API Key 长度不足"

    return True, ""


def validate_temperature(temperature: float) -> tuple[bool, str]:
    """
    验证温度参数

    Args:
        temperature: 温度值

    Returns:
        (是否有效, 错误消息)
    """
    if not isinstance(temperature, (int, float)):
        return False, "温度必须是数字"

    if temperature < 0:
        return False, "温度不能小于 0"

    if temperature > 2:
        return False, "温度不能大于 2"

    return True, ""


def validate_max_tokens(max_tokens: int) -> tuple[bool, str]:
    """
    验证最大 token 数

    Args:
        max_tokens: 最大 token 数

    Returns:
        (是否有效, 错误消息)
    """
    if not isinstance(max_tokens, int):
        return False, "最大 token 数必须是整数"

    if max_tokens < 1:
        return False, "最大 token 数必须大于 0"

    if max_tokens > 8192:
        return False, "最大 token 数不能超过 8192"

    return True, ""


def validate_file_path(file_path: str) -> tuple[bool, str]:
    """
    验证文件路径

    Args:
        file_path: 文件路径

    Returns:
        (是否有效, 错误消息)
    """
    if not file_path or not file_path.strip():
        return False, "文件路径不能为空"

    # 检查非法字符
    invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
    for char in invalid_chars:
        if char in file_path:
            return False, f"文件路径包含非法字符: {char}"

    return True, ""


def sanitize_filename(filename: str) -> str:
    """
    清理文件名，移除非法字符

    Args:
        filename: 原始文件名

    Returns:
        清理后的文件名
    """
    # 移除非法字符
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        filename = filename.replace(char, '_')

    # 移除前后空格
    filename = filename.strip()

    # 如果为空，使用默认名称
    if not filename:
        filename = "untitled"

    return filename
