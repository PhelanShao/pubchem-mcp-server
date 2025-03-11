from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 建立与服务器的连接并调用工具
server_params = StdioServerParameters(
    command='python',
    args=['server.py']  # 服务器脚本路径
)

async def test():
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # 测试JSON格式
                logging.info("测试1: 获取JSON格式数据...")
                result = await session.call_tool("get_pubchem_data", {
                    "query": "aspirin",
                    "format": "JSON"
                })
                print("\nJSON格式结果:", result)
                
                # 测试CSV格式
                logging.info("\n测试2: 获取CSV格式数据...")
                result = await session.call_tool("get_pubchem_data", {
                    "query": "aspirin",
                    "format": "CSV"
                })
                print("\nCSV格式结果:", result)
                
                # 测试XYZ格式（包含3D结构）
                logging.info("\n测试3: 获取XYZ格式数据（包含3D结构）...")
                result = await session.call_tool("get_pubchem_data", {
                    "query": "aspirin",
                    "format": "XYZ",
                    "include_3d": True
                })
                print("\nXYZ格式结果:", result)

    except Exception as e:
        logging.error(f"发生错误: {e}")

if __name__ == "__main__":
    asyncio.run(test())
