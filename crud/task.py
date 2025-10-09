# crud/task.py
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import Optional, List
from models.task import Task, TaskStatus
from schemas.task import TaskCreate, TaskUpdate

class TaskCRUD:
    """CRUD operations for Task model"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.tasks
    
    async def create(self, task_data: TaskCreate, user_id: str) -> Task:
        """Create a new task"""
        task = Task(
            title=task_data.title,
            description=task_data.description,
            user_id=user_id,
            label_ids=task_data.label_ids or [],
            due_date=task_data.due_date
        )
        await self.collection.insert_one(task.to_dict())
        return task
    
    async def get_by_id(self, task_id: str) -> Optional[Task]:
        """Get task by ID"""
        try:
            doc = await self.collection.find_one({"_id": ObjectId(task_id)})
            return Task.from_dict(doc) if doc else None
        except Exception:
            return None
    
    async def get_by_user(self, user_id: str, status: Optional[str] = None) -> List[Task]:
        """Get all tasks for a user"""
        query = {"user_id": user_id}
        if status:
            query["status"] = status
        
        tasks = []
        async for doc in self.collection.find(query).sort("created_at", -1):
            tasks.append(Task.from_dict(doc))
        return tasks
    
    async def get_by_label(self, label_id: str, user_id: str) -> List[Task]:
        """Get tasks by label"""
        tasks = []
        async for doc in self.collection.find({
            "user_id": user_id,
            "label_ids": label_id
        }).sort("created_at", -1):
            tasks.append(Task.from_dict(doc))
        return tasks
    
    async def update(self, task_id: str, task_data: TaskUpdate) -> Optional[Task]:
        """Update task data"""
        update_data = {k: v for k, v in task_data.dict().items() if v is not None}
        if not update_data:
            return await self.get_by_id(task_id)
        
        update_data["updated_at"] = Task().updated_at  # Current timestamp
        
        result = await self.collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": update_data}
        )
        return await self.get_by_id(task_id) if result.modified_count else None
    
    async def update_status(self, task_id: str, status: TaskStatus) -> Optional[Task]:
        """Update task status"""
        result = await self.collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {"status": status.value, "updated_at": Task().updated_at}}
        )
        return await self.get_by_id(task_id) if result.modified_count else None
    
    async def delete(self, task_id: str) -> bool:
        """Delete task by ID"""
        result = await self.collection.delete_one({"_id": ObjectId(task_id)})
        return result.deleted_count > 0
    
    async def get_stats(self, user_id: str) -> dict:
        """Get task statistics for user"""
        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$group": {
                "_id": "$status",
                "count": {"$sum": 1}
            }}
        ]
        
        stats = {"total": 0, "pending": 0, "in_progress": 0, "completed": 0}
        
        async for doc in self.collection.aggregate(pipeline):
            status = doc["_id"]
            count = doc["count"]
            stats["total"] += count
            stats[status] = count
        
        return stats
    
    async def add_label(self, task_id: str, label_id: str) -> Optional[Task]:
        """Add label to task"""
        result = await self.collection.update_one(
            {"_id": ObjectId(task_id)},
            {
                "$addToSet": {"label_ids": label_id},
                "$set": {"updated_at": Task().updated_at}
            }
        )
        return await self.get_by_id(task_id) if result.modified_count else None
    
    async def remove_label(self, task_id: str, label_id: str) -> Optional[Task]:
        """Remove label from task"""
        result = await self.collection.update_one(
            {"_id": ObjectId(task_id)},
            {
                "$pull": {"label_ids": label_id},
                "$set": {"updated_at": Task().updated_at}
            }
        )
        return await self.get_by_id(task_id) if result.modified_count else None
