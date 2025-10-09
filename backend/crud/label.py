# =============================================================================
# LABEL CRUD OPERATIONS
# =============================================================================
# Database operations for Label model
# Handles all label-related database interactions

from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import Optional, List
from models.label import Label
from schemas.label import LabelCreate, LabelUpdate

class LabelCRUD:
    """CRUD operations for Label model"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.labels
    
    async def create(self, label_data: LabelCreate, user_id: str) -> Label:
        """Create a new label for a user"""
        label = Label(
            name=label_data.name,
            color=label_data.color,
            user_id=user_id
        )
        await self.collection.insert_one(label.to_dict())
        return label
    
    async def get_by_id(self, label_id: str) -> Optional[Label]:
        """Get label by ID"""
        try:
            doc = await self.collection.find_one({"_id": ObjectId(label_id)})
            return Label.from_dict(doc) if doc else None
        except Exception:
            return None
    
    async def get_by_user(self, user_id: str) -> List[Label]:
        """Get all labels for a specific user"""
        labels = []
        async for doc in self.collection.find({"user_id": user_id}).sort("created_at", -1):
            labels.append(Label.from_dict(doc))
        return labels
    
    async def update(self, label_id: str, label_data: LabelUpdate) -> Optional[Label]:
        """Update label data"""
        update_data = {k: v for k, v in label_data.dict().items() if v is not None}
        if not update_data:
            return await self.get_by_id(label_id)
        
        result = await self.collection.update_one(
            {"_id": ObjectId(label_id)},
            {"$set": update_data}
        )
        return await self.get_by_id(label_id) if result.modified_count else None
    
    async def delete(self, label_id: str) -> bool:
        """Delete label by ID"""
        result = await self.collection.delete_one({"_id": ObjectId(label_id)})
        return result.deleted_count > 0
    
    async def is_name_taken(self, name: str, user_id: str, exclude_id: Optional[str] = None) -> bool:
        """Check if label name is already taken by the user"""
        query = {"name": name, "user_id": user_id}
        if exclude_id:
            query["_id"] = {"$ne": ObjectId(exclude_id)}
        
        doc = await self.collection.find_one(query)
        return doc is not None
    
    async def get_with_task_count(self, user_id: str) -> List[dict]:
        """Get labels with task count for a user"""
        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$lookup": {
                "from": "tasks",
                "localField": "_id",
                "foreignField": "label_ids",
                "as": "tasks"
            }},
            {"$addFields": {
                "task_count": {"$size": "$tasks"}
            }},
            {"$project": {
                "tasks": 0  # Remove tasks array from output
            }},
            {"$sort": {"created_at": -1}}
        ]
        
        labels = []
        async for doc in self.collection.aggregate(pipeline):
            labels.append({
                "id": str(doc["_id"]),
                "name": doc["name"],
                "color": doc["color"],
                "user_id": doc["user_id"],
                "created_at": doc["created_at"],
                "task_count": doc["task_count"]
            })
        
        return labels