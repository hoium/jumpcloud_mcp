#!/usr/bin/env python3

from fastapi import FastAPI, Header, HTTPException, Depends, Request
from fastapi.responses import JSONResponse, RedirectResponse
from typing import Optional

from jumpcloud.models import UserCreate, PromptRequest
from jumpcloud.client import (
    list_users, list_systems, list_sso_applications, list_user_groups, list_system_groups,
)
from jumpcloud.auth import verify_token
from jumpcloud.mcp_agent_runner import ask_mcp_local, TOOL_REGISTRY

app = FastAPI(title="JumpCloud MCP Server", version="1.0.0")


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@app.post("/", include_in_schema=False)
async def mcp_handshake(request: Request):
    body = await request.json()
    req_id = body.get("id", None)
    method = body.get("method", "")

    CAPABILITIES = {
        "tools": {},
        "prompts": {},
        "resources": {},
        "logging": {},
        "roots": {
            "listChanged": False
        }
    }

    if method == "listOfferings":
        return JSONResponse(
            content={
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "offerings": [
                        {
                            "name": "JumpCloud MCP",
                            "description": "Natural language agent for JumpCloud (users, systems, SSO, groups).",
                            "endpoint": "/ask",
                            "methods": ["POST"]
                        }
                    ],
                    "serverInfo": {
                        "name": "JumpCloud MCP",
                        "version": "1.0.0"
                    },
                    "protocolVersion": "2025-03-26",
                    "capabilities": CAPABILITIES
                }
            }
        )
    elif method == "initialize":
        return JSONResponse(
            content={
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "serverInfo": {
                        "name": "JumpCloud MCP",
                        "version": "1.0.0"
                    },
                    "protocolVersion": "2025-03-26",
                    "capabilities": CAPABILITIES
                }
            }
        )
    elif method == "tools/list":
        return JSONResponse(
            content={
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": [
                        {
                            "name": "list_users",
                            "description": "List all JumpCloud users.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {}
                            }
                        },
                        {
                            "name": "list_systems",
                            "description": "List all JumpCloud systems.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "os": {"type": "string"},
                                    "active": {"type": "boolean"},
                                    "os_version": {"type": "string"},
                                    "serial_number": {"type": "string"}
                                }
                            }
                        },
                        {
                            "name": "list_sso_apps",
                            "description": "List all SSO applications.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {}
                            }
                        },
                        {
                            "name": "list_user_groups",
                            "description": "List all user groups.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {}
                            }
                        },
                        {
                            "name": "list_system_groups",
                            "description": "List all system groups.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {}
                            }
                        },
                    ]
                }
            }
        )
    elif method == "tools/call":
        params = body.get("params") or {}
        tool_name = params.get("tool") or params.get("name")
        args = params.get("args", {})

        print(f"tools/call params: {params}, tool_name: {tool_name}")

        tool = TOOL_REGISTRY.get(tool_name)
        if not tool:
            return JSONResponse(
                content={
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32601,
                        "message": f"Tool '{tool_name}' not found"
                    }
                }
            )
        try:
            result = await tool(**args)
            # MCP requires "content": [ {type: "text", text: ...} ]
            content = [
                {"type": "text", "text": str(item)}
                for item in (result if isinstance(result, list) else [result])
            ]
            return JSONResponse(
                content={
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": content
                    }
                }
            )
        except Exception as e:
            return JSONResponse(
                content={
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32000,
                        "message": str(e)
                    }
                }
            )
    else:
        return JSONResponse(
            content={
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32601,
                    "message": f"Method '{method}' not found"
                }
            }
        )


@app.get("/users", dependencies=[Depends(verify_token)])
async def get_users(email: Optional[str] = None, displayname: Optional[str] = None):
    users = await list_users()
    if email or displayname:
        users = [
            u for u in users if
            (not email or email.lower() in u.get("email", "").lower()) and
            (not displayname or displayname.lower()
             in u.get("displayName", "").lower())
        ]
    return users


@app.post("/users", dependencies=[Depends(verify_token)])
async def create_user(user: UserCreate):
    return await list_users(user.model_dump())


@app.get("/systems", dependencies=[Depends(verify_token)])
async def get_systems(os: Optional[str] = None, os_version: Optional[str] = None, active: Optional[bool] = None, serial_number: Optional[str] = None):
    systems = await list_systems()

    def matches(system):
        os_field = system.get("os", "").lower()
        os_match = os is None or os.lower() in os_field
        active_match = active is None or system.get("active") == active
        os_version_match = os_version is None or os_version.lower(
        ) in system.get("osVersion", "").lower()
        serial_match = serial_number is None or serial_number.lower(
        ) == system.get("serialNumber", "").lower()
        return os_match and active_match and os_version_match and serial_match
    return [s for s in systems if matches(s)]


@app.get("/user-groups", dependencies=[Depends(verify_token)])
async def get_user_groups():
    return await list_user_groups()


@app.get("/system-groups", dependencies=[Depends(verify_token)])
async def get_system_groups():
    return await list_system_groups()


@app.get("/sso-applications", dependencies=[Depends(verify_token)])
async def get_sso_apps():
    return await list_sso_applications()


@app.post("/ask", dependencies=[Depends(verify_token)])
async def ask(prompt: PromptRequest):
    print(f"🧠 Received prompt: {prompt.prompt}")
    tool_name, args = await ask_mcp_local(prompt.prompt)
    print(f"🧠 Matched tool: {tool_name}, args: {args}")

    tool = TOOL_REGISTRY.get(tool_name)
    if not tool:
        raise HTTPException(
            status_code=400, detail=f"Tool '{tool_name}' not found")

    try:
        print(f"⚙️ Calling tool: {tool_name} with args: {args}")
        result = await tool(**args)
        print(f"✅ Tool result: {result}")
        return {"tool": tool_name, "args": args, "result": result}
    except Exception as e:
        print(f"🔥 Tool failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
