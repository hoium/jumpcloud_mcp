# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Environment

### Shell and Virtual Environment

- User uses **Fish Shell** as default shell
- Python virtual environment: `jc-mcp` (managed with VirtualFish)
- Activate with: `vf activate jc-mcp`

## Commands

### Running the application

```bash
# Activate virtual environment (Fish shell)
vf activate jc-mcp

# Start the FastAPI server locally
uvicorn main:app --reload

# Or run with Docker
docker-compose up --build
```

### Running tests

```bash
# Run tests with pytest
pytest

# Run tests with async support
pytest -v
```

### API Documentation

The server provides interactive API documentation at `http://localhost:8000/docs` when running.

## Architecture Overview

This is a **FastAPI-based MCP (Model Context Protocol) server** for JumpCloud integration that provides:

1. **REST API endpoints** for querying JumpCloud resources (users, systems, groups, SSO apps)
2. **Natural language interface** via `/ask` endpoint using a local keyword-matching agent (no LLM required)
3. **MCP protocol support** for tool discovery and execution via JSON-RPC
4. **Docker deployment** for containerized execution

### Key Components

- **main.py**: FastAPI application with REST endpoints and MCP protocol handlers
  - Handles MCP handshake, tool listing, and tool execution
  - Provides REST endpoints for JumpCloud resources
  - `/ask` endpoint for natural language queries

- **jumpcloud/client.py**: JumpCloud API client
  - Async HTTP client using httpx
  - TTL caching for frequently accessed data
  - Handles all JumpCloud API interactions

- **jumpcloud/mcp_agent_runner.py**: Local agent for matching prompts to tools
  - Keyword-based tool matching (no LLM dependency)
  - Maps natural language to specific JumpCloud API calls

- **jumpcloud/auth.py**: API key authentication via x-api-key header

### Authentication

All endpoints require JumpCloud API key authentication via `x-api-key` header. The API key should match the `JUMPCLOUD_API_KEY` environment variable.

### Tool Registry

Tools are registered in `TOOL_REGISTRY` and exposed via MCP protocol:

- list_users
- list_systems
- list_sso_apps
- list_user_groups
- list_system_groups
- search_users

### Environment Configuration

Required environment variables (set in `.env`):

- `JUMPCLOUD_API_KEY`: Your JumpCloud API key
- `MCP_API_URL`: Server URL (default: <http://localhost:8000>)
