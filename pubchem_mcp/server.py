"""PubChem MCP服务器主模块"""

import os
import sys
import logging
import asyncio
from typing import Dict, Any, List

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("pubchem-mcp")

# 导入MCP模块
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
        logger.error("无法导入MCP库，请确保它已正确安装")
        sys.exit(1)

from . import (
    PubChemAPI, MemoryCache, RateLimiter, 
    Compound, CompoundProperty, Structure, StructureConverter
)

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

class PubChemMCPServer:
    """PubChem MCP服务器"""
    
    def __init__(self):
        """初始化服务器"""
        # 初始化组件
        self.rate_limiter = RateLimiter(max_calls=5, period=1.0)
        self.cache = MemoryCache()
        self.api = PubChemAPI(self.rate_limiter)
        self.converter = StructureConverter()
        
        # 初始化MCP服务器
        if HAS_FASTMCP:
            self.mcp = FastMCP("pubchem-server")
            self._register_fastmcp_tools()
        else:
            self.server = Server(
                server_info=ServerInfo(
                    name="pubchem-server",
                    version="1.0.0"
                ),
                capabilities=Capabilities(tools={})
            )
            self._register_lowlevel_tools()
    
    async def search_chemical_by_name(self, name: str, max_results: int = 1, 
                                    output_format: str = "json") -> str:
        """通过名称搜索化学化合物"""
        try:
            # 参数验证
            if not name:
                return {"error": "缺少必需参数: name"}
            
            # 搜索化合物
            cids = await self.api.fetch_cids_by_name(name, max_results)
            if not cids:
                return {"error": f"未找到名称为 '{name}' 的化合物"}
            
            # 获取化合物详情
            results = []
            for cid in cids:
                props = await self.api.fetch_properties(cid, DEFAULT_PROPERTIES)
                if not props:
                    continue
                    
                compound = Compound(
                    cid=cid,
                    properties=CompoundProperty.from_dict(props)
                )
                results.append(compound.to_dict())
            
            if not results:
                return {"error": "无法获取化合物详情"}
                
            return results[0] if max_results == 1 else results
            
        except Exception as e:
            logger.error(f"通过名称搜索化合物出错: {str(e)}")
            return {"error": f"搜索化合物时出错: {str(e)}"}
    
    async def search_chemical_by_formula(self, formula: str, max_results: int = 1,
                                       output_format: str = "json") -> str:
        """通过分子式搜索化学化合物"""
        try:
            # 参数验证
            if not formula:
                return {"error": "缺少必需参数: formula"}
            
            # 搜索化合物
            cids = await self.api.fetch_cids_by_formula(formula, max_results)
            if not cids:
                return {"error": f"未找到分子式为 '{formula}' 的化合物"}
            
            # 获取化合物详情
            results = []
            for cid in cids:
                props = await self.api.fetch_properties(cid, DEFAULT_PROPERTIES)
                if not props:
                    continue
                    
                compound = Compound(
                    cid=cid,
                    properties=CompoundProperty.from_dict(props)
                )
                results.append(compound.to_dict())
            
            if not results:
                return {"error": "无法获取化合物详情"}
                
            return results[0] if max_results == 1 else results
            
        except Exception as e:
            logger.error(f"通过分子式搜索化合物出错: {str(e)}")
            return {"error": f"搜索化合物时出错: {str(e)}"}
    
    async def search_chemical_by_smiles(self, smiles: str, max_results: int = 1,
                                      output_format: str = "json") -> str:
        """通过SMILES表示法搜索化学化合物"""
        try:
            # 参数验证
            if not smiles:
                return {"error": "缺少必需参数: smiles"}
            
            # 搜索化合物
            cids = await self.api.fetch_cids_by_smiles(smiles, max_results)
            if not cids:
                return {"error": f"未找到SMILES为 '{smiles}' 的化合物"}
            
            # 获取化合物详情
            results = []
            for cid in cids:
                props = await self.api.fetch_properties(cid, DEFAULT_PROPERTIES)
                if not props:
                    continue
                    
                compound = Compound(
                    cid=cid,
                    properties=CompoundProperty.from_dict(props)
                )
                results.append(compound.to_dict())
            
            if not results:
                return {"error": "无法获取化合物详情"}
                
            return results[0] if max_results == 1 else results
            
        except Exception as e:
            logger.error(f"通过SMILES搜索化合物出错: {str(e)}")
            return {"error": f"搜索化合物时出错: {str(e)}"}
    
    async def get_compound_by_cid(self, cid: int, output_format: str = "json") -> str:
        """通过PubChem CID获取化合物详细信息"""
        try:
            # 获取属性
            props = await self.api.fetch_properties(cid, DEFAULT_PROPERTIES)
            if not props:
                return {"error": f"未找到CID为 {cid} 的化合物"}
            
            # 创建化合物对象
            compound = Compound(
                cid=cid,
                properties=CompoundProperty.from_dict(props)
            )
            
            return compound.to_dict()
            
        except Exception as e:
            logger.error(f"获取化合物详情出错: {str(e)}")
            return {"error": f"获取化合物详情时出错: {str(e)}"}
    
    async def get_structure_file(self, cid: int, output_format: str = "sdf",
                               as_3d: bool = True) -> str:
        """获取化合物的结构文件"""
        try:
            # 获取SDF结构
            sdf_data = await self.api.fetch_structure(cid, as_3d)
            if not sdf_data:
                return {"error": f"未找到CID为 {cid} 的化合物结构"}
            
            # 获取化合物名称
            props = await self.api.fetch_properties(cid, ["IUPACName"])
            compound_name = props.get("IUPACName", f"Compound_{cid}")
            
            # 转换结构格式
            result = self.converter.convert(sdf_data, cid, compound_name, output_format)
            if result is None:
                return {"error": f"结构转换失败: {output_format}"}
            
            return result
            
        except Exception as e:
            logger.error(f"获取结构文件出错: {str(e)}")
            return {"error": f"获取结构文件时出错: {str(e)}"}
    
    def _register_fastmcp_tools(self):
        """注册FastMCP工具"""
        @server_tool(self.mcp)
        async def search_chemical_by_name(
            name: str, 
            max_results: int = 1, 
            output_format: str = "json"
        ) -> str:
            """通过名称搜索化学化合物"""
            result = await self.search_chemical_by_name(name, max_results, output_format)
            return result
        
        @server_tool(self.mcp)
        async def search_chemical_by_formula(
            formula: str, 
            max_results: int = 1, 
            output_format: str = "json"
        ) -> str:
            """通过分子式搜索化学化合物"""
            result = await self.search_chemical_by_formula(formula, max_results, output_format)
            return result
        
        @server_tool(self.mcp)
        async def search_chemical_by_smiles(
            smiles: str, 
            max_results: int = 1, 
            output_format: str = "json"
        ) -> str:
            """通过SMILES表示法搜索化学化合物"""
            result = await self.search_chemical_by_smiles(smiles, max_results, output_format)
            return result
        
        @server_tool(self.mcp)
        async def get_compound_by_cid(
            cid: int, 
            output_format: str = "json"
        ) -> str:
            """通过PubChem CID获取化合物详细信息"""
            result = await self.get_compound_by_cid(cid, output_format)
            return result
        
        @server_tool(self.mcp)
        async def get_structure_file(
            cid: int, 
            output_format: str = "sdf", 
            as_3d: bool = True
        ) -> str:
            """获取化合物的结构文件"""
            result = await self.get_structure_file(cid, output_format, as_3d)
            return result
    
    def _register_lowlevel_tools(self):
        """注册低级API工具"""
        # 通过名称搜索化合物
        async def search_chemical_by_name_handler(arguments: Dict[str, Any]) -> ToolCallResult:
            name = arguments.get("name", "")
            max_results = arguments.get("max_results", 1)
            output_format = arguments.get("output_format", "json").lower()
            
            result = await self.search_chemical_by_name(name, max_results, output_format)
            return ToolCallResult(
                content=[ContentItem(type="text", text=str(result))]
            )
        
        self.server.register_tool(
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
        async def search_chemical_by_formula_handler(arguments: Dict[str, Any]) -> ToolCallResult:
            formula = arguments.get("formula", "")
            max_results = arguments.get("max_results", 1)
            output_format = arguments.get("output_format", "json").lower()
            
            result = await self.search_chemical_by_formula(formula, max_results, output_format)
            return ToolCallResult(
                content=[ContentItem(type="text", text=str(result))]
            )
        
        self.server.register_tool(
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
        async def search_chemical_by_smiles_handler(arguments: Dict[str, Any]) -> ToolCallResult:
            smiles = arguments.get("smiles", "")
            max_results = arguments.get("max_results", 1)
            output_format = arguments.get("output_format", "json").lower()
            
            result = await self.search_chemical_by_smiles(smiles, max_results, output_format)
            return ToolCallResult(
                content=[ContentItem(type="text", text=str(result))]
            )
        
        self.server.register_tool(
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
        async def get_compound_by_cid_handler(arguments: Dict[str, Any]) -> ToolCallResult:
            cid = arguments.get("cid")
            output_format = arguments.get("output_format", "json").lower()
            
            try:
                cid = int(cid)
            except (ValueError, TypeError):
                return ToolCallResult(
                    content=[ContentItem(type="text", text=str({"error": "cid必须是整数"}))],
                    isError=True
                )
            
            result = await self.get_compound_by_cid(cid, output_format)
            return ToolCallResult(
                content=[ContentItem(type="text", text=str(result))]
            )
        
        self.server.register_tool(
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
        async def get_structure_file_handler(arguments: Dict[str, Any]) -> ToolCallResult:
            cid = arguments.get("cid")
            output_format = arguments.get("output_format", "sdf").lower()
            as_3d = arguments.get("as_3d", True)
            
            try:
                cid = int(cid)
            except (ValueError, TypeError):
                return ToolCallResult(
                    content=[ContentItem(type="text", text=str({"error": "cid必须是整数"}))],
                    isError=True
                )
            
            result = await self.get_structure_file(cid, output_format, as_3d)
            return ToolCallResult(
                content=[ContentItem(type="text", text=str(result))]
            )
        
        self.server.register_tool(
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
    
    async def run(self):
        """运行服务器"""
        logger.info("启动PubChem MCP服务器...")
        
        from mcp.server.stdio import StdioServerTransport
        transport = StdioServerTransport()
        
        if HAS_FASTMCP:
            await self.mcp.run(transport)
        else:
            await self.server.run(transport)

def main():
    """主入口"""
    server = PubChemMCPServer()
    asyncio.run(server.run())

if __name__ == "__main__":
    main()