# 🤖 JumpCloud MCP Server

A natural language API server and agent for your JumpCloud environment, built with FastAPI. Created using ChatGPT and Cursor.

This MCP server lets you:

- 🔎 Query users, systems, groups, and SSO apps via REST
- 💬 Ask natural language questions via `/ask`
- 🤖 Use a **local, LLM-free agent** (keyword-based tool matcher)
- 🐳 Run everything in Docker
- ⚙️ Integrate directly with Cursor using `.cursor/mcp.json`

---

## 📦 Features

- ✅ FastAPI-based REST API for JumpCloud data
- 🔐 Token authentication using `x-api-key`
- 🤖 `/ask` endpoint for semantic/natural language queries
- 🐳 Docker Support
- 💡 Cursor integration via `.cursor/mcp.json`

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
├── .cursor/
│   └── mcp.json             # MCP server config for Cursor
├── main.py                  # FastAPI app + /ask endpoint
├── local_agent.py           # Keyword-based tool-matching agent (no LLM)
├── jumpcloud/
│   ├── client.py            # JumpCloud API calls: users, systems, groups
│   ├── models.py            # Pydantic models for validation
│   ├── mcp_agent_runner.py  # (If used: local agent logic only)
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

---

## 💡 Cursor Integration

Create `.cursor/mcp.json`:

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

Restart Cursor and select your MCP server for in-editor questions!

---

## ✨ Support

This project is maintained for **local/private JumpCloud automation** and is ideal for secure deployments, development, and custom integrations.

---
