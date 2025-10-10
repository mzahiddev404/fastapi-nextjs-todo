# =============================================================================
# TASK MODEL WITH BEANIE
# =============================================================================
# Modern ODM for MongoDB with automatic validation and type safety
# Much cleaner than manual ObjectId handling!

from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    """Task status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Task(Document):
    """Task model with Beanie - automatic MongoDB integration"""
    
    # Indexed fields for better performance
    user_id: Indexed(PydanticObjectId)
    status: TaskStatus
    
    # Regular fields with validation
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    label_ids: List[PydanticObjectId] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "tasks"  # Collection name
        indexes = [
            "user_id",
            "status",
            "due_date",
            "created_at"
        ]
    
    def __str__(self) -> str:
        return f"Task(title={self.title}, status={self.status})"
    
    def update_status(self, status: TaskStatus):
        """Update task status and timestamp"""
        self.status = status
        self.updated_at = datetime.utcnow()
    
    def add_label(self, label_id: PydanticObjectId):
        """Add label to task"""
        if label_id not in self.label_ids:
            self.label_ids.append(label_id)
            self.updated_at = datetime.utcnow()
    
    def remove_label(self, label_id: PydanticObjectId):
        """Remove label from task"""
        if label_id in self.label_ids:
            self.label_ids.remove(label_id)
            self.updated_at = datetime.utcnow()