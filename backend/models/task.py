# =============================================================================
# TASK MODEL
# =============================================================================
# MongoDB document model for task data
# Handles task creation, status management, and label associations

from bson import ObjectId
from typing import Optional, List
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    """Task status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Task:
    """Task model for MongoDB documents"""
    
    def __init__(
        self,
        title: str,
        description: Optional[str] = None,
        status: TaskStatus = TaskStatus.PENDING,
        user_id: str = None,
        label_ids: Optional[List[str]] = None,
        due_date: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        _id: Optional[ObjectId] = None
    ):
        self._id = _id or ObjectId()
        self.title = title
        self.description = description
        self.status = status
        self.user_id = user_id
        self.label_ids = label_ids or []
        self.due_date = due_date
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert task to dictionary for MongoDB storage"""
        return {
            "_id": self._id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "user_id": self.user_id,
            "label_ids": self.label_ids,
            "due_date": self.due_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create task instance from MongoDB document"""
        return cls(
            _id=data["_id"],
            title=data["title"],
            description=data.get("description"),
            status=TaskStatus(data.get("status", TaskStatus.PENDING)),
            user_id=data["user_id"],
            label_ids=data.get("label_ids", []),
            due_date=data.get("due_date"),
            created_at=data.get("created_at", datetime.utcnow()),
            updated_at=data.get("updated_at", datetime.utcnow())
        )
    
    @property
    def id(self) -> str:
        """Get task ID as string"""
        return str(self._id)
    
    def update_status(self, status: TaskStatus):
        """Update task status and timestamp"""
        self.status = status
        self.updated_at = datetime.utcnow()
    
    def add_label(self, label_id: str):
        """Add label to task"""
        if label_id not in self.label_ids:
            self.label_ids.append(label_id)
            self.updated_at = datetime.utcnow()
    
    def remove_label(self, label_id: str):
        """Remove label from task"""
        if label_id in self.label_ids:
            self.label_ids.remove(label_id)
            self.updated_at = datetime.utcnow()