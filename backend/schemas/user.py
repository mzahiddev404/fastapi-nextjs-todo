# =============================================================================
# USER SCHEMAS
# =============================================================================
# Pydantic models for user data validation and serialization
# Handles request/response data structure for user operations

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Base user schema with common fields"""
    username: str
    email: EmailStr

class UserCreate(UserBase):
    """Schema for user registration request"""
    password: str

class UserUpdate(BaseModel):
    """Schema for user update request"""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserInDB(UserBase):
    """User schema with database fields (internal use)"""
    id: str
    hashed_password: str
    is_active: bool
    created_at: datetime

class UserResponse(UserBase):
    """User response schema (public data without sensitive info)"""
    id: str
    is_active: bool
    created_at: datetime

class UserLogin(BaseModel):
    """Schema for user login request"""
    email: EmailStr
    password: str

class Token(BaseModel):
    """JWT token response schema"""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Token data schema for internal use"""
    user_id: Optional[str] = None