from smolagents import ToolCollection, CodeAgent
from smolagents.mcp_client import MCPClient
from mcp.client.stdio import StdioServerParameters

server_params = [
    StdioServerParameters(command="uv", args=["run", "mcp_server_stdio.py"]),
    StdioServerParameters(command="uv", args=["run", "mcp_server_stdio.py"])
]

mcp_client = MCPClient(server_params)
tools = mcp_client.get_tools()

print(tools)
print()
for tool in tools:
    print(f'Tool name: "{tool.name}"')
    print(f'Tool inputs: "{tool.inputs}"')
    print(f'Tool output type: "{tool.output_type}"')
    print(f'Tool description: "{tool.description}"')
    print()

# with ToolCollection.from_mcp(server_params, trust_remote_code=True) as tools:
#     print(tools)
#     print(tools.tools)
#     print(dir(tools.tools))
    # print("\n".join(f"{t.name}: {t.description}" for t in tools))
