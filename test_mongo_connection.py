#!/usr/bin/env python3
"""Test MongoDB connection for the FastAPI TODO app."""

import asyncio
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


async def test_mongodb_connection():
    """Test MongoDB connection."""
    try:
        # Try to connect to MongoDB (Atlas or local)
        connection_string = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        print(f"🔍 Attempting to connect to: {connection_string[:50]}...")
        client = AsyncIOMotorClient(connection_string)
        
        # Test the connection
        await client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        
        # List databases
        databases = await client.list_database_names()
        print(f"📊 Available databases: {databases}")
        
        # Check if our database exists
        db = client["todo_app"]
        collections = await db.list_collection_names()
        print(f"📁 Collections in 'todo_app': {collections}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("\n🔧 Troubleshooting steps:")
        print("1. Make sure MongoDB is running: brew services start mongodb-community")
        print("2. Or start with Docker: docker run -d -p 27017:27017 --name mongodb mongo:7.0")
        print("3. Check if MongoDB is installed: brew list | grep mongodb")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_mongodb_connection())
    sys.exit(0 if success else 1)
