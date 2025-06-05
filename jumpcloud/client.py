#!/usr/bin/env python3

import os
import time
import httpx
from dotenv import load_dotenv
from cachetools import TTLCache

load_dotenv()

# Base URLs
BASE_URL = "https://console.jumpcloud.com"
BASE_URL_V2 = "https://console.jumpcloud.com/api/v2"
API_KEY = os.getenv("JUMPCLOUD_API_KEY")

HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

DEFAULT_TIMEOUT = 10  # seconds
cache = TTLCache(maxsize=128, ttl=300)

# 🔧 Utility for GET requests with logging and timeout


async def _get(url, params=None):
    print(f"🌐 GET {url}")
    start = time.time()

    try:
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            resp = await client.get(url, headers=HEADERS, params=params)
        duration = round((time.time() - start) * 1000, 2)
        print(f"✅ {resp.status_code} in {duration}ms")
        resp.raise_for_status()
        return resp.json()
    except httpx.RequestError as e:
        print(f"❌ RequestError: {e}")
        raise
    except httpx.TimeoutException:
        print("⏱ Timeout hit!")
        raise


# 🔧 Utility for POST requests with logging and timeout


async def _post(url, json):
    print(f"🚀 POST {url} | Payload: {json}")
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        resp = await client.post(url, headers=HEADERS, json=json)
    print(f"✅ {resp.status_code}")
    resp.raise_for_status()
    return resp.json()

# =========================
# API Wrappers
# =========================


async def list_users():
    if "users" in cache:
        return cache["users"]
    data = await _get(f"{BASE_URL}/api/systemusers")
    cache["users"] = data
    return data


async def create_user(user_data: dict):
    return await _post(f"{BASE_URL_V2}/users", user_data)


async def list_systems(os: str = None, active: bool = None, os_version: str = None, serial_number: str = None):
    data = await _get(f"{BASE_URL}/api/systems", params={"limit": 100})
    systems = data.get("results", []) if isinstance(data, dict) else data

    def matches(system):
        os_field = system.get("os", "").lower()
        # 'mac' matches 'mac os x', 'macos', etc.
        os_match = os is None or os.lower() in os_field
        active_match = active is None or system.get("active") == active
        os_version_match = os_version is None or os_version.lower(
        ) in system.get("osVersion", "").lower()
        serial_match = serial_number is None or serial_number.lower(
        ) == system.get("serialNumber", "").lower()
        return os_match and active_match and os_version_match and serial_match

    return [s for s in systems if matches(s)]


async def get_user_groups(user_id: str):
    return await _get(f"{BASE_URL}/api/systemusers/{user_id}/groups")


async def get_user_systems(user_id: str):
    return await _get(f"{BASE_URL}/api/systemusers/{user_id}/systems")


async def get_system_groups(system_id: str):
    return await _get(f"{BASE_URL}/api/systems/{system_id}/groups")


async def list_user_groups():
    if "user_groups" in cache:
        return cache["user_groups"]
    data = await _get(f"{BASE_URL_V2}/usergroups", params={"limit": 100})
    cache["user_groups"] = data
    return data


async def list_system_groups():
    if "system_groups" in cache:
        return cache["system_groups"]
    data = await _get(f"{BASE_URL_V2}/systemgroups", params={"limit": 100})
    cache["system_groups"] = data
    return data


async def list_sso_applications():
    print("🚀 ENTERED list_sso_applications")
    if "sso_apps" in cache:
        print("⚡️ Returning from cache")
        return cache["sso_apps"]

    url = f"{BASE_URL}/api/applications"
    print(f"🌐 Requesting: {url}")
    data = await _get(url, params={"limit": 100})
    print("✅ Response received")
    cache["sso_apps"] = data
    return data


async def search_users(filter: list = None, fields: str = None):
    """
    Search JumpCloud users using the /api/search/systemusers endpoint.
    :param filter: List of filter dicts, e.g., [{"department": "IT"}]
    :param fields: Comma-separated string of fields to return, e.g., "email username sudo"
    """
    payload = {}
    if filter is not None:
        payload["filter"] = filter
    if fields is not None:
        payload["fields"] = fields
    return await _post(f"{BASE_URL}/api/search/systemusers", payload)
