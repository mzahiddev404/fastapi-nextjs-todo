# =============================================================================
# TEMPORARY ADMIN ENDPOINTS FOR DATABASE CLEANUP
# =============================================================================
# WARNING: Remove this file after cleaning the database!

from fastapi import APIRouter, HTTPException
from models.user import User
from models.task import Task
from models.label import Label

router = APIRouter()

@router.delete("/clear-all-data")
async def clear_all_data():
    """
    DANGER: Delete all data from all collections
    This is a temporary endpoint to fix UUID → ObjectId migration
    """
    try:
        # Delete all documents
        user_result = await User.delete_all()
        task_result = await Task.delete_all()
        label_result = await Label.delete_all()
        
        return {
            "message": "All data cleared successfully",
            "deleted": {
                "users": user_result.deleted_count if user_result else 0,
                "tasks": task_result.deleted_count if task_result else 0,
                "labels": label_result.deleted_count if label_result else 0
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear data: {str(e)}")

@router.get("/health")
async def health_check():
    """Simple health check"""
    return {"status": "ok", "message": "Admin endpoints active"}

