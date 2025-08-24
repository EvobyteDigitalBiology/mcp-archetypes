from typing import List

from fastmcp import FastMCP
from fastmcp.prompts.prompt import Message

# Initialize FastMCP server
mcp = FastMCP(
    "PromptServer",
    instructions = "A MCP Server providing prompts to generate blog posts",
    include_tags={'prompt'}
    )

# Provision a simple greeting prompt in different languages
@mcp.prompt(name="Greet MCP Server",
            tags={'prompt'})
def greet_me(language: str = "EN") -> str:
    """Generate a polite greeting in a defined language"""
    return f"Create a greeting for the user in the language {language} (ISO 639 language code)"

# Prompt to extract relevent tech keywords from code sample
@mcp.prompt(name="Get Keywords From Code",
            tags={'prompt'})
def get_keywords_from_code(code: str) -> str:
    """Create an intro section for a blog post from provided code

    Args:
        code (str): Codebase to analyze
        
    Returns:
        keywords as json-formatted text with key "keywords"
    """
    
    prompt = f"""
        ROLE
        You are a helpful developer or code analyst.
        
        TASK
        The task is to analyse the input code and extract the technologies used in the code.
        Define the technologies used in the code in 5 keywords. Focus on frameworks used, for instance Python libraries and
        relevent protocols. Do not return basics of programming such as programming languages or core elements of a programming language standard library
        
        OUTPUT
        Return the keywords as STRICT JSON, with the key "keywords" and a list of keywords. Example: {{'keywords' : ['KeywordA', 'KeywordB']}}
        
        CODE
        {code}
        """
    
    return prompt

# Prompt to create intro section from keywords
@mcp.prompt(name="Get Intro From Keywords",
            tags={'prompt'})
def create_intro_from_code(keywords: List[str]) -> str:
    """Create an intro section from a list of keywords

    Args:
        keywords: Keywords for Intro Post
        
    Returns:
        Intro sections for code prompt with Context
    """
    
    prompt = f"""
        ROLE
        You are a blogger for code development, writing articles for a data science audience.
        
        TASK
        Write an intro section of 5-7 sentences for a blogpost.
        The blogpost focuses on a topics described by those keywords.
        
        Return the blog intro.
        
        KEYWORDS
        {keywords}
        """
    
    return prompt

# Prompt to create main section from code sample
@mcp.prompt(name="Get Main Section From Code",
            tags={'prompt'})
def create_main_section_from_code(keywords: List[str], code: str) -> str:
    """Create an blog post main section from the provided code

    Args:
        keywords: Keywords for Intro Post
        code: Code to analyse
        
    Returns:
        Blog Post Main Section Prompt with Context
    """
    
    prompt = f"""
        ROLE
        You are a blogger for code development, writing articles for a data science audience.
        
        TASK
        1 ) Analyse the provided code and extract 5 sections of code which are related to the provided keywords.
        2 ) Provide for each code section a short description
        3 ) Aggregate the code plus description into a main part of the blogpost
        
        OUTPUT
        Return the main part of the blogpost.
        
        INPUT
        KEYWORDS
        {keywords}
        
        INPUT
        CODE
        {code}
        """
    
    return prompt

# Prompt to aggregate code portions
@mcp.prompt(name="Aggregate Blog Sections",
            tags={'prompt'})
def aggregate_blog_sections(intro: str, main: str, outlook: str) -> str:
    """Aggregate and polish different sections of a blog post

    Args:
        intro: Intro Section
        main: Main Section
        outlook: Outlook Section
        
    Returns:
        Compiled blog post prompt with Context
    """
    
    prompt = f"""
        ROLE
        You are a blogger for code development, writing articles for a data science audience.
        
        TASK
        1) Combine the input from intro, main and outlook blog parts into a single post.
        2) Polish the language into a clear, professional tone.
        
        OUTPUT
        Return the final blog post
        
        INPUT
        INTRO
        {intro}
        
        INPUT
        MAIN
        {main}
        
        OUTLOOK
        {outlook}
        """
    
    return prompt

# Start Server
if __name__ == '__main__':
    mcp.run(transport='stdio')