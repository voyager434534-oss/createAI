# Claude Code Generator - 安装和使用指南

## 系统要求

- **操作系统**: Windows 11
- **Python**: 3.8 或更高版本
- **网络**: 需要互联网连接（调用 Claude API）
- **Claude API Key**: 从 [Anthropic Console](https://console.anthropic.com/) 获取

## 安装步骤

### 1. 安装 Python

如果您的系统还没有安装 Python：

1. 访问 [Python 官网](https://www.python.org/downloads/)
2. 下载并安装 Python 3.8 或更高版本
3. 安装时勾选 "Add Python to PATH"

### 2. 安装依赖

打开命令提示符（CMD）或 PowerShell，进入项目目录：

```bash
cd e:\coding\claude-code-generator
```

安装所需的 Python 包：

```bash
pip install -r requirements.txt
```

或者使用 Python 模块方式：

```bash
python -m pip install -r requirements.txt
```

### 3. 运行应用

有两种方式运行应用：

#### 方式 1: 直接运行 Python 脚本

```bash
python main.py
```

#### 方式 2: 使用启动脚本（推荐）

双击 `run.bat` 文件（如果您创建了该脚本）

## 首次使用

### 1. 获取 Claude API Key

1. 访问 [Anthropic Console](https://console.anthropic.com/)
2. 注册或登录您的账户
3. 在 API Keys 部分创建新的 API Key
4. 复制您的 API Key（格式类似：`sk-ant-...`）

### 2. 配置应用

1. 启动应用后，点击菜单栏的"设置"按钮
2. 在"API 配置"部分输入您的 API Key
3. 选择您想要使用的模型（推荐：Claude 3.5 Sonnet）
4. 调整其他参数（温度、最大 tokens）
5. 选择您喜欢的主题（浅色/深色）
6. 点击"保存"按钮

### 3. 生成代码

1. 在左侧"代码描述"文本框中输入您的需求
2. 从下拉菜单中选择目标编程语言
3. 点击"生成代码"按钮
4. 等待代码生成完成（会实时显示生成过程）
5. 在右侧查看生成的代码
6. 使用"复制"或"保存"按钮获取代码

## 使用技巧

### 有效的代码描述

为了获得更好的生成结果，请提供详细和具体的描述：

**好的描述示例**:
```
创建一个 Python 函数，实现快速排序算法。
要求：
- 使用递归方式实现
- 添加详细注释
- 包含示例用法
- 处理边界情况
```

**不好的描述示例**:
```
排序
```

### 使用模板

应用提供了多个预设模板：
- **函数**: 创建单个函数
- **类**: 创建类定义
- **算法**: 实现算法
- **API**: 创建 API 端点
- **数据处理**: 数据处理逻辑

点击模板按钮可以快速应用对应的提示词格式。

### 调整生成参数

在设置中可以调整以下参数：

- **模型**: 选择不同的 Claude 模型
  - Claude 3.5 Sonnet: 平衡性能和速度（推荐）
  - Claude 3 Opus: 最高质量，但速度较慢
  - Claude 3 Haiku: 最快，但质量较低

- **温度**: 控制生成结果的随机性
  - 0.0-0.3: 更确定性和一致的输出
  - 0.4-0.7: 平衡创造性和一致性（推荐）
  - 0.8-2.0: 更有创造性和多样性

- **最大 Tokens**: 控制生成代码的长度
  - 默认值: 4096
  - 建议范围: 1024-8192

## 常见问题

### Q: 应用无法启动？

**A**: 请确保：
1. Python 已正确安装
2. 所有依赖已安装
3. 使用 `python --version` 检查 Python 版本

### Q: 提示"未配置 API Key"？

**A**:
1. 点击"设置"按钮
2. 输入您的 Claude API Key
3. 保存设置

### Q: API Key 在哪里获取？

**A**: 访问 [Anthropic Console](https://console.anthropic.com/) 注册并获取 API Key。

### Q: 代码生成失败？

**A**: 可能的原因：
1. API Key 无效或过期
2. 网络连接问题
3. API 配额已用完
4. 输入描述不清晰

请检查：
- API Key 是否正确
- 网络连接是否正常
- 代码描述是否清晰

### Q: 生成的代码质量不高？

**A**: 尝试：
1. 提供更详细的描述
2. 调整温度参数
3. 尝试不同的模型（如 Claude 3 Opus）
4. 明确指定代码要求

## 文件结构

```
claude-code-generator/
├── main.py              # 应用入口
├── requirements.txt     # 依赖列表
├── README.md           # 项目说明
├── INSTALL.md          # 本文档
├── config/             # 配置管理
│   ├── constants.py    # 常量定义
│   └── settings.py     # 设置管理
├── core/               # 核心逻辑
│   ├── claude_api.py   # Claude API 客户端
│   └── code_generator.py # 代码生成器
├── ui/                 # 用户界面
│   ├── main_window.py  # 主窗口
│   ├── code_input_panel.py  # 输入面板
│   ├── output_panel.py # 输出面板
│   ├── settings_dialog.py   # 设置对话框
│   └── styles.py       # UI 样式
├── utils/              # 工具函数
│   ├── security.py     # 加密/解密
│   ├── logger.py       # 日志
│   ├── validators.py   # 验证
│   └── file_handler.py # 文件处理
├── data/               # 运行时数据
│   ├── config.json     # 配置文件（加密）
│   ├── conversations/  # 对话历史
│   └── logs/           # 日志文件
└── assets/             # 资源文件
    └── icons/          # 图标
```

## 安全性说明

- **API Key 加密**: 您的 API Key 使用 Windows DPAPI 加密存储，仅当前 Windows 用户可以解密
- **本地存储**: 所有配置和对话历史都存储在本地，不会上传到第三方服务器
- **日志保护**: 日志文件不包含敏感信息（如 API Key）

## 高级功能

### 打包成 EXE

如果您想将应用打包成独立的可执行文件：

1. 安装 PyInstaller：
```bash
pip install pyinstaller
```

2. 运行打包命令：
```bash
pyinstaller --onefile --windowed --icon=assets/icons/app_icon.ico --add-data "assets;assets" --name "ClaudeCodeGenerator" main.py
```

3. 打包完成后，EXE 文件位于 `dist/` 目录

### 自定义主题

您可以通过修改 `ui/styles.py` 中的颜色配置来自定义主题。

## 技术支持

如果您遇到问题或有建议：

1. 查看 `data/logs/` 目录中的日志文件
2. 检查 API Key 是否有效
3. 确认网络连接正常
4. 尝试重新安装依赖

## 许可证

MIT License

## 致谢

- Claude API by Anthropic
- CustomTkinter
- Pygments（语法高亮）
