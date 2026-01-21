"""
常量定义模块
包含应用中使用的所有常量
"""

# 应用信息
APP_NAME = "Claude Code Generator"
APP_VERSION = "1.0.0"
AUTHOR = "Claude Code Generator Team"

# Claude API 配置
CLAUDE_MODELS = {
    "Claude 3.5 Sonnet": "claude-3-5-sonnet-20241022",
    "Claude 3 Opus": "claude-3-opus-20240229",
    "Claude 3 Sonnet": "claude-3-sonnet-20240229",
    "Claude 3 Haiku": "claude-3-haiku-20240307",
}

DEFAULT_MODEL = "claude-3-5-sonnet-20241022"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 4096

# 支持的编程语言
PROGRAMMING_LANGUAGES = [
    "Python",
    "JavaScript",
    "TypeScript",
    "Java",
    "C++",
    "C#",
    "Go",
    "Rust",
    "PHP",
    "Ruby",
    "Swift",
    "Kotlin",
    "HTML/CSS",
    "SQL",
    "Shell",
    "Other",
]

DEFAULT_LANGUAGE = "Python"

# UI 配置
THEMES = ["System", "Dark", "Light"]
DEFAULT_THEME = "System"

WINDOW_MIN_WIDTH = 1000
WINDOW_MIN_HEIGHT = 700
DEFAULT_WINDOW_WIDTH = 1200
DEFAULT_WINDOW_HEIGHT = 800

# 文件路径
DATA_DIR = "data"
CONFIG_FILE = "data/config.json"
CONVERSATIONS_DIR = "data/conversations"
LOGS_DIR = "data/logs"
ICONS_DIR = "assets/icons"

# 配置键名
CONFIG_API_KEY = "api_key"
CONFIG_MODEL = "model"
CONFIG_TEMPERATURE = "temperature"
CONFIG_MAX_TOKENS = "max_tokens"
CONFIG_THEME = "theme"
CONFIG_LANGUAGE = "language"
CONFIG_WINDOW_GEOMETRY = "window_geometry"
CONFIG_HISTORY_ENABLED = "history_enabled"
CONFIG_MAX_HISTORY = "max_history_entries"

# 默认配置值
DEFAULT_CONFIG = {
    CONFIG_API_KEY: "",
    CONFIG_MODEL: DEFAULT_MODEL,
    CONFIG_TEMPERATURE: DEFAULT_TEMPERATURE,
    CONFIG_MAX_TOKENS: DEFAULT_MAX_TOKENS,
    CONFIG_THEME: DEFAULT_THEME,
    CONFIG_LANGUAGE: DEFAULT_LANGUAGE,
    CONFIG_WINDOW_GEOMETRY: f"{DEFAULT_WINDOW_WIDTH}x{DEFAULT_WINDOW_HEIGHT}",
    CONFIG_HISTORY_ENABLED: True,
    CONFIG_MAX_HISTORY: 50,
}

# API 配置
API_RETRY_ATTEMPTS = 3
API_TIMEOUT = 60
API_RETRY_DELAY = 1  # 秒

# 代码模板
CODE_TEMPLATES = {
    "函数": "创建一个{language}函数，功能：{description}",
    "类": "创建一个{language}类，实现：{description}",
    "算法": "用{language}实现{description}算法",
    "API": "创建一个{language} API 端点：{description}",
    "数据处理": "用{language}处理数据：{description}",
}

# 日志配置
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_MAX_BYTES = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT = 5

# 错误消息
ERROR_MESSAGES = {
    "no_api_key": "未找到 API Key，请在设置中配置您的 Claude API Key",
    "invalid_api_key": "API Key 无效，请检查您的配置",
    "network_error": "网络连接失败，请检查您的网络连接",
    "api_error": "API 调用失败：{error}",
    "empty_input": "请输入代码描述",
    "save_error": "保存文件失败：{error}",
}

# 成功消息
SUCCESS_MESSAGES = {
    "copied": "代码已复制到剪贴板",
    "saved": "文件已保存：{filename}",
    "settings_saved": "设置已保存",
}

# 图标文件名（可选，如果有的话）
APP_ICON = "app_icon.ico"
