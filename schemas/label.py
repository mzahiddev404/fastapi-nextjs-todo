# schemas/label.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LabelBase(BaseModel):
    """Base label schema"""
    name: str
    color: str = "#3B82F6"

class LabelCreate(LabelBase):
    """Schema for label creation"""
    pass

class LabelUpdate(BaseModel):
    """Schema for label updates"""
    name: Optional[str] = None
    color: Optional[str] = None

class LabelInDB(LabelBase):
    """Label schema with database fields"""
    id: str
    user_id: str
    created_at: datetime

class LabelResponse(LabelBase):
    """Label response schema"""
    id: str
    user_id: str
    created_at: datetime

class LabelWithTaskCount(LabelResponse):
    """Label response with task count"""
    task_count: int
