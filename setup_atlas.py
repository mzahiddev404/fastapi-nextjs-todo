#!/usr/bin/env python3
"""Setup script for MongoDB Atlas configuration."""

import os
import sys


def setup_mongodb_atlas():
    """Guide user through MongoDB Atlas setup."""
    print("🚀 MongoDB Atlas Setup Guide")
    print("=" * 50)
    
    print("\n1. Go to https://www.mongodb.com/atlas")
    print("2. Create a free account")
    print("3. Create a new cluster (choose FREE tier)")
    print("4. Set up database user with username/password")
    print("5. Allow access from anywhere (0.0.0.0/0)")
    print("6. Get your connection string")
    
    print("\n" + "=" * 50)
    print("📝 Configuration Steps:")
    print("=" * 50)
    
    # Get connection details from user
    username = input("\nEnter your MongoDB Atlas username: ").strip()
    password = input("Enter your MongoDB Atlas password: ").strip()
    cluster_url = input("Enter your cluster URL (e.g., cluster0.xxxxx.mongodb.net): ").strip()
    
    if not all([username, password, cluster_url]):
        print("❌ All fields are required!")
        return False
    
    # Create connection string
    connection_string = f"mongodb+srv://{username}:{password}@{cluster_url}/?retryWrites=true&w=majority"
    
    print(f"\n✅ Your MongoDB Atlas connection string:")
    print(f"   {connection_string}")
    
    # Create .env file
    env_content = f"""# MongoDB Atlas Configuration
MONGODB_URI={connection_string}

# JWT Configuration  
JWT_SECRET=your-super-secret-jwt-key-change-in-production
JWT_ALGO=HS256

# App Configuration
DEBUG=false
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("\n✅ Created .env file with your MongoDB Atlas configuration!")
        
        # Test connection
        print("\n🔍 Testing MongoDB Atlas connection...")
        return test_atlas_connection(connection_string)
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False


def test_atlas_connection(connection_string):
    """Test MongoDB Atlas connection."""
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        import asyncio
        
        async def test_connection():
            client = AsyncIOMotorClient(connection_string)
            await client.admin.command('ping')
            print("✅ MongoDB Atlas connection successful!")
            client.close()
            return True
            
        return asyncio.run(test_connection())
        
    except Exception as e:
        print(f"❌ MongoDB Atlas connection failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your username and password")
        print("2. Make sure your IP is whitelisted")
        print("3. Verify the cluster URL is correct")
        print("4. Check if the cluster is running")
        return False


if __name__ == "__main__":
    print("MongoDB Atlas Setup for FastAPI TODO App")
    print("=" * 50)
    
    if setup_mongodb_atlas():
        print("\n🎉 Setup complete! You can now run your FastAPI app.")
        print("Run: uvicorn app.main:app --reload")
    else:
        print("\n❌ Setup failed. Please check the configuration.")
        sys.exit(1)
