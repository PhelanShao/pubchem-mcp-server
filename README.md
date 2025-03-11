# PubChem MCP Server

一个用于获取PubChem化合物数据的Model Context Protocol (MCP) 服务器。

## 功能特点

- 支持通过化合物名称或CID查询
- 提供多种输出格式：JSON、CSV、XYZ
- 支持3D结构数据获取和转换
- 本地缓存系统，减少API调用
- 自动重试机制，提高可靠性

## 安装

```bash
npm install -g @modelcontextprotocol/server-pubchem
```

## 配置

在你的MCP配置文件中添加以下配置：

```json
{
  "mcpServers": {
    "pubchem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-pubchem"]
    }
  }
}
```

## 使用方法

服务器提供以下工具：

### get_pubchem_data

获取化合物的结构和属性数据。

参数：
- `query`: (必需) 化合物名称或PubChem CID
- `format`: (可选) 输出格式，可选 "JSON"、"CSV" 或 "XYZ"，默认为 "JSON"
- `include_3d`: (可选) 是否包含3D结构信息（仅当format为"XYZ"时有效），默认为 false

示例：

```python
# 获取JSON格式数据
result = await session.call_tool("get_pubchem_data", {
    "query": "aspirin"
})

# 获取CSV格式数据
result = await session.call_tool("get_pubchem_data", {
    "query": "aspirin",
    "format": "CSV"
})

# 获取XYZ格式的3D结构数据
result = await session.call_tool("get_pubchem_data", {
    "query": "aspirin",
    "format": "XYZ",
    "include_3d": True
})
```

## 缓存

- 属性数据缓存在内存中
- 3D结构数据（XYZ格式）缓存在 `~/.pubchem-mcp/cache` 目录下
- 缓存文件名格式为 `[CID].xyz`

## 依赖

- @modelcontextprotocol/sdk
- axios
- rdkit-js

## 开发

```bash
# 安装依赖
npm install

# 构建
npm run build

# 运行测试
npm test
```

## 许可证

MIT
