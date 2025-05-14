import asyncio
import os.path

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama

model = ChatOllama(model="llama3.2", temperature=0)

# os.chdir("../../..")

async def run_agent():
    async with MultiServerMCPClient(
        {
            "csv_server": {
                "command": "python",
                "args": [os.path.join(os.getcwd(), "mcp_module", "servers", "csv_server.py")],
                "transport": "stdio",
            }
        }
    ) as session:
        tools = session.get_tools()
        print(f"Tools: {tools}")
        _input = input("Enter your input: ")
        agent = create_react_agent(model, tools)
        agent_response = await agent.ainvoke({"system": "You are a helpful assistant and give descriptive answers", "messages": _input})
        agent_message = agent_response["messages"][-1].content
        print(agent_message)


if __name__ == "__main__":
    asyncio.run(run_agent())
