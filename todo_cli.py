#!/usr/bin/env python3
"""
=============================================================================
TODO CLI - Standalone Python CRUD Application
=============================================================================
A command-line interface for managing TODO tasks with MongoDB
Uses the project_db_url from .env to connect to MongoDB Atlas
"""

import asyncio
import os
import sys
from datetime import datetime
from typing import Optional, List
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie, Document, Indexed, PydanticObjectId
from pydantic import Field
from enum import Enum
import argparse

# Load environment variables from backend/.env
load_dotenv("backend/.env")

# =============================================================================
# MODELS (Simplified for CLI)
# =============================================================================

class TaskStatus(str, Enum):
    """Task status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Task(Document):
    """Simple Task model for CLI operations"""
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    priority: str = "medium"  # low, medium, high
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "cli_tasks"  # Different collection to avoid conflicts

# =============================================================================
# DATABASE CONNECTION
# =============================================================================

async def init_db():
    """Initialize database connection using project_db_url"""
    
    # Get MongoDB URL from .env (using project_db_url)
    mongo_url = os.getenv("project_db_url")
    
    if not mongo_url:
        print("❌ Error: 'project_db_url' not found in .env file")
        sys.exit(1)
    
    print("🔗 Connecting to MongoDB Atlas...")
    
    try:
        # Connect with Python 3.13 compatible SSL settings
        client = AsyncIOMotorClient(
            mongo_url,
            tls=True,
            tlsAllowInvalidCertificates=True,
            tlsAllowInvalidHostnames=True,
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=20000,
            socketTimeoutMS=30000,
            retryWrites=True,
            retryReads=True
        )
        
        # Use todo_app database
        database = client.todo_app
        
        # Initialize Beanie
        await init_beanie(database=database, document_models=[Task])
        
        # Test connection
        await client.admin.command('ping')
        print("✅ Connected to MongoDB successfully!\n")
        
        return client
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        sys.exit(1)

# =============================================================================
# CRUD OPERATIONS
# =============================================================================

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

# =============================================================================
# CLI INTERFACE
# =============================================================================

async def main():
    """Main CLI interface"""
    
    parser = argparse.ArgumentParser(
        description="TODO CLI - Manage your tasks from the command line",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python todo_cli.py list
  python todo_cli.py add "Buy groceries" --description "Milk, eggs, bread" --priority high
  python todo_cli.py complete <task_id>
  python todo_cli.py search "groceries"
  python todo_cli.py delete <task_id>
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument("--status", choices=["pending", "in_progress", "completed"], 
                            help="Filter by status")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("--description", "-d", help="Task description")
    add_parser.add_argument("--priority", "-p", choices=["low", "medium", "high"], 
                           default="medium", help="Task priority")
    
    # Get command
    get_parser = subparsers.add_parser("get", help="Get task details")
    get_parser.add_argument("task_id", help="Task ID")
    
    # Update command
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("task_id", help="Task ID")
    update_parser.add_argument("--title", "-t", help="New title")
    update_parser.add_argument("--description", "-d", help="New description")
    update_parser.add_argument("--priority", "-p", choices=["low", "medium", "high"], 
                              help="New priority")
    update_parser.add_argument("--status", "-s", 
                              choices=["pending", "in_progress", "completed"], 
                              help="New status")
    
    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark task as completed")
    complete_parser.add_argument("task_id", help="Task ID")
    
    # Pending command
    pending_parser = subparsers.add_parser("pending", help="Mark task as pending")
    pending_parser.add_argument("task_id", help="Task ID")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", help="Task ID")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search tasks")
    search_parser.add_argument("keyword", help="Search keyword")
    
    # Clear command
    clear_parser = subparsers.add_parser("clear", help="Delete ALL tasks (use with caution!)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize database
    client = await init_db()
    
    try:
        # Execute command
        if args.command == "list":
            await list_tasks(args.status)
        
        elif args.command == "add":
            await create_task(args.title, args.description, args.priority)
        
        elif args.command == "get":
            await get_task(args.task_id)
        
        elif args.command == "update":
            await update_task(args.task_id, args.title, args.description, 
                            args.priority, args.status)
        
        elif args.command == "complete":
            await mark_complete(args.task_id)
        
        elif args.command == "pending":
            await mark_pending(args.task_id)
        
        elif args.command == "delete":
            await delete_task(args.task_id)
        
        elif args.command == "search":
            await search_tasks(args.keyword)
        
        elif args.command == "clear":
            await clear_all_tasks()
        
    finally:
        # Close connection
        client.close()
        print("\n👋 Goodbye!")

# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

