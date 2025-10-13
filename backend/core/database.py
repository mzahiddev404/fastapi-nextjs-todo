from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings

class Database:
    client: AsyncIOMotorClient = None
    database = None

db = Database()

async def get_database():
    if db.database is None:
        await connect_to_mongo()
    return db.database

async def connect_to_mongo():
    """Create database connection"""
    # Configure for MongoDB Atlas SSL if needed
    connection_params = {}
    if "mongodb.net" in settings.project_db_url or "mongodb+srv" in settings.project_db_url:
        # MongoDB Atlas connection - handle SSL
        connection_params = {
            "tlsAllowInvalidCertificates": True,  # For development only
        }
    
    db.client = AsyncIOMotorClient(settings.project_db_url, **connection_params)
    db.database = db.client[settings.project_db_name]
    print("✅ Connected to MongoDB")
    
    # Create indexes on startup
    try:
        from core.database_indexes import create_indexes
        await create_indexes(db.database)
    except Exception as e:
        print(f"⚠️  Warning: Could not create indexes: {e}")

async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        print("❌ Disconnected from MongoDB")
