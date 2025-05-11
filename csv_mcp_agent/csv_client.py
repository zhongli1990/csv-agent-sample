import asyncio
import nest_asyncio
import pandas as pd
from langchain import hub
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import render_text_description
from langchain_experimental.agents import create_pandas_dataframe_agent
from mcp import ClientSession
from mcp.client.sse import sse_client
from langchain_mcp_adapters.tools import load_mcp_tools

nest_asyncio.apply()  # Needed to run interactive python

"""
Make sure:
1. The server is running before running this script.
2. The server is configured to use SSE transport.
3. The server is listening on port 8050.

To run the server:
uv run server.py
"""

model = ChatOllama(model="llama3.2")


async def main():
    # Connect to the server using SSE
    async with sse_client("http://localhost:8050/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()

            tools = await load_mcp_tools(session)
            print(f"Tools: {tools}")
            _input = "List all columns for 'C:\\Users\\Wriddhirup Dutta\\coding\\excel-agent\\app\\notebooks\\data.csv'"
            agent = create_react_agent(model, tools)
            agent_response = await agent.ainvoke({"messages": _input})
            agent_message = agent_response["messages"][-1].content
            print(agent_message)




if __name__ == "__main__":
    asyncio.run(main())
