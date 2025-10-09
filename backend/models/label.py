# =============================================================================
# LABEL MODEL
# =============================================================================
# MongoDB document model for label data
# Handles label creation and color management

from bson import ObjectId
from typing import Optional
from datetime import datetime

class Label:
    """Label model for MongoDB documents"""
    
    def __init__(
        self,
        name: str,
        color: str = "#3B82F6",  # Default blue color
        user_id: str = None,
        created_at: Optional[datetime] = None,
        _id: Optional[ObjectId] = None
    ):
        self._id = _id or ObjectId()
        self.name = name
        self.color = color
        self.user_id = user_id
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert label to dictionary for MongoDB storage"""
        return {
            "_id": self._id,
            "name": self.name,
            "color": self.color,
            "user_id": self.user_id,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Label":
        """Create label instance from MongoDB document"""
        return cls(
            _id=data["_id"],
            name=data["name"],
            color=data.get("color", "#3B82F6"),
            user_id=data["user_id"],
            created_at=data.get("created_at", datetime.utcnow())
        )
    
    @property
    def id(self) -> str:
        """Get label ID as string"""
        return str(self._id)