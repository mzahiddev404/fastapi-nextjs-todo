"""
Authentication API tests for the TODO application.
Tests user registration, login, and authentication functionality.
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
import json
from datetime import datetime, timedelta

# Import the FastAPI app
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from core.security import create_access_token

client = TestClient(app)

# Mock MongoDB connection for testing
@pytest.fixture
def mock_db():
    """Mock database connection for testing"""
    with patch('core.db.get_database') as mock_get_db:
        mock_db = AsyncMock()
        mock_get_db.return_value = mock_db
        yield mock_db

# Mock JWT token for authenticated requests
@pytest.fixture
def auth_headers():
    """Create valid JWT token for testing"""
    token = create_access_token(data={"sub": "test_user_id"})
    return {"Authorization": f"Bearer {token}"}

class TestAuthentication:
    """Test user authentication endpoints"""
    
    def test_signup_success(self, mock_db):
        """Test successful user registration"""
        # Mock database responses
        mock_db.users.find_one.return_value = None  # Email not taken
        mock_db.users.insert_one.return_value = AsyncMock(inserted_id="user123")
        
        # Test signup request
        response = client.post("/api/v1/auth/signup", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123"
        })
        
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_signup_email_taken(self, mock_db):
        """Test signup with existing email"""
        # Mock database response - email already exists
        mock_db.users.find_one.return_value = {"email": "test@example.com"}
        
        response = client.post("/api/v1/auth/signup", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123"
        })
        
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]
    
    def test_signup_username_taken(self, mock_db):
        """Test signup with existing username"""
        # Mock database responses
        mock_db.users.find_one.side_effect = [None, {"username": "testuser"}]  # Email OK, username taken
        
        response = client.post("/api/v1/auth/signup", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123"
        })
        
        assert response.status_code == 400
        assert "Username already taken" in response.json()["detail"]
    
    def test_login_success(self, mock_db):
        """Test successful user login"""
        # Mock database response
        mock_user = {
            "id": "user123",
            "username": "testuser",
            "email": "test@example.com",
            "hashed_password": "$2b$12$test_hash",
            "is_active": True
        }
        mock_db.users.find_one.return_value = mock_user
        
        # Mock password verification
        with patch('core.security.verify_password', return_value=True):
            response = client.post("/api/v1/auth/login", json={
                "email": "test@example.com",
                "password": "testpassword123"
            })
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self, mock_db):
        """Test login with invalid credentials"""
        # Mock database response - user not found
        mock_db.users.find_one.return_value = None
        
        response = client.post("/api/v1/auth/login", json={
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        })
        
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]
    
    def test_login_wrong_password(self, mock_db):
        """Test login with wrong password"""
        # Mock database response
        mock_user = {
            "id": "user123",
            "username": "testuser",
            "email": "test@example.com",
            "hashed_password": "$2b$12$test_hash",
            "is_active": True
        }
        mock_db.users.find_one.return_value = mock_user
        
        # Mock password verification failure
        with patch('core.security.verify_password', return_value=False):
            response = client.post("/api/v1/auth/login", json={
                "email": "test@example.com",
                "password": "wrongpassword"
            })
        
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]
    
    def test_get_current_user_success(self, mock_db, auth_headers):
        """Test getting current user information"""
        # Mock database response
        mock_user = {
            "id": "test_user_id",
            "username": "testuser",
            "email": "test@example.com",
            "is_active": True,
            "created_at": datetime.utcnow()
        }
        mock_db.users.find_one.return_value = mock_user
        
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert "hashed_password" not in data  # Sensitive data excluded
    
    def test_get_current_user_invalid_token(self, mock_db):
        """Test getting current user with invalid token"""
        response = client.get("/api/v1/auth/me", headers={"Authorization": "Bearer invalid_token"})
        
        assert response.status_code == 401
        assert "Invalid authentication credentials" in response.json()["detail"]
    
    def test_refresh_token_success(self, mock_db, auth_headers):
        """Test token refresh"""
        # Mock database response
        mock_user = {
            "id": "test_user_id",
            "username": "testuser",
            "email": "test@example.com",
            "is_active": True
        }
        mock_db.users.find_one.return_value = mock_user
        
        response = client.post("/api/v1/auth/refresh", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"