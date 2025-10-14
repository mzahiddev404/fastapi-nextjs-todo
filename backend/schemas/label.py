from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class LabelBase(BaseModel):
    """Base label schema"""
    name: str = Field(..., min_length=1, max_length=50)
    color: str = Field(default="#3B82F6", pattern="^#[0-9A-Fa-f]{6}$")


class LabelCreate(LabelBase):
    """Schema for creating a new label"""
    pass


class LabelUpdate(BaseModel):
    """Schema for updating a label"""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")


class LabelResponse(LabelBase):
    """Schema for label response"""
    id: str = Field(..., alias="_id")
    user_id: str
    created_at: datetime

    # Use Pydantic v2 ConfigDict for proper configuration
    model_config = ConfigDict(
        populate_by_name=True,  # Allow _id as input alias
        from_attributes=True,   # Allow ORM mode
        json_schema_extra={
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "user_id": "507f1f77bcf86cd799439012",
                "name": "Work",
                "color": "#EF4444",
                "created_at": "2025-10-10T12:00:00"
            }
        }
    )


class LabelListResponse(BaseModel):
    """Schema for list of labels"""
    labels: List[LabelResponse]
    total: int