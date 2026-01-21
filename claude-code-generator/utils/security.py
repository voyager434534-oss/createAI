"""
安全模块
提供加密和解密功能，用于保护 API Key 等敏感信息
使用 Windows DPAPI 进行加密
"""

import base64
import win32crypt


def encrypt_api_key(api_key: str) -> str:
    """
    加密 API Key
    使用 Windows DPAPI 加密，仅当前 Windows 用户可以解密

    Args:
        api_key: 明文 API Key

    Returns:
        Base64 编码的加密字符串
    """
    try:
        # 将字符串转换为字节
        data = api_key.encode('utf-8')

        # 使用 Windows DPAPI 加密
        encrypted = win32crypt.CryptProtectData(
            data,
            None,  # 描述
            None,  # 可选熵
            None,  # 保留
            None,  # 提示句柄
            0      # 标志
        )

        # 返回 Base64 编码的字符串
        return base64.b64encode(encrypted).decode('utf-8')
    except Exception as e:
        raise RuntimeError(f"加密失败: {str(e)}")


def decrypt_api_key(encrypted_key: str) -> str:
    """
    解密 API Key
    使用 Windows DPAPI 解密

    Args:
        encrypted_key: Base64 编码的加密字符串

    Returns:
        明文 API Key
    """
    try:
        # 从 Base64 解码
        data = base64.b64decode(encrypted_key)

        # 使用 Windows DPAPI 解密
        decrypted = win32crypt.CryptUnprotectData(
            data,
            None,  # 描述
            None,  # 可选熵
            None,  # 保留
            0      # 标志
        )

        # 返回解密后的字符串
        return decrypted[1].decode('utf-8')
    except Exception as e:
        raise RuntimeError(f"解密失败: {str(e)}")


def is_encrypted(value: str) -> bool:
    """
    检查值是否已加密

    Args:
        value: 要检查的值

    Returns:
        如果是加密的值返回 True，否则返回 False
    """
    try:
        # 尝试 Base64 解码
        decoded = base64.b64decode(value)
        # 如果解码成功且长度合理，认为可能是加密的
        return len(decoded) > 0
    except Exception:
        return False
