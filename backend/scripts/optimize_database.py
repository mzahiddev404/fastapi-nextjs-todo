#!/usr/bin/env python3
"""
Database optimization script for the TODO application.
Creates indexes for better query performance and database health.
"""

import asyncio
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from dotenv import load_dotenv

# Add the parent directory to the path so we can import our models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user import User
from models.task import Task
from models.label import Label

# Load environment variables
load_dotenv()

async def create_indexes():
    """Create database indexes for optimal performance"""
    
    # Get MongoDB URL from environment
    mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    
    # Create MongoDB client
    client = AsyncIOMotorClient(mongo_url)
    database = client.todo_app
    
    # Initialize Beanie
    await init_beanie(
        database=database,
        document_models=[User, Task, Label]
    )
    
    print("🔧 Creating database indexes for optimal performance...")
    
    # User collection indexes
    print("📊 Creating User collection indexes...")
    await User.get_motor_collection().create_index("email", unique=True)
    await User.get_motor_collection().create_index("username", unique=True)
    await User.get_motor_collection().create_index("is_active")
    await User.get_motor_collection().create_index("created_at")
    print("✅ User indexes created")
    
    # Task collection indexes
    print("📊 Creating Task collection indexes...")
    await Task.get_motor_collection().create_index("user_id")
    await Task.get_motor_collection().create_index("status")
    await Task.get_motor_collection().create_index("priority")
    await Task.get_motor_collection().create_index("due_date")
    await Task.get_motor_collection().create_index("created_at")
    await Task.get_motor_collection().create_index("updated_at")
    
    # Compound indexes for common queries
    await Task.get_motor_collection().create_index([("user_id", 1), ("status", 1)])
    await Task.get_motor_collection().create_index([("user_id", 1), ("priority", 1)])
    await Task.get_motor_collection().create_index([("user_id", 1), ("due_date", 1)])
    await Task.get_motor_collection().create_index([("user_id", 1), ("created_at", -1)])
    
    # Text search index for task titles and descriptions
    await Task.get_motor_collection().create_index([
        ("title", "text"),
        ("description", "text")
    ])
    
    print("✅ Task indexes created")
    
    # Label collection indexes
    print("📊 Creating Label collection indexes...")
    await Label.get_motor_collection().create_index("user_id")
    await Label.get_motor_collection().create_index("name")
    await Label.get_motor_collection().create_index("color")
    await Label.get_motor_collection().create_index("created_at")
    
    # Compound index for user-specific label queries
    await Label.get_motor_collection().create_index([("user_id", 1), ("name", 1)])
    
    print("✅ Label indexes created")
    
    # Create additional performance indexes
    print("📊 Creating additional performance indexes...")
    
    # Index for task statistics queries
    await Task.get_motor_collection().create_index([
        ("user_id", 1),
        ("status", 1),
        ("created_at", -1)
    ])
    
    # Index for overdue tasks
    await Task.get_motor_collection().create_index([
        ("user_id", 1),
        ("due_date", 1),
        ("status", 1)
    ])
    
    print("✅ Performance indexes created")
    
    # Display index information
    print("\n📈 Index Information:")
    
    # User indexes
    user_indexes = await User.get_motor_collection().list_indexes().to_list(None)
    print(f"User collection: {len(user_indexes)} indexes")
    
    # Task indexes
    task_indexes = await Task.get_motor_collection().list_indexes().to_list(None)
    print(f"Task collection: {len(task_indexes)} indexes")
    
    # Label indexes
    label_indexes = await Label.get_motor_collection().list_indexes().to_list(None)
    print(f"Label collection: {len(label_indexes)} indexes")
    
    print("\n🎉 Database optimization complete!")
    print("💡 Your database is now optimized for better query performance.")
    
    # Close the client
    client.close()

async def analyze_query_performance():
    """Analyze query performance and suggest optimizations"""
    
    print("\n🔍 Analyzing query performance...")
    
    # Get MongoDB URL from environment
    mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    
    # Create MongoDB client
    client = AsyncIOMotorClient(mongo_url)
    database = client.todo_app
    
    # Initialize Beanie
    await init_beanie(
        database=database,
        document_models=[User, Task, Label]
    )
    
    # Analyze collection sizes
    user_count = await User.count()
    task_count = await Task.count()
    label_count = await Label.count()
    
    print(f"📊 Collection Statistics:")
    print(f"  Users: {user_count:,}")
    print(f"  Tasks: {task_count:,}")
    print(f"  Labels: {label_count:,}")
    
    # Analyze task status distribution
    if task_count > 0:
        pipeline = [
            {"$group": {"_id": "$status", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        
        status_distribution = await Task.get_motor_collection().aggregate(pipeline).to_list(None)
        print(f"\n📈 Task Status Distribution:")
        for status in status_distribution:
            print(f"  {status['_id']}: {status['count']:,} ({status['count']/task_count*100:.1f}%)")
    
    # Analyze priority distribution
    if task_count > 0:
        pipeline = [
            {"$group": {"_id": "$priority", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        
        priority_distribution = await Task.get_motor_collection().aggregate(pipeline).to_list(None)
        print(f"\n📈 Task Priority Distribution:")
        for priority in priority_distribution:
            print(f"  {priority['_id']}: {priority['count']:,} ({priority['count']/task_count*100:.1f}%)")
    
    print("\n💡 Performance Recommendations:")
    print("  - Indexes are optimized for common query patterns")
    print("  - Compound indexes support multi-field queries")
    print("  - Text search is available for task content")
    print("  - Consider implementing caching for frequently accessed data")
    
    # Close the client
    client.close()

async def main():
    """Main function to run database optimization"""
    try:
        await create_indexes()
        await analyze_query_performance()
    except Exception as e:
        print(f"❌ Error during database optimization: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
