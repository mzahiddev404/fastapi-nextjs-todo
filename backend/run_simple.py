#!/usr/bin/env python3
"""
Simple run script that matches the basic example's approach
Runs with auto-reload enabled by default
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
    
    print(f"🚀 Starting TODO API on {host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    print(f"🔍 Health Check: http://{host}:{port}/health")
    print(f"🔄 Auto-reload: {'Enabled' if debug else 'Disabled'}")
    
    # Start the server with auto-reload enabled by default
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,  # Auto-reload enabled by default
        log_level="info",
        access_log=True
    )
