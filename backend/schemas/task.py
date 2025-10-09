# =============================================================================
# TASK SCHEMAS
# =============================================================================
# Pydantic models for task data validation and serialization
# Handles request/response data structure for task operations

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TaskBase(BaseModel):
    """Base task schema with common fields"""
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    """Schema for task creation request"""
    label_ids: Optional[List[str]] = None
    due_date: Optional[datetime] = None

class TaskUpdate(BaseModel):
    """Schema for task update request"""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    label_ids: Optional[List[str]] = None
    due_date: Optional[datetime] = None

class TaskInDB(TaskBase):
    """Task schema with database fields (internal use)"""
    id: str
    status: str
    user_id: str
    label_ids: List[str]
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

class TaskResponse(TaskBase):
    """Task response schema (public data)"""
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