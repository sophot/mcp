from smolagents import ToolCollection, CodeAgent
from smolagents.mcp_client import MCPClient
from mcp.client.stdio import StdioServerParameters

server_params = StdioServerParameters(command="uv", args=["run", "main.py"])

mcp_client = MCPClient(server_params)
tools = mcp_client.get_tools()

print(tools)
print()
print(dir(tools[0]))
print()
print(tools[0].name)
print(tools[0].inputs)
print(tools[0].output_type)
print(tools[0].description)
print(tools[0]._get_tool_code())

# with ToolCollection.from_mcp(server_params, trust_remote_code=True) as tools:
#     print(tools)
#     print(tools.tools)
#     print(dir(tools.tools))
    # print("\n".join(f"{t.name}: {t.description}" for t in tools))