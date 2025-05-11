import asyncio
import nest_asyncio
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import render_text_description
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

            tools=await load_mcp_tools(session)
            print(f"Tools: {tools}")

            prompt = hub.pull("hwchase17/react-json")
            prompt = prompt.partial(
                tools=render_text_description(tools),
                tool_names=", ".join([t.name for t in tools]),
            )
            print(f"Prompt: {prompt}")

            agent = create_react_agent(model, tools, prompt)

            print(agent)

            agent_executor = AgentExecutor(agent=agent, tools=tools, handle_parsing_errors=True, verbose=True, format="json")

            agent_response = agent_executor.invoke({"input": "what's (700 + 6000)"})
            print(f"6+90 = {agent_response["output"]}")



if __name__ == "__main__":
    asyncio.run(main())