# Claude Code Generator

一个基于 Claude API 的 AI 代码生成器，专为 Windows 11 设计。

## 功能特性

- 🎨 现代化 Windows 11 风格界面
- 🤖 使用 Claude 3.5 Sonnet/Opus 生成代码
- 🌍 支持多种编程语言
- ✨ 语法高亮显示
- 🔒 API Key 安全加密存储
- 🌙 深色/浅色主题
- 📝 对话历史管理
- ⚡ 流式响应实时显示

## 安装

### 1. 克隆项目

```bash
git clone <repository-url>
cd claude-code-generator
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行应用

```bash
python main.py
```

## 使用说明

### 首次使用

1. 启动应用后，点击"设置"按钮
2. 输入您的 Claude API Key（从 [Anthropic Console](https://console.anthropic.com/) 获取）
3. 选择默认模型和主题
4. 保存设置

### 生成代码

1. 在输入框中描述您需要的代码
2. 选择目标编程语言
3. 点击"生成代码"按钮
4. 等待代码生成完成
5. 使用"复制"或"保存"按钮获取代码

## 技术栈

- **GUI**: CustomTkinter
- **API**: Anthropic Claude API
- **安全**: Windows DPAPI
- **语法高亮**: Pygments

## 项目结构

```
claude-code-generator/
├── main.py              # 应用入口
├── config/              # 配置管理
├── ui/                  # 用户界面
├── core/                # 核心逻辑
├── utils/               # 工具函数
├── assets/              # 资源文件
└── data/                # 运行时数据
```

## 打包

使用 PyInstaller 打包成 EXE：

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=assets/icons/app_icon.ico --add-data "assets;assets" --name "ClaudeCodeGenerator" main.py
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
