# PubChem MCP服务器安装指南

本文档提供了PubChem MCP服务器的详细安装和配置说明。

## 系统要求

- Python 3.8+
- PIP包管理器
- Git (可选，用于克隆仓库)

## 安装方法

### 1. 准备环境

首先，确保您有Python 3.8或更高版本：

```bash
python --version
# 或
python3 --version
```

建议创建一个虚拟环境来安装依赖：

```bash
# 创建虚拟环境
python -m venv pubchem-env

# 激活虚拟环境
# Windows
pubchem-env\Scripts\activate
# macOS/Linux
source pubchem-env/bin/activate
```

### 2. 安装依赖

有两种方式可以安装依赖：

#### A. 使用MCP SDK（推荐）

如果您已经安装了MCP SDK，可以直接使用：

```bash
pip install httpx
```

#### B. 使用项目内的Python SDK

如果您没有安装MCP SDK，项目内已包含SDK源码：

```bash
# 无需额外操作，服务器会自动使用项目内的SDK
# 仅安装HTTP客户端库
pip install httpx
```

### 3. 运行服务器

启动PubChem MCP服务器：

```bash
python pubchem_server.py
```

如果一切正常，您应该会看到类似以下的输出：

```
INFO - pubchem-mcp - 启动PubChem MCP服务器...
```

服务器会在前台运行并等待连接。保持此终端窗口打开。

### 4. 测试服务器

在另一个终端窗口中，运行测试脚本来验证服务器是否正常工作：

```bash
# 激活相同的虚拟环境（如果使用）
source pubchem-env/bin/activate  # 或Windows对应命令

# 运行测试脚本
python test_pubchem_server.py
```

## 与Claude集成

要将PubChem MCP服务器与Claude Desktop集成，请按照以下步骤操作：

### Claude Desktop配置（macOS/Linux）

1. 打开Claude Desktop应用程序
2. 找到配置文件：
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

3. 编辑配置文件，添加PubChem MCP服务器：

```json
{
  "mcpServers": {
    "pubchem": {
      "command": "python",
      "args": ["/完整路径/到/pubchem_server.py"],
      "disabled": false
    }
  }
}
```

请确保用实际的完整路径替换`/完整路径/到/pubchem_server.py`。

4. 保存配置文件并重启Claude Desktop。

### 验证集成

1. 在Claude中，您可以问类似以下的问题来测试集成：
   - "什么是阿司匹林的分子结构？"
   - "给我展示乙醇的化学特性"
   - "CCO这个SMILES代表什么化合物？"

2. Claude应该能够使用PubChem MCP服务器查询这些信息并返回答案。

## 故障排除

### 常见问题

1. **找不到MCP模块**
   - 确保MCP SDK已安装或python-sdk目录在正确位置
   - 尝试使用完整路径运行服务器

2. **服务器启动但测试脚本无法连接**
   - 确保两个终端窗口使用相同的Python环境
   - 检查是否有防火墙阻止本地连接

3. **Claude无法找到MCP服务器**
   - 检查配置文件路径是否正确
   - 确保服务器路径使用的是绝对路径而非相对路径
   - 重启Claude Desktop并查看日志是否有错误

如有其他问题，请查阅MCP文档或提交问题报告。

## 高级配置

### 自定义服务器端口

默认情况下，服务器使用标准MCP协议通过标准输入/输出(stdio)进行通信。您无需指定端口。

### 缓存配置

服务器默认缓存设置：
- 最大缓存条目数：1000
- 缓存有效期：24小时

如需自定义这些设置，请修改`pubchem_server.py`中的相关参数。