# mcp-servers-demo
varia materials, including sample mcp servers, clients, deep researches relating model context protocol standard, to be used as feed for conference speech presentation and demos

## LLM + Tools + Context — Quick Overview

### Minimal Flow
- User input (CLI) → Chat builds a user message.
- If the input mentions resources (e.g., @report.pdf), a resource layer fetches and injects their content into the user context.
- Chat calls the model with current conversation history and the aggregated list of tools (from multiple MCP servers).
- The model decides:
  - if a tool is needed → it selects a tool and arguments; Tool Manager executes it via the proper MCP client/server; the tool result is appended as context and the loop continues.
  - if no more tools are needed → returns the final text answer.

### When the model “gets” tools
- On every call, the current tool list is provided; the model chooses which tool(s) to use.

### When resources are added to context
- Before the call (based on @mentions in the user input).
- After tool execution (tool results are appended as context for the next turn).

### Key Files (quick map)
- `core/cli.py` — console UI (prompt loop, autocomplete for `/` and `@`).
- `main.py` — app bootstrap (model service, MCP clients, chat + CLI wiring).
- `core/chat.py` — chat loop + tool orchestration with the model.
- `core/cli_chat.py` — resource mentions and command prompts integration.
- `core/claude.py` — model service wrapper (messages, tools, optional system/thinking).
- `core/tools.py` — tool aggregation and execution across MCP clients.
- `mcp_client.py` — MCP client (stdio transport, list/call tools; prompts/resources TODOs).
- `mcp_server.py` — sample MCP server exposing example tools.
