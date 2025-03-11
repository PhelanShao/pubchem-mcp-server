from mcp.server.fastmcp import FastMCP
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
import csv
from io import StringIO
import logging
import os
from rdkit import Chem
from rdkit.Chem import AllChem
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 初始化 MCP 服务器并声明依赖
mcp = FastMCP("PubChem MCP Server", dependencies=["requests", "rdkit"])

# 全局缓存字典：存储查询结果 { key: 数据字典 }
cache_data = {}
# 结构文件缓存目录
CACHE_DIR = "structure_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None):
    """创建具有重试功能的请求会话"""
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def download_sdf_with_hydrogens(cid, session=None):
    """下载化合物的3D结构SDF文件"""
    if session is None:
        session = requests_retry_session()
    
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/record/SDF/?record_type=3d&response_type=display&display_type=sdf"
    try:
        response = session.get(url, timeout=30)
        if response.status_code == 200:
            return response.text
        elif response.status_code == 404:
            logging.warning(f"CID {cid} not found (404 error)")
            return None
        else:
            logging.error(f"Failed to download SDF for CID: {cid}. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading SDF for CID: {cid}. Error: {e}")
        return None

def sdf_to_xyz(sdf_content, cid, metadata=None):
    """将SDF内容转换为XYZ格式"""
    if sdf_content is None:
        return None
        
    mol = Chem.MolFromMolBlock(sdf_content, removeHs=False)
    if mol is None:
        logging.error(f"Failed to create RDKit mol object for CID: {cid}")
        return None
    
    has_hydrogens = any(atom.GetAtomicNum() == 1 for atom in mol.GetAtoms())
    if not has_hydrogens:
        logging.warning(f"No hydrogen atoms found in the structure for CID: {cid}")
        mol = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol, randomSeed=42)
        AllChem.MMFFOptimizeMolecule(mol)
    
    conf = mol.GetConformer()
    xyz_content = f"{mol.GetNumAtoms()}\n"
    
    # 添加元数据到注释行
    if metadata:
        metadata_str = " ".join([f"{k}={v}" for k, v in metadata.items()])
        xyz_content += f"{metadata_str}\n"
    else:
        xyz_content += f"cid={cid}\n"
    
    for i in range(mol.GetNumAtoms()):
        atom = mol.GetAtomWithIdx(i)
        pos = conf.GetAtomPosition(i)
        xyz_content += f"{atom.GetSymbol()} {pos.x:.4f} {pos.y:.4f} {pos.z:.4f}\n"
    
    return xyz_content

