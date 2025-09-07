# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Application
```bash
# Run with UV (recommended)
USE_UV=1 python main.py [server_scripts...]

# Run with standard Python
python main.py [server_scripts...]

# Example: Run with additional MCP server scripts
python main.py hello/server.py
```

### MCP Server Development
```bash
# Run the document MCP server standalone
python mcp_server.py

# Run with UV
uv run mcp_server.py

# Test MCP client standalone
python mcp_client.py
```

### Environment Setup
- Copy `.env.example` to `.env` and configure:
  - `CLAUDE_MODEL` (required) - Claude model to use
  - `ANTHROPIC_API_KEY` (required) - Anthropic API key
  - `USE_UV=1` - Optional, use UV for Python execution

## Architecture Overview

This is an **MCP (Model Context Protocol) demonstration project** that showcases how to build chat applications with Claude using multiple MCP servers for tool integration.

### Core Components

**Main Application Flow (`main.py`)**
- Entry point that orchestrates MCP client connections and CLI interface
- Manages multiple MCP server connections via `AsyncExitStack`
- Supports both UV and standard Python execution modes

**MCP Client (`mcp_client.py`)**
- Generic MCP client wrapper for connecting to any MCP server via STDIO transport
- Handles tool listing, tool execution, and session management
- Context manager support for proper resource cleanup

**Core Chat System (`core/`)**
- `Chat` - Base chat functionality with Claude integration and tool management
- `CliChat` - Extended chat with document resource handling and command processing
- `Claude` - Anthropic API wrapper with tool support and thinking mode
- `ToolManager` - Handles tool discovery and execution across multiple MCP clients
- `cli.py` - Command-line interface implementation

**MCP Server (`mcp_server.py`)**
- Sample FastMCP server providing document management tools
- Implements `read_document` and `edit_document` tools
- Contains TODO items for resource and prompt implementations

### Key Architectural Patterns

**Multi-Client MCP Architecture**
- One dedicated document client (`doc_client`) for core document operations
- Additional clients dynamically created from server script arguments
- Tool routing automatically finds correct client for each tool

**Document Resource System**
- Query processing supports `@document` mentions for resource inclusion
- Command system (`/command`) for predefined prompts and workflows
- Resource extraction automatically includes referenced documents in context

**Async Context Management**
- Proper resource cleanup using `AsyncExitStack`
- MCP clients implement async context manager protocol
- Session initialization and cleanup handled automatically

## Project Structure

- `core/` - Core chat and CLI functionality
- `hello/` - Sample MCP server implementations
- `DOCS/` - Technical documentation and research materials
- `mcp_server.py` - Main document management MCP server
- `mcp_client.py` - Generic MCP client implementation

## Development Notes

- The project uses **UV** as the preferred Python package manager (set `USE_UV=1`)
- MCP servers run as separate processes connected via STDIO transport
- Tool execution is distributed across multiple MCP server instances
- Windows compatibility included with `WindowsProactorEventLoopPolicy`