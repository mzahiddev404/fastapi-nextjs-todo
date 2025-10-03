"""User CRUD operations."""

from typing import Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from ..core.db import get_database
from ..core.security import get_password_hash, verify_password
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate


async def get_user_by_email(db: AsyncIOMotorDatabase, email: str) -> Optional[User]:
    """Get user by email."""
    user_data = await db.users.find_one({"email": email})
    if user_data:
        user_data["id"] = str(user_data["_id"])
        return User(**user_data)
    return None


async def get_user_by_id(db: AsyncIOMotorDatabase, user_id: str) -> Optional[User]:
    """Get user by ID."""
    user_data = await db.users.find_one({"_id": ObjectId(user_id)})
    if user_data:
        user_data["id"] = str(user_data["_id"])
        return User(**user_data)
    return None


async def get_user_by_username(db: AsyncIOMotorDatabase, username: str) -> Optional[User]:
    """Get user by username."""
    user_data = await db.users.find_one({"username": username})
    if user_data:
        user_data["id"] = str(user_data["_id"])
        return User(**user_data)
    return None


async def create_user(db: AsyncIOMotorDatabase, user: UserCreate) -> User:
    """Create new user."""
    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    del user_dict["password"]
    user_dict["hashed_password"] = hashed_password
    user_dict["_id"] = ObjectId()
    
    result = await db.users.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    return User(**user_dict)


async def update_user(db: AsyncIOMotorDatabase, user_id: str, user_update: UserUpdate) -> Optional[User]:
    """Update user."""
    update_data = user_update.dict(exclude_unset=True)
    
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    if not update_data:
        return await get_user_by_id(db, user_id)
    
    update_data["updated_at"] = user_update.updated_at if hasattr(user_update, 'updated_at') else None
    
    result = await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data}
    )
    
    if result.modified_count:
        return await get_user_by_id(db, user_id)
    return None


async def delete_user(db: AsyncIOMotorDatabase, user_id: str) -> bool:
    """Delete user."""
    result = await db.users.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count > 0


async def authenticate_user(db: AsyncIOMotorDatabase, email: str, password: str) -> Optional[User]:
    """Authenticate user with email and password."""
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
