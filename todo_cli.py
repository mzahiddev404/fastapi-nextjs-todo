#!/usr/bin/env python3
"""
=============================================================================
TODO CLI - Standalone Python CRUD Application
=============================================================================
A command-line interface for managing TODO tasks with MongoDB
Uses the project_db_url from .env to connect to MongoDB Atlas

This is a simplified entry point that delegates to the modular CLI package.
"""

import asyncio
import sys
from dotenv import load_dotenv

# Load environment variables from backend/.env
load_dotenv("backend/.env")

# Import the modular CLI interface
from cli.interface import main

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

