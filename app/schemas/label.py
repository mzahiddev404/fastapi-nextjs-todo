"""Label schemas for API requests and responses."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class LabelBase(BaseModel):
    """Base label schema."""
    name: str
    color: str = "#3B82F6"


class LabelCreate(LabelBase):
    """Schema for creating a label."""
    pass


class LabelUpdate(BaseModel):
    """Schema for updating a label."""
    name: Optional[str] = None
    color: Optional[str] = None


class LabelInDB(LabelBase):
    """Label schema as stored in database."""
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Label(LabelBase):
    """Label schema for API responses."""
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
