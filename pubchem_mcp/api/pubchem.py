"""PubChem API访问模块"""

import httpx
import logging
from typing import List, Dict, Optional, Any

logger = logging.getLogger("pubchem-mcp.api")

PUBCHEM_REST_BASE = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
USER_AGENT = "PubChem-MCP-Server/1.0"
HTTP_TIMEOUT = 30

class PubChemAPI:
    """PubChem API访问类"""
    
    def __init__(self, rate_limiter):
        """初始化API访问器"""
        self.rate_limiter = rate_limiter
        
    async def fetch_cids_by_name(self, name: str, max_results: int = 10) -> List[int]:
        """通过名称搜索化合物ID"""
        await self.rate_limiter.wait()
        try:
            async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
                response = await client.get(
                    f"{PUBCHEM_REST_BASE}/compound/name/{name}/cids/JSON",
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
            
    async def fetch_cids_by_formula(self, formula: str, max_results: int = 10) -> List[int]:
        """通过分子式搜索化合物ID"""
        await self.rate_limiter.wait()
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
            
    async def fetch_cids_by_smiles(self, smiles: str, max_results: int = 10) -> List[int]:
        """通过SMILES搜索化合物ID"""
        await self.rate_limiter.wait()
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
            
    async def fetch_properties(self, cid: int, properties: List[str]) -> Dict:
        """获取化合物属性"""
        await self.rate_limiter.wait()
        try:
            property_list = ",".join(properties)
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
            
    async def fetch_structure(self, cid: int, as_3d: bool = True) -> str:
        """获取化合物结构"""
        await self.rate_limiter.wait()
        try:
            record_type = "3d" if as_3d else "2d"
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