import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.mcp_module.client.stdio_client import run_agent

async def main():
    print("Starting CSV MCP Client...")
    while True:
        command = input("\nWhat do you want to do with the CSV? (type 'exit' to quit)\n> ")
        if command.lower() == "exit":
            break
        await run_agent(command)

if __name__ == "__main__":
    asyncio.run(main())