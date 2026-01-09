from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    mobile: str
    password: str
    identity: Optional[str] = None
    avatar_file_id: Optional[str] = None
    gender: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    mobile: str
    identity: Optional[str] = None
    avatar_file_id: Optional[str] = None
    gender: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserLogin(BaseModel):
    email: EmailStr
    password: str        