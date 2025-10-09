# =============================================================================
# LABEL SCHEMAS
# =============================================================================
# Pydantic models for label data validation and serialization
# Handles request/response data structure for label operations

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LabelBase(BaseModel):
    """Base label schema with common fields"""
    name: str
    color: str = "#3B82F6"

class LabelCreate(LabelBase):
    """Schema for label creation request"""
    pass

class LabelUpdate(BaseModel):
    """Schema for label update request"""
    name: Optional[str] = None
    color: Optional[str] = None

class LabelInDB(LabelBase):
    """Label schema with database fields (internal use)"""
    id: str
    user_id: str
    created_at: datetime

class LabelResponse(LabelBase):
    """Label response schema (public data)"""
    id: str
    user_id: str
    created_at: datetime

class LabelWithTaskCount(LabelResponse):
    """Label response with task count"""
    task_count: int