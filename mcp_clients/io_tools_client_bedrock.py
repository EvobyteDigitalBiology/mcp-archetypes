#!/

import os
import asyncio
from typing import Optional, List
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import boto3
from botocore.config import Config


import dotenv

# Load AWS Credentials from ENV
dotenv.load_dotenv()

# Expected Credentials
# AWS_BEARER_TOKEN_BEDROCK
# or
# Configured IAM Role for Service
# or
# AWS_SECRET_ACCESS_KEY (not recommended)
# AWS_ACCESS_KEY_ID (not recommended)
# or
# Configured AWS CLI 

BEDROCK_MODEL_ID = 'amazon.nova-lite-v1:0'

class MCPClient():
    
    def __init__(self):
        
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        
        config = Config(
            region_name = 'us-east-1'
        )
        
        self.bedrock_client = boto3.client(
            'bedrock-runtime',
            config=config
        )
    
    async def get_available_tools(self) -> List[dict]:
        """Return a list of available tools

        Returns:
            List[dict]: Available tools
            
            Format
                {'name' : ,
                'description' ,
                'inputSchema'}
        """
        
        response = await self.session.list_tools()
        
        available_tools = [{
            'name' : tool.name,
            'description' : tool.description,
            'inputSchema': tool.inputSchema
        } for tool in response.tools]
        
        return available_tools


    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP Server

        Args:
            server_script_path (python script)
        """
        
        server_script_path = os.path.abspath(
            server_script_path
        )
        
        server_params = StdioServerParameters(
            command = 'python3',
            args=[server_script_path]
        )
        
        # Opens Process
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        
        self.stdio, self.write = stdio_transport
        
        # Create Client to Connect To
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()
        
        tools = await self.get_available_tools()
        
        print("\nConnected to server with tools:", [tool['name'] for tool in tools])
    
    
    async def process_query(self, query: str) -> str:
        """
            Process Input Query and Tool Usage using Bedrock Converse API
        """
            
        messages = [
            {
                'role' : 'user',
                'content' : [{'text' : query}]            
            }
        ]
        
        system_prompts = [{"text": """
                           You are an app that returns information on the weather in the US. 
                           If queries are not related to wheather return the message "I am just a simple weather app :( ).
                           When using tools, infer required arguments from user inputs and do not ask user again".
                           """}]
        
        tools = await self.get_available_tools()
        
        # Bedrock Tools config for Converse API
        # Format MCP Server reponse to Bedrock ToolConfiguration https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ToolConfiguration.html
        
        tools_specs = []
        for tool in tools:
            tools_spec = { 'toolSpec' :
                {
                    'name' : tool['name'],
                    'description' : tool['description'],
                    'inputSchema' : {
                        'json' : tool['inputSchema']
                    }
                }
            }
            tools_specs.append(tools_spec)
        
        
        tool_config = {
            "tools" : tools_specs
        }
                
        response = self.bedrock_client.converse(
            modelId=BEDROCK_MODEL_ID,
            messages=messages,
            system=system_prompts,
            toolConfig=tool_config
        )

        # Converse Output Structure
        
        # { 'ResponseMetadata' :
        #        'output'
        #           'message'
        #               'content' [{}]
        
        # Process response and handle tool calls
        
        final_text = []
        
        assistant_message_content = []
        
        # response['output']['message']['content']: List of contents
        # content structure example: {'text': 'Reponse Text'}
        for content in response['output']['message']['content']:
            
            if 'text' in content:
                final_text.append(content['text'])
                assistant_message_content.append(content)
           
            if 'toolUse' in content:
                tool_name = content['toolUse']['name']
                tool_args = content['toolUse']['input']
                tool_use_id = content['toolUse']['toolUseId']
                
                tool_result = await self.session.call_tool(tool_name, tool_args)
                
                # Reformat tool_result content
                tool_result_content = []
                for res in tool_result.content:
                    if res.type == 'text':
                        tool_result_content.append({
                            'text' : res.text
                        })
                
                final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")
                
                assistant_message_content.append(content)
                
                messages.append({
                    "role" : "assistant",
                    "content": assistant_message_content
                })
                messages.append({
                    "role" : "user",
                    "content": [
                        {
                            "toolResult" : {
                                "toolUseId": tool_use_id,
                                "content": tool_result_content
                            }
                        }
                    ]
                    })
                
                # Invoke Model with Tool results
                response = self.bedrock_client.converse(
                    modelId=BEDROCK_MODEL_ID,
                    messages=messages,
                    system=system_prompts,
                    toolConfig=tool_config
                )
                
                final_text.append(response['output']['message']['content'][0]['text'])
        
        return "\n".join(final_text)
        
    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

    async def chat_loop(self):
        """Print start an interactive chat loop"""
        
        print("\n\nThe MCP Weather Client Started")
        print("Type your weather-releated queries or 'quit'")
        
        while True:
            try:
                query = input("\nQuery: ").strip()
                
                if query.lower() == 'quit':
                    break
                
                response = await self.process_query(query)
                
                print("\n" + response)
                
            except Exception as e:
               print(f"\nError: {str(e)}") 


async def main():
    if len(sys.argv) < 2:
        print("Usage: python io_tools_client_bedrock.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])        
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    import sys
    asyncio.run(main())
    
    