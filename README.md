# 🤖 JumpCloud MCP Server

A natural language API server and agent for your JumpCloud environment, built with FastAPI. Supports the Model Context Protocol (MCP) for integration with AI assistants and code editors.

This MCP server lets you:

- 🔎 Query users, systems, groups, and SSO apps via REST
- 💬 Ask natural language questions via `/ask`
- 🤖 Use a **local, LLM-free agent** (keyword-based tool matcher)
- 🐳 Run everything in Docker
- ⚙️ Integrate with MCP-compatible clients (Claude Desktop, Cursor, etc.)

---

## 📦 Features

- ✅ FastAPI-based REST API for JumpCloud data
- 🔐 Token authentication using `x-api-key`
- 🤖 `/ask` endpoint for semantic/natural language queries
- 🐳 Docker Support
- 💡 MCP protocol support for AI assistants and code editors

---

## 🛠️ Quick Setup

### 1. Clone and configure environment

```bash
git clone https://gitlab.com/barkada/itops/jumpcloud-mcp
cd jumpcloud-mcp
cp .env.example .env
```

Update `.env` with your keys:

```env
JUMPCLOUD_API_KEY=your_jumpcloud_api_key
MCP_API_URL=http://localhost:8000
```

---

### 2. Build and run with Docker

```bash
docker-compose up --build
```

The server will start on `http://localhost:8000`.

---

### 3. Call MCP via REST

```bash
curl -X GET http://localhost:8000/systems   -H "x-api-key: $JUMPCLOUD_API_KEY"
```

---

### 4. Ask with natural language

```bash
curl -X POST http://localhost:8000/ask   -H "Content-Type: application/json"   -H "x-api-key: $JUMPCLOUD_API_KEY"   -d '{"prompt": "List all active Mac systems"}'
```

---

## 📁 Directory Structure

```graphql
jumpcloud_mcp/
├── main.py                  # FastAPI app + MCP protocol + /ask endpoint
├── jumpcloud/
│   ├── client.py            # JumpCloud API calls: users, systems, groups
│   ├── models.py            # Pydantic models for validation
│   ├── mcp_agent_runner.py  # Keyword-based tool-matching agent (no LLM)
│   └── auth.py              # API key auth
├── .env                     # Secrets/config
├── Dockerfile               # Build FastAPI server container
├── docker-compose.yml       # Docker Compose for dev/prod
├── requirements.txt         # Python dependencies (NO openai/anthropic)
└── README.md                # Docs and usage guide
```

---

## 🔧 REST API Reference - [API Docs](http://localhost:8000/docs)

### 📍 GET Endpoints

- `/users`
- `/systems`
- `/user-groups`
- `/system-groups`
- `/sso-applications`

### 📍 POST

- `/ask` — Accepts `{"prompt": "..."}`
- `/users/search` Search JumpCloud users using filters and fields.
  - `{"filter": [{"department": "IT"}], "fields": "email username sudo"}`
- `/commands/search` Search JumpCloud commands using filters and fields.
  - `{"filter": [{"command": "restart"}], "fields": "name command sudo"}`

---

## 💡 MCP Client Integration

This server supports the Model Context Protocol (MCP) and can be used with various AI assistants and code editors.

### Claude Desktop

Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "jumpcloud-mcp": {
      "command": "uvicorn",
      "args": ["main:app", "--host", "0.0.0.0", "--port", "8000"],
      "cwd": "/path/to/jumpcloud_mcp"
    }
  }
}
```

### Cursor IDE

Create `.cursor/mcp.json` in your workspace:

```json
{
  "mcpServers": {
    "jumpcloud-mcp": {
      "url": "http://localhost:8000",
      "description": "JumpCloud MCP Server"
    }
  }
}
```

### Other MCP Clients

For any MCP-compatible client, configure it to connect to:

- **HTTP URL**: `http://localhost:8000`
- **Protocol**: MCP over HTTP
- **Authentication**: Include `x-api-key` header with your JumpCloud API key

---

## ✨ Support

This project is maintained for **local/private JumpCloud automation** and is ideal for secure deployments, development, and custom integrations with MCP-compatible AI assistants and code editors.

---

## 📜 License
