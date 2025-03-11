# PubChem MCP服务器

PubChem MCP服务器是一个基于Model Context Protocol (MCP)的服务器，它使大语言模型（如Claude）能够顺畅地访问PubChem API，获取化学结构和分子属性数据。

## 主要功能

- **多方式搜索**：支持通过化合物名称、分子式、SMILES表示法等搜索化合物
- **结构获取**：支持获取化合物的多种结构格式（SDF、XYZ、CIF、PDB、MOL）
- **属性获取**：获取化合物的物理化学特性
- **灵活输出**：支持JSON和CSV格式输出
- **内置缓存**：减少重复API调用，加快响应速度
- **速率限制**：遵循PubChem API使用政策（每秒最多5个请求）

## 安装

```bash
# 从源代码安装
git clone https://github.com/roo-ai/pubchem-mcp.git
cd pubchem-mcp
pip install -e .

# 或直接通过pip安装
pip install pubchem-mcp
```

## 使用方法

### 作为MCP服务器运行

```bash
# 直接运行
pubchem-mcp

# 或通过Python模块运行
python -m pubchem_mcp.server
```

### 在Python代码中使用

```python
from pubchem_mcp import PubChemMCPServer

# 创建服务器实例
server = PubChemMCPServer()

# 搜索化合物
result = await server.search_chemical_by_name("aspirin")

# 获取结构文件
structure = await server.get_structure_file(2244, output_format="xyz")

# 获取化合物属性
compound = await server.get_compound_by_cid(2244)
```

## MCP工具

服务器提供以下MCP工具：

1. `search_chemical_by_name`
   - 通过化学名称搜索化合物
   - 参数：
     - name: 化学名称(如"aspirin")
     - max_results: 最大返回结果数(默认1)
     - output_format: 输出格式(json/csv)

2. `search_chemical_by_formula`
   - 通过分子式搜索化合物
   - 参数：
     - formula: 分子式(如"C9H8O4")
     - max_results: 最大返回结果数(默认1)
     - output_format: 输出格式(json/csv)

3. `search_chemical_by_smiles`
   - 通过SMILES表示法搜索化合物
   - 参数：
     - smiles: SMILES字符串
     - max_results: 最大返回结果数(默认1)
     - output_format: 输出格式(json/csv)

4. `get_compound_by_cid`
   - 通过PubChem CID获取化合物详情
   - 参数：
     - cid: PubChem化合物ID
     - output_format: 输出格式(json/csv)

5. `get_structure_file`
   - 获取化合物结构文件
   - 参数：
     - cid: PubChem化合物ID
     - output_format: 结构格式(sdf/xyz/cif/pdb/mol)
     - as_3d: 是否获取3D结构(默认True)

## 示例

### 在Claude中使用

```python
# 搜索阿司匹林
Assistant: 让我帮你搜索阿司匹林的化学结构。
Human: 使用工具: search_chemical_by_name name=aspirin output_format=json
Assistant: 找到了阿司匹林的信息，它的分子式是C9H8O4，我来获取它的3D结构。
Human: 使用工具: get_structure_file cid=2244 output_format=xyz
Assistant: 这是阿司匹林的3D结构坐标...
```

## 开发指南

### 添加新功能

1. 在相应模块中实现功能
2. 在server.py中添加MCP工具
3. 更新文档和测试

### 运行测试

```bash
python -m pytest tests/
```

## 许可证

MIT License
