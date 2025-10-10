# =============================================================================
# USER MODEL WITH BEANIE
# =============================================================================
# Modern ODM for MongoDB with automatic validation and type safety
# Much cleaner than manual ObjectId handling!

from beanie import Document, Indexed
from pydantic import Field, EmailStr
from datetime import datetime
from typing import Optional

class User(Document):
    """User model with Beanie - automatic MongoDB integration"""
    
    # Indexed fields for better performance and uniqueness
    email: Indexed(EmailStr, unique=True)
    username: Indexed(str, unique=True)
    
    # Regular fields with validation
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "users"  # Collection name
        indexes = [
            "email",
            "username", 
            "created_at"
        ]
    
    def __str__(self) -> str:
        return f"User(username={self.username}, email={self.email})"