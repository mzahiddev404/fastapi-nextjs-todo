#!/usr/bin/env python3
"""
Script to clear old UUID-based data from MongoDB
This fixes the migration issue from UUID to ObjectId
"""

import asyncio
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Load environment variables
load_dotenv()

async def clear_old_data():
    """Clear all collections to fix UUID → ObjectId migration"""
    
    mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    
    print(f"🔗 Connecting to MongoDB...")
    
    try:
        # Create MongoDB client
        if "mongodb+srv://" in mongo_url:
            client = AsyncIOMotorClient(
                mongo_url,
                tls=True,
                tlsAllowInvalidCertificates=True,
                tlsAllowInvalidHostnames=True,
                serverSelectionTimeoutMS=10000
            )
        else:
            client = AsyncIOMotorClient(mongo_url)
        
        database = client.todo_app
        
        # Test connection
        await client.admin.command('ping')
        print("✅ Connected to MongoDB successfully!")
        
        # Clear all collections
        collections = ["users", "tasks", "labels"]
        
        for collection_name in collections:
            collection = database[collection_name]
            result = await collection.delete_many({})
            print(f"🗑️  Deleted {result.deleted_count} documents from '{collection_name}' collection")
        
        print("\n✅ Database cleanup complete!")
        print("💡 You can now create a new account with fresh ObjectId-based data.")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n⚠️  If using MongoDB Atlas, ensure:")
        print("   1. Your IP is whitelisted")
        print("   2. Connection string is correct")
        print("   3. User has proper permissions")

if __name__ == "__main__":
    asyncio.run(clear_old_data())

