# api/v1/labels.py
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from schemas.label import LabelCreate, LabelUpdate, LabelResponse, LabelWithTaskCount
from models.user import User
from crud.label import LabelCRUD
from core.db import get_database
from api.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=LabelResponse, status_code=status.HTTP_201_CREATED)
async def create_label(
    label_data: LabelCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Create a new label"""
    
    label_crud = LabelCRUD(db)
    
    # Check if label name is already taken by this user
    if await label_crud.is_name_taken(label_data.name, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Label name already exists"
        )
    
    label = await label_crud.create(label_data, current_user.id)
    
    return LabelResponse(
        id=label.id,
        name=label.name,
        color=label.color,
        user_id=label.user_id,
        created_at=label.created_at
    )

@router.get("/", response_model=List[LabelWithTaskCount])
async def get_labels(
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get all labels for current user with task counts"""
    
    label_crud = LabelCRUD(db)
    labels = await label_crud.get_with_task_count(current_user.id)
    
    return [
        LabelWithTaskCount(
            id=label["id"],
            name=label["name"],
            color=label["color"],
            user_id=label["user_id"],
            created_at=label["created_at"],
            task_count=label["task_count"]
        )
        for label in labels
    ]

@router.get("/{label_id}", response_model=LabelResponse)
async def get_label(
    label_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get a specific label"""
    
    label_crud = LabelCRUD(db)
    label = await label_crud.get_by_id(label_id)
    
    if not label:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not found"
        )
    
    if label.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this label"
        )
    
    return LabelResponse(
        id=label.id,
        name=label.name,
        color=label.color,
        user_id=label.user_id,
        created_at=label.created_at
    )

@router.put("/{label_id}", response_model=LabelResponse)
async def update_label(
    label_id: str,
    label_data: LabelUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Update a label"""
    
    label_crud = LabelCRUD(db)
    
    # Check if label exists and belongs to user
    existing_label = await label_crud.get_by_id(label_id)
    if not existing_label:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not found"
        )
    
    if existing_label.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this label"
        )
    
    # Check if new name is taken (if name is being updated)
    if label_data.name and label_data.name != existing_label.name:
        if await label_crud.is_name_taken(label_data.name, current_user.id, label_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Label name already exists"
            )
    
    # Update label
    label = await label_crud.update(label_id, label_data)
    if not label:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update label"
        )
    
    return LabelResponse(
        id=label.id,
        name=label.name,
        color=label.color,
        user_id=label.user_id,
        created_at=label.created_at
    )

@router.delete("/{label_id}")
async def delete_label(
    label_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Delete a label"""
    
    label_crud = LabelCRUD(db)
    
    # Check if label exists and belongs to user
    existing_label = await label_crud.get_by_id(label_id)
    if not existing_label:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not found"
        )
    
    if existing_label.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this label"
        )
    
    # Delete label
    success = await label_crud.delete(label_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete label"
        )
    
    return {"message": "Label deleted successfully"}
