# =============================================================================
# TASK API ROUTES
# =============================================================================
# FastAPI routes for task management
# Handles task CRUD operations and status management

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional, List
from schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskStats
from models.task import Task, TaskStatus
from models.user import User
from crud.task import TaskCRUD
from api.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new task for the current user"""
    
    task_crud = TaskCRUD()
    task = await task_crud.create(task_data, current_user.id)
    
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status.value,
        user_id=task.user_id,
        label_ids=task.label_ids,
        due_date=task.due_date,
        created_at=task.created_at,
        updated_at=task.updated_at
    )

@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    status_filter: Optional[str] = Query(None, alias="status"),
    current_user: User = Depends(get_current_user),
):
    """Get all tasks for the current user, optionally filtered by status"""
    
    task_crud = TaskCRUD()
    tasks = await task_crud.get_by_user(current_user.id, status_filter)
    
    return [
        TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status.value,
            user_id=task.user_id,
            label_ids=task.label_ids,
            due_date=task.due_date,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
        for task in tasks
    ]

@router.get("/stats", response_model=TaskStats)
async def get_task_stats(
    current_user: User = Depends(get_current_user),
):
    """Get task statistics for the current user"""
    
    task_crud = TaskCRUD()
    stats = await task_crud.get_stats(current_user.id)
    
    return TaskStats(**stats)

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
):
    """Get a specific task by ID"""
    
    task_crud = TaskCRUD()
    task = await task_crud.get_by_id(task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )
    
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status.value,
        user_id=task.user_id,
        label_ids=task.label_ids,
        due_date=task.due_date,
        created_at=task.created_at,
        updated_at=task.updated_at
    )

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
):
    """Update a task"""
    
    task_crud = TaskCRUD()
    
    # Check if task exists and belongs to user
    existing_task = await task_crud.get_by_id(task_id)
    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    if existing_task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )
    
    # Update task
    task = await task_crud.update(task_id, task_data)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update task"
        )
    
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status.value,
        user_id=task.user_id,
        label_ids=task.label_ids,
        due_date=task.due_date,
        created_at=task.created_at,
        updated_at=task.updated_at
    )

@router.patch("/{task_id}/status", response_model=TaskResponse)
async def update_task_status(
    task_id: str,
    status: TaskStatus,
    current_user: User = Depends(get_current_user),
):
    """Update task status"""
    
    task_crud = TaskCRUD()
    
    # Check if task exists and belongs to user
    existing_task = await task_crud.get_by_id(task_id)
    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    if existing_task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )
    
    # Update status
    task = await task_crud.update_status(task_id, status)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update task status"
        )
    
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status.value,
        user_id=task.user_id,
        label_ids=task.label_ids,
        due_date=task.due_date,
        created_at=task.created_at,
        updated_at=task.updated_at
    )

@router.delete("/{task_id}")
async def delete_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
):
    """Delete a task"""
    
    task_crud = TaskCRUD()
    
    # Check if task exists and belongs to user
    existing_task = await task_crud.get_by_id(task_id)
    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    if existing_task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )
    
    # Delete task
    success = await task_crud.delete(task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete task"
        )
    
    return {"message": "Task deleted successfully"}