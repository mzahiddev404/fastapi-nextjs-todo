# schemas/task.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .user import UserResponse

class TaskBase(BaseModel):
    """Base task schema"""
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    """Schema for task creation"""
    label_ids: Optional[List[str]] = None
    due_date: Optional[datetime] = None

class TaskUpdate(BaseModel):
    """Schema for task updates"""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    label_ids: Optional[List[str]] = None
    due_date: Optional[datetime] = None

class TaskInDB(TaskBase):
    """Task schema with database fields"""
    id: str
    status: str
    user_id: str
    label_ids: List[str]
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

class TaskResponse(TaskBase):
    """Task response schema"""
    id: str
    status: str
    user_id: str
    label_ids: List[str]
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

class TaskWithLabels(TaskResponse):
    """Task response with label details"""
    labels: Optional[List[dict]] = None

class TaskStats(BaseModel):
    """Task statistics schema"""
    total: int
    pending: int
    in_progress: int
    completed: int
