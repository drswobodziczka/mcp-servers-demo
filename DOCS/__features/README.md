# MCP Servers Demo — Features Overview

This document describes the functional architecture of the demo application, focusing on how the MCP Server, MCP Client, CLI chat app, and tool orchestration interact. It also highlights the difference between MCP Tools and MCP Resources and provides short usage flows.

## Components

- __MCP Server (`mcp_server.py`)__

   - Service name: `DocumentMCP` (via `FastMCP`).
   - In-memory document store: `docs: dict[str, str]`.
   - Tools:

      - `read_document(doc_id: str) -> str` — returns document content.
      - `edit_document(doc_id: str, old_content: str, new_content: str)` — replaces text in a document.

   - Resources:

      - `docs://documents` (`application/json`) — list of available document IDs.
      - `docs://documents/{doc_id}` (`text/plain`) — content of a specific document.

   - Transport: `stdio` when run directly.

- __MCP Client (`mcp_client.py`)__

   - Creates a stdio MCP session to the server (via `uv run mcp_server.py`).
   - Key methods:
      - `list_tools() -> list[types.Tool]` — enumerates server tools.
      - `call_tool(tool_name: str, tool_input: dict)` — invokes a tool.
      - `read_resource(uri: str) -> Any` — reads and parses a resource (handles `application/json` vs `text/plain`).
      - `list_prompts()`, `get_prompt(...)` — placeholders for future MCP prompt support.

- **Tool Orchestration (`core/tools.py`)**

   - `ToolManager.get_all_tools(clients) -> list[Tool]` — aggregates tools exposed by all configured MCP clients.
   - `ToolManager.run_tool(...)` (and helpers) — executes tools by routing calls to the right client/server and wraps results as JSON for the model.

- **Chat Service (`core/chat.py`)**

   - Manages the message loop with the model (Anthropic) and provides access to multiple MCP clients.
   - Delegates tool calls to `ToolManager` based on the model’s tool-use responses.

- __CLI Chat Facade (`core/cli_chat.py`)__

   - Convenience wrapper for CLI interactions.
   - Examples:
      - `list_docs_ids() -> list[str]` — `read_resource("docs://documents")`.
      - `get_doc_content(doc_id: str) -> str` — `read_resource(f"docs://documents/{doc_id}")`.

- **Claude Service (`core/claude.py`)**

   - Minimal Anthropics client wrapper to send/receive model messages.

## Tools vs Resources (MCP)

- **Tools**

   - Imperative actions with parameters and validation (e.g., `read_document`, `edit_document`).
   - May have side-effects and compute or transform data.
   - Invoked by the client/model planning step (tool-use).

- **Resources**

   - Addressable, discoverable data (e.g., lists and views) exposed via `resources/list` and `resources/read`.
   - Carry `mime_type` so the client knows how to render/attach content.
   - Ideal for read-only views, large blobs, and automatic context attachments for the model.

## Typical Flows

- **Discover and read data (Resources)**

   1. Client connects to the MCP server.
   2. Client calls `resources/list` and sees:

      - `docs://documents` — list of IDs
      - `docs://documents/{doc_id}` — templated content endpoint

   3. Client calls `read_resource("docs://documents")` → gets JSON array of IDs.
   4. Client calls `read_resource("docs://documents/plan.md")` → gets text of the document.

- **Edit data (Tools)**

   1. Model or user triggers `edit_document` with `doc_id`, `old_content`, `new_content`.
   2. Server mutates `docs[doc_id]` accordingly.
   3. Client can re-read `docs://documents/{doc_id}` to confirm changes.

- **Model-assisted workflow**

   1. Chat collects available tools from all MCP clients via `ToolManager.get_all_tools`.
   2. The model decides to call a tool (e.g., `read_document`) based on the user request.
   3. The client executes the tool, receives results, and may attach related resources to the next model prompt.

## Extensibility

- Add new resources for additional views (e.g., search results URI returning JSON).
- Add prompts (MCP Prompts API) for reusable prompt templates (e.g., summarize/markdown‑rewrite).
- Introduce persistence (replace in-memory `docs` with a DB) without changing the MCP interface for clients.
- Support streaming updates via MCP resource update events when underlying data changes.

## CLI Commands

Below is a concise list of common commands used in this project. Use `uv` where possible for speed and reproducibility; you can substitute `python` where noted.

### Run the sample MCP server (`mcp_server.py`)

```bash
# Recommended (uv)
uv run mcp_server.py

# Alternative (plain Python)
python mcp_server.py
```

What this does:

- Starts the demo MCP server over STDIO so any MCP client (including our app) can connect.

### Run the full chat application (`main.py`)

Environment requirements (see assertions in `main.py`): `ANTHROPIC_API_KEY`, `CLAUDE_MODEL`.

```bash
# Using uv (recommended)
uv run main.py

# Using Python directly
python main.py
```

You can pass additional server scripts to `main.py` to spin up extra MCP clients. Example (using uv):

```bash
uv run main.py hello/server.py
```

What this does:

- Launches the interactive CLI chat.
- Starts the default document server client which in turn spawns the server process (`mcp_server.py`).
- For each extra script argument (e.g., `hello/server.py`), starts an additional MCP client which also spawns that server process.

Implementation note:

- `main.py` internally decides how to launch the default document server based on `USE_UV`:

```bash
# If set, uses 'uv run mcp_server.py'; otherwise falls back to 'python mcp_server.py'
export USE_UV=1
uv run main.py
```

### Inspect the MCP server with MCP Inspector

You can run the Inspector against any MCP server script. Examples:

```bash
# Inspector + demo server
npx @modelcontextprotocol/inspector uv run mcp_server.py

# Inspector + minimal hello server
npx @modelcontextprotocol/inspector uv run hello/server.py
```

Note: If you do not use `uv`, replace the command part accordingly, e.g.:

```bash
npx @modelcontextprotocol/inspector python mcp_server.py
```

If you installed the Python MCP CLI (`mcp[cli]`), you can also use:

```bash
mcp inspector uv run mcp_server.py
```

### Quick test client (list tools)

`mcp_client.py` includes a small test harness under `__main__` that connects to the server and prints tools:

```bash
uv run mcp_client.py
```

What this does:

- Starts the Python client which internally spawns the demo server via `uv run mcp_server.py` and then lists tools.
- No need to pre-run the server; the client manages the server process for this test.

## Notes

- Transport is local stdio (no HTTP/CORS/ports); resources are discoverable and typed by `mime_type`.
- The same pattern generalizes to remote servers (e.g., behind SSH) while keeping the MCP surface unified for the client.

#mcp-speech #mcp-cli-tools #uv #mcp-client #mcp-server #mcp-inspector
