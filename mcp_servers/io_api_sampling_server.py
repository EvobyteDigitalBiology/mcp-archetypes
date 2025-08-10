from typing import Any, List, Tuple, Dict
import sys
import os
import httpx
from fastmcp import FastMCP
from fastmcp import Context
from fastmcp.exceptions import FastMCPError
import datetime

# Initialize FastMCP server
mcp = FastMCP(
    "SpaceNewsTranslation"
)

# Constants
API_BASE = "https://api.spaceflightnewsapi.net/v4/articles/"

async def get_spaceflight_news_date(date: datetime.date) -> List[Tuple[str, str]] | None:
    
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "Accept": "application/json"
    }
    
    endpoint = API_BASE + f'?published_at_gte={date.isoformat()}'
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(endpoint, headers=headers, timeout=30.0)
            response.raise_for_status()

            news_summaries = []
            for res in response.json()['results']:
                news_summaries.append((res['title'],res['summary']))
            
            return news_summaries
            
        except Exception:
            return None
        
@mcp.tool()
async def get_todays_spacenews(ctx: Context, language: str = 'EN') -> List[Dict[str,str]]:
    """Get todays latest Space News from the portal spaceflightnewsapi.net

    Invoke automatics translation by LLM sampling if the selected language is not EN.
    
    Args:
        language: ISO639 codes for language to return
        
    Returns:
        JSON format: List of key-values with keys: 'title' and 'summary'

    Raises:
        McpError: If the news data is not in the expected format.
    """
    
    date = datetime.date.today()
    
    news_today = await get_spaceflight_news_date(date)

    if not news_today:
        raise FastMCPError("API Call Failed.")

    # reformat
    news_out = []
    
    for news in news_today:
        news_out.append(
            {
                'title' : news[0],
                'summary' : news[1]
            }
        )
    
    if language != 'EN':
        
        prompt = f"""Translate the title and the summary of each news entry into the language {language} (ISO639 format).
                
                The input format is a  json list of key-value pairs with "title" : "News Title" and "summary" : "News Summary".
                The expected return format must be a json list of key-value pairs with keys "title" and "summary", and the values must be translated into the specified language
            
                Example Language : DE
                Example Input: 
                    [
                        {{'title' : "Live Coverage: SpaceX Falcon 9 to make another attempt to launch Amazon Project Kuiper mission",
                        'summary' : "Liftoff from Space Launch Complex 40 at Cape Canaveral Space Force Station in Florida is scheduled for 8:57 a.m. EDT (1257 UTC), after three earlier attempts were scrubbed."}}
                    ]
                Example Output:
                    [
                        {{
                        'title' : "Live Übertragung: SpaceX Falcon 9 macht erneuten Cersuch für Amazon Projekt Kuiper Mission",
                        'summary' : "Start von Space Launch Complex 40 auf Cape Canaveral Space Force Station in Florida ist geplant für 8:57 a.m. EDT (1257 UTC), nachdem dre vorherige Termine abgesagt wurden."}}
                    ]

                Input News Data (json-format)
                {news_out}
            """

        try:
            response = await ctx.sample(prompt)
        except:
            raise FastMCPError("Translation failed, LLM Sampling not available.")
    
    else:
        response = news_out
    
    return response


if __name__ == "__main__":
    
    # Initialize and run the server
    mcp.run(transport='stdio')