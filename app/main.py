import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.mcp_module.client.stdio_client import run_agent

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

if __name__ == "__main__":
    while True:
        try:
            command = input("Enter your command for the CSV Agent (type 'exit' to exit the agent): \n> ")
            if command.lower() == "exit":
                print("Exiting CSV agent...")
                break
            result = loop.run_until_complete(run_agent(command))
            print(result)
        except Exception as e:
            print(f"Error occurred: {e}")
            break
