import os.path
from typing import Union

from mcp.server.fastmcp import FastMCP, Context
from pandas import DataFrame
import pandas as pd

mcp = FastMCP("CSV Server Stdio")

@mcp.tool()
async def read_csv(file_path: str) -> Union[str, DataFrame]:
    """
        Read a CSV file and return the DataFrame
    :param file_path:
    :return: DataFrame
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print("Error reading CSV file: %s", e)
        return f"Error reading CSV file: {e}"

@mcp.tool()
def list_columns(file_path: str) -> Union[str, list]:
    """
        List the columns of the DataFrame
    :param file_path:
    :return: List of columns in the DataFrame
    """
    try:
        data = pd.read_csv(file_path)
        return data.columns.to_list()
    except Exception as e:
        print("Error listing columns in CSV file: %s", e)
        return f"Error reading CSV file: {e}"

@mcp.tool()
def describe(file_path: str) -> Union[str, DataFrame]:
    """
        Describe the DataFrame
    :param file_path:
    :return: Description of the DataFrame
    """
    try:
        data = pd.read_csv(file_path)
        return data.describe()
    except Exception as e:
        print("Error describing CSV file: %s", e)
        return f"Error reading CSV file: {e}"

@mcp.prompt(name="visualize_csv")
def visualize_csv():
    """
        Visualize the DataFrame with matplotlib based on the plot type specified
        Your goal is to generate Python scripts that visualize data using matplotlib. Follow these rules:
        The needed libraries are already part of the running environment, so you don't need to install them.

        1. Always import the necessary libraries at the top:
            ```python
            import matplotlib.pyplot as plt
            import pandas as pd
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
    pass


# Run the server
if __name__ == "__main__":
    mcp.run(transport="stdio")
