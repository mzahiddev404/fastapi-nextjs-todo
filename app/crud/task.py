"""Task CRUD operations."""

from typing import List, Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from ..core.db import get_database
from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate


async def get_task_by_id(db: AsyncIOMotorDatabase, task_id: str, user_id: str) -> Optional[Task]:
    """Get task by ID for specific user."""
    task_data = await db.tasks.find_one({
        "_id": ObjectId(task_id),
        "user_id": ObjectId(user_id)
    })
    if task_data:
        task_data["id"] = str(task_data["_id"])
        return Task(**task_data)
    return None


async def get_tasks_by_user(db: AsyncIOMotorDatabase, user_id: str, skip: int = 0, limit: int = 100) -> List[Task]:
    """Get all tasks for a user."""
    cursor = db.tasks.find({"user_id": ObjectId(user_id)}).skip(skip).limit(limit)
    tasks = []
    async for task_data in cursor:
        task_data["id"] = str(task_data["_id"])
        tasks.append(Task(**task_data))
    return tasks


async def get_tasks_by_label(db: AsyncIOMotorDatabase, user_id: str, label_id: str) -> List[Task]:
    """Get tasks by label for a user."""
    cursor = db.tasks.find({
        "user_id": ObjectId(user_id),
        "label_ids": ObjectId(label_id)
    })
    tasks = []
    async for task_data in cursor:
        task_data["id"] = str(task_data["_id"])
        tasks.append(Task(**task_data))
    return tasks


async def create_task(db: AsyncIOMotorDatabase, task: TaskCreate, user_id: str) -> Task:
    """Create new task."""
    task_dict = task.dict()
    task_dict["user_id"] = ObjectId(user_id)
    task_dict["label_ids"] = [ObjectId(label_id) for label_id in task_dict["label_ids"]]
    task_dict["_id"] = ObjectId()
    
    result = await db.tasks.insert_one(task_dict)
    task_dict["id"] = str(result.inserted_id)
    return Task(**task_dict)


async def update_task(db: AsyncIOMotorDatabase, task_id: str, user_id: str, task_update: TaskUpdate) -> Optional[Task]:
    """Update task."""
    update_data = task_update.dict(exclude_unset=True)
    
    if "label_ids" in update_data:
        update_data["label_ids"] = [ObjectId(label_id) for label_id in update_data["label_ids"]]
    
    if not update_data:
        return await get_task_by_id(db, task_id, user_id)
    
    result = await db.tasks.update_one(
        {"_id": ObjectId(task_id), "user_id": ObjectId(user_id)},
        {"$set": update_data}
    )
    
    if result.modified_count:
        return await get_task_by_id(db, task_id, user_id)
    return None


async def delete_task(db: AsyncIOMotorDatabase, task_id: str, user_id: str) -> bool:
    """Delete task."""
    result = await db.tasks.delete_one({
        "_id": ObjectId(task_id),
        "user_id": ObjectId(user_id)
    })
    return result.deleted_count > 0


async def get_completed_tasks(db: AsyncIOMotorDatabase, user_id: str) -> List[Task]:
    """Get completed tasks for a user."""
    cursor = db.tasks.find({
        "user_id": ObjectId(user_id),
        "completed": True
    })
    tasks = []
    async for task_data in cursor:
        task_data["id"] = str(task_data["_id"])
        tasks.append(Task(**task_data))
    return tasks


async def get_pending_tasks(db: AsyncIOMotorDatabase, user_id: str) -> List[Task]:
    """Get pending tasks for a user."""
    cursor = db.tasks.find({
        "user_id": ObjectId(user_id),
        "completed": False
    })
    tasks = []
    async for task_data in cursor:
        task_data["id"] = str(task_data["_id"])
        tasks.append(Task(**task_data))
    return tasks
