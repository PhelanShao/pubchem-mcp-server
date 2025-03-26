"""
PubChem MCP Server

Implements a Model Context Protocol (MCP) server that provides PubChem compound data retrieval functionality.

Note: This module requires the MCP SDK to be installed. Since the MCP SDK may not be publicly available on PyPI,
you may need to install it manually. Please refer to the MCP documentation for how to install the MCP SDK.

If you don't have the MCP SDK installed, you can still use the command line interface (cli.py) to retrieve PubChem data.
"""

import json
import logging
import signal
import sys
from typing import Any, Dict, List, Optional, Union

# Try to import MCP SDK, provide a simplified version of the server if not available
try:
    from mcp.server import Server
    from mcp.server.stdio import StdioServerTransport
    from mcp.types import (
        CallToolRequest,
        ListToolsRequest,
        McpError,
        INVALID_REQUEST,
        METHOD_NOT_FOUND,
        INVALID_PARAMS,
    )
    MCP_SDK_AVAILABLE = True
except ImportError:
    MCP_SDK_AVAILABLE = False
    print("Warning: MCP SDK is not installed, server functionality will not be available.")
    print("You can still use the command line interface (pubchem-mcp) to retrieve PubChem data.")

from .pubchem_api import get_pubchem_data
from .async_processor import get_processor

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class PubChemServer:
    """PubChem MCP Server class"""
    
    def __init__(self):
        """Initialize PubChem MCP server"""
        self.server = Server(
            {
                "name": "pubchem-server",
                "version": "1.0.0",
            },
            {
                "capabilities": {
                    "tools": {},
                },
            }
        )
        
        self.setup_tool_handlers()
        
        # Error handling
        self.server.onerror = lambda error: logger.error(f"[MCP Error] {error}")
        signal.signal(signal.SIGINT, self.handle_sigint)
    
    def handle_sigint(self, sig, frame):
        """Handle SIGINT signal"""
        logger.info("Received interrupt signal, shutting down server...")
        self.server.close()
        sys.exit(0)
    
    def setup_tool_handlers(self):
        """Set up tool handlers"""
        self.server.set_request_handler(ListToolsRequest, self.handle_list_tools)
        self.server.set_request_handler(CallToolRequest, self.handle_call_tool)
    
    async def handle_list_tools(self, request):
        """Handle list tools request"""
        return {
            "tools": [
                {
                    "name": "get_pubchem_data",
                    "description": "Retrieve compound structure and property data",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Compound name or PubChem CID",
                            },
                            "format": {
                                "type": "string",
                                "description": "Output format, options: 'JSON', 'CSV', or 'XYZ', default: 'JSON'",
                                "enum": ["JSON", "CSV", "XYZ"],
                            },
                            "include_3d": {
                                "type": "boolean",
                                "description": "Whether to include 3D structure information (only valid when format is 'XYZ'), default: false",
                            },
                        },
                        "required": ["query"],
                    },
                },
                {
                    "name": "submit_pubchem_request",
                    "description": "Submit asynchronous request for PubChem data (useful for slower queries)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Compound name or PubChem CID",
                            },
                            "format": {
                                "type": "string",
                                "description": "Output format, options: 'JSON', 'CSV', or 'XYZ', default: 'JSON'",
                                "enum": ["JSON", "CSV", "XYZ"],
                            },
                            "include_3d": {
                                "type": "boolean",
                                "description": "Whether to include 3D structure information (only valid when format is 'XYZ'), default: false",
                            },
                        },
                        "required": ["query"],
                    },
                },
                {
                    "name": "get_request_status",
                    "description": "Get status of an asynchronous PubChem data request",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "request_id": {
                                "type": "string",
                                "description": "Request ID returned from submit_pubchem_request",
                            },
                        },
                        "required": ["request_id"],
                    },
                },
            ],
        }
    
    async def handle_call_tool(self, request):
        """Handle call tool request"""
        tool_name = request.params.name
        args = request.params.arguments
        
        # Handle get_pubchem_data (synchronous)
        if tool_name == "get_pubchem_data":
            if not args.get("query"):
                raise McpError(
                    INVALID_PARAMS,
                    "Missing required parameter: query"
                )
            
            try:
                # Check if XYZ format requires include_3d parameter
                if args.get("format", "").upper() == "XYZ" and not args.get("include_3d"):
                    return {
                        "content": [
                            {
                                "type": "text",
                                "text": "When using XYZ format, the include_3d parameter must be set to true",
                            },
                        ],
                        "isError": True,
                    }
                
                result = get_pubchem_data(
                    args.get("query"),
                    args.get("format", "JSON"),
                    args.get("include_3d", False)
                )
                
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": result,
                        },
                    ],
                }
            except Exception as e:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Error: {str(e)}",
                        },
                    ],
                    "isError": True,
                }
                
        # Handle submit_pubchem_request (asynchronous)
        elif tool_name == "submit_pubchem_request":
            if not args.get("query"):
                raise McpError(
                    INVALID_PARAMS,
                    "Missing required parameter: query"
                )
            
            try:
                # Check if XYZ format requires include_3d parameter
                if args.get("format", "").upper() == "XYZ" and not args.get("include_3d"):
                    return {
                        "content": [
                            {
                                "type": "text",
                                "text": "When using XYZ format, the include_3d parameter must be set to true",
                            },
                        ],
                        "isError": True,
                    }
                
                # Submit to async processor
                processor = get_processor()
                request_id = processor.submit_request(
                    args.get("query"),
                    args.get("format", "JSON"),
                    args.get("include_3d", False)
                )
                
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps({
                                "request_id": request_id,
                                "message": "Request submitted successfully. Use get_request_status with this request_id to check the status."
                            }, indent=2),
                        },
                    ],
                }
            except Exception as e:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Error submitting request: {str(e)}",
                        },
                    ],
                    "isError": True,
                }
                
        # Handle get_request_status
        elif tool_name == "get_request_status":
            if not args.get("request_id"):
                raise McpError(
                    INVALID_PARAMS,
                    "Missing required parameter: request_id"
                )
            
            try:
                processor = get_processor()
                status = processor.get_status(args.get("request_id"))
                
                if status is None:
                    return {
                        "content": [
                            {
                                "type": "text",
                                "text": f"Request ID not found: {args.get('request_id')}",
                            },
                        ],
                        "isError": True,
                    }
                
                # Return status
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(status, indent=2),
                        },
                    ],
                }
            except Exception as e:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Error getting request status: {str(e)}",
                        },
                    ],
                    "isError": True,
                }
        else:
            raise McpError(
                METHOD_NOT_FOUND,
                f"Unknown tool: {tool_name}"
            )
    
    async def run(self):
        """Run the server"""
        # Initialize processor
        get_processor()
        
        transport = StdioServerTransport()
        await self.server.connect(transport)
        logger.info("PubChem MCP server running on stdio")


def main():
    """Main function"""
    if not MCP_SDK_AVAILABLE:
        print("Error: MCP SDK is not installed, cannot start server.")
        print("Please install the MCP SDK and try again, or use the command line interface (pubchem-mcp) to retrieve PubChem data.")
        
        # Instead of exiting, try to run the command line interface
        from .cli import main as cli_main
        print("Falling back to command line interface...")
        cli_main()
        return
    
    import asyncio
    
    # Set logging level
    logging.basicConfig(level=logging.INFO)
    
    try:
        # Create and run server
        server = PubChemServer()
        asyncio.run(server.run())
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)
    finally:
        # Shutdown processor if server closes
        try:
            processor = get_processor()
            processor.shutdown()
        except Exception:
            pass


if __name__ == "__main__":
    main()
