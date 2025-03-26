# PubChem MCP 服务器异步请求功能

## 介绍

PubChem MCP 服务器现在支持异步请求处理，解决了某些查询导致的 "MCP error -2: Request timed out" 问题。新功能通过请求中转机制实现，允许长时间运行的查询在后台处理，同时向用户提供实时状态更新。

## 工作原理

异步请求处理采用以下流程：

1. 客户端发起异步请求并立即获得请求ID
2. 请求在服务器后台线程中处理
3. 客户端使用请求ID定期查询请求状态
4. 请求完成后，客户端可获取完整结果

## 新增工具

此更新添加了两个新的MCP工具：

### 1. submit_pubchem_request

异步提交PubChem数据请求。

**参数：**
- `query`: 化合物名称或PubChem CID
- `format`: 输出格式，选项包括 "JSON"（默认）、"CSV" 或 "XYZ"
- `include_3d`: 是否包含3D结构信息（仅当format为"XYZ"时有效），默认为false

**返回：**
包含请求ID的JSON对象，可用于查询请求状态。

**示例：**
```json
{
  "request_id": "d8e8fca2-dc2f-4a9d-8e17-75990a7842e1",
  "message": "Request submitted successfully. Use get_request_status with this request_id to check the status."
}
```

### 2. get_request_status

查询异步请求的状态。

**参数：**
- `request_id`: 从submit_pubchem_request获得的请求ID

**返回：**
包含请求状态信息的JSON对象，包括：
- 基本请求信息（ID、查询、格式等）
- 当前状态（pending、processing、completed、failed）
- 如果已完成，包含结果数据
- 如果失败，包含错误信息

**示例响应（处理中）：**
```json
{
  "request_id": "d8e8fca2-dc2f-4a9d-8e17-75990a7842e1",
  "query": "aspirin",
  "format": "JSON",
  "include_3d": false,
  "status": "processing",
  "created_at": 1647945600.123,
  "updated_at": 1647945601.456,
  "result": null,
  "error": null
}
```

**示例响应（已完成）：**
```json
{
  "request_id": "d8e8fca2-dc2f-4a9d-8e17-75990a7842e1",
  "query": "aspirin",
  "format": "JSON",
  "include_3d": false,
  "status": "completed",
  "created_at": 1647945600.123,
  "updated_at": 1647945605.789,
  "result": "{\"CID\":\"2244\",\"IUPACName\":\"2-acetoxybenzoic acid\",\"MolecularFormula\":\"C9H8O4\",\"MolecularWeight\":\"180.16\",\"CanonicalSMILES\":\"CC(=O)OC1=CC=CC=C1C(=O)O\",\"InChI\":\"InChI=1S/C9H8O4/c1-6(10)13-8-5-3-2-4-7(8)9(11)12/h2-5H,1H3,(H,11,12)\",\"InChIKey\":\"BSYNRYMUTXBXSQ-UHFFFAOYSA-N\"}",
  "error": null
}
```

## 使用示例

以下是在客户端使用异步请求功能的典型流程：

1. 提交异步请求：
```python
request_id = client.call_tool("submit_pubchem_request", {"query": "aspirin", "format": "JSON"})["request_id"]
```

2. 定期查询状态直到完成：
```python
while True:
    status = client.call_tool("get_request_status", {"request_id": request_id})
    if status["status"] in ["completed", "failed"]:
        break
    time.sleep(1)  # 等待一秒后再次查询

if status["status"] == "completed":
    result = status["result"]
    # 处理结果...
else:
    error = status["error"]
    # 处理错误...
```

## 技术说明

异步处理器模块使用Python的ThreadPoolExecutor在后台线程中处理请求，同时维护请求状态信息。所有已完成的请求状态会保存一段时间（默认1小时）供客户端查询，然后自动清理以防止内存泄漏。

此实现确保MCP服务器能够快速响应请求，而不会因为长时间运行的PubChem API调用而超时。
