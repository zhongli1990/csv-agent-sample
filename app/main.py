import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.mcp_module.client.stdio_client import run_agent
from app.utils.logger import logger



if __name__ == "__main__":
    logger.info("Starting CSV MCP Client...")
    asyncio.run(run_agent())