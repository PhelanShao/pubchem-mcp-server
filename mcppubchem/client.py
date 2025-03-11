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
                logging.info("调用 get_pubchem_data...")
                result = await session.call_tool("get_pubchem_data", {"query": "aspirin", "format": "JSON"})
                print("返回结果:", result)
    except Exception as e:
        logging.error(f"发生错误: {e}")

if __name__ == "__main__":
    asyncio.run(test())
