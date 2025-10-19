import asyncio
from fastmcp import Client, FastMCP
from fastmcp.client.auth import OAuth
import boto3
from botocore.config import Config

import dotenv

# Load AWS Credentials from ENV
dotenv.load_dotenv()

# Define oauth settings for MCP Client
oauth = OAuth(mcp_url="http://localhost:8000/mcp", client_name = "Weather API Client")

config = Config(
            region_name = 'us-east-1'
        )
        
BEDROCK_CLIENT = boto3.client(
    'bedrock-runtime',
    config=config
)

BEDROCK_MODEL_ID = 'amazon.nova-lite-v1:0'


async def process_query(client: Client, query: str) -> str:
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
    
    # Bedrock Tools config for Converse API
    # Format MCP Server reponse to Bedrock ToolConfiguration https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ToolConfiguration.html
    
    tools = await client.list_tools()

    tools_specs = []
    for tool in tools:
        tools_spec = { 'toolSpec' :
            {
                'name' : tool.name,
                'description' : tool.description,
                'inputSchema' : {
                    'json' : tool.inputSchema
                }
            }
        }
        tools_specs.append(tools_spec)
    
    
    tool_config = {
        "tools" : tools_specs
    }
            
    response = BEDROCK_CLIENT.converse(
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
            
            tool_result = await client.call_tool(tool_name, tool_args)
            
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
            response = BEDROCK_CLIENT.converse(
                modelId=BEDROCK_MODEL_ID,
                messages=messages,
                system=system_prompts,
                toolConfig=tool_config
            )
            
            final_text.append(response['output']['message']['content'][0]['text'])
    
    return "\n".join(final_text)


async def main():
    # The client will automatically handle GitHub OAuth
    async with Client("http://localhost:8000/mcp", auth=oauth) as client:
        
        # First-time connection will open GitHub login in your browser
        print("Authenticated with GitHub!")
        
        # Test the protected tool
        tools = await client.list_tools()
        tool_names = [tool.name for tool in tools]

        print("\nConnected to server with tools:\n", '\n'.join(tool_names))

        # Get user info from GitHub Token
        try:
            result = await client.call_tool("get_user_info")
            print(f"GitHub user: {result.data['github_user']}")

        except Exception as e:
            print(f"\nError: {str(e)}")

        # Begin chat loop
        print("\n\nThe MCP Weather Client Started")
        print("Type your weather-releated queries or 'quit'")
        
        while True:
            try:
                query = input("\nQuery: ").strip()
                
                if query.lower() == 'quit':
                    break
                
                response = await process_query(client, query)
                
                print("\n" + response)
                
            except Exception as e:
               print(f"\nError: {str(e)}") 
        

if __name__ == "__main__":
    asyncio.run(main())