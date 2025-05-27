#!/usr/bin/env python3

# jumpcloud/auth.py

from fastapi import Header, HTTPException

# Basic API token check (you can expand this later)


def verify_token(x_api_key: str = Header(...)) -> None:
    from os import getenv

    expected = getenv("JUMPCLOUD_API_KEY")
    if not expected or x_api_key != expected:
        raise HTTPException(status_code=403, detail="Forbidden")
