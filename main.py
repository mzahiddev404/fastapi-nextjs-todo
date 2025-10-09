# =============================================================================
# TODO APP - FastAPI Backend with MongoDB
# =============================================================================
# This is our main FastAPI application file
# Handles user authentication and todo management

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from api.v1.auth import router as auth_router
from api.v1.tasks import router as tasks_router
from api.v1.labels import router as labels_router
from core.db import connect_to_mongo, close_mongo_connection

# =============================================================================
# LIFESPAN EVENTS (Modern FastAPI approach)
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown"""
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()

# =============================================================================
# FASTAPI APPLICATION
# =============================================================================

# Create FastAPI app with lifespan events
app = FastAPI(
    title="TODO API", 
    version="1.0.0",
    lifespan=lifespan
)

# CORS setup - allows frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# =============================================================================
# API ROUTES
# =============================================================================

# Include API routes
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(tasks_router, prefix="/api/v1/tasks", tags=["Tasks"])
app.include_router(labels_router, prefix="/api/v1/labels", tags=["Labels"])

# =============================================================================
# HEALTH CHECK
# =============================================================================

@app.get("/")
async def health_check():
    """Check if API is running"""
    return {"message": "TODO API is running! 🚀"}

@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "message": "TODO API is running",
        "version": "1.0.0"
    }

# =============================================================================
# RUN SERVER
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)