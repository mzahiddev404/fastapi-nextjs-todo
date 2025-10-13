"""
Database indexes for MongoDB collections
This script creates indexes for better query performance
"""

async def create_indexes(database):
    """Create database indexes for all collections"""
    
    # Users collection indexes
    await database.users.create_index("email", unique=True)
    await database.users.create_index("created_at")
    
    # Tasks collection indexes
    await database.tasks.create_index([("user_id", 1), ("created_at", -1)])
    await database.tasks.create_index([("user_id", 1), ("status", 1)])
    await database.tasks.create_index([("user_id", 1), ("priority", 1)])
    await database.tasks.create_index([("user_id", 1), ("deadline", 1)])
    await database.tasks.create_index([("user_id", 1), ("labels", 1)])
    
    # Labels collection indexes
    await database.labels.create_index([("user_id", 1), ("name", 1)], unique=True)
    await database.labels.create_index([("user_id", 1), ("created_at", -1)])
    
    print("✅ Database indexes created successfully!")
