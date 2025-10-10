# =============================================================================
# TASK CRUD OPERATIONS WITH BEANIE
# =============================================================================
# Much cleaner database operations using Beanie ODM
# No more manual ObjectId handling or collection management!

from bson import ObjectId
from typing import Optional, List
from models.task import Task, TaskStatus
from schemas.task import TaskCreate, TaskUpdate

class TaskCRUD:
    """CRUD operations for Task model with Beanie"""
    
    async def create(self, task_data: TaskCreate, user_id: str) -> Task:
        """Create a new task for a user"""
        task = Task(
            title=task_data.title,
            description=task_data.description,
            user_id=ObjectId(user_id),
            label_ids=[ObjectId(lid) for lid in (task_data.label_ids or [])],
            due_date=task_data.due_date
        )
        await task.insert()  # Beanie handles everything
        return task
    
    async def get_by_id(self, task_id: str) -> Optional[Task]:
        """Get task by ID"""
        try:
            return await Task.get(ObjectId(task_id))
        except Exception:
            return None
    
    async def get_by_user(self, user_id: str, status: Optional[str] = None) -> List[Task]:
        """Get all tasks for a specific user, optionally filtered by status"""
        query = Task.user_id == ObjectId(user_id)
        if status:
            query = query & (Task.status == TaskStatus(status))
        
        return await Task.find(query).sort("-created_at").to_list()
    
    async def get_by_label(self, label_id: str, user_id: str) -> List[Task]:
        """Get tasks that have a specific label"""
        return await Task.find(
            Task.user_id == ObjectId(user_id) & 
            ObjectId(label_id) in Task.label_ids
        ).sort("-created_at").to_list()
    
    async def update(self, task_id: str, task_data: TaskUpdate) -> Optional[Task]:
        """Update task data"""
        task = await Task.get(ObjectId(task_id))
        if not task:
            return None
        
        # Update fields that are provided
        update_data = task_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == "label_ids" and value:
                setattr(task, field, [ObjectId(lid) for lid in value])
            else:
                setattr(task, field, value)
        
        await task.save()  # Beanie handles the update
        return task
    
    async def update_status(self, task_id: str, status: TaskStatus) -> Optional[Task]:
        """Update task status"""
        task = await Task.get(ObjectId(task_id))
        if task:
            task.update_status(status)
            await task.save()
        return task
    
    async def delete(self, task_id: str) -> bool:
        """Delete task by ID"""
        task = await Task.get(ObjectId(task_id))
        if task:
            await task.delete()
            return True
        return False
    
    async def get_stats(self, user_id: str) -> dict:
        """Get task statistics for a user"""
        tasks = await Task.find(Task.user_id == ObjectId(user_id)).to_list()
        
        stats = {"total": len(tasks), "pending": 0, "in_progress": 0, "completed": 0}
        
        for task in tasks:
            stats[task.status.value] += 1
        
        return stats
    
    async def add_label(self, task_id: str, label_id: str) -> Optional[Task]:
        """Add a label to a task"""
        task = await Task.get(ObjectId(task_id))
        if task:
            task.add_label(ObjectId(label_id))
            await task.save()
        return task
    
    async def remove_label(self, task_id: str, label_id: str) -> Optional[Task]:
        """Remove a label from a task"""
        task = await Task.get(ObjectId(task_id))
        if task:
            task.remove_label(ObjectId(label_id))
            await task.save()
        return task