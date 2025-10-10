# =============================================================================
# AUTHENTICATION API ROUTES
# =============================================================================
# FastAPI routes for user authentication
# Handles user registration, login, and JWT token management

from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from schemas.user import UserCreate, UserLogin, UserResponse, Token
from models.user import User
from crud.user import UserCRUD
from core.security import get_password_hash, verify_password, create_access_token
from api.deps import get_current_user

router = APIRouter()

# Token expiration time (30 minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserCreate
):
    """Register a new user account and return JWT token"""
    
    user_crud = UserCRUD()
    
    # Check if email is already taken
    if await user_crud.is_email_taken(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username is already taken
    if await user_crud.is_username_taken(user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Hash password and create user
    hashed_password = get_password_hash(user_data.password)
    user = await user_crud.create(user_data, hashed_password)
    
    # Create access token for immediate login
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")

@router.post("/login", response_model=Token)
async def login(
    user_credentials: UserLogin
):
    """Login user and return JWT token"""
    
    user_crud = UserCRUD()
    
    # Get user by email
    user = await user_crud.get_by_email(user_credentials.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current user information"""
    
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )

@router.post("/refresh", response_model=Token)
async def refresh_token(
    current_user: User = Depends(get_current_user)
):
    """Refresh JWT token for current user"""
    
    # Create new access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.id}, expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")