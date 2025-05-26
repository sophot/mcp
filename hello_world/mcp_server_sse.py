import uvicorn
from mcp.server import Server
from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.requests import Request
from starlette.routing import Mount, Route
from starlette.applications import Starlette

mcp = FastMCP(name="hello-world")

@mcp.tool()
def greet_tool(name: str):
    """
    This is a tool that greets a name
    Args:
        name: The name to greet
    """
    return f"Hello {name} from Tool! LFG!!!"

@mcp.resource("greet://{name}")
def greet_resource_template(name: str):
    return f"Hello {name} from Resource!"
    
@mcp.prompt()
def greet_prompt(name: str):
    return f"Hello {name} from Prompt!"


def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    """Create a Starlette application that can server the provied mcp server with SSE."""
    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> None:
        async with sse.connect_sse(
                request.scope,
                request.receive,
                request._send,
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )

    return Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )


if __name__ == "__main__":
    mcp_server = mcp._mcp_server
    
    starlette_app = create_starlette_app(mcp_server, debug=True)

    uvicorn.run(starlette_app, host='0.0.0.0', port=6270)

