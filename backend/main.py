# =============================================================================
# TODO APP - FastAPI Backend
# =============================================================================
# Main FastAPI application with MongoDB integration
# Handles authentication, tasks, and labels management
# This is the entry point that sets up all routes and middleware

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Import API routes
from api.v1.auth import router as auth_router
from api.v1.tasks import router as tasks_router
from api.v1.labels import router as labels_router

# Import database connection
from core.db import connect_to_mongo, close_mongo_connection

# =============================================================================
# APPLICATION LIFECYCLE
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown events"""
    # Startup: Connect to MongoDB when the app starts
    await connect_to_mongo()
    yield
    # Shutdown: Clean up MongoDB connection when app stops
    await close_mongo_connection()

# =============================================================================
# FASTAPI APPLICATION
# =============================================================================

# Create FastAPI app with lifespan management
app = FastAPI(
    title="TODO API",
    version="1.0.0",
    description="A simple TODO app with user authentication and task management",
    lifespan=lifespan
)

# CORS middleware allows frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# API ROUTES
# =============================================================================

# Authentication routes
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])

# Task management routes
app.include_router(tasks_router, prefix="/api/v1/tasks", tags=["Tasks"])

# Label management routes
app.include_router(labels_router, prefix="/api/v1/labels", tags=["Labels"])

# =============================================================================
# HEALTH CHECK ENDPOINTS
# =============================================================================

@app.get("/", tags=["Health"])
async def root():
    """Basic health check endpoint"""
    return {"message": "TODO API is running! 🚀"}

@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check with API information"""
    return {
        "status": "healthy",
        "message": "TODO API is running",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/api/v1/auth",
            "tasks": "/api/v1/tasks",
            "labels": "/api/v1/labels",
            "docs": "/docs"
        }
    }

# =============================================================================
# SERVER RUNNER
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)