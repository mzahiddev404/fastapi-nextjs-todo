# =============================================================================
# LABEL MODEL WITH BEANIE
# =============================================================================
# Modern ODM for MongoDB with automatic validation and type safety
# Much cleaner than manual ObjectId handling!

from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field
from typing import Optional
from datetime import datetime

class Label(Document):
    """Label model with Beanie - automatic MongoDB integration"""
    
    # Indexed fields for better performance
    user_id: Indexed(PydanticObjectId)
    name: str
    
    # Regular fields with validation
    color: str = "#3B82F6"  # Default blue color
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "labels"  # Collection name
        indexes = [
            "user_id",
            "name",
            "created_at"
        ]
    
    def __str__(self) -> str:
        return f"Label(name={self.name}, color={self.color})"