"""Label API routes."""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from ...core.db import get_database
from ...crud.label import (
    create_label, delete_label, get_label_by_id, get_labels_by_user,
    get_label_by_name, update_label, get_label_usage_count
)
from ...crud.task import get_tasks_by_label
from ...schemas.label import Label, LabelCreate, LabelUpdate
from ...schemas.task import Task
from ...schemas.user import User
from .auth import get_current_user

router = APIRouter()


@router.get("/", response_model=List[Label])
async def get_labels(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> Any:
    """Get all labels for current user."""
    labels = await get_labels_by_user(db, str(current_user.id), skip=skip, limit=limit)
    return labels


@router.post("/", response_model=Label)
async def create_label_endpoint(
    label_data: LabelCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> Any:
    """Create a new label."""
    # Check if label with same name already exists
    existing_label = await get_label_by_name(db, label_data.name, str(current_user.id))
    if existing_label:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Label with this name already exists"
        )
    
    label = await create_label(db, label_data, str(current_user.id))
    return label


@router.get("/{label_id}", response_model=Label)
async def get_label(
    label_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> Any:
    """Get a specific label by ID."""
    label = await get_label_by_id(db, label_id, str(current_user.id))
    if not label:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not found"
        )
    return label


@router.put("/{label_id}", response_model=Label)
async def update_label_endpoint(
    label_id: str,
    label_update: LabelUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> Any:
    """Update a label."""
    # Check if new name conflicts with existing label
    if label_update.name:
        existing_label = await get_label_by_name(db, label_update.name, str(current_user.id))
        if existing_label and str(existing_label.id) != label_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Label with this name already exists"
            )
    
    label = await update_label(db, label_id, str(current_user.id), label_update)
    if not label:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not found"
        )
    return label


@router.delete("/{label_id}")
async def delete_label_endpoint(
    label_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> Any:
    """Delete a label."""
    # Check if label is being used by any tasks
    usage_count = await get_label_usage_count(db, label_id, str(current_user.id))
    if usage_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete label. It is being used by {usage_count} task(s)."
        )
    
    success = await delete_label(db, label_id, str(current_user.id))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not found"
        )
    return {"message": "Label deleted successfully"}


@router.get("/{label_id}/tasks", response_model=List[Task])
async def get_tasks_by_label_endpoint(
    label_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> Any:
    """Get all tasks with a specific label."""
    # Verify label exists
    label = await get_label_by_id(db, label_id, str(current_user.id))
    if not label:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not found"
        )
    
    tasks = await get_tasks_by_label(db, str(current_user.id), label_id)
    return tasks
