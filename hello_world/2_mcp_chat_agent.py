from smolagents import ToolCollection, CodeAgent
from mcp.client.stdio import StdioServerParameters
from smolagents import CodeAgent, InferenceClientModel
from smolagents.models import TransformersModel
import os
from dotenv import load_dotenv

api = False
if not api:
    model = TransformersModel(
            model_id="Qwen/Qwen2.5-Coder-3B-Instruct",
        )
else:
    load_dotenv()
    HF_TOKEN = os.getenv("HF_TOKEN")
    model = InferenceClientModel(token=HF_TOKEN)

server_parameters = StdioServerParameters(command="uv", args=["run", "server/mcp_server_stdio.py"])

with ToolCollection.from_mcp(
    server_parameters, trust_remote_code=True
) as tool_collection:
    agent = CodeAgent(tools=[*tool_collection.tools], model=model)
    agent.run("Greet 'Phot'")
