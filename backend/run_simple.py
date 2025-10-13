#!/usr/bin/env python3
"""
FastAPI Backend Server Runner
Starts the TODO API with uvicorn
"""

import os
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Get configuration from environment variables with defaults
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", "8000"))
    debug = os.getenv("DEBUG", "true").lower() == "true"
    
    print("=" * 60)
    print(f"🚀 Starting TODO API Backend Server")
    print(f"📍 Server: http://{host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    print(f"🔍 Health Check: http://{host}:{port}/health")
    print(f"🔄 Auto-reload: {'Enabled' if debug else 'Disabled'}")
    print("=" * 60)
    
    # Start the server with auto-reload enabled in development
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,  # Auto-reload based on DEBUG env var
        log_level="info",
        access_log=True
    )
