#!/

import asyncio
import os
from fastmcp import Client
from mcp.types import Resource
from typing import List

import boto3
from botocore.config import Config

import dotenv

# Load AWS Credentials from ENV
dotenv.load_dotenv()

BEDROCK_MODEL_ID = 'amazon.nova-lite-v1:0'

# Expected Credentials
# AWS_BEARER_TOKEN_BEDROCK
# or
# Configured IAM Role for Service
# or
# AWS_SECRET_ACCESS_KEY (not recommended)
# AWS_ACCESS_KEY_ID (not recommended)
# or
# Configured AWS CLI 


class MCPClient():
    """
        MCP Client for interacting with a MCP Resource Server using Bedrock AI.

        The Client is using FastMCP framework to connect to the MCP Server. 
    """
            
    def __init__(self, mcp_server_script: str):
        
        config = Config(
            region_name = 'us-east-1'
        )
        
        self.bedrock_client = boto3.client(
            'bedrock-runtime',
            config=config
        )

        assert os.path.isfile(mcp_server_script), 'MCP Server Script not Found'

        self.client = Client(mcp_server_script)
    
    
    def _get_resource(self, resources: List[Resource], resource_name: str) -> Resource:
        """Identify and return a specific resource by name.

        Args:
            resources (List[Resource]): List of available resources or resource templates.
            resource_name (str): Name of the resource to find.

        Raises:
            KeyError: If the resource is not found.

        Returns:
            Resource: The requested resource.
        """
            
        for resource in resources:
            if resource_name == resource.name:
                return resource
        else:
            raise KeyError(f'Resource {resource_name} not found')
        
    
    async def run(self, query: str, reference_year: int, reference_month: str) -> str:
        """
        Run the MCP Client to analyze sales data for a specific month and year.
        Args:
            query (str): User's query about the sales data.
            reference_year (int): Year for the sales data.
            reference_month (str): Month for the sales data.
            
        Returns:
            str: Response from the Bedrock AI model based on the sales data and user query.
            
        Raises:
            Exception: If there is an error during the process.
        """
        
        # Initialize the connection to MCP Server
        async with self.client:
            
            # Ping Server to check connection
            await self.client.ping()
            
            # List resources
            resources = await self.client.list_resources()
            print("Available Resources:")
            for resource in resources:
                print(f"- {resource.name}: {resource.description}")

            resource_templates = await self.client.list_resource_templates()
            print("Available Resources Templates")
            for template in resource_templates:
                print(f"- {template.name}: {template.description}")

            readme_resource = self._get_resource(resources, 'README')
            readme_content = await self.client.read_resource(readme_resource.uri)
            
            # Create system prompt
            system_prompts = [{"text": 
                f"""
                You are a smart assistant that analyzes monthly sales data.
                
                More Information in the MCP Resources:
                
                {readme_content}
                """}]
            
            # Get sales resource
            sales_data_resource = self._get_resource(resource_templates, 'get_sales')
            
            resource_uri = sales_data_resource.uriTemplate.format(year = reference_year, month = reference_month)
            try:
                month_sales = await self.client.read_resource(resource_uri)
            except Exception as e:
                print(f"Error fetching sales data: {e}")
                sys.exit(1)
            
            messages = [
                {
                'role' : 'user',
                'content' : [
                    {'text' : f"""
                    {query}

                    Sales Data:
                    {month_sales}
                """}]            
                }
            ]
            
            # Pass data to Bedrock Converse API together with query
            response = self.bedrock_client.converse(
                modelId=BEDROCK_MODEL_ID,
                messages=messages,
                system=system_prompts,
            )
            
            model_response = response['output']['message']['content'][0]['text']
            
            return model_response            


async def main():
    
    if len(sys.argv) < 2:
        print("Usage: python io_resources_client_bedrock.py <path_to_server_script>")
        sys.exit(1)

    print("Starting the MCP Client for EvoResourceServer")
    month = input("Enter the month for analysis (e.g., 'january'): ").strip().lower()
    year = int(input("Enter the year for analysis (e.g., 2025): ").strip())
    query = input("Enter your query about the sales data: ").strip()
    
    print("\n\nGetting Results...\n\n")
    
    client = MCPClient(sys.argv[1])

    res = await client.run(query=query,
                            reference_year = int(year),
                            reference_month = month)        
    
    print(res)    
    

if __name__ == "__main__":
    import sys
    asyncio.run(main())
