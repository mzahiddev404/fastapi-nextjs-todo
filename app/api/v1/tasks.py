"""Task API routes."""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from ...core.db import get_database
from ...crud.task import (
    create_task, delete_task, get_task_by_id, get_tasks_by_user,
    get_completed_tasks, get_pending_tasks, update_task
)
from ...crud.user import get_user_by_id
from ...schemas.task import Task, TaskCreate, TaskUpdate
from ...schemas.user import User
from .auth import get_current_user

router = APIRouter()


@router.get("/", response_model=List[Task])
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> Any:
    """Get all tasks for current user."""
    tasks = await get_tasks_by_user(db, str(current_user.id), skip=skip, limit=limit)
    return tasks


@router.get("/completed", response_model=List[Task])
async def get_completed_tasks_endpoint(
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> Any:
    """Get completed tasks for current user."""
    tasks = await get_completed_tasks(db, str(current_user.id))
    return tasks


@router.get("/pending", response_model=List[Task])
async def get_pending_tasks_endpoint(
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> Any:
    """Get pending tasks for current user."""
    tasks = await get_pending_tasks(db, str(current_user.id))
    return tasks


@router.post("/", response_model=Task)
async def create_task_endpoint(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> Any:
    """Create a new task."""
    task = await create_task(db, task_data, str(current_user.id))
    return task


@router.get("/{task_id}", response_model=Task)
async def get_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> Any:
    """Get a specific task by ID."""
    task = await get_task_by_id(db, task_id, str(current_user.id))
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.put("/{task_id}", response_model=Task)
async def update_task_endpoint(
    task_id: str,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> Any:
    """Update a task."""
    task = await update_task(db, task_id, str(current_user.id), task_update)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.delete("/{task_id}")
async def delete_task_endpoint(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> Any:
    """Delete a task."""
    success = await delete_task(db, task_id, str(current_user.id))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return {"message": "Task deleted successfully"}
