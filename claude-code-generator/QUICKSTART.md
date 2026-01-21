# Claude Code Generator - 快速开始

## 🚀 5 分钟快速上手

### 第一步：安装依赖

打开命令提示符，进入项目目录并运行：

```bash
cd e:\coding\claude-code-generator
pip install -r requirements.txt
```

或者双击 `run.bat` 文件，它会自动检查并安装依赖。

### 第二步：获取 API Key

1. 访问 [https://console.anthropic.com/](https://console.anthropic.com/)
2. 注册并登录
3. 创建 API Key
4. 复制您的 API Key（格式：`sk-ant-...`）

### 第三步：启动应用

```bash
python main.py
```

或双击 `run.bat`

### 第四步：配置应用

1. 启动后，点击菜单栏的"设置"
2. 粘贴您的 API Key
3. 点击"保存"

### 第五步：生成代码

1. 在左侧输入框描述您需要的代码
2. 选择编程语言
3. 点击"生成代码"

## 📝 示例

### 示例 1：生成 Python 函数

**输入**:
```
创建一个 Python 函数计算斐波那契数列的第 n 项
要求使用递归实现，添加注释
```

**语言**: Python

点击"生成代码"，您将获得：

```python
def fibonacci(n):
    """
    计算斐波那契数列的第 n 项

    Args:
        n: 要计算的项数（从0开始）

    Returns:
        斐波那契数列的第 n 项
    """
    # 处理边界情况
    if n < 0:
        raise ValueError("n 必须是非负整数")
    if n == 0:
        return 0
    if n == 1:
        return 1

    # 递归计算
    return fibonacci(n - 1) + fibonacci(n - 2)

# 示例用法
if __name__ == "__main__":
    for i in range(10):
        print(f"F({i}) = {fibonacci(i)}")
```

### 示例 2：生成 REST API

**输入**:
```
创建一个 Python Flask REST API 端点，实现用户注册功能
包括：用户名、密码、邮箱验证
```

**语言**: Python

您将获得完整的 Flask API 实现！

### 示例 3：生成算法

**输入**:
```
用 Python 实现快速排序算法
要求：原地排序、包含测试用例
```

**语言**: Python

## 💡 使用技巧

### 1. 详细的描述 = 更好的结果

❌ 不好的描述：
```
排序
```

✅ 好的描述：
```
用 Python 实现快速排序算法
要求：
- 使用递归方式
- 原地排序（不需要额外空间）
- 添加详细注释
- 包含测试用例
```

### 2. 使用模板

应用提供了 5 个快速模板：
- **函数**: 快速创建函数
- **类**: 创建类定义
- **算法**: 实现算法
- **API**: 创建 API 端点
- **数据处理**: 数据处理逻辑

点击模板按钮可以快速应用对应的提示词格式。

### 3. 调整参数

在设置中：
- **温度 0.3-0.5**: 更稳定的输出
- **温度 0.7-1.0**: 更有创意的输出（推荐）
- **温度 1.0-2.0**: 非常有创意但可能不稳定

### 4. 选择合适的模型

- **Claude 3.5 Sonnet**: 日常使用，平衡速度和质量（推荐）
- **Claude 3 Opus**: 复杂任务，最高质量
- **Claude 3 Haiku**: 简单任务，最快速度

## 🔧 常见问题

### Q: 如何获取免费 API Key？

A: 访问 [Anthropic Console](https://console.anthropic.com/)，新用户通常有免费额度。

### Q: 生成的代码可以直接使用吗？

A: 是的，但建议：
1. 检查代码逻辑
2. 添加必要的错误处理
3. 根据实际需求调整
4. 编写测试用例

### Q: 可以生成其他编程语言的代码吗？

A: 可以！应用支持多种语言：
- Python, JavaScript, TypeScript
- Java, C++, C#, Go, Rust
- PHP, Ruby, Swift, Kotlin
- HTML/CSS, SQL, Shell 等

### Q: 如何保存生成的代码？

A: 两种方式：
1. 点击"复制"按钮，粘贴到您的编辑器
2. 点击"保存"按钮，保存为文件

## 📚 更多信息

- 详细安装说明：查看 [INSTALL.md](INSTALL.md)
- 项目介绍：查看 [README.md](README.md)
- API 文档：[Anthropic Documentation](https://docs.anthropic.com/)

## 🎉 开始使用

现在您已经准备好了！运行应用并开始生成代码吧！

```bash
python main.py
```

祝您使用愉快！🚀
