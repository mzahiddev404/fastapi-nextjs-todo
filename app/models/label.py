"""Label model for MongoDB."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from bson import ObjectId
from .user import PyObjectId


class Label(BaseModel):
    """Label model for categorizing tasks."""
    
    id: Optional[PyObjectId] = None
    name: str
    color: str = "#3B82F6"  # Default blue color
    user_id: PyObjectId
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
