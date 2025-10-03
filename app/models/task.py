"""Task model for MongoDB."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from bson import ObjectId
from .user import PyObjectId


class Task(BaseModel):
    """Task model."""
    
    id: Optional[PyObjectId] = None
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "medium"  # low, medium, high
    due_date: Optional[datetime] = None
    user_id: PyObjectId
    label_ids: List[PyObjectId] = []
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
