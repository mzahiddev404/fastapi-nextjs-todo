"""
CLI-specific models for the TODO application.
Simplified models for command-line operations.
"""

from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field
from enum import Enum
from datetime import datetime

class TaskStatus(str, Enum):
    """Task status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Task(Document):
    """Simple Task model for CLI operations"""
    title: str
    description: str = None
    status: TaskStatus = TaskStatus.PENDING
    priority: str = "medium"  # low, medium, high
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "cli_tasks"  # Different collection to avoid conflicts
