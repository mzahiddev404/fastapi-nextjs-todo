from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from bson import ObjectId

from core.database import get_database
from core.security import get_current_active_user
from schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
from models.task import Priority, TaskStatus

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: dict = Depends(get_current_active_user)
):
    """Create a new task"""
    db = await get_database()
    
    # Convert label IDs to ObjectId
    label_ids = []
    for label_id in task_data.labels:
        if not ObjectId.is_valid(label_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid label ID: {label_id}"
            )
        # Verify label exists and belongs to user
        label = await db.labels.find_one({
            "_id": ObjectId(label_id),
            "user_id": current_user["_id"]
        })
        if not label:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Label not found: {label_id}"
            )
        label_ids.append(ObjectId(label_id))
    
    # Create task document
    task_dict = {
        "user_id": current_user["_id"],
        "title": task_data.title,
        "description": task_data.description,
        "priority": task_data.priority,
        "deadline": task_data.deadline,
        "status": TaskStatus.INCOMPLETE,
        "labels": label_ids,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await db.tasks.insert_one(task_dict)
    created_task = await db.tasks.find_one({"_id": result.inserted_id})
    
    # Convert ObjectIds to strings for response
    created_task["_id"] = str(created_task["_id"])
    created_task["user_id"] = str(created_task["user_id"])
    created_task["labels"] = [str(label_id) for label_id in created_task["labels"]]
    
    return created_task


@router.get("", response_model=TaskListResponse)
async def get_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[Priority] = None,
    label_id: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: dict = Depends(get_current_active_user)
):
    """Get all tasks for current user with optional filters"""
    db = await get_database()
    
    # Build query
    query = {"user_id": current_user["_id"]}
    
    if status:
        query["status"] = status
    
    if priority:
        query["priority"] = priority
    
    if label_id:
        if not ObjectId.is_valid(label_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid label ID: {label_id}"
            )
        query["labels"] = ObjectId(label_id)
    
    # Get tasks with pagination
    cursor = db.tasks.find(query).sort("created_at", -1).skip(skip).limit(limit)
    tasks = await cursor.to_list(length=limit)
    
    # Get total count
    total = await db.tasks.count_documents(query)
    
    # Convert ObjectIds to strings
    for task in tasks:
        task["_id"] = str(task["_id"])
        task["user_id"] = str(task["user_id"])
        task["labels"] = [str(label_id) for label_id in task["labels"]]
    
    return {"tasks": tasks, "total": total}


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    current_user: dict = Depends(get_current_active_user)
):
    """Get a specific task by ID"""
    if not ObjectId.is_valid(task_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID"
        )
    
    db = await get_database()
    task = await db.tasks.find_one({
        "_id": ObjectId(task_id),
        "user_id": current_user["_id"]
    })
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Convert ObjectIds to strings
    task["_id"] = str(task["_id"])
    task["user_id"] = str(task["user_id"])
    task["labels"] = [str(label_id) for label_id in task["labels"]]
    
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    """Update a task"""
    if not ObjectId.is_valid(task_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID"
        )
    
    db = await get_database()
    
    # Check if task exists and belongs to user
    existing_task = await db.tasks.find_one({
        "_id": ObjectId(task_id),
        "user_id": current_user["_id"]
    })
    
    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Build update document
    update_data = {}
    if task_data.title is not None:
        update_data["title"] = task_data.title
    if task_data.description is not None:
        update_data["description"] = task_data.description
    if task_data.priority is not None:
        update_data["priority"] = task_data.priority
    if task_data.deadline is not None:
        update_data["deadline"] = task_data.deadline
    if task_data.status is not None:
        update_data["status"] = task_data.status
    
    # Handle labels
    if task_data.labels is not None:
        label_ids = []
        for label_id in task_data.labels:
            if not ObjectId.is_valid(label_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid label ID: {label_id}"
                )
            # Verify label exists and belongs to user
            label = await db.labels.find_one({
                "_id": ObjectId(label_id),
                "user_id": current_user["_id"]
            })
            if not label:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Label not found: {label_id}"
                )
            label_ids.append(ObjectId(label_id))
        update_data["labels"] = label_ids
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    update_data["updated_at"] = datetime.utcnow()
    
    # Update task
    await db.tasks.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": update_data}
    )
    
    # Get updated task
    updated_task = await db.tasks.find_one({"_id": ObjectId(task_id)})
    
    # Convert ObjectIds to strings
    updated_task["_id"] = str(updated_task["_id"])
    updated_task["user_id"] = str(updated_task["user_id"])
    updated_task["labels"] = [str(label_id) for label_id in updated_task["labels"]]
    
    return updated_task


@router.patch("/{task_id}/status", response_model=TaskResponse)
async def update_task_status(
    task_id: str,
    status_data: dict,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Update only the status of a task (quick toggle between incomplete/complete)
    
    Args:
        task_id: The task ID
        status_data: Dictionary containing the new status {"status": "complete" or "incomplete"}
        current_user: Current authenticated user
    
    Returns:
        Updated task with new status
    """
    if not ObjectId.is_valid(task_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID"
        )
    
    db = await get_database()
    
    # Verify task exists and belongs to user
    task = await db.tasks.find_one({
        "_id": ObjectId(task_id),
        "user_id": current_user["_id"]
    })
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Get new status from request
    new_status = status_data.get("status")
    
    # Validate status value
    if new_status not in [TaskStatus.INCOMPLETE, TaskStatus.COMPLETE]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status value. Must be 'incomplete' or 'complete'"
        )
    
    # Update task status
    update_data = {
        "status": new_status,
        "updated_at": datetime.utcnow()
    }
    
    await db.tasks.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": update_data}
    )
    
    # Get updated task
    updated_task = await db.tasks.find_one({"_id": ObjectId(task_id)})
    
    # Convert ObjectIds to strings
    updated_task["_id"] = str(updated_task["_id"])
    updated_task["user_id"] = str(updated_task["user_id"])
    updated_task["labels"] = [str(label_id) for label_id in updated_task["labels"]]
    
    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    current_user: dict = Depends(get_current_active_user)
):
    """Delete a task"""
    if not ObjectId.is_valid(task_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID"
        )
    
    db = await get_database()
    
    # Check if task exists and belongs to user
    result = await db.tasks.delete_one({
        "_id": ObjectId(task_id),
        "user_id": current_user["_id"]
    })
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return None