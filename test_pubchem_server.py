#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PubChem MCP服务器测试脚本

这个脚本演示了如何使用PubChem MCP服务器的各种功能，
并展示了每个API函数的调用方式和返回结果。
"""

import sys
import os
import json
import asyncio
from typing import Any, Dict, List, Optional

# 确保MCP SDK在路径中
sdk_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "python-sdk", "src")
if os.path.exists(sdk_path):
    sys.path.insert(0, sdk_path)

# 尝试导入MCP客户端库
try:
    from mcp.client.session import Session as MCPSession
except ImportError:
    print("错误: 未找到MCP客户端库。确保python-sdk路径正确或者通过 'pip install mcp' 安装。")
    sys.exit(1)

# 美化输出的助手函数
def print_separator(title: str):
    """打印分隔符和标题"""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80 + "\n")

def print_json(data: Any):
    """美化打印JSON数据"""
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            print(data)
            return
    
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print()

async def test_search_by_name():
    """测试通过名称搜索化合物"""
    print_separator("通过名称搜索化合物 (search_chemical_by_name)")
    
    async with MCPSession() as session:
        servers = list(session.servers.items())
        if not servers:
            print("未找到可用的MCP服务器")
            return
            
        for server_name, server in servers:
            if hasattr(server, "search_chemical_by_name"):
                print(f"使用服务器: {server_name}")
                
                # 搜索阿司匹林
                print("搜索化合物: 阿司匹林/aspirin")
                try:
                    result = await server.search_chemical_by_name(name="aspirin")
                    print_json(result)
                except Exception as e:
                    print(f"搜索失败: {str(e)}")
                
                # 搜索多个结果并使用CSV格式
                print("搜索化合物(多个结果，CSV格式): 葡萄糖/glucose")
                try:
                    result = await server.search_chemical_by_name(
                        name="glucose", 
                        max_results=3, 
                        output_format="csv"
                    )
                    print(result)
                except Exception as e:
                    print(f"搜索失败: {str(e)}")
                
                return
    
    print("未找到支持search_chemical_by_name的服务器")

async def test_search_by_formula():
    """测试通过分子式搜索化合物"""
    print_separator("通过分子式搜索化合物 (search_chemical_by_formula)")
    
    async with MCPSession() as session:
        servers = list(session.servers.items())
        if not servers:
            print("未找到可用的MCP服务器")
            return
            
        for server_name, server in servers:
            if hasattr(server, "search_chemical_by_formula"):
                print(f"使用服务器: {server_name}")
                
                # 搜索乙醇
                print("搜索分子式: C2H6O (乙醇)")
                try:
                    result = await server.search_chemical_by_formula(formula="C2H6O")
                    print_json(result)
                except Exception as e:
                    print(f"搜索失败: {str(e)}")
                
                return
    
    print("未找到支持search_chemical_by_formula的服务器")

async def test_search_by_smiles():
    """测试通过SMILES搜索化合物"""
    print_separator("通过SMILES搜索化合物 (search_chemical_by_smiles)")
    
    async with MCPSession() as session:
        servers = list(session.servers.items())
        if not servers:
            print("未找到可用的MCP服务器")
            return
            
        for server_name, server in servers:
            if hasattr(server, "search_chemical_by_smiles"):
                print(f"使用服务器: {server_name}")
                
                # 搜索乙醇
                print("搜索SMILES: CCO (乙醇)")
                try:
                    result = await server.search_chemical_by_smiles(smiles="CCO")
                    print_json(result)
                except Exception as e:
                    print(f"搜索失败: {str(e)}")
                
                return
    
    print("未找到支持search_chemical_by_smiles的服务器")

async def test_get_compound_by_cid():
    """测试获取化合物详情"""
    print_separator("获取化合物详情 (get_compound_by_cid)")
    
    async with MCPSession() as session:
        servers = list(session.servers.items())
        if not servers:
            print("未找到可用的MCP服务器")
            return
            
        for server_name, server in servers:
            if hasattr(server, "get_compound_by_cid"):
                print(f"使用服务器: {server_name}")
                
                # 获取阿司匹林详情
                print("获取化合物CID: 2244 (阿司匹林)")
                try:
                    result = await server.get_compound_by_cid(cid=2244)
                    print_json(result)
                except Exception as e:
                    print(f"获取失败: {str(e)}")
                
                return
    
    print("未找到支持get_compound_by_cid的服务器")

async def test_get_structure_file():
    """测试获取结构文件"""
    print_separator("获取结构文件 (get_structure_file)")
    
    async with MCPSession() as session:
        servers = list(session.servers.items())
        if not servers:
            print("未找到可用的MCP服务器")
            return
            
        for server_name, server in servers:
            if hasattr(server, "get_structure_file"):
                print(f"使用服务器: {server_name}")
                
                # 获取阿司匹林的PDB结构
                print("获取CID 2244 (阿司匹林) 的PDB结构:")
                try:
                    result = await server.get_structure_file(
                        cid=2244,
                        output_format="pdb"
                    )
                    # 只显示结构的开头部分
                    if isinstance(result, str) and len(result) > 500:
                        print(result[:500] + "...\n")
                    else:
                        print(result)
                        print()
                except Exception as e:
                    print(f"获取失败: {str(e)}")
                
                return
    
    print("未找到支持get_structure_file的服务器")

async def check_available_servers():
    """检查可用的MCP服务器"""
    print_separator("检查可用的MCP服务器")
    
    try:
        async with MCPSession() as session:
            if not session.servers:
                print("未找到MCP服务器。请确保pubchem_server.py正在运行。")
                return False
            
            print("找到的MCP服务器:")
            for name, server in session.servers.items():
                print(f"- {name}")
                
                # 列出可用的工具
                print("  可用工具:")
                tools = await server.list_tools()
                for tool in tools:
                    print(f"  • {tool.name}: {tool.description}")
            
            return True
    except Exception as e:
        print(f"连接到MCP服务器时出错: {str(e)}")
        return False

async def main():
    """运行所有测试"""
    print("\nPubChem MCP服务器测试脚本")
    print("------------------------\n")
    print("本脚本将测试PubChem MCP服务器的各种功能")
    print("如果测试失败，请确保服务器正在运行\n")
    
    # 检查服务器是否可用
    servers_available = await check_available_servers()
    if not servers_available:
        print("\n无法继续测试 - 未找到可用的MCP服务器。")
        print("请确保先运行 'python pubchem_server.py'，然后再运行此测试脚本。")
        return
    
    # 运行测试
    await test_search_by_name()
    await test_search_by_formula()
    await test_search_by_smiles()
    await test_get_compound_by_cid()
    await test_get_structure_file()
    
    print_separator("测试完成")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n测试被用户中断")