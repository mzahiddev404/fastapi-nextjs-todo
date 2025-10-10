# =============================================================================
# LABEL CRUD OPERATIONS WITH BEANIE
# =============================================================================
# Much cleaner database operations using Beanie ODM
# No more manual ObjectId handling or collection management!

from bson import ObjectId
from typing import Optional, List
from models.label import Label
from models.task import Task
from schemas.label import LabelCreate, LabelUpdate

class LabelCRUD:
    """CRUD operations for Label model with Beanie"""
    
    async def create(self, label_data: LabelCreate, user_id: str) -> Label:
        """Create a new label for a user"""
        label = Label(
            name=label_data.name,
            color=label_data.color,
            user_id=ObjectId(user_id)
        )
        await label.insert()  # Beanie handles everything
        return label
    
    async def get_by_id(self, label_id: str) -> Optional[Label]:
        """Get label by ID"""
        try:
            return await Label.get(ObjectId(label_id))
        except Exception:
            return None
    
    async def get_by_user(self, user_id: str) -> List[Label]:
        """Get all labels for a specific user"""
        return await Label.find(Label.user_id == ObjectId(user_id)).sort("-created_at").to_list()
    
    async def update(self, label_id: str, label_data: LabelUpdate) -> Optional[Label]:
        """Update label data"""
        label = await Label.get(ObjectId(label_id))
        if not label:
            return None
        
        # Update fields that are provided
        update_data = label_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(label, field, value)
        
        await label.save()  # Beanie handles the update
        return label
    
    async def delete(self, label_id: str) -> bool:
        """Delete label by ID"""
        label = await Label.get(ObjectId(label_id))
        if label:
            await label.delete()
            return True
        return False
    
    async def is_name_taken(self, name: str, user_id: str, exclude_id: Optional[str] = None) -> bool:
        """Check if label name is already taken by the user"""
        query = (Label.name == name) & (Label.user_id == ObjectId(user_id))
        if exclude_id:
            query = query & (Label.id != ObjectId(exclude_id))
        
        label = await Label.find_one(query)
        return label is not None
    
    async def get_with_task_count(self, user_id: str) -> List[dict]:
        """Get labels with task count for a user"""
        labels = await Label.find(Label.user_id == ObjectId(user_id)).sort("-created_at").to_list()
        
        result = []
        for label in labels:
            # Count tasks that use this label
            task_count = await Task.find(
                Task.user_id == ObjectId(user_id) & 
                ObjectId(label.id) in Task.label_ids
            ).count()
            
            result.append({
                "id": str(label.id),
                "name": label.name,
                "color": label.color,
                "user_id": str(label.user_id),
                "created_at": label.created_at,
                "task_count": task_count
            })
        
        return result