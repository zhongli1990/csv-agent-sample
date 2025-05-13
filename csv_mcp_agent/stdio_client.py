import asyncio
import os.path

from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from mcp import ClientSession, StdioServerParameters, stdio_client
from mcp.client.sse import sse_client
from langchain_mcp_adapters.tools import load_mcp_tools

model = ChatOllama(model="llama3.2")

server_params = StdioServerParameters(
    command="python",
    args=[os.path.join(os.path.dirname(__file__), "server.py")]
)

async def main():
    # Connect to the server using SSE
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()

            tools = await load_mcp_tools(session)
            print(f"Tools: {tools}")
            _input = input("Enter your input: ")
            agent = create_react_agent(model, tools)
            agent_response = await agent.ainvoke({"system": "You are a helpful assistant and give descriptive answers", "messages": _input})
            agent_message = agent_response["messages"][-1].content
            print(agent_message)


if __name__ == "__main__":
    asyncio.run(main())
