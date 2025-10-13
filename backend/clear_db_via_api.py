#!/usr/bin/env python3
"""
Script to clear old data via the running backend API
Creates an admin endpoint temporarily to clean the database
"""

import asyncio
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models.user import User
from models.task import Task
from models.label import Label
import os
from dotenv import load_dotenv

load_dotenv()

async def clear_collections():
    """Clear all collections using Beanie"""
    
    mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    
    print("🔗 Connecting to MongoDB via Beanie...")
    
    try:
        # Use same connection logic as main app
        if "mongodb+srv://" in mongo_url:
            client = AsyncIOMotorClient(
                mongo_url,
                tls=True,
                tlsAllowInvalidCertificates=True,
                tlsAllowInvalidHostnames=True,
                serverSelectionTimeoutMS=10000,
                connectTimeoutMS=20000,
                socketTimeoutMS=30000,
                retryWrites=True,
                retryReads=True,
                maxPoolSize=10,
                minPoolSize=1,
                maxIdleTimeMS=30000,
                waitQueueTimeoutMS=5000,
                heartbeatFrequencyMS=10000
            )
        else:
            client = AsyncIOMotorClient(mongo_url)
        
        database = client.todo_app
        
        # Initialize Beanie
        await init_beanie(
            database=database,
            document_models=[User, Task, Label]
        )
        
        await client.admin.command('ping')
        print("✅ Connected successfully!")
        
        # Delete all documents using Beanie
        print("\n🗑️  Clearing collections...")
        
        user_count = await User.delete_all()
        print(f"   ✓ Deleted {user_count.deleted_count if user_count else 0} users")
        
        task_count = await Task.delete_all()
        print(f"   ✓ Deleted {task_count.deleted_count if task_count else 0} tasks")
        
        label_count = await Label.delete_all()
        print(f"   ✓ Deleted {label_count.deleted_count if label_count else 0} labels")
        
        print("\n✅ Database cleanup complete!")
        print("💡 Please restart the backend and create a new account.")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(clear_collections())

