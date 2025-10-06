#!/usr/bin/env python3
"""Test MongoDB Atlas connection using PyMongo directly."""

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get credentials from environment
username = os.getenv("MONGODB_USERNAME")
password = os.getenv("MONGODB_PASSWORD")
cluster = os.getenv("MONGODB_CLUSTER")

if not all([username, password, cluster]):
    print("❌ MONGODB_USERNAME, MONGODB_PASSWORD, and MONGODB_CLUSTER must be set in .env file")
    exit(1)

# Construct URI with environment variables
uri = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority&appName=Cluster0"

print("🔍 Testing MongoDB Atlas connection with PyMongo...")
print(f"URI: {uri[:50]}... (truncated)")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("✅ Pinged your deployment. You successfully connected to MongoDB!")
    
    # List databases
    databases = client.list_database_names()
    print(f"📊 Available databases: {databases}")
    
    # Check our database
    db = client["todo_app"]
    collections = db.list_collection_names()
    print(f"📁 Collections in 'todo_app': {collections}")
    
    client.close()
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\n🔧 Troubleshooting:")
    print("1. Check if your IP is whitelisted in MongoDB Atlas")
    print("2. Verify the cluster is running")
    print("3. Check your username and password")
    print("4. Try connecting from MongoDB Atlas web interface first")

