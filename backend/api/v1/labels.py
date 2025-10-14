from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from bson import ObjectId

from core.database import get_database
from core.security import get_current_active_user
from schemas.label import LabelCreate, LabelUpdate, LabelResponse, LabelListResponse

router = APIRouter(prefix="/labels", tags=["Labels"])


@router.post("", response_model=LabelResponse, response_model_by_alias=False, status_code=status.HTTP_201_CREATED)
async def create_label(
    label_data: LabelCreate,
    current_user: dict = Depends(get_current_active_user)
):
    """Create a new label"""
    db = await get_database()
    
    # Check if label with same name already exists for this user
    existing_label = await db.labels.find_one({
        "user_id": current_user["_id"],
        "name": label_data.name
    })
    
    if existing_label:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Label with name '{label_data.name}' already exists"
        )
    
    # Create label document
    label_dict = {
        "user_id": current_user["_id"],
        "name": label_data.name,
        "color": label_data.color,
        "created_at": datetime.utcnow()
    }
    
    result = await db.labels.insert_one(label_dict)
    created_label = await db.labels.find_one({"_id": result.inserted_id})
    
    # Convert ObjectIds to strings for response
    label_id = str(created_label["_id"])
    created_label["_id"] = label_id
    created_label["id"] = label_id  # Add id field for frontend compatibility
    created_label["user_id"] = str(created_label["user_id"])
    
    return created_label


@router.get("", response_model=LabelListResponse, response_model_by_alias=False)
async def get_labels(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: dict = Depends(get_current_active_user)
):
    """Get all labels for current user"""
    db = await get_database()
    
    # Build query
    query = {"user_id": current_user["_id"]}
    
    # Get labels with pagination
    cursor = db.labels.find(query).sort("created_at", -1).skip(skip).limit(limit)
    labels = await cursor.to_list(length=limit)
    
    # Get total count
    total = await db.labels.count_documents(query)
    
    # Convert ObjectIds to strings
    for label in labels:
        label_id = str(label["_id"])
        label["_id"] = label_id
        label["id"] = label_id  # Add id field for frontend compatibility
        label["user_id"] = str(label["user_id"])
    
    return {"labels": labels, "total": total}


@router.get("/{label_id}", response_model=LabelResponse, response_model_by_alias=False)
async def get_label(
    label_id: str,
    current_user: dict = Depends(get_current_active_user)
):
    """Get a specific label by ID"""
    if not ObjectId.is_valid(label_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid label ID"
        )
    
    db = await get_database()
    label = await db.labels.find_one({
        "_id": ObjectId(label_id),
        "user_id": current_user["_id"]
    })
    
    if not label:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not found"
        )
    
    # Convert ObjectIds to strings
    label_id_str = str(label["_id"])
    label["_id"] = label_id_str
    label["id"] = label_id_str  # Add id field for frontend compatibility
    label["user_id"] = str(label["user_id"])
    
    return label


@router.put("/{label_id}", response_model=LabelResponse, response_model_by_alias=False)
async def update_label(
    label_id: str,
    label_data: LabelUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    """Update a label"""
    if not ObjectId.is_valid(label_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid label ID"
        )
    
    db = await get_database()
    
    # Check if label exists and belongs to user
    existing_label = await db.labels.find_one({
        "_id": ObjectId(label_id),
        "user_id": current_user["_id"]
    })
    
    if not existing_label:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not found"
        )
    
    # Build update document
    update_data = {}
    
    if label_data.name is not None:
        # Check if new name conflicts with existing label
        name_conflict = await db.labels.find_one({
            "user_id": current_user["_id"],
            "name": label_data.name,
            "_id": {"$ne": ObjectId(label_id)}
        })
        if name_conflict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Label with name '{label_data.name}' already exists"
            )
        update_data["name"] = label_data.name
    
    if label_data.color is not None:
        update_data["color"] = label_data.color
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    # Update label
    await db.labels.update_one(
        {"_id": ObjectId(label_id)},
        {"$set": update_data}
    )
    
    # Get updated label
    updated_label = await db.labels.find_one({"_id": ObjectId(label_id)})
    
    # Convert ObjectIds to strings
    label_id_str = str(updated_label["_id"])
    updated_label["_id"] = label_id_str
    updated_label["id"] = label_id_str  # Add id field for frontend compatibility
    updated_label["user_id"] = str(updated_label["user_id"])
    
    return updated_label


@router.delete("/{label_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_label(
    label_id: str,
    current_user: dict = Depends(get_current_active_user)
):
    """Delete a label"""
    if not ObjectId.is_valid(label_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid label ID"
        )
    
    db = await get_database()
    
    # Check if label exists and belongs to user
    result = await db.labels.delete_one({
        "_id": ObjectId(label_id),
        "user_id": current_user["_id"]
    })
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not found"
        )
    
    # Remove this label from all tasks
    await db.tasks.update_many(
        {"user_id": current_user["_id"]},
        {"$pull": {"labels": ObjectId(label_id)}}
    )
    
    return None