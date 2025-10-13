"""
CRUD operations for CLI task management.
Handles all task-related database operations.
"""

from datetime import datetime
from typing import Optional, List
from beanie import PydanticObjectId
from .models import Task, TaskStatus

async def create_task(title: str, description: str = None, priority: str = "medium"):
    """Create a new task"""
    task = Task(
        title=title,
        description=description,
        priority=priority,
        status=TaskStatus.PENDING
    )
    await task.insert()
    print(f"✅ Task created successfully!")
    print(f"   ID: {task.id}")
    print(f"   Title: {task.title}")
    print(f"   Priority: {task.priority}")
    print(f"   Status: {task.status.value}")

async def list_tasks(status_filter: Optional[str] = None):
    """List all tasks, optionally filtered by status"""
    query = {}
    if status_filter:
        try:
            query["status"] = TaskStatus(status_filter)
        except ValueError:
            print(f"❌ Invalid status. Use: pending, in_progress, or completed")
            return
    
    tasks = await Task.find(query).sort("-created_at").to_list()
    
    if not tasks:
        print("📝 No tasks found.")
        return
    
    print(f"\n📋 Found {len(tasks)} task(s):\n")
    print("=" * 80)
    
    for task in tasks:
        status_icon = "✓" if task.status == TaskStatus.COMPLETED else "○"
        priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task.priority, "⚪")
        
        print(f"{status_icon} [{str(task.id)[:8]}...] {priority_icon} {task.title}")
        print(f"   Status: {task.status.value} | Priority: {task.priority}")
        if task.description:
            print(f"   Description: {task.description}")
        print(f"   Created: {task.created_at.strftime('%Y-%m-%d %H:%M')}")
        print("-" * 80)

async def get_task(task_id: str):
    """Get a specific task by ID"""
    try:
        task = await Task.get(PydanticObjectId(task_id))
        if not task:
            print(f"❌ Task not found: {task_id}")
            return
        
        print("\n📄 Task Details:")
        print("=" * 80)
        print(f"ID: {task.id}")
        print(f"Title: {task.title}")
        print(f"Description: {task.description or 'N/A'}")
        print(f"Status: {task.status.value}")
        print(f"Priority: {task.priority}")
        print(f"Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Updated: {task.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ Error: {e}")

async def update_task(task_id: str, title: str = None, description: str = None, 
                     priority: str = None, status: str = None):
    """Update a task"""
    try:
        task = await Task.get(PydanticObjectId(task_id))
        if not task:
            print(f"❌ Task not found: {task_id}")
            return
        
        updated = False
        
        if title:
            task.title = title
            updated = True
        if description:
            task.description = description
            updated = True
        if priority:
            task.priority = priority
            updated = True
        if status:
            try:
                task.status = TaskStatus(status)
                updated = True
            except ValueError:
                print(f"❌ Invalid status. Use: pending, in_progress, or completed")
                return
        
        if updated:
            task.updated_at = datetime.utcnow()
            await task.save()
            print(f"✅ Task updated successfully!")
            print(f"   ID: {task.id}")
            print(f"   Title: {task.title}")
            print(f"   Status: {task.status.value}")
        else:
            print("⚠️  No updates provided")
            
    except Exception as e:
        print(f"❌ Error: {e}")

async def delete_task(task_id: str):
    """Delete a task"""
    try:
        task = await Task.get(PydanticObjectId(task_id))
        if not task:
            print(f"❌ Task not found: {task_id}")
            return
        
        title = task.title
        await task.delete()
        print(f"✅ Task deleted successfully!")
        print(f"   Title: {title}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

async def mark_complete(task_id: str):
    """Mark a task as completed"""
    await update_task(task_id, status="completed")

async def mark_pending(task_id: str):
    """Mark a task as pending"""
    await update_task(task_id, status="pending")

async def search_tasks(keyword: str):
    """Search tasks by keyword in title or description"""
    # Simple text search (case-insensitive)
    tasks = await Task.find().to_list()
    
    keyword_lower = keyword.lower()
    matching_tasks = [
        task for task in tasks 
        if keyword_lower in task.title.lower() or 
           (task.description and keyword_lower in task.description.lower())
    ]
    
    if not matching_tasks:
        print(f"📝 No tasks found matching '{keyword}'")
        return
    
    print(f"\n🔍 Found {len(matching_tasks)} task(s) matching '{keyword}':\n")
    print("=" * 80)
    
    for task in matching_tasks:
        status_icon = "✓" if task.status == TaskStatus.COMPLETED else "○"
        priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task.priority, "⚪")
        
        print(f"{status_icon} [{str(task.id)[:8]}...] {priority_icon} {task.title}")
        print(f"   Status: {task.status.value} | Priority: {task.priority}")
        if task.description:
            print(f"   Description: {task.description}")
        print("-" * 80)

async def clear_all_tasks():
    """Delete all tasks (use with caution!)"""
    count = await Task.find().count()
    if count == 0:
        print("📝 No tasks to delete.")
        return
    
    print(f"⚠️  Are you sure you want to delete ALL {count} tasks? (yes/no): ", end="")
    confirm = input().strip().lower()
    
    if confirm == "yes":
        result = await Task.delete_all()
        print(f"✅ Deleted {result.deleted_count} tasks successfully!")
    else:
        print("❌ Operation cancelled.")
