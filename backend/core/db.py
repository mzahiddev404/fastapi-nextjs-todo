# =============================================================================
# DATABASE CONNECTION MANAGEMENT
# =============================================================================
# Handles MongoDB connection using PyMongo
# Provides async database access for the application

from motor.motor_asyncio import AsyncIOMotorClient
from typing import AsyncGenerator
import os

# Global database client and database instance
client: AsyncIOMotorClient = None
database = None

async def get_database() -> AsyncGenerator:
    """Dependency to get database instance for FastAPI routes"""
    global database
    if database is None:
        await connect_to_mongo()
    yield database

async def connect_to_mongo():
    """Establish connection to MongoDB"""
    global client, database
    
    # Get MongoDB URL from environment variables
    mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    
    # Create MongoDB client
    client = AsyncIOMotorClient(mongo_url)
    database = client.todo_app  # Database name
    
    print("✅ Connected to MongoDB!")

async def close_mongo_connection():
    """Close MongoDB connection on application shutdown"""
    global client
    if client:
        client.close()
        print("❌ Disconnected from MongoDB")