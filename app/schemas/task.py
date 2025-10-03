"""Task schemas for API requests and responses."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class TaskBase(BaseModel):
    """Base task schema."""
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    due_date: Optional[datetime] = None
    label_ids: List[str] = []


class TaskCreate(TaskBase):
    """Schema for creating a task."""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    label_ids: Optional[List[str]] = None


class TaskInDB(TaskBase):
    """Task schema as stored in database."""
    id: str
    completed: bool
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Task(TaskBase):
    """Task schema for API responses."""
    id: str
    completed: bool
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
