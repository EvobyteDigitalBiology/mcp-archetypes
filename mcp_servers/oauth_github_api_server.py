import os
from typing import Any
import sys
import httpx
from fastmcp import FastMCP
from fastmcp.server.auth.providers.github import GitHubProvider
import dotenv
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

dotenv.load_dotenv()

# The GitHubProvider handles GitHub's token format and validation
auth_provider = GitHubProvider(
    client_id=os.getenv("GITHUB_OAUTH_CLIENT_ID"),  # Your GitHub OAuth App Client ID
    client_secret=os.getenv("GITHUB_OAUTH_CLIENT_SECRET"),     # Your GitHub OAuth App Client Secret
    base_url="http://localhost:8000",   # Must match your OAuth App configuration
    redirect_path="/auth/callback",   # Default value, customize if needed,
)

# Initialize FastMCP server
mcp = FastMCP(
    "Weather API - GitHub OAuth App",
    auth=auth_provider,
    log_level="DEBUG",
    debug=True
)

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
        Event: {props.get('event', 'Unknown')}
        Area: {props.get('areaDesc', 'Unknown')}
        Severity: {props.get('severity', 'Unknown')}
        Description: {props.get('description', 'No description available')}
        Instructions: {props.get('instruction', 'No specific instructions provided')}
    """

# Add a protected tool to test authentication
@mcp.tool()
async def get_user_info() -> dict:
    """Returns information about the authenticated GitHub user."""
    from fastmcp.server.dependencies import get_access_token
    
    token = get_access_token()

    # The GitHubProvider stores user data in token claims
    return {
        "github_user": token.claims.get("login"),
        "name": token.claims.get("name"),
    }

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
            {period['name']}:
            Temperature: {period['temperature']}°{period['temperatureUnit']}
            Wind: {period['windSpeed']} {period['windDirection']}
            Forecast: {period['detailedForecast']}
            """
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)

if __name__ == "__main__":

    logger.info(f'ClientID {os.getenv("GITHUB_OAUTH_CLIENT_ID")}')

    # Initialize and run the server
    mcp.run(transport='http')