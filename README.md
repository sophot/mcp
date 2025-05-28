## Getting started

This repository is a collection of what I learn about MCP and my [notes (notion)](https://www.notion.so/sophot/MCP-1f8c90c362f480a998accda61a33297d?pvs=4).

**1. Clone the repository**

```
git clone https://github.com/sophot/mcp.git
```

**2. Each folder is a separate project. Navigate to any folder to see what it's doing**

```
cd hello_wold
```

**3. Follow the Readme in each project folder.**


<hr />

### Background

Before this repository, I have played with pre-built MCP servers such as Spotify, File-system and Notion with Claude Desktop MCP Client.

Therefore, as of now, I'm curious of how the MCP Client (technically speaking: MCP Host) handle users' query.

I'm trying to answer these question.
1. **Question:** MCP's job is to provide more context to the LLM so that the LLM generate responses with less hallucination, accurate and real time.
   1. Is it a pre-module to the LLM? How does it work with the LLM? (I want to see the code it actually executed rather than learning for texts or blogs)

   **(2025/05/28) Answer:** It is not a pre-module, it works collaboratively with LLM.
   The typical flow works like this:
      - User submits a query to the MCP Host
      - Host analyzes the query and determines what context might be needed
      - Host may call MCP servers to gather relevant tools, resources, or data
      - Host constructs an enhanced prompt with the gathered context
      - LLM generates response using both the original query and the enriched context
<br />

2. **Question:** Given a query, what next?
   1. How does it (MCP Host) decide when to use MCP servers' tools, resources. When to just generate result like the old LLMs. 
   2. Say it has decided to use MCP server, how are things formed?
      1. Like how are the parameters that are passed to the MCP tool functions generated?

   **(2025/05/28) Answer:** The MCP Host typically uses several strategies to decide when to invoke MCP servers:
   * Query Analysis: The host analyzes the user's query for keywords, intent, and context clues that suggest external data might be needed.
   * Available Tools Matching: The host maintains a registry of available MCP servers and their capabilities, then matches query requirements to available tools.
   * LLM-Driven Decisions: Some implementations actually ask the LLM itself to decide which tools to use by providing it with a list of available tools and asking it to generate function calls.

   The key insight is that MCP Hosts act as intelligent middleware - they're not just passing queries directly to LLMs, but actively enriching the context and orchestrating tool usage to provide more accurate, real-time responses. This reduces hallucination because the LLM is working with actual, current data rather than just its training knowledge.
<br />

3. **Question:** So the MCP Host have LLM, rule base code in it?
   
   **(2025/05/28) Answer:** Yes!!
   
   **LLM Integration**
   Most MCP Hosts have an LLM integrated within them (or access to one via API). This LLM serves multiple purposes:
      * **Tool Selection**: The LLM helps decide which MCP servers/tools to invoke based on the user's query. For example, it might receive a prompt like:
         ```bash
         Available tools: file_reader, weather_api, database_query
         User query: "Show me the sales data from last month"
         Which tools should I use?
         ```
   
      * **Parameter Extraction**: The LLM generates structured function calls with proper parameters:
         ```bash
         User: "What's the temperature in San Francisco?"
         LLM generates: weather_api(location="San Francisco", metric="temperature")
         ```
   
      * **Response Synthesis**: After gathering data from MCP servers, the LLM combines everything into a coherent response.
   
      **Rule-Based Code**
   The Host also contains traditional programming logic for:
   
      * **Query Routing**: Pattern matching and keyword detection to quickly identify obvious tool needs
         ```python
         if "weather" in query.lower():
            candidate_tools.append("weather_api")
         ```
   
      * **Parameter Validation**: Ensuring extracted parameters meet tool requirements before making calls
   
      * **Error Handling**: Managing timeouts, failed tool calls, and fallback strategies
   
      * **Security & Access Control**: Determining which tools a user can access
   
      * **Orchestration Logic**: Managing the sequence of tool calls, caching, and response formatting
   
      **Hybrid Approach**
   The most sophisticated MCP Hosts use both approaches together:
      - Rule-based systems handle straightforward, deterministic routing
      - LLMs handle complex reasoning, ambiguous queries, and natural language processing
      - Rules provide guardrails and efficiency while LLMs provide flexibility and intelligence
   
      This hybrid architecture allows MCP Hosts to be both fast (rules) and smart (LLM) in determining how to best serve each user query.
