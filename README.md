## Getting started

This repository is a collection of what I learn about MCP and my [notes (notion)](https://www.notion.so/sophot/MCP-1f8c90c362f480a998accda61a33297d?pvs=4).

1. Clone the repository

```
git clone https://github.com/sophot/mcp.git
```

2. Each folder is a separate project. Navigate to any folder to see what it's doing

```
cd hello_wold
```

3. Follow the Readme in each project folder.


<hr />

### Background

Before this repository, I have played with pre-built MCP servers such as Spotify, File-system and Notion with Claude Desktop MCP Client.

Therefore, as of now, I'm curious of how the MCP Client (technically speaking: MCP Host) handle users' query.

I'm trying to answer these question.
1. MCP's job is to provide more context to the LLM so that the LLM generate responses with less hallucination, accurate and real time.
   1. Is it a pre-module to the LLM? How does it work with the LLM? (I want to see the code it actually executed rather than learning for texts or blogs)
2. Given a query, what next?
   1. How does it (MCP Host) decide when to use MCP servers' tools, resources. When to just generate result like the old LLMs. 
   2. Say it has decided to use MCP server, how are things formed?
      1. Like how are the parameters that are passed to the MCP tool functions generated?
      2. ....