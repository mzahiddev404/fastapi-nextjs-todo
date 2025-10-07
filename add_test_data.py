#!/usr/bin/env python3
"""Add test entries to the MongoDB database."""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from datetime import datetime
import uuid


async def add_test_entries():
    """Add test entries to the database."""
    try:
        # Get connection details
        username = os.getenv("MONGODB_USERNAME")
        password = os.getenv("MONGODB_PASSWORD")
        cluster = os.getenv("MONGODB_CLUSTER")
        
        if not all([username, password, cluster]):
            print("❌ Please set MONGODB_USERNAME, MONGODB_PASSWORD, and MONGODB_CLUSTER environment variables")
            return False
        
        # Connect to MongoDB
        connection_string = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority&appName=Cluster0&ssl=true&tlsAllowInvalidCertificates=true"
        
        print("🔍 Connecting to MongoDB...")
        client = AsyncIOMotorClient(connection_string, server_api=ServerApi('1'))
        
        # Test connection
        await client.admin.command('ping')
        print("✅ Connected!")
        
        db = client["todo_app"]
        
        # Add a new user
        new_user = {
            "_id": str(uuid.uuid4()),
            "username": "john_doe",
            "email": "john@example.com",
            "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8Kz8Kz8",
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        user_result = await db.users.insert_one(new_user)
        user_id = str(user_result.inserted_id)
        print(f"✅ Added user: {new_user['username']} (ID: {user_id})")
        
        # Add some labels
        labels = [
            {"name": "Shopping", "color": "#FF9F43", "user_id": user_id},
            {"name": "Health", "color": "#10AC84", "user_id": user_id},
            {"name": "Learning", "color": "#5F27CD", "user_id": user_id}
        ]
        
        label_results = await db.labels.insert_many([
            {
                "_id": str(uuid.uuid4()),
                "name": label["name"],
                "color": label["color"],
                "user_id": label["user_id"],
                "created_at": datetime.now()
            } for label in labels
        ])
        
        label_ids = [str(label_id) for label_id in label_results.inserted_ids]
        print(f"✅ Added {len(labels)} labels: {[label['name'] for label in labels]}")
        
        # Add some tasks
        tasks = [
            {
                "title": "Learn FastAPI",
                "description": "Complete the FastAPI tutorial and build a REST API",
                "completed": False,
                "priority": "high",
                "user_id": user_id,
                "label_ids": [label_ids[2]],  # Learning
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            },
            {
                "title": "Go to gym",
                "description": "Workout session - cardio and weights",
                "completed": False,
                "priority": "medium",
                "user_id": user_id,
                "label_ids": [label_ids[1]],  # Health
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            },
            {
                "title": "Buy laptop charger",
                "description": "Need a new charger for my MacBook",
                "completed": True,
                "priority": "high",
                "user_id": user_id,
                "label_ids": [label_ids[0]],  # Shopping
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "completed_at": datetime.now()
            },
            {
                "title": "Plan weekend trip",
                "description": "Research destinations and book accommodation",
                "completed": False,
                "priority": "low",
                "user_id": user_id,
                "label_ids": [],
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
        ]
        
        task_results = await db.tasks.insert_many([
            {
                "_id": str(uuid.uuid4()),
                **task
            } for task in tasks
        ])
        
        print(f"✅ Added {len(tasks)} tasks")
        
        # Show what we added
        print("\n📊 Database Summary:")
        print("=" * 40)
        
        user_count = await db.users.count_documents({})
        task_count = await db.tasks.count_documents({})
        label_count = await db.labels.count_documents({})
        
        print(f"👥 Total Users: {user_count}")
        print(f"📋 Total Tasks: {task_count}")
        print(f"🏷️  Total Labels: {label_count}")
        
        # Show recent tasks
        print("\n📝 Recent Tasks:")
        print("-" * 30)
        recent_tasks = await db.tasks.find({"user_id": user_id}).sort("created_at", -1).limit(3).to_list(length=3)
        
        for i, task in enumerate(recent_tasks, 1):
            status = "✅" if task["completed"] else "⏳"
            print(f"{i}. {status} {task['title']}")
            print(f"   Priority: {task['priority']}")
            print(f"   Description: {task['description']}")
            print()
        
        client.close()
        print("🎉 Test entries added successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to add test entries: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Adding Test Entries to MongoDB")
    print("=" * 40)
    
    success = asyncio.run(add_test_entries())
    if not success:
        print("\n❌ Failed to add test entries.")
        exit(1)
