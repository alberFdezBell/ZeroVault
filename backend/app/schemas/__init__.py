from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime

# Auth Schemas
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

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    role: str = "employee"

class UserCreate(UserBase):
    master_key_salt: str
    auth_hash: str

class UserUpdate(BaseModel):
    auth_hash: Optional[str] = None
    encrypted_dek: Optional[str] = None
    requires_password_change: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    uuid: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

# Secret Schemas
class SecretBase(BaseModel):
    label: str
    encrypted_value: str
    category: Optional[str] = None
    metadata: Optional[str] = None

class SecretCreate(SecretBase):
    pass

class SecretUpdate(BaseModel):
    label: Optional[str] = None
    encrypted_value: Optional[str] = None
    category: Optional[str] = None
    metadata: Optional[str] = None
    is_favorite: Optional[bool] = None

class SecretResponse(SecretBase):
    id: int
    uuid: str
    owner_id: int
    is_favorite: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SecretListResponse(SecretResponse):
    pass

# Audit Log Schemas
class AuditLogResponse(BaseModel):
    id: int
    user_id: int
    secret_id: Optional[int]
    action: str
    ip_address: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
