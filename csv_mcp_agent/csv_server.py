from typing import Union, Any

from mcp.server.fastmcp import FastMCP
from pandas import DataFrame
import pandas as pd
from pydantic import BaseModel
from pydantic_core import core_schema

mcp = FastMCP("CSV Server", host="127.0.0.1", port=8050)

file_path = "C:\\Users\\Wriddhirup Dutta\\coding\\excel-agent\\app\\notebooks\\data.csv"

df = pd.read_csv(file_path)


class ModelWithDataFrame(BaseModel):
    data: list[dict]

    @classmethod
    def __get_pydantic_core_schema__(
            cls, _source_type: Any, _handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.list_schema(core_schema.dict_schema()),
            python_schema=core_schema.is_instance_schema(pd.DataFrame)
        )


@mcp.tool()
def list_columns() -> Union[str, list]:
    """List the columns of the DataFrame"""
    if df is not None:
        return df.columns.to_list()
    else:
        return "No DataFrame loaded. Please read a CSV file first."


@mcp.resource(f"file:///{file_path}", mime_type="text/csv")
def get_df() -> DataFrame:
    """Get the DataFrame"""
    if df is not None:
        return df
    else:
        return "No DataFrame loaded. Please read a CSV file first."


# Run the server
if __name__ == "__main__":
    print("df: ", df)
    mcp.run(transport="sse")
