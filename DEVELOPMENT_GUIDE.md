# PubChem MCP服务器开发指南

## 项目概述

PubChem MCP服务器是一个基于Model Context Protocol (MCP)的服务器，它使大语言模型（如Claude）能够顺畅地访问PubChem API，获取化学结构和分子属性数据。该服务器作为Claude和PubChem数据库之间的桥梁，允许Claude在对话中检索、展示和分析化学数据。

## 开发进度

### 已完成工作

1. **代码重构（2025-03-11）**
   - 将代码重构为模块化结构
   - 创建了独立的功能模块
   - 改进了错误处理和日志记录
   - 优化了缓存系统
   - 增强了速率限制器

2. **核心功能实现**
   - 支持多种搜索方式
   - 支持多种结构格式
   - 实现缓存系统
   - 实现速率限制
   - 支持JSON/CSV输出

3. **文档完善**
   - 创建了详细的README
   - 更新了开发指南
   - 添加了示例代码

### 当前项目结构

```
pubchem-mcp/
├── pubchem_mcp/
│   ├── __init__.py
│   ├── server.py
│   ├── api/
│   │   └── pubchem.py
│   ├── cache/
│   │   └── memory_cache.py
│   ├── utils/
│   │   └── rate_limiter.py
│   ├── models/
│   │   └── compound.py
│   └── converters/
│       └── structure.py
├── setup.py
└── README.md
```

### 后续开发计划

1. **短期目标**
   - [x] 重构代码结构
   - [x] 增强错误处理
   - [x] 扩展缓存系统
   - [ ] 添加文件系统缓存
   - [ ] 添加缓存管理工具

2. **中期目标**
   - [ ] 添加毒理学数据支持
   - [ ] 添加生物活性数据支持
   - [ ] 实现高级结构搜索
   - [ ] 添加分子可视化支持
   - [ ] 改进批量操作性能

3. **长期目标**
   - [ ] 添加化合物比较功能
   - [ ] 集成QSAR模型
   - [ ] 添加其他数据源支持
   - [ ] 实现高级搜索算法
   - [ ] 添加机器学习功能

## 技术细节

### 模块说明

1. **api/pubchem.py**
   - PubChem API访问实现
   - 请求速率限制
   - 错误处理和重试

2. **cache/memory_cache.py**
   - 内存缓存实现
   - 缓存统计
   - 过期管理

3. **utils/rate_limiter.py**
   - 速率限制实现
   - 统计和监控
   - 异步等待

4. **models/compound.py**
   - 化合物数据模型
   - 属性定义
   - 序列化支持

5. **converters/structure.py**
   - 结构格式转换
   - 支持多种格式
   - 错误处理

### API使用

服务器使用PubChem的REST API（PUG REST）：
- 主要端点：`https://pubchem.ncbi.nlm.nih.gov/rest/pug`
- 速率限制：每秒5个请求
- 支持的搜索方式：名称、分子式、SMILES等
- 支持的结构格式：SDF、XYZ、CIF、PDB、MOL

### 缓存系统

- 默认使用内存缓存
- 缓存条目上限：1000
- 缓存有效期：24小时
- 支持缓存统计和管理
- 计划添加文件系统缓存支持

### MCP集成

- 支持FastMCP和低级API两种实现
- 自动检测可用的MCP库
- 提供5个核心工具：
  1. search_chemical_by_name
  2. search_chemical_by_formula
  3. search_chemical_by_smiles
  4. get_compound_by_cid
  5. get_structure_file

## 贡献指南

1. 代码风格
   - 使用Python类型注解
   - 遵循PEP 8规范
   - 添加详细的文档字符串
   - 使用异步编程

2. 提交流程
   - 创建功能分支
   - 添加测试用例
   - 更新文档
   - 提交PR

3. 测试要求
   - 单元测试覆盖率 > 80%
   - 包含集成测试
   - 测试异常情况
   - 测试性能影响

## 结论

PubChem MCP服务器现在具有更好的代码结构和更强大的功能。通过持续的开发和改进，我们将使其成为连接大语言模型和化学数据的重要工具。