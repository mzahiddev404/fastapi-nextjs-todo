#!/usr/bin/env python3
"""Create database collections and test data for the FastAPI TODO app."""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from datetime import datetime
import uuid


async def setup_todo_database():
    """Set up the todo_app database with collections and sample data."""
    try:
        # Get connection details from environment
        username = os.getenv("MONGODB_USERNAME")
        password = os.getenv("MONGODB_PASSWORD")
        cluster = os.getenv("MONGODB_CLUSTER")
        
        if not all([username, password, cluster]):
            print("❌ Please set MONGODB_USERNAME, MONGODB_PASSWORD, and MONGODB_CLUSTER environment variables")
            return False
        
        # Construct connection string
        connection_string = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority&appName=Cluster0&ssl=true&tlsAllowInvalidCertificates=true"
        
        print("🔍 Connecting to MongoDB Atlas...")
        client = AsyncIOMotorClient(connection_string, server_api=ServerApi('1'))
        
        # Test connection
        await client.admin.command('ping')
        print("✅ Connected to MongoDB Atlas!")
        
        # Get the todo_app database
        db = client["todo_app"]
        print(f"📁 Using database: todo_app")
        
        # Create collections
        collections_to_create = ["users", "tasks", "labels"]
        
        for collection_name in collections_to_create:
            # Check if collection exists
            existing_collections = await db.list_collection_names()
            
            if collection_name not in existing_collections:
                # Create collection by inserting a document
                await db[collection_name].insert_one({
                    "_id": "init_" + str(uuid.uuid4()),
                    "created_at": datetime.now(),
                    "purpose": "Collection initialization"
                })
                # Remove the initialization document
                await db[collection_name].delete_many({"purpose": "Collection initialization"})
                print(f"✅ Created collection: {collection_name}")
            else:
                print(f"📁 Collection already exists: {collection_name}")
        
        # Create sample data
        print("\n📝 Creating sample data...")
        
        # Sample user
        sample_user = {
            "_id": str(uuid.uuid4()),
            "username": "testuser",
            "email": "test@example.com",
            "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8Kz8Kz8",  # "password"
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        # Insert sample user
        user_result = await db.users.insert_one(sample_user)
        user_id = str(user_result.inserted_id)
        print(f"✅ Created sample user: {sample_user['username']} (ID: {user_id})")
        
        # Sample labels
        sample_labels = [
            {
                "_id": str(uuid.uuid4()),
                "name": "Work",
                "color": "#FF6B6B",
                "user_id": user_id,
                "created_at": datetime.now()
            },
            {
                "_id": str(uuid.uuid4()),
                "name": "Personal",
                "color": "#4ECDC4",
                "user_id": user_id,
                "created_at": datetime.now()
            },
            {
                "_id": str(uuid.uuid4()),
                "name": "Urgent",
                "color": "#FFE66D",
                "user_id": user_id,
                "created_at": datetime.now()
            }
        ]
        
        # Insert sample labels
        label_results = await db.labels.insert_many(sample_labels)
        label_ids = [str(label_id) for label_id in label_results.inserted_ids]
        print(f"✅ Created {len(sample_labels)} sample labels")
        
        # Sample tasks
        sample_tasks = [
            {
                "_id": str(uuid.uuid4()),
                "title": "Complete project documentation",
                "description": "Write comprehensive documentation for the FastAPI TODO app",
                "completed": False,
                "priority": "high",
                "user_id": user_id,
                "label_ids": [label_ids[0]],  # Work label
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "due_date": datetime(2024, 12, 31)
            },
            {
                "_id": str(uuid.uuid4()),
                "title": "Buy groceries",
                "description": "Get milk, bread, and vegetables from the store",
                "completed": False,
                "priority": "medium",
                "user_id": user_id,
                "label_ids": [label_ids[1]],  # Personal label
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            },
            {
                "_id": str(uuid.uuid4()),
                "title": "Fix critical bug",
                "description": "Resolve authentication issue in production",
                "completed": True,
                "priority": "high",
                "user_id": user_id,
                "label_ids": [label_ids[0], label_ids[2]],  # Work + Urgent labels
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "completed_at": datetime.now()
            }
        ]
        
        # Insert sample tasks
        task_results = await db.tasks.insert_many(sample_tasks)
        print(f"✅ Created {len(sample_tasks)} sample tasks")
        
        # Display summary
        print("\n📊 Database Summary:")
        print("=" * 50)
        
        # Count documents in each collection
        user_count = await db.users.count_documents({})
        task_count = await db.tasks.count_documents({})
        label_count = await db.labels.count_documents({})
        
        print(f"👥 Users: {user_count}")
        print(f"📋 Tasks: {task_count}")
        print(f"🏷️  Labels: {label_count}")
        
        # Show sample data
        print("\n📝 Sample Data Preview:")
        print("-" * 30)
        
        # Show one task
        sample_task = await db.tasks.find_one({"completed": False})
        if sample_task:
            print(f"📋 Task: {sample_task['title']}")
            print(f"   Description: {sample_task['description']}")
            print(f"   Priority: {sample_task['priority']}")
            print(f"   Completed: {sample_task['completed']}")
        
        # Show one label
        sample_label = await db.labels.find_one()
        if sample_label:
            print(f"🏷️  Label: {sample_label['name']} ({sample_label['color']})")
        
        client.close()
        
        print("\n🎉 Database setup complete!")
        print("✅ Collections created: users, tasks, labels")
        print("✅ Sample data inserted")
        print("\n📝 Next steps:")
        print("1. Set environment variables:")
        print("   export MONGODB_USERNAME='mzahiddev404_db_user'")
        print("   export MONGODB_PASSWORD='newpassword'")
        print("   export MONGODB_CLUSTER='cluster0.sqcjidp.mongodb.net'")
        print("2. Run the FastAPI app: uvicorn app.main:app --reload")
        print("3. Visit: http://localhost:8000/docs")
        
        return True
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False


if __name__ == "__main__":
    print("🚀 FastAPI TODO App - Database Setup")
    print("=" * 50)
    
    success = asyncio.run(setup_todo_database())
    if not success:
        print("\n❌ Setup failed. Please check your connection details.")
        exit(1)
