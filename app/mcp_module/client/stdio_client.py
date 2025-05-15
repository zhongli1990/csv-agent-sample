import asyncio
import os.path
import re
from typing import Any
from uuid import uuid4

from langchain_core.messages.utils import count_tokens_approximately
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt.chat_agent_executor import AgentState
from langmem.short_term import SummarizationNode

model = ChatOllama(model="llama3.1", temperature=0)

summarization_node = SummarizationNode(
    token_counter=count_tokens_approximately,
    model=model,
    max_tokens=384,
    max_summary_tokens=128,
    output_messages_key="llm_input_messages",
)

class State(AgentState):
    # NOTE: we're adding this key to keep track of previous summary information
    # to make sure we're not summarizing on every LLM call
    context: dict[str, Any]


checkpointer = InMemorySaver()

def extract_python_code(text):
    """
    Extracts the first Python code block (inside triple backticks with 'python') from a string.
    """
    match = re.search(r"```python(.*?)```", text, re.DOTALL)
    return match.group(1).strip() if match else None

create_resource = False

def set_file_path(command: str):
    global create_resource
    if not create_resource:
        # Create a resource for the CSV server
        # This is a workaround for the fact that the CSV server doesn't have a resource
        system_prompt = """
                    You are an assistant that extracts file paths from natural language input.
                    Your task is:
                    - Identify the full file path from the user's message
                    - Output only the path exactly as it appears (do not modify or interpret it)
                    - Do not execute any code or describe the file
                    - If no file path is found, respond with: "No file path found."

                    The file path:
                    - May include spaces
                    - May use backslashes (Windows) or slashes (Unix)
                    - Ends with a file name and extension (e.g., .csv, .xlsx, .json, .txt)

                    Output only the path as plain text — no formatting, no explanation.

                    User Input:

                """
        filename = model.invoke(f"{system_prompt} {command}").text()
        print("filename: ", filename)
        os.environ["CSV_FILE_PATH"] = filename
        print("file_path set: ", os.environ["CSV_FILE_PATH"])
        create_resource = True

visualization_prompt = """
        Visualize the DataFrame with matplotlib based on the plot type specified
        Your goal is to generate Python scripts that visualize data using matplotlib. Follow these rules:
        The needed libraries are already part of the running environment, so you don't need to install them.

        1. Always import the necessary libraries at the top:
            ```python
            import matplotlib.pyplot as plt
            import pandas as pd
            import numpy as np
            ```

        2. Use `plt.figure()` if multiple plots or custom sizing is needed.

        3. Label axes and add titles if the data allows:
            ```python
            plt.title("...")
            plt.xlabel("...")
            plt.ylabel("...")
            ```

        4. Use appropriate chart types:
            - Line plot: `plt.plot(...)`
            - Bar chart: `plt.bar(...)`
            - Scatter: `plt.scatter(...)`
            - Histogram: `plt.hist(...)`
            - Pie chart: `plt.pie(...)`

        5. Always include `plt.tight_layout()` before `plt.show()`.

        6. Do not output explanation or markdown — only raw Python code.

        7. If data is not provided, mock it with reasonable placeholder values using lists.
"""

async def run_agent(command: str = ""):
    # set_file_path(command)
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
        system_prompt = ""
        check_prompt = """
            You are a helpful assistant that determines the type of action to take based on user input.
            If user is asking to visualize or draw a chart or plot, print "visualization"
            If user is asking to describe a CSV file, print "describe"
            If user is asking to list columns in a CSV file, print "list_columns"
        """
        # check_prompt += f"User Input: {command}\n"
        # check_result = model.invoke(check_prompt).text()
        # print("check_result: ", check_result)
        # if "visualization" in check_result:
        #     system_prompt = visualization_prompt
        # print("calling agent...")
        # print("system_prompt: ", system_prompt)
        agent = create_react_agent(
            model=model,
            tools=tools,
            pre_model_hook=summarization_node,
            state_schema=State,
            checkpointer=checkpointer,
            # prompt=system_prompt,
        )
        agent_response = await agent.ainvoke(
            {"messages": [
                {"role": "user", "content": f'{system_prompt} {command}'},
            ]},
            config={"configurable": {"thread_id": uuid4()}},
        )
        agent_message = agent_response["messages"][-1].content
        print("checkpointer: ", checkpointer)
        print("state: ", agent_response)
        # Extract Python code from the agent's response
        python_code = extract_python_code(agent_message)
        if python_code:
            print("Extracted Python code... \n", python_code)
            exec(python_code)
        print("agent_message: ", agent_message)


if __name__ == "__main__":
    asyncio.run(run_agent())
