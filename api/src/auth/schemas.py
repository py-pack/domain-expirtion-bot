from uuid import UUID
from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    session_id: UUID


class GoogleCallbackRequest(BaseModel):
    code: str
    session_id: UUID


class GoogleLoginRequest(BaseModel):
    id_token: str
    session_id: UUID


class RefreshRequest(BaseModel):
    refresh_token: str
    session_id: UUID


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
