@echo off
REM Claude Code Generator 启动脚本

echo ========================================
echo   Claude Code Generator
echo   启动中...
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到 Python
    echo 请先安装 Python 3.8 或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查依赖是否安装
echo 检查依赖...
python -c "import customtkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo 依赖未安装，正在安装...
    echo.
    python -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo.
        echo 错误: 依赖安装失败
        echo 请手动运行: pip install -r requirements.txt
        pause
        exit /b 1
    )
    echo.
    echo 依赖安装完成！
    echo.
)

REM 启动应用
echo 正在启动应用...
echo.
python main.py

REM 如果应用异常退出
if %errorlevel% neq 0 (
    echo.
    echo 应用异常退出，错误代码: %errorlevel%
    pause
)
