## Setup
**1. Sync dependencies and update lockfile.**

```bash
$ uv sync
```

**2. Activate an independent environment to work with.**

```bash
$ source .venv/bin/activate
```

**3. Testing server (Protocol = STDIO)**
If `node.js` is not installed, go ahead and install it at https://nodejs.org/en/download.

```bash
$ mcp dev server/mcp_server_stdio.py

# You'll see sth like below, head to the url and you can test the available tools, resources, prompts we implemented.
Starting MCP inspector...
⚙️ Proxy server listening on port 6277
🔍 MCP Inspector is up and running at http://127.0.0.1:6274 🚀
```

**4. Testing server (Protocol = SSE)**

```bash
# Running the MCP SSE Server
$ python server/mcp_server_sse.py
# Run MCP Inspector
$ mcp dev servermcp_server_sse.py

# You'll see sth like below, head to the url and you can test the available tools, resources, prompts we implemented.
Starting MCP inspector...
⚙️ Proxy server listening on port 6277
🔍 MCP Inspector is up and running at http://127.0.0.1:6274 🚀

# In case the Inspector connection setting is mixed up with the previous STDIO protocol.
In the MCP Inspector page, set:
Transport Type = 'SSE'
URL = 'http://127.0.0.1:6270/sse'
```



**5. Run a simple client code that connect to our MCP server created at [server.py](server.py)**

```bash
$ python 1_mcp_client.py

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


**6. Run a simple Chat Agent code provided my `smolagents` package**

```bash
# Create a .env file and add a huggingface token
$ touch .env
$ echo HF_TOKEN=<your_huggingface_token> > .env

# run
$ python 2_mcp_chat_agent.py
```

Output:
![output_agent_demo_img](imgs/out_demo1.png)


**7. Run a gradio chatbot app that executes on MCP tools**

```bash
# Create a .env file and add a huggingface token
$ touch .env
$ echo HF_TOKEN=<your_huggingface_token> > .env

# run
$ python 3_gradio_app.py
```
Output:
![output_chatbot_demo_img](imgs/out_demo2.png)
