#!/bin/bash
# 启动PubChem MCP服务器的脚本 (Linux/macOS)

echo "启动PubChem MCP服务器..."

# 检查Python是否可用
if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
elif command -v python &>/dev/null; then
    PYTHON_CMD=python
else
    echo "错误: 找不到Python。请确保Python已安装且在PATH中。"
    exit 1
fi

# 检查版本
PY_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
if (( $(echo "$PY_VERSION < 3.8" | bc -l) )); then
    echo "错误: 需要Python 3.8或更高版本。当前版本: $PY_VERSION"
    exit 1
fi

# 检查httpx库
if ! $PYTHON_CMD -c "import httpx" &>/dev/null; then
    echo "警告: 未找到httpx库。尝试安装..."
    $PYTHON_CMD -m pip install httpx
    if [ $? -ne 0 ]; then
        echo "错误: 无法安装httpx库。请手动安装: pip install httpx"
        exit 1
    fi
fi

# 启动服务器
echo "启动PubChem MCP服务器..."
$PYTHON_CMD pubchem_server.py

# 如果服务器异常退出，等待按键继续
echo "服务器已退出。按任意键继续..."
read -n 1 -s