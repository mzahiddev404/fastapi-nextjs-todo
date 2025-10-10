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
    
    # Create MongoDB client with enhanced SSL configuration for Python 3.13 compatibility
    try:
        # For Atlas connections, use enhanced SSL settings with Python 3.13 workaround
        if "mongodb+srv://" in mongo_url:
            # Python 3.13 workaround: Use more permissive SSL settings for Atlas
            client = AsyncIOMotorClient(
                mongo_url,
                tls=True,
                tlsAllowInvalidCertificates=True,   # Workaround for Python 3.13 SSL issues
                tlsAllowInvalidHostnames=True,      # Workaround for Python 3.13 SSL issues
                serverSelectionTimeoutMS=10000,     # 10 second timeout
                connectTimeoutMS=20000,             # 20 second connection timeout
                socketTimeoutMS=30000,              # 30 second socket timeout
                retryWrites=True,                   # Enable retryable writes
                retryReads=True,                    # Enable retryable reads
                maxPoolSize=10,                     # Connection pool size
                minPoolSize=1,                      # Minimum connections
                maxIdleTimeMS=30000,                # 30 second idle timeout
                waitQueueTimeoutMS=5000,            # 5 second wait timeout
                heartbeatFrequencyMS=10000          # 10 second heartbeat
            )
        else:
            # For local connections, use standard settings
            client = AsyncIOMotorClient(mongo_url)
        
        database = client.todo_app  # Database name
        
        # Test the connection with a more robust ping
        await client.admin.command('ping')
        print("✅ Connected to MongoDB!")
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("🔄 Attempting fallback to localhost...")
        
        try:
            # Fallback to localhost for development
            client = AsyncIOMotorClient("mongodb://localhost:27017")
            database = client.todo_app
            await client.admin.command('ping')
            print("✅ Connected to localhost MongoDB!")
        except Exception as fallback_error:
            print(f"❌ Localhost MongoDB also failed: {fallback_error}")
            print("⚠️  Please ensure MongoDB is running locally or fix Atlas connection")
            raise fallback_error

async def close_mongo_connection():
    """Close MongoDB connection on application shutdown"""
    global client
    if client:
        client.close()
        print("❌ Disconnected from MongoDB")