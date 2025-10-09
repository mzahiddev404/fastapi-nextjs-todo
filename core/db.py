# core/db.py
from motor.motor_asyncio import AsyncIOMotorClient
from typing import AsyncGenerator
import os

# Global database client
client: AsyncIOMotorClient = None
database = None

async def get_database() -> AsyncGenerator:
    """Get database instance"""
    global database
    if database is None:
        await connect_to_mongo()
    yield database

async def connect_to_mongo():
    """Create database connection"""
    global client, database
    
    mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    client = AsyncIOMotorClient(mongo_url)
    database = client.todo_app
    
    print("✅ Connected to MongoDB!")

async def close_mongo_connection():
    """Close database connection"""
    global client
    if client:
        client.close()
        print("❌ Disconnected from MongoDB")
