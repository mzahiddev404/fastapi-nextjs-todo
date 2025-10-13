from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from models.task import Priority, TaskStatus


class TaskBase(BaseModel):
    """Base task schema"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    priority: Priority = Priority.MEDIUM
    deadline: datetime
    labels: List[str] = Field(default_factory=list)


class TaskCreate(TaskBase):
    """Schema for creating a new task"""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating a task"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    priority: Optional[Priority] = None
    deadline: Optional[datetime] = None
    status: Optional[TaskStatus] = None
    labels: Optional[List[str]] = None


class TaskResponse(TaskBase):
    """Schema for task response"""
    id: str = Field(..., alias="_id")
    user_id: str
    status: TaskStatus = TaskStatus.INCOMPLETE
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "user_id": "507f1f77bcf86cd799439012",
                "title": "Complete project documentation",
                "description": "Write comprehensive README and API docs",
                "priority": "high",
                "deadline": "2025-10-13T23:59:59",
                "status": "incomplete",
                "labels": ["507f1f77bcf86cd799439013"],
                "created_at": "2025-10-10T12:00:00",
                "updated_at": "2025-10-10T12:00:00"
            }
        }


class TaskListResponse(BaseModel):
    """Schema for list of tasks"""
    tasks: List[TaskResponse]
    total: int