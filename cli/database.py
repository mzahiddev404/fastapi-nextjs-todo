"""
Database connection utilities for CLI operations.
Handles MongoDB connection and initialization.
"""

import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .models import Task

async def init_db():
    """Initialize database connection using project_db_url"""
    
    # Get MongoDB URL from .env (using project_db_url)
    mongo_url = os.getenv("project_db_url")
    
    if not mongo_url:
        print("❌ Error: 'project_db_url' not found in .env file")
        sys.exit(1)
    
    print("🔗 Connecting to MongoDB Atlas...")
    
    try:
        # Connect with Python 3.13 compatible SSL settings
        client = AsyncIOMotorClient(
            mongo_url,
            tls=True,
            tlsAllowInvalidCertificates=True,
            tlsAllowInvalidHostnames=True,
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=20000,
            socketTimeoutMS=30000,
            retryWrites=True,
            retryReads=True
        )
        
        # Use todo_app database
        database = client.todo_app
        
        # Initialize Beanie
        await init_beanie(database=database, document_models=[Task])
        
        # Test connection
        await client.admin.command('ping')
        print("✅ Connected to MongoDB successfully!\n")
        
        return client
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        sys.exit(1)
