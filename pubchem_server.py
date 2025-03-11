#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PubChem MCP Server

这是一个Model Context Protocol (MCP) 服务器，允许大语言模型顺畅访问PubChem API，
获取化学结构和相关属性数据，支持多种输出格式。

主要功能:
- 支持多种搜索方式：名称、分子式、SMILES、CID等
- 支持多种输出格式：JSON、CSV
- 支持结构文件格式转换：SDF、XYZ、CIF、PDB、MOL
- 内置缓存系统减少API调用
- 速率限制器确保符合PubChem API使用政策
"""

import sys
import os
import httpx
import json
import asyncio
import time
import csv
import io
import re
import logging
from typing import Optional, Dict, Any, List, Union, Tuple

# 添加python-sdk到系统路径
sdk_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "python-sdk", "src")
if os.path.exists(sdk_path):
    sys.path.insert(0, sdk_path)

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("pubchem-mcp")

# 尝试导入MCP模块
try:
    from mcp.server.fastmcp import FastMCP, Tool, server_tool
    from mcp.types import ToolCallResult, ContentItem
    HAS_FASTMCP = True
except ImportError:
    try:
        from mcp.server.lowlevel.server import Server
        from mcp.types import (
            ServerInfo, Capabilities, ToolInfo, ResourceInfo,
            ContentItem, ToolCallResult, ErrorCode, ToolJSONSchema
        )
        HAS_FASTMCP = False
    except ImportError:
        logger.error("无法导入MCP库，请确保它已正确安装或python-sdk路径正确")
        sys.exit(1)

###################
# 常量和配置
###################

PUBCHEM_REST_BASE = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
USER_AGENT = "PubChem-MCP-Server/1.0"

# 允许的输出格式
OUTPUT_FORMATS = ["json", "csv"]

# 允许的化学结构输出格式
STRUCTURE_FORMATS = ["sdf", "xyz", "cif", "pdb", "mol"]

# 默认属性列表
DEFAULT_PROPERTIES = [
    "MolecularFormula",
    "MolecularWeight",
    "CanonicalSMILES",
    "IsomericSMILES", 
    "InChI",
    "InChIKey",
    "IUPACNAME",
    "XLogP",
    "TPSA",
    "HBondDonorCount",
    "HBondAcceptorCount"
]

# HTTP客户端超时设置(秒)
HTTP_TIMEOUT = 30

###################
# 缓存系统
###################

class SimpleCache:
    """简单的内存缓存系统"""
    
    def __init__(self, max_size=1000, ttl=24*60*60):
        """初始化缓存"""
        self.cache = {}
        self.max_size = max_size
        self.ttl = ttl
        
    async def get(self, key: str) -> Optional[Any]:
        """从缓存获取值"""
        if key not in self.cache:
            return None
        
        value, timestamp = self.cache[key]
        if time.time() - timestamp > self.ttl:
            # 缓存已过期
            del self.cache[key]
            return None
            
        return value
    
    async def set(self, key: str, value: Any) -> None:
        """设置缓存值"""
        # 如果缓存已满，移除最旧的项
        if len(self.cache) >= self.max_size and key not in self.cache:
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k][1])
            del self.cache[oldest_key]
        
        self.cache[key] = (value, time.time())
    
    async def get_or_set(self, key: str, value_func) -> Any:
        """获取缓存值，如果不存在则设置"""
        cached_value = await self.get(key)
        if cached_value is not None:
            return cached_value
        
        value = await value_func()
        await self.set(key, value)
        return value

# 初始化缓存
cache = SimpleCache()

###################
# 速率限制器
###################

class RateLimiter:
    """速率限制器，限制API请求频率"""
    
    def __init__(self, max_calls: int, period: float):
        self.max_calls = max_calls
        self.period = period
        self.calls = []
        self.lock = asyncio.Lock()
    
    async def wait(self):
        """等待，如有必要，以遵守速率限制"""
        async with self.lock:
            now = time.time()
            self.calls = [call_time for call_time in self.calls if now - call_time < self.period]
            
            if len(self.calls) >= self.max_calls:
                oldest_call = min(self.calls)
                sleep_time = oldest_call + self.period - now
                if sleep_time > 0:
                    logger.debug(f"速率限制达到，等待 {sleep_time:.2f}s")
                    await asyncio.sleep(sleep_time)
            
            self.calls.append(time.time())

# 初始化速率限制器(遵循PubChem每秒最多5个请求的限制)
pubchem_rate_limiter = RateLimiter(max_calls=5, period=1.0)

###################
# 辅助函数
###################

def format_as_csv(data: Union[List[Dict], Dict]) -> str:
    """将数据格式化为CSV字符串"""
    # 处理单个字典的情况
    if isinstance(data, dict):
        data = [data]
    
    # 处理空列表
    if not data:
        return ""
    
    # 展平嵌套字典
    flattened_data = []
    for item in data:
        flat_item = {}
        for k, v in item.items():
            if isinstance(v, dict):
                for sub_k, sub_v in v.items():
                    flat_item[f"{k}.{sub_k}"] = sub_v
            elif isinstance(v, list):
                flat_item[k] = ", ".join(str(x) for x in v)
            else:
                flat_item[k] = v
        flattened_data.append(flat_item)
    
    # 收集所有可能的字段名
    all_fields = set()
    for item in flattened_data:
        all_fields.update(item.keys())
    
    # 生成CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=sorted(all_fields))
    writer.writeheader()
    writer.writerows(flattened_data)
    
    return output.getvalue()

def format_output(data: Any, output_format: str = "json") -> str:
    """根据指定的格式格式化输出数据"""
    if output_format.lower() == "json":
        return json.dumps(data, indent=2)
    elif output_format.lower() == "csv":
        return format_as_csv(data)
    else:
        raise ValueError(f"不支持的输出格式: {output_format}")

def sanitize_name(name: str) -> str:
    """清理名称，使其适合用于API查询"""
    # 替换特殊字符为URL编码
    return re.sub(r'[^a-zA-Z0-9]', lambda m: '%' + hex(ord(m.group(0)))[2:].upper(), name)

def convert_sdf_to_xyz(sdf_data: str) -> str:
    """将SDF格式转换为XYZ格式"""
    lines = sdf_data.strip().split('\n')
    
    try:
        # 提取原子数量
        counts_line = lines[3]
        atom_count = int(counts_line[:3].strip())
        
        # 构建XYZ文件
        xyz_lines = [str(atom_count), "Generated from PubChem SDF"]
        
        # 提取原子块
        for i in range(4, 4 + atom_count):
            if i < len(lines):
                parts = lines[i].split()
                if len(parts) >= 4:
                    x, y, z = parts[0:3]
                    atom_symbol = parts[3]
                    xyz_lines.append(f"{atom_symbol} {x} {y} {z}")
        
        return "\n".join(xyz_lines)
    except Exception as e:
        logger.error(f"转换SDF到XYZ格式出错: {str(e)}")
        return f"Error converting to XYZ: {str(e)}"

def convert_sdf_to_cif(sdf_data: str, cid: int, compound_name: str) -> str:
    """将SDF格式转换为CIF格式"""
    lines = sdf_data.strip().split('\n')
    
    try:
        # 提取原子数量
        counts_line = lines[3]
        atom_count = int(counts_line[:3].strip())
        
        # 构建CIF文件
        cif_lines = [
            f"data_{cid}",
            f"_chemical_name_systematic '{compound_name}'",
            "_chemical_name_common .",
            f"_chemical_compound_source 'PubChem CID: {cid}'",
            "_chemical_formula_moiety .",
            "_chemical_formula_sum .",
            "_chemical_formula_weight .",
            "loop_",
            "_atom_site_label",
            "_atom_site_type_symbol",
            "_atom_site_fract_x",
            "_atom_site_fract_y",
            "_atom_site_fract_z"
        ]
        
        # 提取原子块
        for i in range(4, 4 + atom_count):
            if i < len(lines):
                parts = lines[i].split()
                if len(parts) >= 4:
                    x, y, z = [float(coord) for coord in parts[0:3]]
                    atom_symbol = parts[3]
                    atom_idx = i - 3
                    
                    # 转换为分数坐标（简化处理）
                    cif_lines.append(f"{atom_symbol}{atom_idx} {atom_symbol} {x:.6f} {y:.6f} {z:.6f}")
        
        return "\n".join(cif_lines)
    except Exception as e:
        logger.error(f"转换SDF到CIF格式出错: {str(e)}")
        return f"Error converting to CIF: {str(e)}"

def convert_sdf_to_pdb(sdf_data: str, cid: int) -> str:
    """将SDF格式转换为PDB格式"""
    lines = sdf_data.strip().split('\n')
    
    try:
        # 提取原子数量
        counts_line = lines[3]
        atom_count = int(counts_line[:3].strip())
        
        # 构建PDB文件
        pdb_lines = [
            f"HEADER    PUBCHEM COMPOUND {cid}",
            f"TITLE     PUBCHEM COMPOUND {cid}",
            "AUTHOR    GENERATED BY PUBCHEM-MCP-SERVER"
        ]
        
        # 提取原子块
        for i in range(4, 4 + atom_count):
            if i < len(lines):
                parts = lines[i].split()
                if len(parts) >= 4:
                    x, y, z = [float(coord) for coord in parts[0:3]]
                    atom_symbol = parts[3]
                    atom_idx = i - 3
                    
                    # 格式化PDB ATOM记录
                    pdb_lines.append(f"ATOM  {atom_idx:5d}  {atom_symbol:<3} LIG A   1    {x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00          {atom_symbol}")
        
        pdb_lines.append("END")
        return "\n".join(pdb_lines)
    except Exception as e:
        logger.error(f"转换SDF到PDB格式出错: {str(e)}")
        return f"Error converting to PDB: {str(e)}"

def convert_sdf_to_mol(sdf_data: str) -> str:
    """将SDF格式转换为MOL格式（本质上是提取SDF中的第一个分子）"""
    try:
        # MOL格式本质上是SDF格式的单分子形式
        mol_end_pos = sdf_data.find("M  END")
        if mol_end_pos < 0:
            return "Error: No MOL data found in SDF"
        
        # 包含"M  END"行
        return sdf_data[:mol_end_pos + 6]
    except Exception as e:
        logger.error(f"转换SDF到MOL格式出错: {str(e)}")
        return f"Error converting to MOL: {str(e)}"

def convert_structure(sdf_data: str, cid: int, compound_name: str, output_format: str) -> str:
    """将结构数据转换为请求的格式"""
    output_format = output_format.lower()
    
    if output_format == "sdf":
        return sdf_data
    elif output_format == "xyz":
        return convert_sdf_to_xyz(sdf_data)
    elif output_format == "cif":
        return convert_sdf_to_cif(sdf_data, cid, compound_name)
    elif output_format == "pdb":
        return convert_sdf_to_pdb(sdf_data, cid)
    elif output_format == "mol":
        return convert_sdf_to_mol(sdf_data)
    else:
        return f"Unsupported output format: {output_format}"

###################
# API访问函数
###################

async def fetch_cids_by_name(name: str, max_results: int = 10) -> List[int]:
    """通过名称搜索化合物ID"""
    cache_key = f"name_to_cid:{name}:{max_results}"
    
    async def fetch_data():
        await pubchem_rate_limiter.wait()
        try:
            async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
                response = await client.get(
                    f"{PUBCHEM_REST_BASE}/compound/name/{sanitize_name(name)}/cids/JSON",
                    headers={"User-Agent": USER_AGENT}
                )
                
                if response.status_code != 200:
                    return []
                    
                data = response.json()
                if "IdentifierList" not in data or "CID" not in data["IdentifierList"]:
                    return []
                
                cids = data["IdentifierList"]["CID"]
                return cids[:max_results] if max_results > 0 else cids
        except Exception as e:
            logger.error(f"获取CID出错: {str(e)}")
            return []
    
    return await cache.get_or_set(cache_key, fetch_data)

async def fetch_cids_by_formula(formula: str, max_results: int = 10) -> List[int]:
    """通过分子式搜索化合物ID"""
    cache_key = f"formula_to_cid:{formula}:{max_results}"
    
    async def fetch_data():
        await pubchem_rate_limiter.wait()
        try:
            async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
                response = await client.get(
                    f"{PUBCHEM_REST_BASE}/compound/formula/{formula}/cids/JSON",
                    headers={"User-Agent": USER_AGENT}
                )
                
                if response.status_code != 200:
                    return []
                    
                data = response.json()
                if "IdentifierList" not in data or "CID" not in data["IdentifierList"]:
                    return []
                
                cids = data["IdentifierList"]["CID"]
                return cids[:max_results] if max_results > 0 else cids
        except Exception as e:
            logger.error(f"获取CID出错: {str(e)}")
            return []
    
    return await cache.get_or_set(cache_key, fetch_data)

async def fetch_cids_by_smiles(smiles: str, max_results: int = 10) -> List[int]:
    """通过SMILES搜索化合物ID"""
    cache_key = f"smiles_to_cid:{smiles}:{max_results}"
    
    async def fetch_data():
        await pubchem_rate_limiter.wait()
        try:
            async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
                response = await client.get(
                    f"{PUBCHEM_REST_BASE}/compound/smiles/{smiles}/cids/JSON",
                    headers={"User-Agent": USER_AGENT}
                )
                
                if response.status_code != 200:
                    return []
                    
                data = response.json()
                if "IdentifierList" not in data or "CID" not in data["IdentifierList"]:
                    return []
                
                cids = data["IdentifierList"]["CID"]
                return cids[:max_results] if max_results > 0 else cids
        except Exception as e:
            logger.error(f"获取CID出错: {str(e)}")
            return []
    
    return await cache.get_or_set(cache_key, fetch_data)

async def fetch_properties(cid: int, properties: List[str] = None) -> Dict:
    """获取化合物属性"""
    if properties is None or len(properties) == 0:
        properties = DEFAULT_PROPERTIES
    
    property_list = ",".join(properties)
    cache_key = f"properties:{cid}:{property_list}"
    
    async def fetch_data():
        await pubchem_rate_limiter.wait()
        try:
            async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
                response = await client.get(
                    f"{PUBCHEM_REST_BASE}/compound/cid/{cid}/property/{property_list}/JSON",
                    headers={"User-Agent": USER_AGENT}
                )
                
                if response.status_code != 200:
                    return {}
                    
                data = response.json()
                if "PropertyTable" not in data or "Properties" not in data["PropertyTable"]:
                    return {}
                
                return data["PropertyTable"]["Properties"][0]
        except Exception as e:
            logger.error(f"获取属性出错: {str(e)}")
            return {}
    
    return await cache.get_or_set(cache_key, fetch_data)

async def fetch_synonyms(cid: int, max_synonyms: int = 10) -> List[str]:
    """获取化合物同义词"""
    cache_key = f"synonyms:{cid}:{max_synonyms}"
    
    async def fetch_data():
        await pubchem_rate_limiter.wait()
        try:
            async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
                response = await client.get(
                    f"{PUBCHEM_REST_BASE}/compound/cid/{cid}/synonyms/JSON",
                    headers={"User-Agent": USER_AGENT}
                )
                
                if response.status_code != 200:
                    return []
                    
                data = response.json()
                if "InformationList" not in data or "Information" not in data["InformationList"]:
                    return []
                
                if not data["InformationList"]["Information"] or "Synonym" not in data["InformationList"]["Information"][0]:
                    return []
                
                synonyms = data["InformationList"]["Information"][0]["Synonym"]
                return synonyms[:max_synonyms] if max_synonyms > 0 else synonyms
        except Exception as e:
            logger.error(f"获取同义词出错: {str(e)}")
            return []
    
    return await cache.get_or_set(cache_key, fetch_data)

async def fetch_structure(cid: int, as_3d: bool = True) -> str:
    """获取化合物结构"""
    record_type = "3d" if as_3d else "2d"
    cache_key = f"structure:{cid}:{record_type}"
    
    async def fetch_data():
        await pubchem_rate_limiter.wait()
        try:
            async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
                response = await client.get(
                    f"{PUBCHEM_REST_BASE}/compound/cid/{cid}/record/SDF/?record_type={record_type}",
                    headers={"User-Agent": USER_AGENT}
                )
                
                if response.status_code != 200:
                    return ""
                
                return response.text
        except Exception as e:
            logger.error(f"获取结构出错: {str(e)}")
            return ""
    
    return await cache.get_or_set(cache_key, fetch_data)

async def fetch_compound_data(cid: int, get_structure: bool = True, as_3d: bool = True, 
                             properties: List[str] = None, get_synonyms: bool = True) -> Dict:
    """获取化合物完整数据"""
    # 获取基本属性
    result = {"cid": cid}
    
    # 获取化学属性
    props = await fetch_properties(cid, properties)
    if props:
        result["properties"] = props
    
    # 获取同义词
    if get_synonyms:
        synonyms = await fetch_synonyms(cid)
        if synonyms:
            result["synonyms"] = synonyms
    
    # 获取结构
    if get_structure:
        sdf_data = await fetch_structure(cid, as_3d)
        if sdf_data:
            # 获取化合物名称(用于结构转换)
            compound_name = props.get("IUPACNAME", f"Compound_{cid}")
            
            # 添加各种格式的结构数据
            result["structures"] = {
                "sdf": sdf_data[:500] + "..." if len(sdf_data) > 500 else sdf_data,  # 截断长结构
                "xyz": convert_sdf_to_xyz(sdf_data),
                "mol": convert_sdf_to_mol(sdf_data)
            }
    
    return result

###################
# MCP工具函数处理器
###################

async def search_chemical_by_name(name: str, max_results: int = 1, output_format: str = "json"):
    """
    通过名称搜索化学化合物
    
    Args:
        name: 化学名称或标识符(如'ethanol', 'aspirin')
        max_results: 最大返回结果数(默认为1)
        output_format: 输出格式(json或csv)
        
    Returns:
        化合物数据
    """
    try:
        # 参数验证
        if not name:
            return {"error": "缺少必需参数: name"}
        
        if output_format not in OUTPUT_FORMATS:
            return {"error": f"不支持的输出格式: {output_format}"}
        
        # 搜索化合物
        cids = await fetch_cids_by_name(name, max_results)
        if not cids:
            return {"error": f"未找到名称为 '{name}' 的化合物"}
        
        # 获取化合物详情
        if max_results == 1:
            # 单个结果
            data = await fetch_compound_data(cids[0])
            return data
        else:
            # 多个结果
            results = []
            for cid in cids:
                compound_data = await fetch_compound_data(cid, get_structure=False)
                results.append(compound_data)
            return results
    except Exception as e:
        logger.error(f"通过名称搜索化合物出错: {str(e)}")
        return {"error": f"搜索化合物时出错: {str(e)}"}

async def search_chemical_by_formula(formula: str, max_results: int = 1, output_format: str = "json"):
    """
    通过分子式搜索化学化合物
    
    Args:
        formula: 分子式(如'C2H6O', 'H2O')
        max_results: 最大返回结果数(默认为1)
        output_format: 输出格式(json或csv)
        
    Returns:
        化合物数据
    """
    try:
        # 参数验证
        if not formula:
            return {"error": "缺少必需参数: formula"}
        
        if output_format not in OUTPUT_FORMATS:
            return {"error": f"不支持的输出格式: {output_format}"}
        
        # 搜索化合物
        cids = await fetch_cids_by_formula(formula, max_results)
        if not cids:
            return {"error": f"未找到分子式为 '{formula}' 的化合物"}
        
        # 获取化合物详情
        if max_results == 1:
            # 单个结果
            data = await fetch_compound_data(cids[0])
            return data
        else:
            # 多个结果
            results = []
            for cid in cids:
                compound_data = await fetch_compound_data(cid, get_structure=False)
                results.append(compound_data)
            return results
    except Exception as e:
        logger.error(f"通过分子式搜索化合物出错: {str(e)}")
        return {"error": f"搜索化合物时出错: {str(e)}"}

async def search_chemical_by_smiles(smiles: str, max_results: int = 1, output_format: str = "json"):
    """
    通过SMILES表示法搜索化学化合物
    
    Args:
        smiles: SMILES表示法(如'CCO'代表乙醇)
        max_results: 最大返回结果数(默认为1)
        output_format: 输出格式(json或csv)
        
    Returns:
        化合物数据
    """
    try:
        # 参数验证
        if not smiles:
            return {"error": "缺少必需参数: smiles"}
        
        if output_format not in OUTPUT_FORMATS:
            return {"error": f"不支持的输出格式: {output_format}"}
        
        # 搜索化合物
        cids = await fetch_cids_by_smiles(smiles, max_results)
        if not cids:
            return {"error": f"未找到SMILES为 '{smiles}' 的化合物"}
        
        # 获取化合物详情
        if max_results == 1:
            # 单个结果
            data = await fetch_compound_data(cids[0])
            return data
        else:
            # 多个结果
            results = []
            for cid in cids:
                compound_data = await fetch_compound_data(cid, get_structure=False)
                results.append(compound_data)
            return results
    except Exception as e:
        logger.error(f"通过SMILES搜索化合物出错: {str(e)}")
        return {"error": f"搜索化合物时出错: {str(e)}"}

async def get_compound_by_cid(cid: int, output_format: str = "json"):
    """
    通过PubChem CID获取化合物详细信息
    
    Args:
        cid: PubChem化合物ID(如702代表乙醇)
        output_format: 输出格式(json或csv)
        
    Returns:
        化合物数据
    """
    try:
        # 参数验证
        if output_format not in OUTPUT_FORMATS:
            return {"error": f"不支持的输出格式: {output_format}"}
        
        # 获取化合物详情
        data = await fetch_compound_data(cid)
        if not data.get("properties"):
            return {"error": f"未找到CID为 {cid} 的化合物"}
        
        return data
    except Exception as e:
        logger.error(f"获取化合物详情出错: {str(e)}")
        return {"error": f"获取化合物详情时出错: {str(e)}"}

async def get_structure_file(cid: int, output_format: str = "sdf", as_3d: bool = True):
    """
    获取化合物的结构文件
    
    Args:
        cid: PubChem化合物ID
        output_format: 输出结构格式(sdf、xyz、cif、pdb或mol)
        as_3d: 是否获取3D结构(若可用)
        
    Returns:
        结构文件内容
    """
    try:
        # 参数验证
        if output_format not in STRUCTURE_FORMATS:
            return {"error": f"不支持的结构格式: {output_format}。有效格式: {', '.join(STRUCTURE_FORMATS)}"}
        
        # 获取SDF结构
        sdf_data = await fetch_structure(cid, as_3d)
        if not sdf_data:
            return {"error": f"未找到CID为 {cid} 的化合物结构"}
        
        # 获取化合物名称(用于结构转换)
        props = await fetch_properties(cid)
        compound_name = props.get("IUPACNAME", f"Compound_{cid}")
        
        # 转换为请求的格式
        result = convert_structure(sdf_data, cid, compound_name, output_format)
        
        return result
    except Exception as e:
        logger.error(f"获取结构文件出错: {str(e)}")
        return {"error": f"获取结构文件时出错: {str(e)}"}

###################
# 服务器设置
###################

if HAS_FASTMCP:
    # 使用FastMCP API
    mcp = FastMCP("pubchem-server")
    
    @server_tool(mcp)
    async def search_chemical_by_name(
        name: str, 
        max_results: int = 1, 
        output_format: str = "json"
    ) -> str:
        """通过名称搜索化学化合物"""
        result = await search_chemical_by_name(name, max_results, output_format)
        return format_output(result, output_format)
    
    @server_tool(mcp)
    async def search_chemical_by_formula(
        formula: str, 
        max_results: int = 1, 
        output_format: str = "json"
    ) -> str:
        """通过分子式搜索化学化合物"""
        result = await search_chemical_by_formula(formula, max_results, output_format)
        return format_output(result, output_format)
    
    @server_tool(mcp)
    async def search_chemical_by_smiles(
        smiles: str, 
        max_results: int = 1, 
        output_format: str = "json"
    ) -> str:
        """通过SMILES表示法搜索化学化合物"""
        result = await search_chemical_by_smiles(smiles, max_results, output_format)
        return format_output(result, output_format)
    
    @server_tool(mcp)
    async def get_compound_by_cid(
        cid: int, 
        output_format: str = "json"
    ) -> str:
        """通过PubChem CID获取化合物详细信息"""
        result = await get_compound_by_cid(cid, output_format)
        return format_output(result, output_format)
    
    @server_tool(mcp)
    async def get_structure_file(
        cid: int, 
        output_format: str = "sdf", 
        as_3d: bool = True
    ) -> str:
        """获取化合物的结构文件"""
        return await get_structure_file(cid, output_format, as_3d)
    
else:
    # 使用低级API
    server = Server(
        server_info=ServerInfo(
            name="pubchem-server", 
            version="1.0.0"
        ),
        capabilities=Capabilities(
            tools={}
        )
    )
    
    # 通过名称搜索化合物处理器
    async def search_chemical_by_name_handler(arguments: Dict[str, Any]) -> ToolCallResult:
        name = arguments.get("name", "")
        max_results = arguments.get("max_results", 1)
        output_format = arguments.get("output_format", "json").lower()
        
        result = await search_chemical_by_name(name, max_results, output_format)
        formatted_result = format_output(result, output_format)
        
        return ToolCallResult(
            content=[ContentItem(type="text", text=formatted_result)]
        )
    
    # 通过分子式搜索化合物处理器
    async def search_chemical_by_formula_handler(arguments: Dict[str, Any]) -> ToolCallResult:
        formula = arguments.get("formula", "")
        max_results = arguments.get("max_results", 1)
        output_format = arguments.get("output_format", "json").lower()
        
        result = await search_chemical_by_formula(formula, max_results, output_format)
        formatted_result = format_output(result, output_format)
        
        return ToolCallResult(
            content=[ContentItem(type="text", text=formatted_result)]
        )
    
    # 通过SMILES搜索化合物处理器
    async def search_chemical_by_smiles_handler(arguments: Dict[str, Any]) -> ToolCallResult:
        smiles = arguments.get("smiles", "")
        max_results = arguments.get("max_results", 1)
        output_format = arguments.get("output_format", "json").lower()
        
        result = await search_chemical_by_smiles(smiles, max_results, output_format)
        formatted_result = format_output(result, output_format)
        
        return ToolCallResult(
            content=[ContentItem(type="text", text=formatted_result)]
        )
    
    # 通过CID获取化合物处理器
    async def get_compound_by_cid_handler(arguments: Dict[str, Any]) -> ToolCallResult:
        cid = arguments.get("cid")
        output_format = arguments.get("output_format", "json").lower()
        
        try:
            cid = int(cid)
        except (ValueError, TypeError):
            return ToolCallResult(
                content=[ContentItem(type="text", text=json.dumps({"error": "cid必须是整数"}))],
                isError=True
            )
        
        result = await get_compound_by_cid(cid, output_format)
        formatted_result = format_output(result, output_format)
        
        return ToolCallResult(
            content=[ContentItem(type="text", text=formatted_result)]
        )
    
    # 获取结构文件处理器
    async def get_structure_file_handler(arguments: Dict[str, Any]) -> ToolCallResult:
        cid = arguments.get("cid")
        output_format = arguments.get("output_format", "sdf").lower()
        as_3d = arguments.get("as_3d", True)
        
        try:
            cid = int(cid)
        except (ValueError, TypeError):
            return ToolCallResult(
                content=[ContentItem(type="text", text=json.dumps({"error": "cid必须是整数"}))],
                isError=True
            )
        
        result = await get_structure_file(cid, output_format, as_3d)
        
        return ToolCallResult(
            content=[ContentItem(type="text", text=result if isinstance(result, str) else json.dumps(result))]
        )
    
    def register_tools():
        """注册所有MCP工具"""
        # 通过名称搜索化合物
        server.register_tool(
            name="search_chemical_by_name",
            description="通过名称搜索化学化合物",
            input_schema=ToolJSONSchema(
                type="object",
                properties={
                    "name": {
                        "type": "string", 
                        "description": "化学名称或标识符(如'ethanol', 'aspirin')"
                    },
                    "max_results": {
                        "type": "integer", 
                        "description": "最大返回结果数(默认为1)",
                        "default": 1
                    },
                    "output_format": {
                        "type": "string", 
                        "description": "输出格式(json或csv)",
                        "default": "json",
                        "enum": ["json", "csv"]
                    }
                },
                required=["name"]
            ),
            handler=search_chemical_by_name_handler
        )
        
        # 通过分子式搜索化合物
        server.register_tool(
            name="search_chemical_by_formula",
            description="通过分子式搜索化学化合物",
            input_schema=ToolJSONSchema(
                type="object",
                properties={
                    "formula": {
                        "type": "string", 
                        "description": "分子式(如'C2H6O', 'H2O')"
                    },
                    "max_results": {
                        "type": "integer", 
                        "description": "最大返回结果数(默认为1)",
                        "default": 1
                    },
                    "output_format": {
                        "type": "string", 
                        "description": "输出格式(json或csv)",
                        "default": "json",
                        "enum": ["json", "csv"]
                    }
                },
                required=["formula"]
            ),
            handler=search_chemical_by_formula_handler
        )
        
        # 通过SMILES搜索化合物
        server.register_tool(
            name="search_chemical_by_smiles",
            description="通过SMILES表示法搜索化学化合物",
            input_schema=ToolJSONSchema(
                type="object",
                properties={
                    "smiles": {
                        "type": "string", 
                        "description": "SMILES表示法(如'CCO'代表乙醇)"
                    },
                    "max_results": {
                        "type": "integer", 
                        "description": "最大返回结果数(默认为1)",
                        "default": 1
                    },
                    "output_format": {
                        "type": "string", 
                        "description": "输出格式(json或csv)",
                        "default": "json",
                        "enum": ["json", "csv"]
                    }
                },
                required=["smiles"]
            ),
            handler=search_chemical_by_smiles_handler
        )
        
        # 通过CID获取化合物
        server.register_tool(
            name="get_compound_by_cid",
            description="通过PubChem CID获取化合物详细信息",
            input_schema=ToolJSONSchema(
                type="object",
                properties={
                    "cid": {
                        "type": "integer", 
                        "description": "PubChem化合物ID(如702代表乙醇)"
                    },
                    "output_format": {
                        "type": "string", 
                        "description": "输出格式(json或csv)",
                        "default": "json",
                        "enum": ["json", "csv"]
                    }
                },
                required=["cid"]
            ),
            handler=get_compound_by_cid_handler
        )
        
        # 获取结构文件
        server.register_tool(
            name="get_structure_file",
            description="获取化合物的结构文件",
            input_schema=ToolJSONSchema(
                type="object",
                properties={
                    "cid": {
                        "type": "integer", 
                        "description": "PubChem化合物ID"
                    },
                    "output_format": {
                        "type": "string", 
                        "description": "输出结构格式(sdf、xyz、cif、pdb或mol)",
                        "default": "sdf",
                        "enum": ["sdf", "xyz", "cif", "pdb", "mol"]
                    },
                    "as_3d": {
                        "type": "boolean", 
                        "description": "是否获取3D结构(若可用)",
                        "default": True
                    }
                },
                required=["cid"]
            ),
            handler=get_structure_file_handler
        )

###################
# 主入口
###################

if __name__ == "__main__":
    logger.info("启动PubChem MCP服务器...")
    
    if HAS_FASTMCP:
        from mcp.server.stdio import StdioServerTransport
        transport = StdioServerTransport()
        asyncio.run(mcp.run(transport))
    else:
        logger.info("注册PubChem MCP服务器工具...")
        register_tools()
        
        from mcp.server.stdio import StdioServerTransport
        transport = StdioServerTransport()
        asyncio.run(server.run(transport))
