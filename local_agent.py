#!/usr/bin/env python3

# local_agent.py
from jumpcloud.client import (
    list_users,
    list_systems,
    list_sso_applications,
    list_user_groups,
    list_system_groups,
    search_commands,
)

tools = [
    {
        "name": "list_users",
        "description": "List all users optionally filtered by email or display name.",
        "parameters": {
            "type": "object",
            "properties": {
                "email": {"type": "string"},
                "displayname": {"type": "string"},
            },
        },
        "function": list_users,
    },
    {
        "name": "list_systems",
        "description": "List all systems optionally filtered by os, active status, os version, or serial number.",
        "parameters": {
            "type": "object",
            "properties": {
                "os": {"type": "string"},
                "active": {"type": "boolean"},
                "os_version": {"type": "string"},
                "serial_number": {"type": "string"},
            },
        },
        "function": list_systems,
    },
    {
        "name": "list_sso_apps",
        "description": "List all SSO applications.",
        "parameters": {"type": "object", "properties": {}},
        "function": list_sso_applications,
    },
    {
        "name": "list_user_groups",
        "description": "List all user groups.",
        "parameters": {"type": "object", "properties": {}},
        "function": list_user_groups,
    },
    {
        "name": "list_system_groups",
        "description": "List all system groups.",
        "parameters": {"type": "object", "properties": {}},
        "function": list_system_groups,
    },
    {
        "name": "search_commands",
        "description": "Search JumpCloud commands.",
        "parameters": {
            "type": "object",
            "properties": {
                "filter": {"type": "array"},
                "fields": {"type": "string"},
            },
        },
        "function": search_commands,
    },
]

TOOL_REGISTRY = {tool["name"]: tool["function"] for tool in tools}


def ask_mcp_local(prompt: str):
    prompt = prompt.lower()
    if "command" in prompt:
        return "search_commands", {}
    elif "sso" in prompt and "app" in prompt:
        return "list_sso_apps", {}
    elif "mac" in prompt:
        return "list_systems", {"os": "mac", "active": True}
    elif "user groups" in prompt:
        return "list_user_groups", {}
    elif "system groups" in prompt:
        return "list_system_groups", {}
    elif "users" in prompt:
        return "list_users", {}
    return None
