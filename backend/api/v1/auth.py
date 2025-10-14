from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from bson import ObjectId

from core.config import settings
from core.database import get_database
from core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_active_user
)
from schemas.user import UserCreate, UserResponse, UserLogin, UserUpdate, Token, AuthResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


async def create_default_labels(db, user_id: ObjectId):
    """
    Create default labels (Personal and Work) for a new user.
    
    Args:
        db: Database connection
        user_id: The user's ObjectId
    """
    default_labels = [
        {
            "user_id": user_id,
            "name": "Personal",
            "color": "#3B82F6",  # Blue
            "created_at": datetime.utcnow()
        },
        {
            "user_id": user_id,
            "name": "Work",
            "color": "#EF4444",  # Red
            "created_at": datetime.utcnow()
        }
    ]
    
    # Check if labels already exist to avoid duplicates
    existing_labels = await db.labels.find_one({"user_id": user_id})
    if not existing_labels:
        await db.labels.insert_many(default_labels)


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """Register a new user and create default labels"""
    db = await get_database()
    
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user_dict = {
        "email": user_data.email,
        "name": user_data.name,
        "hashed_password": get_password_hash(user_data.password),
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await db.users.insert_one(user_dict)
    created_user = await db.users.find_one({"_id": result.inserted_id})
    
    # Create default labels for the new user
    await create_default_labels(db, created_user["_id"])
    
    # Convert ObjectId to string for response
    created_user["_id"] = str(created_user["_id"])
    
    # Create access token for the new user
    access_token = create_access_token(data={"sub": created_user["email"]})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": created_user
    }


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login user and return JWT token"""
    db = await get_database()
    
    # Find user by email
    user = await db.users.find_one({"email": form_data.username})
    
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.jwt_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user["_id"])},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login/json", response_model=AuthResponse)
async def login_json(user_data: UserLogin):
    """Login user with JSON payload and return JWT token with user data"""
    db = await get_database()
    
    # Find user by email
    user = await db.users.find_one({"email": user_data.email})
    
    if not user or not verify_password(user_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Convert ObjectId to string for response
    user["_id"] = str(user["_id"])
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.jwt_expire_minutes)
    access_token = create_access_token(
        data={"sub": user["email"]},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_active_user)):
    """Get current user information"""
    current_user["_id"] = str(current_user["_id"])
    return current_user


@router.post("/logout")
async def logout():
    """Logout user (token invalidation should be handled on client side)"""
    return {"message": "Successfully logged out"}


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate):
    """Sign up a new user (alias for /register)"""
    return await register(user_data)


@router.post("/demo", response_model=AuthResponse)
async def demo_login():
    """Login with demo account and create default labels if needed"""
    db = await get_database()
    
    # Demo account credentials
    demo_email = "demo@example.com"
    demo_password = "demo123"
    demo_name = "Demo User"
    
    # Check if demo user exists
    user = await db.users.find_one({"email": demo_email})
    
    # If demo user doesn't exist, create it
    if not user:
        user_dict = {
            "email": demo_email,
            "name": demo_name,
            "hashed_password": get_password_hash(demo_password),
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        result = await db.users.insert_one(user_dict)
        user = await db.users.find_one({"_id": result.inserted_id})
        
        # Create default labels for demo user
        await create_default_labels(db, user["_id"])
    
    # Convert ObjectId to string for response
    user["_id"] = str(user["_id"])
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.jwt_expire_minutes)
    access_token = create_access_token(
        data={"sub": user["email"]},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(current_user: dict = Depends(get_current_active_user)):
    """Refresh access token for authenticated user"""
    # Create new access token
    access_token_expires = timedelta(minutes=settings.jwt_expire_minutes)
    access_token = create_access_token(
        data={"sub": current_user["email"]},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    user_data: UserUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Update current user's profile information.
    Only name and email can be updated.
    """
    db = await get_database()
    
    # Build update data - only include fields that are provided
    update_data = {}
    if user_data.name is not None:
        update_data["name"] = user_data.name
    if user_data.email is not None:
        # Check if email is already taken by another user
        existing_user = await db.users.find_one({
            "email": user_data.email,
            "_id": {"$ne": ObjectId(current_user["_id"])}
        })
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        update_data["email"] = user_data.email
    
    # Nothing to update
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No update data provided"
        )
    
    # Add updated timestamp
    update_data["updated_at"] = datetime.utcnow()
    
    # Update user in database
    result = await db.users.find_one_and_update(
        {"_id": ObjectId(current_user["_id"])},
        {"$set": update_data},
        return_document=True
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Add id field for response
    result["id"] = str(result["_id"])
    
    return result