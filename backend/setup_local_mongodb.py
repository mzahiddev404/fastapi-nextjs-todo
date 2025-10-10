#!/usr/bin/env python3
"""
Local MongoDB Setup Script
Helps set up local MongoDB for development with Python 3.13
"""

import subprocess
import sys
import os
import asyncio
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_mongodb_installed():
    """Check if MongoDB is installed"""
    try:
        subprocess.run(["mongod", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_mongodb_macos():
    """Install MongoDB on macOS using Homebrew"""
    commands = [
        ("brew tap mongodb/brew", "Adding MongoDB tap"),
        ("brew install mongodb-community", "Installing MongoDB Community Edition"),
        ("brew services start mongodb/brew/mongodb-community", "Starting MongoDB service")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    return True

def create_env_file():
    """Create .env file with local MongoDB configuration"""
    env_content = """# Local MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017/todo_app
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
"""
    
    env_path = Path(".env")
    if env_path.exists():
        print("⚠️  .env file already exists. Backing up to .env.backup")
        env_path.rename(".env.backup")
    
    with open(env_path, "w") as f:
        f.write(env_content)
    
    print("✅ Created .env file with local MongoDB configuration")

async def test_connection():
    """Test MongoDB connection"""
    try:
        from core.db import connect_to_mongo
        await connect_to_mongo()
        print("✅ MongoDB connection test successful!")
        return True
    except Exception as e:
        print(f"❌ MongoDB connection test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up local MongoDB for development...")
    print("=" * 50)
    
    # Check if MongoDB is already installed
    if check_mongodb_installed():
        print("✅ MongoDB is already installed")
    else:
        print("📦 MongoDB not found. Installing...")
        if sys.platform == "darwin":  # macOS
            if not install_mongodb_macos():
                print("❌ Failed to install MongoDB. Please install manually.")
                return False
        else:
            print("❌ This script only supports macOS. Please install MongoDB manually.")
            print("   Visit: https://docs.mongodb.com/manual/installation/")
            return False
    
    # Create .env file
    create_env_file()
    
    # Test connection
    print("\n🧪 Testing MongoDB connection...")
    if asyncio.run(test_connection()):
        print("\n🎉 Setup completed successfully!")
        print("You can now run the backend with: python3 run.py")
        return True
    else:
        print("\n❌ Setup completed but connection test failed.")
        print("Please check MongoDB is running: brew services list | grep mongodb")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
