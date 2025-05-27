#!/usr/bin/env python3

from pydantic import BaseModel, EmailStr
from typing import Optional, Dict
from pydantic import BaseModel


class UserCreate(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    username: str
    attributes: Optional[Dict] = {}


class PromptRequest(BaseModel):
    prompt: str
