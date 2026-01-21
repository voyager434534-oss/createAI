"""
设置管理模块
负责配置的读取、写入和验证
"""

import json
import os
from typing import Any, Dict

from config.constants import (
    CONFIG_FILE,
    DEFAULT_CONFIG,
    CONFIG_API_KEY,
)
from utils.security import encrypt_api_key, decrypt_api_key


class SettingsManager:
    """设置管理器"""

    def __init__(self, config_file: str = CONFIG_FILE):
        """
        初始化设置管理器

        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file
        self._config = None
        self._load_config()

    def _load_config(self) -> None:
        """从文件加载配置"""
        # 如果配置文件不存在，创建默认配置
        if not os.path.exists(self.config_file):
            self._create_default_config()
            return

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                encrypted_config = json.load(f)

            # 解密 API Key
            config = {}
            for key, value in encrypted_config.items():
                if key == CONFIG_API_KEY and value:
                    try:
                        config[key] = decrypt_api_key(value)
                    except Exception:
                        config[key] = value
                else:
                    config[key] = value

            self._config = config
        except Exception as e:
            print(f"加载配置失败: {e}")
            self._create_default_config()

    def _create_default_config(self) -> None:
        """创建默认配置文件"""
        self._config = DEFAULT_CONFIG.copy()
        self.save_config()

    def save_config(self) -> None:
        """保存配置到文件"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)

            # 加密 API Key
            encrypted_config = {}
            for key, value in self._config.items():
                if key == CONFIG_API_KEY and value:
                    try:
                        encrypted_config[key] = encrypt_api_key(value)
                    except Exception:
                        encrypted_config[key] = value
                else:
                    encrypted_config[key] = value

            # 保存到文件
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(encrypted_config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise RuntimeError(f"保存配置失败: {str(e)}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值

        Args:
            key: 配置键
            default: 默认值

        Returns:
            配置值
        """
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        设置配置值

        Args:
            key: 配置键
            value: 配置值
        """
        self._config[key] = value

    def get_all(self) -> Dict[str, Any]:
        """
        获取所有配置

        Returns:
            配置字典
        """
        return self._config.copy()

    def update(self, config_dict: Dict[str, Any]) -> None:
        """
        更新多个配置值

        Args:
            config_dict: 配置字典
        """
        self._config.update(config_dict)

    def reset_to_default(self) -> None:
        """重置为默认配置"""
        self._config = DEFAULT_CONFIG.copy()
        self.save_config()


# 全局设置管理器实例
_settings_manager = None


def get_settings_manager() -> SettingsManager:
    """
    获取全局设置管理器实例

    Returns:
        SettingsManager 实例
    """
    global _settings_manager
    if _settings_manager is None:
        _settings_manager = SettingsManager()
    return _settings_manager
