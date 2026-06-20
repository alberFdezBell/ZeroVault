from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID

class PreLoginRequest(BaseModel):
    email: EmailStr

class PreLoginResponse(BaseModel):
    master_key_salt: str

class LoginRequest(BaseModel):
    email: EmailStr
    auth_hash: str = Field(..., min_length=64, max_length=255)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    encrypted_dek: str
    requires_password_change: bool