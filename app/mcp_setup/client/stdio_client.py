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

# Model selection (uncomment to switch models)
# model = ChatOllama(model="llama3.2", temperature=0)  # Llama 3.2 8B (default)
# model = ChatOllama(model="qwen3:8b", temperature=0)  # Qwen3 8B
# model = ChatOllama(model="deepseek-coder:6.7b-instruct", temperature=0)  # DeepSeek Coder 6.7B
# model = ChatOllama(model="stablelm2:12b", temperature=0)  # StableLM2 12B
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

async def get_intent_of_user_ask(command: str) -> str:
    """
    Determines the intent of the user's command.
    :param command: The command string from the user.
    :return: A string indicating the intent.
    """
    system_prompt = """

    You are a CSV file processing assistant. Your task is to determine the intent of the user's command.
    If the command is related to CSV file analysis, return "describe".
    If the command is related to CSV file visualization, return "visualize".
    If the command is related to CSV file preview, return "preview".
    """

    # Create a prompt for the model
    prompt = f"{system_prompt}\nUser command: {command}\nIntent:"
    # Get the model's response
    response = await model.ainvoke(prompt)
    print(f"Intent: {response.text()}")
    return response.text().lower()

async def run_agent(command: str = ""):
    intent = await get_intent_of_user_ask(command)
    async with MultiServerMCPClient(
        {
            "csv_server": {
                "command": "python",
                "args": [os.path.join(os.getcwd(), "app", "mcp_setup", "servers", "csv_server.py")],
                "transport": "stdio",
            }
        }
    ) as session:
        tools = session.get_tools()

        prompt: str = ""
        if "visualize" in intent:
            visualize_prompt = await session.get_prompt(
                server_name="csv_server",
                prompt_name="visualize_csv",
                arguments={"input": command},
            )
            prompt = visualize_prompt[0].content if visualize_prompt else ""

        print(f"Prompt: {prompt}")
        structured_prompt = {"messages": prompt if prompt else command}
        agent = create_react_agent(
            model=model,
            tools=tools,
            pre_model_hook=summarization_node,
            state_schema=State,
            checkpointer=checkpointer,
        )
        agent_response = await agent.ainvoke(
            input=structured_prompt,
            config={"configurable": {"thread_id": uuid4()}},
        )
        agent_message = agent_response["messages"][-1].content
        # Extract Python code from the agent's response
        python_code = extract_python_code(agent_message)
        if python_code:
            try:
                print("Extracted Python code... \n", python_code)
                # exec(python_code)
                exec(python_code, globals(), globals())
            except Exception as e:
                print(traceback.print_exc())
                print(f"Error executing extracted Python code: {e}")
        print("agent_message: ", agent_message)


if __name__ == "__main__":
    asyncio.run(run_agent())
