from pathlib import Path
import os
import pandas as pd

from fastmcp import FastMCP
from fastmcp.resources import FileResource

import boto3
from botocore.config import Config

# Initialize FastMCP server
mcp = FastMCP(
    "ResourceServer"
)

# Define file paths
base_path = Path(__file__).parent
readme_path = base_path / Path("data/README.md")
sales_base_path = base_path / Path("data/sales_data")

# Add static resource for README file
readme_resource = FileResource(
    uri=f"file:///{readme_path}",
    path=readme_path,
    name="README",
    description='ReadMe File for MCP Server',
    mime_type="text/markdown",
    tags={"documentation"}
)
mcp.add_resource(readme_resource)

# Create a resource template / dynamic resource for sales data
# Template URI includes {city} placeholder
@mcp.resource(uri="resource://sales/{year}/{month}",
              name = 'get_sales',
              description = 'Provides Sales Stats per month and per year',
              mime_type = "application/json",
              tags = {"statistics"})
def get_sales(year: int, month: str) -> dict:
    
    month = month.lower()
    sales_csv_file = sales_base_path / Path(month + '_' + str(year) + '.csv')

    if os.path.isfile(sales_csv_file):
        data = pd.read_csv(sales_csv_file, sep=',')
        return data.to_dict(orient='records')
    else:
        raise FileNotFoundError(f"Sales data for {month} {year} not found at {sales_csv_file.as_posix()}. Month must be written, month must be numeric")
    
    
if __name__ == "__main__":
    
    # Initialize and run the server
    mcp.run(transport='stdio')