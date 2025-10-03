"""Label CRUD operations."""

from typing import List, Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from ..core.db import get_database
from ..models.label import Label
from ..schemas.label import LabelCreate, LabelUpdate


async def get_label_by_id(db: AsyncIOMotorDatabase, label_id: str, user_id: str) -> Optional[Label]:
    """Get label by ID for specific user."""
    label_data = await db.labels.find_one({
        "_id": ObjectId(label_id),
        "user_id": ObjectId(user_id)
    })
    if label_data:
        label_data["id"] = str(label_data["_id"])
        return Label(**label_data)
    return None


async def get_labels_by_user(db: AsyncIOMotorDatabase, user_id: str, skip: int = 0, limit: int = 100) -> List[Label]:
    """Get all labels for a user."""
    cursor = db.labels.find({"user_id": ObjectId(user_id)}).skip(skip).limit(limit)
    labels = []
    async for label_data in cursor:
        label_data["id"] = str(label_data["_id"])
        labels.append(Label(**label_data))
    return labels


async def get_label_by_name(db: AsyncIOMotorDatabase, name: str, user_id: str) -> Optional[Label]:
    """Get label by name for specific user."""
    label_data = await db.labels.find_one({
        "name": name,
        "user_id": ObjectId(user_id)
    })
    if label_data:
        label_data["id"] = str(label_data["_id"])
        return Label(**label_data)
    return None


async def create_label(db: AsyncIOMotorDatabase, label: LabelCreate, user_id: str) -> Label:
    """Create new label."""
    label_dict = label.dict()
    label_dict["user_id"] = ObjectId(user_id)
    label_dict["_id"] = ObjectId()
    
    result = await db.labels.insert_one(label_dict)
    label_dict["id"] = str(result.inserted_id)
    return Label(**label_dict)


async def update_label(db: AsyncIOMotorDatabase, label_id: str, user_id: str, label_update: LabelUpdate) -> Optional[Label]:
    """Update label."""
    update_data = label_update.dict(exclude_unset=True)
    
    if not update_data:
        return await get_label_by_id(db, label_id, user_id)
    
    result = await db.labels.update_one(
        {"_id": ObjectId(label_id), "user_id": ObjectId(user_id)},
        {"$set": update_data}
    )
    
    if result.modified_count:
        return await get_label_by_id(db, label_id, user_id)
    return None


async def delete_label(db: AsyncIOMotorDatabase, label_id: str, user_id: str) -> bool:
    """Delete label."""
    result = await db.labels.delete_one({
        "_id": ObjectId(label_id),
        "user_id": ObjectId(user_id)
    })
    return result.deleted_count > 0


async def get_label_usage_count(db: AsyncIOMotorDatabase, label_id: str, user_id: str) -> int:
    """Get count of tasks using this label."""
    count = await db.tasks.count_documents({
        "user_id": ObjectId(user_id),
        "label_ids": ObjectId(label_id)
    })
    return count
