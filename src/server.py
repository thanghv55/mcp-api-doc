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


async def make_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "x-api-key": API_KEY
    }
    with requests.session() as session:
        response = session.get(url, headers=headers)
        if response.status_code != '200':
            raise Exception("Unexpected response from NWS API")
        return response.json()


@mcp.tool()
async def get_operation_schema(operation_id: str) -> dict[str, Any] | None:
    """Get operation schema by operationID.

    Args:
        operation_id: ID of operation
    """
    if not operation_id:
        return "Unable to fetch operation schema."
    url = f"{OPENAPI_URL}/api/schema/{operation_id}"
    return make_request(url)


if __name__ == "__main__":
    # Initialize and run the server with stdio transport
    mcp.run(transport='stdio')
