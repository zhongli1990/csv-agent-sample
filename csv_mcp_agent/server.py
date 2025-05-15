from typing import Union, Any

from mcp.server.fastmcp import FastMCP
from pandas import DataFrame
import pandas as pd
import matplotlib.pyplot as plt

# csv_mcp = FastMCP("CSV Server SSE", host="127.0.0.1", port=8050)
mcp = FastMCP("CSV Server Stdio")
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
        return f"Error reading CSV file: {e}"


@mcp.tool()
def visualize(file_path: str, plot_type: str, plot_column: str) -> str:
    """
        Visualize the DataFrame with matplotlib
    :param file_path:
    :param plot_type: Type of plot to create (e.g., 'line', 'bar', 'scatter')
    :param plot_column: Column to plot
    :return: Plot of the DataFrame
    """

    try:
        data = pd.read_csv(file_path)
        if plot_type == "line":
            plt.plot(data[plot_column])
        elif plot_type == "bar":
            plt.bar(data.index, data[plot_column])
        elif plot_type == "scatter":
            plt.scatter(data.index, data[plot_column])
        else:
            return "Invalid plot type. Use 'line', 'bar', or 'scatter'."

        plt.xlabel("Index")
        plt.ylabel(plot_column)
        plt.title(f"{plot_type.capitalize()} Plot of {plot_column}")
        plt.show()
        return "Plot displayed successfully."
    except Exception as e:
        return f"Error reading CSV file: {e}"

# Run the server
if __name__ == "__main__":
    mcp.run(transport="stdio")
