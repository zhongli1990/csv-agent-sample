import asyncio
import os.path
import re
import traceback
from typing import Any
from uuid import uuid4

from langchain_core.messages.utils import count_tokens_approximately
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt.chat_agent_executor import AgentState
from langmem.short_term import SummarizationNode

model = ChatOllama(model="llama3.2", temperature=0)

summarization_node = SummarizationNode(
    token_counter=count_tokens_approximately,
    model=model,
    max_tokens=384,
    max_summary_tokens=128,
    output_messages_key="llm_input_messages",
)

class State(AgentState):
    context: dict[str, Any]


checkpointer = InMemorySaver()

def extract_python_code(text):
    """
    Extracts the first Python code block (inside triple backticks with 'python') from a string.
    """
    match = re.search(r"```python(.*?)```", text, re.DOTALL)
    return match.group(1).strip() if match else None

create_resource = False

async def run_agent(command: str = ""):
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
        agent = create_react_agent(
            model=model,
            tools=tools,
            pre_model_hook=summarization_node,
            state_schema=State,
            checkpointer=checkpointer,
        )
        agent_response = await agent.ainvoke(
            {"messages": [
                {"role": "user", "content": f'{command}'},
            ]},
            config={"configurable": {"thread_id": uuid4()}},
        )
        agent_message = agent_response["messages"][-1].content
        # Extract Python code from the agent's response
        python_code = extract_python_code(agent_message)
        if python_code:
            try:
                print("Extracted Python code... \n", python_code)
                exec(python_code)
            except Exception as e:
                print(traceback.print_exc())
                print(f"Error executing extracted Python code: {e}")
        print("agent_message: ", agent_message)


if __name__ == "__main__":
    asyncio.run(run_agent())
