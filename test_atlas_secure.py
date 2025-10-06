#!/usr/bin/env python3
"""Secure test of MongoDB Atlas connection using environment variables."""

import asyncio
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


async def test_atlas_connection():
    """Test MongoDB Atlas connection using environment variables."""
    try:
        # Try to get full URI first, then fall back to components
        connection_string = os.getenv("MONGODB_URI")
        
        if not connection_string:
            # Fall back to individual components
            username = os.getenv("MONGODB_USERNAME", "mzahiddev404_db_user")
            password = os.getenv("MONGODB_PASSWORD")
            cluster = os.getenv("MONGODB_CLUSTER", "cluster0.sqcjidp.mongodb.net")
            
            if not password:
                print("❌ Neither MONGODB_URI nor MONGODB_PASSWORD is set!")
                print("Please set either MONGODB_URI or MONGODB_PASSWORD in your .env file")
                return False
            
            # Construct connection string from components with SSL parameters
            connection_string = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority&appName=Cluster0&ssl=true&tlsAllowInvalidCertificates=true"
            print(f"Using individual components: {username}@{cluster}")
        else:
            print("Using full MONGODB_URI")
        
        print("🔍 Testing MongoDB Atlas connection...")
        if not os.getenv("MONGODB_URI"):
            print(f"Username: {username}")
            print(f"Cluster: {cluster}")
            print(f"Password: {'*' * len(password)} (hidden)")
        else:
            print(f"URI: {connection_string[:50]}... (truncated)")
        
        # Connect to MongoDB Atlas using PyMongo approach
        client = AsyncIOMotorClient(
            connection_string,
            server_api=ServerApi('1')
        )
        
        # Test the connection
        await client.admin.command('ping')
        print("✅ MongoDB Atlas connection successful!")
        
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
        print(f"❌ MongoDB Atlas connection failed: {e}")
        print("\n🔧 Troubleshooting steps:")
        print("1. Make sure MONGODB_PASSWORD is set in your .env file")
        print("2. Check if your IP is whitelisted in MongoDB Atlas")
        print("3. Verify the cluster is running")
        print("4. Check your username and password")
        return False


if __name__ == "__main__":
    print("MongoDB Atlas Secure Connection Test")
    print("=" * 50)
    
    success = asyncio.run(test_atlas_connection())
    if success:
        print("\n🎉 MongoDB Atlas connection successful!")
        print("You can now run your FastAPI app: uvicorn app.main:app --reload")
    else:
        print("\n❌ Connection failed. Please check your .env file.")
        sys.exit(1)
