import gradio as gr

from mcp.client.stdio import StdioServerParameters
from smolagents import InferenceClientModel, CodeAgent
from smolagents.mcp_client import MCPClient
from smolagents.models import TransformersModel
import os
from dotenv import load_dotenv

server_parameters = StdioServerParameters(command="uv", args=["run", "server/mcp_server_stdio.py"])


mcp_client = MCPClient(
    server_parameters
                # {"url": "http://localhost:6270/sse"}
                # {"url": "http://localhost:7860/gradio_api/mcp/sse"}
            )

try:
    tools = mcp_client.get_tools()
    
    api = False
    if not api:
        model = TransformersModel(
                model_id="Qwen/Qwen2.5-Coder-3B-Instruct",
            )
    else:
        load_dotenv()
        HF_TOKEN = os.getenv("HF_TOKEN")
        model = InferenceClientModel(token=HF_TOKEN)
        
    agent = CodeAgent(tools=[*tools], model=model)

    demo = gr.ChatInterface(
        fn=lambda message, history: str(agent.run(message)),
        type="messages",
        examples=["Hello Sophot"],
        title="Agent with MCP Tools",
        description="This is a simple agent that uses MCP tools to answer questions.",
    )

    demo.launch(mcp_server=True, server_port=6274, server_name="0.0.0.0", share=True)
finally:
    mcp_client.disconnect()
