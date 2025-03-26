#!/usr/bin/env python3
"""
PubChem MCP 服务器

实现 MCP 服务器与 PubChem API 的集成，提供化合物数据检索功能。
"""

import json
import sys
import os
import logging
import traceback
from datetime import datetime
from typing import Dict, Any

# 导入 PubChem API 模块
from pubchem_api import get_pubchem_data

# 确保没有缓冲
os.environ['PYTHONUNBUFFERED'] = '1'

# 设置日志记录
log_dir = os.path.expanduser("~/.pubchem-mcp")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"pubchem_server_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger("pubchem_mcp_server")

def handle_get_pubchem_data(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    处理 get_pubchem_data 工具调用
    
    Args:
        params: 工具参数
        
    Returns:
        工具执行结果
    """
    query = params.get("query")
    format_type = params.get("format", "JSON")
    include_3d = params.get("include_3d", False)
    
    if not query:
        return {
            "content": [
                {
                    "type": "text",
                    "text": "Error: Missing required parameter 'query'"
                }
            ],
            "isError": True
        }
    
    # 验证 XYZ 格式需要 include_3d 参数
    if format_type.upper() == "XYZ" and not include_3d:
        return {
            "content": [
                {
                    "type": "text",
                    "text": "When using XYZ format, the include_3d parameter must be set to true"
                }
            ],
            "isError": True
        }
    
    try:
        logger.info(f"调用 PubChem API: query={query}, format={format_type}, include_3d={include_3d}")
        result = get_pubchem_data(query, format_type, include_3d)
        
        # 检查是否有错误
        if result.startswith("Error:"):
            return {
                "content": [
                    {
                        "type": "text",
                        "text": result
                    }
                ],
                "isError": True
            }
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": result
                }
            ]
        }
    except Exception as e:
        logger.error(f"处理 PubChem 数据时出错: {str(e)}")
        logger.error(traceback.format_exc())
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error: {str(e)}"
                }
            ],
            "isError": True
        }

def handle_hello_world(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    处理 hello_world 工具调用（简单的测试功能）
    
    Args:
        params: 工具参数
        
    Returns:
        工具执行结果
    """
    name = params.get("name", "World")
    return {
        "content": [
            {
                "type": "text",
                "text": f"Hello, {name}!"
            }
        ]
    }

def main():
    """主函数 - MCP 服务器入口点"""
    logger.info("PubChem MCP 服务器启动")
    
    while True:
        try:
            # 读取一行
            line = sys.stdin.readline()
            if not line:
                logger.info("输入结束")
                break
                
            logger.debug(f"收到: {line.strip()}")
            
            # 解析请求
            request = json.loads(line)
            request_id = request.get("id")
            method = request.get("method")
            params = request.get("params", {})
            
            logger.info(f"处理请求: method={method}, id={request_id}")
            
            # 处理不同类型的请求
            if method == "initialize":
                # 记录客户端信息
                client_info = params.get("clientInfo", {})
                client_name = client_info.get("name", "unknown")
                client_version = client_info.get("version", "unknown")
                protocol_version = params.get("protocolVersion", "unknown")
                logger.info(f"客户端: {client_name} {client_version}, 协议版本: {protocol_version}")
                
                # 创建正确的初始化响应
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": protocol_version,
                        "serverInfo": {
                            "name": "pubchem-mcp-server",
                            "version": "1.0.0"
                        },
                        "capabilities": {
                            "tools": {}
                        }
                    }
                }
                
            elif method == "list_tools":
                logger.info("处理工具列表请求")
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "tools": [
                            {
                                "name": "get_pubchem_data",
                                "description": "检索化合物结构和属性数据",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "query": {
                                            "type": "string",
                                            "description": "化合物名称或 PubChem CID",
                                        },
                                        "format": {
                                            "type": "string",
                                            "description": "输出格式，选项: 'JSON', 'CSV', 或 'XYZ', 默认: 'JSON'",
                                            "enum": ["JSON", "CSV", "XYZ"],
                                        },
                                        "include_3d": {
                                            "type": "boolean",
                                            "description": "是否包含3D结构信息（仅当format为'XYZ'时有效），默认: false",
                                        },
                                    },
                                    "required": ["query"],
                                },
                            },
                            {
                                "name": "hello_world",
                                "description": "简单的测试函数，返回问候消息",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "name": {
                                            "type": "string",
                                            "description": "要问候的名称",
                                        }
                                    }
                                }
                            }
                        ]
                    }
                }
            elif method == "call_tool":
                logger.info("处理工具调用请求")
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                if not tool_name:
                    logger.warning("缺少工具名称")
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32602,
                            "message": "Invalid params: missing tool name"
                        }
                    }
                elif tool_name == "get_pubchem_data":
                    result = handle_get_pubchem_data(arguments)
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": result
                    }
                elif tool_name == "hello_world":
                    result = handle_hello_world(arguments)
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": result
                    }
                else:
                    logger.warning(f"未知工具: {tool_name}")
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32601,
                            "message": f"Tool not found: {tool_name}"
                        }
                    }
            else:
                logger.warning(f"未知方法: {method}")
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
            
            # 序列化响应
            response_json = json.dumps(response)
            logger.debug(f"发送响应: {response_json}")
            
            # 写入 stdout 并立即刷新
            sys.stdout.write(response_json + "\n")
            sys.stdout.flush()
            
            logger.info(f"已发送响应: method={method}, id={request_id}")
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON 解析错误: {e}")
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": "Parse error: Invalid JSON"
                }
            }
            sys.stdout.write(json.dumps(error_response) + "\n")
            sys.stdout.flush()
            
        except Exception as e:
            logger.error(f"未处理的异常: {e}")
            logger.error(traceback.format_exc())
            try:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": request_id if 'request_id' in locals() else None,
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    }
                }
                sys.stdout.write(json.dumps(error_response) + "\n")
                sys.stdout.flush()
            except:
                logger.error("发送错误响应失败")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"致命错误: {e}")
        logger.critical(traceback.format_exc())
