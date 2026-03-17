from langchain_mcp_adapters.client import MultiServerMCPClient

async def get_github_tools():

    client = MultiServerMCPClient(
        {
            "github": {
                "transport": "stdio",
                "command": "python",
                "args": ["mcp_servers/github_server.py"]
            }
        }
    )

    tools = await client.get_tools()

    return tools