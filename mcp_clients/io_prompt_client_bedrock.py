import os
import asyncio
import sys
import json
from typing import List

import boto3
from botocore.config import Config

from fastmcp import Client


import dotenv

# Load AWS Credentials from ENV
dotenv.load_dotenv()

BEDROCK_MODEL_ID = 'us.deepseek.r1-v1:0'

class MCPClient():
    """
        MCP Client for interacting with a MCP Prompt Server using Bedrock AI.
        The Client is using FastMCP framework to connect to the MCP Server. 
    """

    def __init__(self,
                 mcp_server_script: str):
        
        config = Config(
            region_name = 'us-east-1'
        )
        
        self.bedrock_client = boto3.client(
            'bedrock-runtime',
            config=config
        )

        assert os.path.isfile(mcp_server_script), 'MCP Server Script not Found'

        self.client = Client(mcp_server_script)
    
    
    async def run_keyword_prompt(self, code: str) -> List[str]:
        """
            Run prompt to extract keywords from code
            
            Args:
                code: code to analyze

            Returns:
                List of keywords extracted from the code
                
            Raises:
                ValueError: If keywords cannot be loaded
        """
        

        # Get keywords prompt
        keywords_prompt = await self.client.get_prompt(
            "Get Keywords From Code",
            {'code' : code}
        )

        messages = [
            {
            'role' : 'user',
            'content' : [
                {'text' : f"""
                {keywords_prompt}
            """}]            
            }
        ]

        keywords_res = self.bedrock_client.converse(
            modelId=BEDROCK_MODEL_ID,
            messages=messages
        )

        keywords_json = (keywords_res['output']['message']['content'][0]['text'])
        try:
            keywords_json = keywords_json.replace("""```json""", "").replace("""```""", "")
            keywords = json.loads(keywords_json)
        except Exception as e:
            raise ValueError("Error Loading Keyword Response")
        
        return keywords
                
    async def run_intro_prompt(self, keywords: List[str]) -> str:
        """
            Run prompt to create an intro section
            
            Args:
                keywords: List of keywords to include in the intro

            Returns:
                Intro section for the blog post
        """
        
        # Get keywords prompt
        keywords_prompt = await self.client.get_prompt(
            "Get Intro From Keywords",
            {'keywords' : keywords}
        )

        messages = [
            {
            'role' : 'user',
            'content' : [
                {'text' : f"""
                {keywords_prompt}
            """}]            
            }
        ]

        keywords_res = self.bedrock_client.converse(
            modelId=BEDROCK_MODEL_ID,
            messages=messages
        )

        intro = (keywords_res['output']['message']['content'][0]['text'])
        return intro
    

    async def run_main_prompt(self, keywords: List[str], code: str) -> str:
        """
            Run prompt to create the main section

            Args:
                keywords: List of keywords to reference and prioritze from the code
                code: Code base to analyze

            Returns:
                Main section for the blog post
        """

        # Get keywords prompt
        main_prompt = await self.client.get_prompt(
            "Get Main Section From Code",
            {'keywords' : keywords, 'code': code}
        )

        messages = [
            {
            'role' : 'user',
            'content' : [
                {'text' : f"""
                {main_prompt}
            """}]            
            }
        ]

        main_res = self.bedrock_client.converse(
            modelId=BEDROCK_MODEL_ID,
            messages=messages
        )

        main_part = (main_res['output']['message']['content'][0]['text'])
        return main_part

    
    async def run_aggregate_prompt(self, intro: str, main: str, outlook: str) -> str:
        """
            Run prompt to aggregate sections into blog post

            Args:
                intro: Intro section for the blog post
                main: Main section for the blog post
                outlook: Outlook section for the blog post

            Returns:
                Aggregated blog post
        """
        
        # Get keywords prompt
        main_prompt = await self.client.get_prompt(
            "Aggregate Blog Sections",
            {'intro' : intro, 'main': main, 'outlook' : outlook}
        )

        messages = [
            {
            'role' : 'user',
            'content' : [
                {'text' : f"""
                {main_prompt}
            """}]            
            }
        ]

        main_res = self.bedrock_client.converse(
            modelId=BEDROCK_MODEL_ID,
            messages=messages
        )

        main_part = (main_res['output']['message']['content'][0]['text'])
        return main_part


    async def run(self,
                  code_file: str) -> str:
        """
        Run the MCP Client

        Args:
            code_file: Path to code file to base blog post on
        
        Raises:
            Exception: If there is an error
        """
        
        assert os.path.isfile(code_file)
        
        with open(code_file, 'r') as fh:
            code = fh.read()
    
        async with self.client:
            
            await self.client.ping()
            
            # List prompts
            prompts = await self.client.list_prompts()
            print("Available Prompts:")
            print(f"Total Prompts: {len(prompts)}")
            for prompt in prompts:
                print(f"- {prompt.name}")
            
            # Extract keywords from code
            keywords = await self.run_keyword_prompt(
                code=code
            )
            
            # Write short intro for keyword
            intro = await self.run_intro_prompt(
                keywords=['MCP', 'FastMCP', 'Prompts']
            )
            
            # Write main for keyword
            main_part = await self.run_main_prompt(
                 keywords=['MCP', 'FastMCP', 'Prompts'],
                 code = code
            )
            
            outlook_text = """
            If you want to learn more about MCP, or have questions on individual blog posts, visit www.evo-byte.com
            """

            # Aggregate
            blogpost = await self.run_aggregate_prompt(
                intro = intro,
                main=main_part,
                outlook=outlook_text                
            )

        return blogpost


async def main():
    
    if len(sys.argv) < 2:
        print("Usage: python io_resources_client_bedrock.py <path_to_server_script> <path_to_code_file>")
        sys.exit(1)

    print("Starting the MCP Client for EvoPromptServer")
    
    client = MCPClient(sys.argv[1])
    
    blogpost = await client.run(code_file = sys.argv[2])

    print(blogpost)


if __name__ == "__main__":
    asyncio.run(main())