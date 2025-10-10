# =============================================================================
# USER CRUD OPERATIONS WITH BEANIE
# =============================================================================
# Much cleaner database operations using Beanie ODM
# No more manual ObjectId handling or collection management!

from bson import ObjectId
from typing import Optional
from models.user import User
from schemas.user import UserCreate, UserUpdate

class UserCRUD:
    """CRUD operations for User model with Beanie"""
    
    async def create(self, user_data: UserCreate, hashed_password: str) -> User:
        """Create a new user in the database"""
        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )
        await user.insert()  # That's it! Beanie handles everything
        return user
    
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        try:
            return await User.get(ObjectId(user_id))
        except Exception:
            return None
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email address"""
        return await User.find_one(User.email == email)
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return await User.find_one(User.username == username)
    
    async def update(self, user_id: str, user_data: UserUpdate) -> Optional[User]:
        """Update user data"""
        user = await User.get(ObjectId(user_id))
        if not user:
            return None
        
        # Update fields that are provided
        update_data = user_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        await user.save()  # Beanie handles the update
        return user
    
    async def delete(self, user_id: str) -> bool:
        """Delete user by ID"""
        user = await User.get(ObjectId(user_id))
        if user:
            await user.delete()
            return True
        return False
    
    async def is_email_taken(self, email: str, exclude_id: Optional[str] = None) -> bool:
        """Check if email is already taken by another user"""
        query = User.email == email
        if exclude_id:
            query = query & (User.id != ObjectId(exclude_id))
        
        user = await User.find_one(query)
        return user is not None
    
    async def is_username_taken(self, username: str, exclude_id: Optional[str] = None) -> bool:
        """Check if username is already taken by another user"""
        query = User.username == username
        if exclude_id:
            query = query & (User.id != ObjectId(exclude_id))
        
        user = await User.find_one(query)
        return user is not None