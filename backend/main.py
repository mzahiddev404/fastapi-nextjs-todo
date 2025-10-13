# =============================================================================
# TODO APP - FastAPI Backend
# =============================================================================
# Main FastAPI application with MongoDB integration
# Handles authentication, tasks, and labels management
# This is the entry point that sets up all routes and middleware

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import time
import logging
import os
import uvicorn

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import API routes
from api.v1.auth import router as auth_router
from api.v1.tasks import router as tasks_router
from api.v1.labels import router as labels_router
from api.v1.admin import router as admin_router  # TEMPORARY: For database cleanup
from api.v1.health import router as health_router

# Import database connection
from core.database import connect_to_mongo, close_mongo_connection

# =============================================================================
# APPLICATION LIFECYCLE
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown events"""
    # Startup: Connect to MongoDB when the app starts
    try:
        await connect_to_mongo()
        logger.info("✅ Database connected successfully")
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        raise

    yield
    
    # Shutdown: Clean up MongoDB connection when app stops
    try:
        await close_mongo_connection()
        logger.info("✅ Database connection closed")
    except Exception as e:
        logger.error(f"❌ Error closing database connection: {e}")

# =============================================================================
# FASTAPI APPLICATION
# =============================================================================

# Create FastAPI app with lifespan management
app = FastAPI(
    title="TODO API",
    version="1.0.0",
    description="A production-ready TODO app with user authentication and task management",
    lifespan=lifespan
)

# =============================================================================
# MIDDLEWARE CONFIGURATION
# =============================================================================

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests with timing information"""
    start_time = time.time()
    
    # Log request details
    logger.info(f"📥 {request.method} {request.url.path} - {request.client.host}")
    
    # Process request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Log response details
    logger.info(f"📤 {request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
    
    return response

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time and custom headers to all responses"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Add custom headers
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-App-Name"] = "TODO-API"
    response.headers["X-App-Version"] = "1.0.0"
    response.headers["X-Environment"] = os.getenv("ENVIRONMENT", "development")
    
    return response

# Import security middleware
from middleware.security import security_middleware

# Apply security middleware
app.middleware("http")(security_middleware)

# Environment-based CORS configuration
allowed_origins = [
    "http://localhost:3000",  # Development frontend
    "http://127.0.0.1:3000",  # Alternative localhost
    "http://localhost:3001",  # Alternative port
    "http://127.0.0.1:3001",  # Alternative port
]

# Add production origins if specified
if os.getenv("ALLOWED_ORIGINS"):
    allowed_origins.extend(os.getenv("ALLOWED_ORIGINS").split(","))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

# =============================================================================
# API ROUTES
# =============================================================================

# Authentication routes
app.include_router(auth_router, prefix="/api/v1", tags=["Authentication"])

# Task management routes
app.include_router(tasks_router, prefix="/api/v1", tags=["Tasks"])

# Label management routes
app.include_router(labels_router, prefix="/api/v1", tags=["Labels"])

# Admin routes (TEMPORARY - for database cleanup)
app.include_router(admin_router, prefix="/api/v1/admin", tags=["Admin"])

# Health check routes
app.include_router(health_router, prefix="/api/v1", tags=["Health"])

# =============================================================================
# ROOT ENDPOINTS
# =============================================================================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with basic API information"""
    return {
        "message": "TODO API is running! 🚀",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "docs": "/docs",
        "health": "/api/v1/health"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "message": "TODO API is running",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "endpoints": {
            "auth": "/api/v1/auth",
            "tasks": "/api/v1/tasks",
            "labels": "/api/v1/labels",
            "docs": "/docs"
        }
    }

# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.exception_handler(400)
async def bad_request_handler(request: Request, exc: HTTPException):
    """Handle 400 Bad Request errors"""
    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "code": 400,
                "message": "Bad Request",
                "detail": str(exc.detail) if hasattr(exc, 'detail') else "Validation error",
                "type": "validation_error"
            }
        }
    )

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Handle 404 Not Found errors"""
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "code": 404,
                "message": "Not Found",
                "detail": str(exc.detail) if hasattr(exc, 'detail') else "Resource not found",
                "type": "not_found_error"
            }
        }
    )

@app.exception_handler(500)
async def internal_server_error_handler(request: Request, exc: Exception):
    """Handle 500 Internal Server Error"""
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": 500,
                "message": "Internal Server Error",
                "detail": "An unexpected error occurred",
                "type": "internal_error"
            }
        }
    )

@app.exception_handler(503)
async def service_unavailable_handler(request: Request, exc: Exception):
    """Handle 503 Service Unavailable errors (database connection issues)"""
    logger.error(f"Service unavailable: {exc}")
    return JSONResponse(
        status_code=503,
        content={
            "error": {
                "code": 503,
                "message": "Service Unavailable",
                "detail": "Database connection issues",
                "type": "service_unavailable_error"
            }
        }
    )

# =============================================================================
# APPLICATION STARTUP
# =============================================================================

if __name__ == "__main__":
    # Get configuration from environment variables
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", "8000"))
    debug = os.getenv("DEBUG", "true").lower() == "true"
    
    # Start the server with auto-reload enabled in development
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,  # Auto-reload enabled by default in development
        log_level="info",
        access_log=True
    )