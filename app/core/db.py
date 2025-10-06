"""Database connection and configuration."""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from .config import settings


class Database:
    """Database connection manager."""
    
    client: AsyncIOMotorClient = None
    database: AsyncIOMotorDatabase = None


db = Database()


async def connect_to_mongo():
    """Create database connection."""
    # Use PyMongo approach for better SSL compatibility
    db.client = AsyncIOMotorClient(
        settings.get_mongodb_uri,
        server_api=ServerApi('1')
    )
    db.database = db.client[settings.database_name]
    print(f"Connected to MongoDB: {settings.database_name}")


async def close_mongo_connection():
    """Close database connection."""
    if db.client:
        db.client.close()
        print("Disconnected from MongoDB")


def get_database() -> AsyncIOMotorDatabase:
    """Get database instance."""
    return db.database
