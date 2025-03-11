# PubChem MCP服务器安装指南

## 前提条件

- Python >= 3.8
- pip

## 安装步骤

1. 首先安装MCP SDK：
```bash
# 进入python-sdk目录
cd python-sdk

# 安装SDK
pip install -e .
```

2. 然后安装PubChem MCP服务器：
```bash
# 返回项目根目录
cd ..

# 安装服务器
pip install -e .
```

## 验证安装

安装完成后，可以运行以下命令验证安装是否成功：

```bash
# 运行服务器
pubchem-mcp

# 或通过Python模块运行
python -m pubchem_mcp.server
```

## 常见问题

### 1. 找不到mcp-sdk包

如果遇到错误：
```
ERROR: Could not find a version that satisfies the requirement mcp-sdk>=0.1.0
```

请确保已经按照步骤1安装了MCP SDK。

### 2. 导入错误

如果遇到导入错误，请检查：
- Python版本是否 >= 3.8
- MCP SDK是否正确安装
- 是否在正确的目录下安装

### 3. 权限问题

如果遇到权限错误，可以：
- 使用虚拟环境
- 添加--user参数：`pip install --user -e .`

## 卸载

要卸载服务器和SDK：

```bash
pip uninstall pubchem-mcp
pip uninstall mcp-sdk