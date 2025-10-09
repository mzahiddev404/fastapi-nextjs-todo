# =============================================================================
# USER CRUD OPERATIONS
# =============================================================================
# Database operations for User model
# Handles all user-related database interactions

from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import Optional
from models.user import User
from schemas.user import UserCreate, UserUpdate

class UserCRUD:
    """CRUD operations for User model"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.users
    
    async def create(self, user_data: UserCreate, hashed_password: str) -> User:
        """Create a new user in the database"""
        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )
        await self.collection.insert_one(user.to_dict())
        return user
    
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        try:
            doc = await self.collection.find_one({"_id": ObjectId(user_id)})
            return User.from_dict(doc) if doc else None
        except Exception:
            return None
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email address"""
        doc = await self.collection.find_one({"email": email})
        return User.from_dict(doc) if doc else None
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        doc = await self.collection.find_one({"username": username})
        return User.from_dict(doc) if doc else None
    
    async def update(self, user_id: str, user_data: UserUpdate) -> Optional[User]:
        """Update user data"""
        update_data = {k: v for k, v in user_data.dict().items() if v is not None}
        if not update_data:
            return await self.get_by_id(user_id)
        
        result = await self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        return await self.get_by_id(user_id) if result.modified_count else None
    
    async def delete(self, user_id: str) -> bool:
        """Delete user by ID"""
        result = await self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0
    
    async def is_email_taken(self, email: str, exclude_id: Optional[str] = None) -> bool:
        """Check if email is already taken by another user"""
        query = {"email": email}
        if exclude_id:
            query["_id"] = {"$ne": ObjectId(exclude_id)}
        
        doc = await self.collection.find_one(query)
        return doc is not None
    
    async def is_username_taken(self, username: str, exclude_id: Optional[str] = None) -> bool:
        """Check if username is already taken by another user"""
        query = {"username": username}
        if exclude_id:
            query["_id"] = {"$ne": ObjectId(exclude_id)}
        
        doc = await self.collection.find_one(query)
        return doc is not None