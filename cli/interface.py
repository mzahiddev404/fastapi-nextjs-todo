"""
Command-line interface for the TODO application.
Handles argument parsing and command execution.
"""

import argparse
import asyncio
from .database import init_db
from .operations import (
    create_task, list_tasks, get_task, update_task, 
    delete_task, mark_complete, mark_pending, 
    search_tasks, clear_all_tasks
)

async def main():
    """Main CLI interface"""
    
    parser = argparse.ArgumentParser(
        description="TODO CLI - Manage your tasks from the command line",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m cli list
  python -m cli add "Buy groceries" --description "Milk, eggs, bread" --priority high
  python -m cli complete <task_id>
  python -m cli search "groceries"
  python -m cli delete <task_id>
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

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        exit(1)
