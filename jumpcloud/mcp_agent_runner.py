#!/usr/bin/env python3

import re
from typing import Any, Dict, Tuple, Optional
from jumpcloud.client import (
    list_sso_applications, list_systems, list_users,
    list_user_groups, list_system_groups,
    search_users, search_commands,
)

# Define a tool registry as a dictionary
TOOL_REGISTRY = {
    "list_sso_apps": list_sso_applications,
    "list_systems": list_systems,
    "list_users": list_users,
    "list_user_groups": list_user_groups,
    "list_system_groups": list_system_groups,
    "search_users": search_users,
    "search_commands": search_commands,
}


def match_prompt_to_tool(prompt: str) -> Tuple[Optional[str], Dict[str, Any]]:
    prompt = prompt.lower()
    if "command" in prompt:
        args = {}
        # Check if searching for specific command text
        if "search" in prompt:
            return "search_commands", args
        return "search_commands", args
    if "sso" in prompt or "application" in prompt:
        return "list_sso_apps", {}
    if "system" in prompt or "device" in prompt:
        args = {}
        if "mac" in prompt:
            args["os"] = "mac"
        elif "windows" in prompt:
            args["os"] = "windows"
        elif "ipados" in prompt:
            args["os"] = "ipados"
        if "active" in prompt:
            args["active"] = True
        elif "inactive" in prompt:
            args["active"] = False
        return "list_systems", args
    if "user group" in prompt:
        return "list_user_groups", {}
    if "system group" in prompt:
        return "list_system_groups", {}
    if "user" in prompt:
        args = {}
        match = re.search(r"email\\s*([\\w@.]+)", prompt)
        if match:
            args["email"] = match.group(1)
        return "list_users", args
    return None, {}


async def ask_mcp_local(prompt: str):
    tool_name, args = match_prompt_to_tool(prompt)
    if not tool_name:
        raise ValueError("No matching tool found for prompt")
    tool = TOOL_REGISTRY.get(tool_name)
    if not tool:
        raise ValueError(f"Tool '{tool_name}' not found")
    return tool_name, args
