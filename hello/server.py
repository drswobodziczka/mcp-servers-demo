"""
Minimal MCP server (Python, STDIO)

Tools:
- echo(text: str) -> str

Run locally with MCP Inspector (requires Node >= 18 and uv):
  uv pip install --upgrade mcp
  npx @modelcontextprotocol/inspector uv run server.py

This starts the server via STDIO under the Inspector. You can then invoke the
"echo" tool and observe JSON request/response and streaming events.
"""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server


server = Server("hello")


@server.tool()
async def echo(text: str) -> str:
    """Echo back the provided text."""
    return text


async def main() -> None:
    # Start an MCP STDIO server and serve requests until stdin closes.
    async with stdio_server() as (read, write):
        await server.run(read, write)


if __name__ == "__main__":
    asyncio.run(main())
