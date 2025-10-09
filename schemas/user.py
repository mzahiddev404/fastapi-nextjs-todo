# schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Base user schema"""
    username: str
    email: EmailStr

class UserCreate(UserBase):
    """Schema for user creation"""
    password: str

class UserUpdate(BaseModel):
    """Schema for user updates"""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserInDB(UserBase):
    """User schema with database fields"""
    id: str
    hashed_password: str
    is_active: bool
    created_at: datetime

class UserResponse(UserBase):
    """User response schema (without sensitive data)"""
    id: str
    is_active: bool
    created_at: datetime

class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str

class Token(BaseModel):
    """JWT token response schema"""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Token data schema"""
    user_id: Optional[str] = None
