## Setup
1. Sync dependencies and update lockfile.

```bash
uv sync
```

2. Activate an independent environment to work with.

```bash
source .venv/bin/activate
```

3. Run a simple client code that connect to our MCP server created at [server.py](server.py)

```bash
python mcp_client.py

# Output
Tool name: "greet_tool"
Tool inputs: "{'name': {'title': 'Name', 'type': 'string', 'description': 'see tool description'}}"
Tool output type: "string"
Tool description: "
    This is a tool that greets a name
    Args:
        name: The name to greet
    "
```


4. Run a simple Chat Agent code provided my `smolagents` package

```bash
# Create a .env file and add a huggingface token
touch .env
echo HF_TOKEN=<your_huggingface_token> > .env

# run
python mcp_chat_agent.py
```

Output:
![output_img](imgs/out_demo1.png)