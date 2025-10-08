# =============================================================================
# TODO APP - FastAPI Backend with MongoDB
# =============================================================================
# This is our main FastAPI application file
# Handles user authentication and todo management

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

# =============================================================================
# CONFIGURATION & SETUP
# =============================================================================

# Load environment variables from .env file
load_dotenv()

# Create FastAPI app
app = FastAPI(title="TODO API", version="1.0.0")

# CORS setup - allows frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# DATABASE CONNECTION
# =============================================================================

client = None
database = None

@app.on_event("startup")
async def startup_db():
    """Connect to MongoDB when server starts"""
    global client, database
    mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    client = AsyncIOMotorClient(mongo_url)
    database = client.todo_app
    print("✅ Connected to MongoDB!")

@app.on_event("shutdown")
async def shutdown_db():
    """Close MongoDB connection when server stops"""
    global client
    if client:
        client.close()
        print("❌ Disconnected from MongoDB")

# =============================================================================
# DATA MODELS
# =============================================================================

class User(BaseModel):
    """User data structure"""
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    """User response (without password)"""
    id: str
    username: str
    email: str

class Todo(BaseModel):
    """Todo item structure"""
    title: str
    description: Optional[str] = None
    completed: bool = False
    user_id: str

class TodoResponse(BaseModel):
    """Todo response structure"""
    id: str
    title: str
    description: Optional[str] = None
    completed: bool
    user_id: str

# =============================================================================
# AUTHENTICATION ROUTES
# =============================================================================

@app.post("/auth/register", response_model=UserResponse)
async def register_user(user: User):
    """Register a new user"""
    # Check if user already exists
    existing = await database.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Save user to database
    result = await database.users.insert_one(user.dict())
    
    return UserResponse(
        id=str(result.inserted_id),
        username=user.username,
        email=user.email
    )

@app.post("/auth/login")
async def login_user(email: str, password: str):
    """Login user"""
    user = await database.users.find_one({"email": email})
    
    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {"message": "Login successful!", "user_id": str(user["_id"])}

# =============================================================================
# TODO ROUTES
# =============================================================================

@app.post("/todos", response_model=TodoResponse)
async def create_todo(todo: Todo):
    """Create a new todo"""
    result = await database.todos.insert_one(todo.dict())
    
    return TodoResponse(
        id=str(result.inserted_id),
        **todo.dict()
    )

@app.get("/todos/{user_id}", response_model=List[TodoResponse])
async def get_user_todos(user_id: str):
    """Get all todos for a user"""
    todos = []
    
    async for todo in database.todos.find({"user_id": user_id}):
        todos.append(TodoResponse(
            id=str(todo["_id"]),
            title=todo["title"],
            description=todo.get("description"),
            completed=todo["completed"],
            user_id=todo["user_id"]
        ))
    
    return todos

@app.put("/todos/{todo_id}")
async def update_todo(todo_id: str, completed: bool):
    """Update todo completion status"""
    result = await database.todos.update_one(
        {"_id": todo_id},
        {"$set": {"completed": completed}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return {"message": "Todo updated!"}

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str):
    """Delete a todo"""
    result = await database.todos.delete_one({"_id": todo_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return {"message": "Todo deleted!"}

# =============================================================================
# HEALTH CHECK
# =============================================================================

@app.get("/")
async def health_check():
    """Check if API is running"""
    return {"message": "TODO API is running! 🚀"}

# =============================================================================
# RUN SERVER
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)