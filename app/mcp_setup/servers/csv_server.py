from typing import Union

from mcp.server.fastmcp import FastMCP
from pandas import DataFrame
import pandas as pd

mcp = FastMCP("CSV Server Stdio")

@mcp.tool()
def preview_csv(file_path: str, n_rows: int = 5) -> Union[str, DataFrame]:
    """
        Preview the first n rows of the DataFrame
    :param file_path:
    :param n_rows:
    :return: First n rows of the DataFrame in dataframe format
    """
    try:
        data = pd.read_csv(file_path)
        return data.head(n_rows)
    except Exception as e:
        print("Error previewing CSV file: %s", e)
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

@mcp.tool()
def filter_csv(file_path: str, column: str, value: str) -> Union[str, DataFrame]:
    """
        Filter the DataFrame based on a column and value
    :param file_path:
    :param column:
    :param value:
    :return: Filtered DataFrame
    """
    try:
        data = pd.read_csv(file_path)
        filtered_data = data[data[column] == value]
        return filtered_data
    except Exception as e:
        print("Error filtering CSV file: %s", e)
        return f"Error reading CSV file: {e}"

@mcp.tool()
def write_to_csv(file_path: str, row_data: dict) -> Union[str, DataFrame]:
    """
        Add a new row to the DataFrame and save it to a new CSV file
    :param file_path:
    :param row_data:
    :return: Updated DataFrame
    """
    try:
        data = pd.read_csv(file_path)
        data = data.append(row_data, ignore_index=True)
        file_name = file_path.split("/")[-1]
        file_path = file_path.replace(file_name, "new_" + file_name)
        data.to_csv(file_path, index=False)
        return data
    except Exception as e:
        print("Error adding row to CSV file: %s", e)
        return f"Error reading CSV file: {e}"

# Run the server
if __name__ == "__main__":
    mcp.run(transport="stdio")