@mcp.tool()
def get_pubchem_data(query: str, format: str = "JSON", include_3d: bool = False) -> str:
    """通过 PubChem API 获取指定化合物的结构和属性数据。
    
    参数:
        query: 化合物名称或 PubChem CID 标识符。
        format: 返回格式，可选 "JSON"、"CSV" 或 "XYZ"（默认 "JSON"）。
        include_3d: 是否包含3D结构信息（仅当format为"XYZ"时有效）。
    返回:
        包含化合物结构及属性的字符串，格式由 format 参数决定。
    """
    logging.info(f"接收到查询请求: query={query}, format={format}, include_3d={include_3d}")
    
    # 规范化查询关键字作为缓存键
    if query is None or query.strip() == "":
        return "Error: query cannot be empty."
    query_str = query.strip()
    
    # 判断是名称查询还是CID查询
    if query_str.isdigit():
        cache_key = f"cid:{query_str}"
        identifier_path = f"cid/{query_str}"
        cid = query_str
    else:
        cache_key = f"name:{query_str.lower()}"
        # 对名称进行URL编码（处理空格等特殊字符）
        identifier_path = f"name/{requests.utils.requote_uri(query_str)}"
        cid = None  # 稍后从API响应中获取
    
    logging.info(f"查询路径: {identifier_path}")
    
    # 如果缓存中已有结果，直接返回指定格式的数据
    if cache_key in cache_data:
        logging.info("从缓存中获取数据")
        data = cache_data[cache_key]
        if cid is None:
            cid = data.get("CID", "")
            if not cid:
                error_msg = "Error: Could not find CID in cached data"
                logging.error(error_msg)
                return error_msg
    else:
        # 调用 PubChem PUG REST 接口获取属性数据（JSON格式）
        session = requests_retry_session()
        properties = ["IUPACName", "MolecularFormula", "MolecularWeight", "CanonicalSMILES", "InChI", "InChIKey"]
        properties_str = ",".join(properties)
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/{identifier_path}/property/{properties_str}/JSON"
        logging.info(f"请求 PubChem API: {url}")
        
        try:
            res = session.get(url, timeout=10)
            logging.info(f"API响应状态码: {res.status_code}")
        except Exception as e:
            error_msg = f"Error: failed to connect to PubChem ({e})"
            logging.error(error_msg)
            return error_msg
            
        if res.status_code != 200:
            error_text = res.text if res.text else "No error details"
            error_msg = f"Error: PubChem API returned status {res.status_code}. Details: {error_text}"
            logging.error(error_msg)
            return error_msg
            
        # 解析返回的JSON数据
        result_json = res.json()
        props_list = result_json.get("PropertyTable", {}).get("Properties", [])
        if not props_list:
            error_msg = "Error: compound not found or no data available."
            logging.error(error_msg)
            return error_msg
            
        comp = props_list[0]  # 取第一个化合物的数据
        logging.info("成功获取化合物数据")
        
        # 如果是通过名称查询，获取CID
        if cid is None:
            cid = str(comp.get("CID", ""))
            if not cid:
                error_msg = "Error: Could not find CID in the response"
                logging.error(error_msg)
                return error_msg
        
        # 提取需要的字段，若缺失则以空字符串代替
        field_mapping = {
            "IUPACName": "IUPACName",
            "MolecularFormula": "MolecularFormula",
            "MolecularWeight": "MolecularWeight",
            "CanonicalSMILES": "CanonicalSMILES",
            "InChI": "InChI",
            "InChIKey": "InChIKey",
            "CID": "CID"
        }
        data = {k: str(comp.get(v, "")) for k, v in field_mapping.items()}
        
        # 缓存结果
        cache_data[cache_key] = data
        if cid and f"cid:{cid}" not in cache_data:
            cache_data[f"cid:{cid}"] = data
    
    # 根据请求的格式返回数据
    fmt = format.strip().upper()
    if fmt == "XYZ" and include_3d:
        # 检查是否已经缓存了XYZ文件
        xyz_cache_path = os.path.join(CACHE_DIR, f"{cid}.xyz")
        if os.path.exists(xyz_cache_path):
            logging.info(f"从缓存读取XYZ文件: {xyz_cache_path}")
            with open(xyz_cache_path, 'r') as f:
                return f.read()
        
        # 下载并转换结构
        logging.info(f"下载3D结构数据: CID={cid}")
        sdf_content = download_sdf_with_hydrogens(cid)
        if sdf_content:
            metadata = {
                "cid": cid,
                "iupac_name": data["IUPACName"],
                "formula": data["MolecularFormula"],
                "smiles": data["CanonicalSMILES"]
            }
            xyz_content = sdf_to_xyz(sdf_content, cid, metadata)
            if xyz_content:
                # 缓存XYZ文件
                with open(xyz_cache_path, 'w') as f:
                    f.write(xyz_content)
                return xyz_content
            else:
                return "Error: Failed to convert structure to XYZ format"
        else:
            return "Error: Failed to download 3D structure"
    elif fmt == "CSV":
        # 使用CSV模块将数据字典转换为CSV字符串
        output = StringIO()
        writer = csv.writer(output)
        # 写入表头和单行数据
        headers = ["CID", "IUPACName", "MolecularFormula", "MolecularWeight", 
                   "CanonicalSMILES", "InChI", "InChIKey"]
        writer.writerow(headers)
        writer.writerow([data.get(h, "") for h in headers])
        result = output.getvalue().strip()  # strip去除末尾换行符
    else:
        # 缺省输出 JSON 字符串
        result = json.dumps(data, ensure_ascii=False)
    
    logging.info("数据处理完成，准备返回结果")
    return result

# 启动 MCP 服务器（供 LLM 客户端连接调用）
if __name__ == "__main__":
    logging.info("启动 PubChem MCP 服务器...")
    mcp.run()
