# MCP Client Configuration Examples

This document provides configuration examples for connecting various MCP clients to the JumpCloud MCP Server.

## Prerequisites

1. Ensure the JumpCloud MCP Server is running:

   ```bash
   docker-compose up --build
   # OR
   uvicorn main:app --reload
   ```

2. Have your JumpCloud API key ready (set in `.env` file)

## Claude Desktop

### macOS Configuration

Edit your Claude Desktop configuration file at:
`~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "jumpcloud-mcp": {
      "command": "uvicorn",
      "args": [
        "main:app",
        "--host", "0.0.0.0",
        "--port", "8000"
      ],
      "cwd": "/path/to/your/jumpcloud_mcp",
      "env": {
        "JUMPCLOUD_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Windows Configuration

Edit your Claude Desktop configuration file at:
`%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "jumpcloud-mcp": {
      "command": "python",
      "args": [
        "-m", "uvicorn",
        "main:app",
        "--host", "0.0.0.0",
        "--port", "8000"
      ],
      "cwd": "C:\\path\\to\\your\\jumpcloud_mcp",
      "env": {
        "JUMPCLOUD_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

## Cursor IDE

Create `.cursor/mcp.json` in your workspace root:

```json
{
  "mcpServers": {
    "jumpcloud-mcp": {
      "url": "http://localhost:8000",
      "description": "JumpCloud MCP Server - Manage JumpCloud users, systems, groups, and SSO apps",
      "headers": {
        "x-api-key": "your-jumpcloud-api-key"
      }
    }
  }
}
```

## Continue.dev

Add to your Continue configuration (`~/.continue/config.json`):

```json
{
  "mcpServers": [
    {
      "name": "jumpcloud-mcp",
      "url": "http://localhost:8000",
      "description": "JumpCloud integration for user and system management",
      "headers": {
        "x-api-key": "your-jumpcloud-api-key"
      }
    }
  ]
}
```

## VS Code with MCP Extension

If using a VS Code MCP extension, add to your `settings.json`:

```json
{
  "mcp.servers": {
    "jumpcloud-mcp": {
      "url": "http://localhost:8000",
      "name": "JumpCloud MCP Server",
      "description": "Manage JumpCloud environment",
      "headers": {
        "x-api-key": "your-jumpcloud-api-key"
      }
    }
  }
}
```

## Generic HTTP MCP Client

For any MCP client that supports HTTP connections:

- **Server URL**: `http://localhost:8000`
- **Protocol**: MCP over HTTP (JSON-RPC)
- **Authentication**: HTTP header `x-api-key` with your JumpCloud API key
- **Content-Type**: `application/json`

### Example HTTP Request

```http
POST / HTTP/1.1
Host: localhost:8000
Content-Type: application/json
x-api-key: your-jumpcloud-api-key

{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list"
}
```

## Docker-based MCP Client

If your MCP client runs in Docker and needs to connect to the server:

1. Use host networking or connect containers:

   ```yaml
   services:
     mcp-client:
       image: your-mcp-client
       network_mode: host
       # OR
       depends_on:
         - jumpcloud-mcp
   ```

2. Use the service name as hostname:

   ```json
   {
     "url": "http://jumpcloud-mcp:8000"
   }
   ```

## Environment Variables

All configurations can use environment variables instead of hardcoded values:

```json
{
  "mcpServers": {
    "jumpcloud-mcp": {
      "url": "${MCP_SERVER_URL:-http://localhost:8000}",
      "headers": {
        "x-api-key": "${JUMPCLOUD_API_KEY}"
      }
    }
  }
}
```

## Troubleshooting

### Connection Issues

1. Verify the server is running: `curl http://localhost:8000/docs`
2. Check the API key is correct
3. Ensure no firewall blocking port 8000
4. Check server logs: `docker-compose logs`

### Authentication Errors

1. Verify `JUMPCLOUD_API_KEY` is set correctly
2. Test API key directly: `curl -H "x-api-key: YOUR_KEY" http://localhost:8000/users`
3. Check JumpCloud API key permissions

### MCP Protocol Issues

1. Ensure your client supports MCP protocol version `2024-11-05`
2. Check JSON-RPC format matches specification
3. Verify content-type headers are correct

## Available Tools

Once connected, these tools will be available in your MCP client:

- `list_users` - List all JumpCloud users
- `list_systems` - List all JumpCloud systems/devices
- `list_sso_apps` - List all SSO applications
- `list_user_groups` - List all user groups
- `list_system_groups` - List all system groups
- `search_users` - Search users with filters
- `search_commands` - Search commands with filters

## Testing Connection

Test your MCP connection with a simple tool call:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "list_users"
  }
}
```
