#!/usr/bin/env python3
"""Debug MongoDB Atlas connection issues."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("🔍 MongoDB Atlas Connection Debug")
print("=" * 50)

# Check environment variables
username = os.getenv("MONGODB_USERNAME")
password = os.getenv("MONGODB_PASSWORD")
cluster = os.getenv("MONGODB_CLUSTER")
uri = os.getenv("MONGODB_URI")

print(f"Username: {username}")
print(f"Password: {'*' * len(password) if password else 'NOT SET'}")
print(f"Cluster: {cluster}")
print(f"URI: {uri[:50] + '...' if uri else 'NOT SET'}")

print("\n🔧 Connection String Analysis:")
if uri:
    print(f"Using MONGODB_URI: {uri}")
elif password:
    connection_string = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority&appName=Cluster0"
    print(f"Constructed from components: {connection_string}")
else:
    print("❌ No connection method available!")

print("\n📋 Next Steps:")
print("1. Check MongoDB Atlas Network Access (whitelist your IP)")
print("2. Verify Database User permissions")
print("3. Ensure cluster is running")
print("4. Try connecting from MongoDB Atlas web interface first")

