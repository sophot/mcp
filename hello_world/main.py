from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="hello-world")

@mcp.tool()
def greet_tool(name: str):
    """This is a tool that greets a name
    
    Args:
        name: The name to greet
    """
    return f"Hello {name} from Tool!"

@mcp.resource("greet://{name}")
def greet_resource_template(name: str):
    return f"Hello {name} from Resource!"
    
@mcp.prompt()
def greet_prompt(name: str):
    return f"Hello {name} from Prompt!"

if __name__ == "__main__":
    mcp.run()
