import pandas as pd
import matplotlib.pyplot as plt
from typing import TypedDict, Annotated

from langchain.agents import initialize_agent, AgentType, Tool
from langchain_community.chat_models import ChatOllama
from langchain.schema import HumanMessage
from langchain_core.tools import StructuredTool
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, validator
import io, contextlib

# ---- Shared LLM + Storage ----
# llm = ChatOllama(model="llama3.1", temperature=0)
global_df = {"df": None}

from langchain import OpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
import pandas as pd



def create_agent(filename: str):
    """
    Create an agent that can access and use a large language model (LLM).

    Args:
        filename: The path to the CSV file that contains the data.

    Returns:
        An agent that can access and use the LLM.
    """

    # Create an OpenAI object.
    llm = ChatOllama(model="llama3.1", temperature=0)

    # Read the CSV file into a Pandas DataFrame.
    df = pd.read_csv(filename)

    # Create a Pandas DataFrame agent.
    return create_pandas_dataframe_agent(llm, df, verbose=False)


def query_agent(agent, query):
    """
    Query an agent and return the response as a string.

    Args:
        agent: The agent to query.
        query: The query to ask the agent.

    Returns:
        The response from the agent as a string.
    """

    prompt = (
            """
                For the following query, if it requires drawing a table, reply as follows:
                {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...]}}
    
                If the query requires creating a bar chart, reply as follows:
                {"bar": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}
    
                If the query requires creating a line chart, reply as follows:
                {"line": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}
    
                There can only be two types of chart, "bar" and "line".
    
                If it is just asking a question that requires neither, reply as follows:
                {"answer": "answer"}
                Example:
                {"answer": "The title with the highest rating is 'Gilead'"}
    
                If you do not know the answer, reply as follows:
                {"answer": "I do not know."}
    
                Return all output as a string.
    
                All strings in "columns" list and data list, should be in double quotes,
    
                For example: {"columns": ["title", "ratings_count"], "data": [["Gilead", 361], ["Spider's Web", 5164]]}
    
                Lets think step by step.
    
                Below is the query.
                Query: 
                """
            + query
    )

    # Run the prompt through the agent.
    response = agent.run(prompt)

    # Convert the response to a string.
    return response.__str__()


# # ---- Tool: Load CSV ----
# class LoadCSVInput(BaseModel):
#     file_path: str
#
#     @validator("file_path")
#     def validate_file_path(cls, value):
#         if not value.endswith(".csv"):
#             raise ValueError("file_path must point to a .csv file")
#         return value
#
# def load_csv(file_path: str) -> str:
#     try:
#         df = pd.read_csv(file_path)
#         global_df["df"] = df
#         return f"CSV loaded. Columns: {', '.join(df.columns)}"
#     except Exception as e:
#         return f"Error loading CSV: {str(e)}"
#
#
# # ---- Tool: Summarize CSV ----
# def summarize_csv(_: str) -> str:
#     df = global_df.get("df")
#     if df is None:
#         return "CSV not loaded."
#
#     description = df.describe(include="all").to_string()
#     prompt = f"""You are a data analyst. Summarize this CSV dataset based on the pandas describe() output:\n\n{description}"""
#     response = llm([HumanMessage(content=prompt)])
#     return response.content
#
#
# # ---- Tool: Visualize CSV ----
# class VisualizeInput(BaseModel):
#     request: str
#
# def visualize_csv(user_request: str) -> str:
#     df = global_df.get("df")
#     if df is None:
#         return "CSV not loaded."
#
#     system_prompt = (
#         "You're a Python expert. Generate matplotlib code to visualize a DataFrame 'df'. Only return code."
#     )
#     prompt = f"User request: {user_request}"
#
#     response = llm([
#         HumanMessage(content=system_prompt),
#         HumanMessage(content=prompt)
#     ])
#     code = response.content
#
#     try:
#         safe_locals = {"df": df, "plt": plt}
#         with io.StringIO() as buf, contextlib.redirect_stdout(buf):
#             exec(code, {}, safe_locals)
#             output = buf.getvalue()
#         plt.savefig("output.png")
#         plt.close()
#         return f"Chart saved as output.png\n\nCode:\n{code}"
#     except Exception as e:
#         return f"Code error: {e}\n\nCode:\n{code}"
#
#
# # ---- Tool List ----
# tools = [
#     StructuredTool.from_function(
#         name="load_csv",
#         description="Load a CSV from a local file path. Input should be a JSON object with a 'file_path' key.",
#         func=load_csv,
#         args_schema=LoadCSVInput,
#     ),
#     Tool(
#         name="summarize_csv",
#         description="Summarize the loaded CSV using the LLM. Takes no input, just call it.",
#         func=summarize_csv,
#     ),
#     Tool(
#         name="visualize_csv",
#         description="Create a visualization from the CSV. Input should be a user request like 'plot histogram of age'.",
#         func=visualize_csv,
#     ),
# ]
#
#
# # tools = [
# #     Tool.from_function(
# #         name="load_csv",
# #         description="Load a CSV from local path",
# #         func=load_csv,
# #         args_schema=LoadCSVInput,
# #     ),
# #     Tool.from_function(
# #         name="summarize_csv",
# #         description="Summarize the loaded CSV using the LLM",
# #         func=summarize_csv,
# #     ),
# #     Tool.from_function(
# #         name="visualize_csv",
# #         description="Create a visualization based on the user's request",
# #         func=visualize_csv,
# #         args_schema=VisualizeInput,
# #     ),
# # ]
#
#
# # ---- LangChain Agent ----
# agent_executor = initialize_agent(
#     tools=tools,
#     llm=llm,
#     agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True,
# )
#
#
# # ---- LangGraph Setup ----
# class AgentState(TypedDict):
#     input: str
#     output: str
#
# def invoke_agent(state: AgentState) -> AgentState:
#     result = agent_executor.run(state["input"])
#     return {"input": state["input"], "output": result}
#
# graph = StateGraph(AgentState)
# graph.add_node("agent", invoke_agent)
# graph.set_entry_point("agent")
# graph.set_finish_point("agent")
#
# app = graph.compile()
#
#
# # ---- Run Agent with Prompt ----
# if __name__ == "__main__":
#     print("👋 Hello! You can now type commands like:")
#     print(" - load_csv with path: 'data.csv'")
#     print(" - summarize_csv")
#     print(" - visualize_csv to 'plot a histogram of age'")
#
#     while True:
#         user_input = input("\n📥 Your command: ")
#         if user_input.lower() in ["exit", "quit"]:
#             break
#         result = app.invoke({"input": user_input})
#         print("\n📤 Agent Output:\n", result["output"])
