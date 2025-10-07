#!/usr/bin/env python3
"""Setup and test MongoDB connection for the FastAPI TODO app."""

import asyncio
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi


async def test_mongodb_connection(connection_string):
    """Test MongoDB connection with the provided connection string."""
    try:
        print(f"🔍 Testing connection to: {connection_string[:50]}...")
        
        # Connect to MongoDB
        client = AsyncIOMotorClient(connection_string, server_api=ServerApi('1'))
        
        # Test the connection
        await client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        
        # List databases
        databases = await client.list_database_names()
        print(f"📊 Available databases: {databases}")
        
        # Create or access our database
        db = client["todo_app"]
        print(f"📁 Using database: todo_app")
        
        # Create collections for our app
        collections_to_create = ["users", "tasks", "labels"]
        existing_collections = await db.list_collection_names()
        
        for collection_name in collections_to_create:
            if collection_name not in existing_collections:
                # Create collection by inserting a dummy document
                await db[collection_name].insert_one({"_id": "init", "created": "setup"})
                # Remove the dummy document
                await db[collection_name].delete_one({"_id": "init"})
                print(f"✅ Created collection: {collection_name}")
            else:
                print(f"📁 Collection already exists: {collection_name}")
        
        # List final collections
        final_collections = await db.list_collection_names()
        print(f"📁 Final collections in 'todo_app': {final_collections}")
        
        # Test inserting a sample task
        sample_task = {
            "title": "Test Task",
            "description": "This is a test task created during setup",
            "completed": False,
            "user_id": "test_user"
        }
        
        result = await db.tasks.insert_one(sample_task)
        print(f"✅ Test task inserted with ID: {result.inserted_id}")
        
        # Clean up test task
        await db.tasks.delete_one({"_id": result.inserted_id})
        print("🧹 Test task cleaned up")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False


def get_connection_string():
    """Get MongoDB connection string from user input."""
    print("MongoDB Connection Setup")
    print("=" * 50)
    print()
    print("Choose your connection method:")
    print("1. MongoDB Atlas (cloud) - Recommended")
    print("2. Local MongoDB")
    print("3. Enter custom connection string")
    print()
    
    choice = input("Enter your choice (1-3): ").strip()
    
    if choice == "1":
        print("\n📝 MongoDB Atlas Setup:")
        print("1. Go to https://www.mongodb.com/atlas")
        print("2. Create a free account and cluster")
        print("3. Get your connection string from 'Connect your application'")
        print("4. It should look like: mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/")
        print()
        
        username = input("Enter your Atlas username: ").strip()
        password = input("Enter your Atlas password: ").strip()
        cluster = input("Enter your cluster name (e.g., cluster0.xxxxx.mongodb.net): ").strip()
        
        if not all([username, password, cluster]):
            print("❌ All fields are required!")
            return None
            
        return f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority&appName=Cluster0"
    
    elif choice == "2":
        print("\n📝 Local MongoDB Setup:")
        print("Make sure MongoDB is running on localhost:27017")
        return "mongodb://localhost:27017"
    
    elif choice == "3":
        print("\n📝 Custom Connection String:")
        connection_string = input("Enter your MongoDB connection string: ").strip()
        return connection_string if connection_string else None
    
    else:
        print("❌ Invalid choice!")
        return None


async def main():
    """Main function to setup and test MongoDB."""
    print("🚀 FastAPI TODO App - MongoDB Setup")
    print("=" * 50)
    print()
    
    connection_string = get_connection_string()
    
    if not connection_string:
        print("❌ No connection string provided. Exiting.")
        sys.exit(1)
    
    print(f"\n🔧 Testing connection...")
    success = await test_mongodb_connection(connection_string)
    
    if success:
        print("\n🎉 MongoDB setup successful!")
        print("✅ Database 'todo_app' is ready")
        print("✅ Collections created: users, tasks, labels")
        print("\n📝 Next steps:")
        print("1. Save your connection string to a .env file")
        print("2. Run: uvicorn app.main:app --reload")
        print("3. Visit: http://localhost:8000/docs")
    else:
        print("\n❌ MongoDB setup failed!")
        print("Please check your connection details and try again.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
