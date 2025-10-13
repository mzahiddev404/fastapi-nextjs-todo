"""
Pytest configuration and fixtures for backend tests
Provides test setup, database mocking, and common utilities
"""

import pytest
import asyncio
from typing import AsyncGenerator, Generator
from httpx import AsyncClient
from unittest.mock import AsyncMock, MagicMock

# Configure pytest-asyncio
pytest_plugins = ('pytest_asyncio',)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_app():
    """Get FastAPI application for testing"""
    from main import app
    return app


@pytest.fixture
async def client(test_app) -> AsyncGenerator:
    """Create an HTTP client for testing"""
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def mock_database():
    """Mock database connection"""
    mock_db = AsyncMock()
    
    # Mock collections
    mock_db.users = AsyncMock()
    mock_db.tasks = AsyncMock()
    mock_db.labels = AsyncMock()
    
    return mock_db


@pytest.fixture
def test_user_data():
    """Sample test user data"""
    return {
        "_id": "507f1f77bcf86cd799439011",
        "email": "test@example.com",
        "name": "Test User",
        "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYfZdkYB3Pu",  # "testpassword123"
        "is_active": True
    }


@pytest.fixture
def test_token(test_user_data):
    """Create a test JWT token"""
    from core.security import create_access_token
    token = create_access_token(data={"sub": test_user_data["email"]})
    return token


@pytest.fixture
def auth_headers(test_token):
    """Get authorization headers with test token"""
    return {"Authorization": f"Bearer {test_token}"}


@pytest.fixture
def test_task_data():
    """Sample test task data"""
    from datetime import datetime, timedelta
    return {
        "title": "Test Task",
        "description": "Test Description",
        "priority": "medium",
        "deadline": (datetime.utcnow() + timedelta(days=7)).isoformat(),
        "labels": []
    }


@pytest.fixture
def test_label_data():
    """Sample test label data"""
    return {
        "name": "Test Label",
        "color": "#FF5733"
    }


@pytest.fixture(autouse=True)
async def cleanup_test_data():
    """Cleanup test data after each test"""
    yield
    # Cleanup logic can be added here if needed
    # For now, we're using mocked databases, so no cleanup is required


@pytest.fixture
def mock_get_database(mock_database):
    """Mock the get_database dependency"""
    async def _mock_get_database():
        return mock_database
    return _mock_get_database

