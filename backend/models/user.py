# =============================================================================
# USER MODEL
# =============================================================================
# MongoDB document model for user data
# Handles user creation, validation, and data conversion

from bson import ObjectId
from typing import Optional
from datetime import datetime

class User:
    """User model for MongoDB documents"""
    
    def __init__(
        self,
        username: str,
        email: str,
        hashed_password: str,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        _id: Optional[ObjectId] = None
    ):
        self._id = _id or ObjectId()
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert user to dictionary for MongoDB storage"""
        return {
            "_id": self._id,
            "username": self.username,
            "email": self.email,
            "hashed_password": self.hashed_password,
            "is_active": self.is_active,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Create user instance from MongoDB document"""
        return cls(
            _id=data["_id"],
            username=data["username"],
            email=data["email"],
            hashed_password=data["hashed_password"],
            is_active=data.get("is_active", True),
            created_at=data.get("created_at", datetime.utcnow())
        )
    
    @property
    def id(self) -> str:
        """Get user ID as string"""
        return str(self._id)