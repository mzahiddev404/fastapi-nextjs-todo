# =============================================================================
# API DEPENDENCIES
# =============================================================================
# FastAPI dependency functions for authentication
# Handles JWT token validation and user authentication

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Optional
from models.user import User
from crud.user import UserCRUD
from core.security import verify_token
from core.db import get_database

# HTTP Bearer token scheme
security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> User:
    """Get current authenticated user from JWT token"""
    
    # Extract token from credentials
    token = credentials.credentials
    
    # Verify token and get user_id
    user_id = verify_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from database
    user_crud = UserCRUD(db)
    user = await user_crud.get_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user (alias for get_current_user)"""
    return current_user

async def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> Optional[User]:
    """Get current user if token is provided, otherwise return None"""
    
    if credentials is None:
        return None
    
    try:
        token = credentials.credentials
        user_id = verify_token(token)
        if user_id is None:
            return None
        
        user_crud = UserCRUD(db)
        user = await user_crud.get_by_id(user_id)
        return user if user and user.is_active else None
    
    except Exception:
        return None