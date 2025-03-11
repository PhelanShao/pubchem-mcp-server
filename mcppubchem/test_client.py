
from mcp.server.fastmcp import FastMCP
import requests, json, csv
from io import StringIO

# 初始化 MCP 服务器并声明依赖
mcp = FastMCP("PubChem MCP Server", dependencies=["requests"])

# 全局缓存字典：存储查询结果 { key: 数据字典 }
cache_data = {}

@mcp.tool()
def get_pubchem_data(query: str, format: str = "JSON") -> str:
    """通过 PubChem API 获取指定化合物的结构和属性数据。
    
    参数:
        query: 化合物名称或 PubChem CID 标识符。
        format: 返回格式，可选 "JSON" 或 "CSV"（默认 "JSON"）。
    返回:
        包含化合物结构及属性的字符串，格式由 format 参数决定。
    """
    # 规范化查询关键字作为缓存键
    if query is None or query.strip() == "":
        return "Error: query cannot be empty."
    query_str = query.strip()
    # 判断是名称查询还是CID查询
    if query_str.isdigit():
        cache_key = f"cid:{query_str}"
        identifier_path = f"cid/{query_str}"
    else:
        cache_key = f"name:{query_str.lower()}"
        # 对名称进行URL编码（处理空格等特殊字符）
        identifier_path = f"name/{requests.utils.requote_uri(query_str)}"
    # 如果缓存中已有结果，直接返回指定格式的数据
    if cache_key in cache_data:
        data = cache_data[cache_key]
    else:
        # 调用 PubChem PUG REST 接口获取属性数据（JSON格式）
        properties = "CID,MolecularFormula,MolecularWeight,CanonicalSMILES,InChIKey,IUPACName"
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/{identifier_path}/property/{properties}/JSON"
        try:
            res = requests.get(url, timeout=10)
        except Exception as e:
            return f"Error: failed to connect to PubChem ({e})"
        if res.status_code != 200:
            error_text = res.text if res.text else "No error details"
            return f"Error: PubChem API returned status {res.status_code}. Details: {error_text}"
        # 解析返回的JSON数据
        result_json = res.json()
        props_list = result_json.get("PropertyTable", {}).get("Properties", [])
        if not props_list:
            return "Error: compound not found or no data available."
        comp = props_list[0]  # 取第一个化合物的数据
        # 提取需要的字段，若缺失则以空字符串代替
        fields = ["CID", "MolecularFormula", "MolecularWeight", 
                  "CanonicalSMILES", "InChIKey", "IUPACName"]
        data = {f: (comp[f] if f in comp else "") for f in fields}
        # 缓存结果（名称查询也缓存对应CID，方便下次直接用CID查询）
        cache_data[cache_key] = data
        cid_val = str(data.get("CID", "")).strip()
        if cid_val and f"cid:{cid_val}" not in cache_data:
            cache_data[f"cid:{cid_val}"] = data
    # 根据请求的格式返回数据
    fmt = format.strip().upper()
    if fmt == "CSV":
        # 使用CSV模块将数据字典转换为CSV字符串
        output = StringIO()
        writer = csv.writer(output)
        # 写入表头和单行数据
        headers = ["CID", "MolecularFormula", "MolecularWeight", 
                   "CanonicalSMILES", "InChIKey", "IUPACName"]
        writer.writerow(headers)
        writer.writerow([data.get(h, "") for h in headers])
        return output.getvalue().strip()  # strip去除末尾换行符
    else:
        # 缺省输出 JSON 字符串
        return json.dumps(data, ensure_ascii=False)

# 启动 MCP 服务器（供 LLM 客户端连接调用）
if __name__ == "__main__":
    mcp.run()
