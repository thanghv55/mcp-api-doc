import asyncio
from typing import Any
import requests
from mcp.server.fastmcp import FastMCP
import os

# Initialize FastMCP server
mcp = FastMCP("openapi-swagger")

# Constants
OPENAPI_URL = os.environ.get("OPENAPI_URL", "https://default-openapi-url.com")
API_KEY = os.environ.get("API_KEY", "default_api_key")
USER_AGENT = "openapi-mcp"


def make_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "x-api-key": API_KEY
    }
    with requests.session() as session:
        response = session.get(url, headers=headers, verify=False)
        if response.status_code != 200:
            raise Exception("Unexpected response from NWS API")
        return response.json()


@mcp.tool()
def get_operation_schema(operation_id: str, service: str=None) -> dict[str, Any] | None:
    """Get details about a specific operation from an OpenAPI specification with the given operation ID and service.

    Args:
        operation_id: ID of operation
        service: Service name (optional)
    """
    if not operation_id:
        return "Unable to fetch operation schema."
    if service:
        url = f"{OPENAPI_URL}/api/schema/{service}/{operation_id}"
    else:
        url = f"{OPENAPI_URL}/api/schema/{operation_id}"
    return make_request(url)


def main():
    print(OPENAPI_URL)
    print(API_KEY)
    print("Running MCP server...")
    # Initialize and run the server with stdio transport
    mcp.run(transport='stdio')
