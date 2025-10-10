"""
Core API tests for the TODO application.
Tests authentication, task management, and label functionality.
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
            "password": "testpass123"
        })
        
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert "password" not in data  # Password should not be returned
    
    def test_signup_email_taken(self, mock_db):
        """Test signup with existing email"""
        # Mock database response - email already exists
        mock_db.users.find_one.return_value = {"email": "test@example.com"}
        
        response = client.post("/api/v1/auth/signup", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        })
        
        assert response.status_code == 400
        assert "email already registered" in response.json()["detail"].lower()
    
    def test_login_success(self, mock_db):
        """Test successful user login"""
        # Mock user data with hashed password
        mock_user = {
            "id": "user123",
            "username": "testuser",
            "email": "test@example.com",
            "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/4QZ8K2"  # bcrypt hash for "testpass123"
        }
        mock_db.users.find_one.return_value = mock_user
        
        response = client.post("/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "testpass123"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self, mock_db):
        """Test login with invalid credentials"""
        # Mock user not found
        mock_db.users.find_one.return_value = None
        
        response = client.post("/api/v1/auth/login", json={
            "email": "nonexistent@example.com",
            "password": "wrongpass"
        })
        
        assert response.status_code == 401
        assert "invalid credentials" in response.json()["detail"].lower()

class TestTaskManagement:
    """Test task CRUD operations"""
    
    def test_create_task_success(self, mock_db, auth_headers):
        """Test successful task creation"""
        # Mock user authentication
        mock_user = {"id": "test_user_id", "username": "testuser", "email": "test@example.com"}
        mock_db.users.find_one.return_value = mock_user
        
        # Mock task creation
        mock_db.tasks.insert_one.return_value = AsyncMock(inserted_id="task123")
        
        response = client.post("/api/v1/tasks", json={
            "title": "Test Task",
            "description": "This is a test task",
            "priority": "medium",
            "due_date": "2024-12-31"
        }, headers=auth_headers)
        
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["title"] == "Test Task"
        assert data["description"] == "This is a test task"
        assert data["priority"] == "medium"
    
    def test_get_tasks_success(self, mock_db, auth_headers):
        """Test retrieving user tasks"""
        # Mock user authentication
        mock_user = {"id": "test_user_id", "username": "testuser", "email": "test@example.com"}
        mock_db.users.find_one.return_value = mock_user
        
        # Mock tasks data
        mock_tasks = [
            {
                "id": "task1",
                "title": "Task 1",
                "description": "First task",
                "status": "pending",
                "priority": "high",
                "user_id": "test_user_id"
            },
            {
                "id": "task2", 
                "title": "Task 2",
                "description": "Second task",
                "status": "completed",
                "priority": "medium",
                "user_id": "test_user_id"
            }
        ]
        mock_db.tasks.find.return_value = mock_tasks
        
        response = client.get("/api/v1/tasks", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["title"] == "Task 1"
        assert data[1]["title"] == "Task 2"
    
    def test_update_task_success(self, mock_db, auth_headers):
        """Test successful task update"""
        # Mock user authentication
        mock_user = {"id": "test_user_id", "username": "testuser", "email": "test@example.com"}
        mock_db.users.find_one.return_value = mock_user
        
        # Mock existing task
        existing_task = {
            "id": "task123",
            "title": "Original Task",
            "description": "Original description",
            "status": "pending",
            "priority": "low",
            "user_id": "test_user_id"
        }
        mock_db.tasks.find_one.return_value = existing_task
        mock_db.tasks.update_one.return_value = AsyncMock(modified_count=1)
        
        response = client.put("/api/v1/tasks/task123", json={
            "title": "Updated Task",
            "description": "Updated description",
            "priority": "high"
        }, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Task"
        assert data["description"] == "Updated description"
        assert data["priority"] == "high"
    
    def test_delete_task_success(self, mock_db, auth_headers):
        """Test successful task deletion"""
        # Mock user authentication
        mock_user = {"id": "test_user_id", "username": "testuser", "email": "test@example.com"}
        mock_db.users.find_one.return_value = mock_user
        
        # Mock existing task
        existing_task = {
            "id": "task123",
            "title": "Task to Delete",
            "user_id": "test_user_id"
        }
        mock_db.tasks.find_one.return_value = existing_task
        mock_db.tasks.delete_one.return_value = AsyncMock(deleted_count=1)
        
        response = client.delete("/api/v1/tasks/task123", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Task deleted successfully"

class TestLabelManagement:
    """Test label CRUD operations"""
    
    def test_create_label_success(self, mock_db, auth_headers):
        """Test successful label creation"""
        # Mock user authentication
        mock_user = {"id": "test_user_id", "username": "testuser", "email": "test@example.com"}
        mock_db.users.find_one.return_value = mock_user
        
        # Mock label creation
        mock_db.labels.insert_one.return_value = AsyncMock(inserted_id="label123")
        
        response = client.post("/api/v1/labels", json={
            "name": "Work",
            "color": "#FF5733"
        }, headers=auth_headers)
        
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["name"] == "Work"
        assert data["color"] == "#FF5733"
    
    def test_get_labels_success(self, mock_db, auth_headers):
        """Test retrieving user labels"""
        # Mock user authentication
        mock_user = {"id": "test_user_id", "username": "testuser", "email": "test@example.com"}
        mock_db.users.find_one.return_value = mock_user
        
        # Mock labels data
        mock_labels = [
            {
                "id": "label1",
                "name": "Work",
                "color": "#FF5733",
                "user_id": "test_user_id"
            },
            {
                "id": "label2",
                "name": "Personal", 
                "color": "#33FF57",
                "user_id": "test_user_id"
            }
        ]
        mock_db.labels.find.return_value = mock_labels
        
        response = client.get("/api/v1/labels", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "Work"
        assert data[1]["name"] == "Personal"
    
    def test_update_label_success(self, mock_db, auth_headers):
        """Test successful label update"""
        # Mock user authentication
        mock_user = {"id": "test_user_id", "username": "testuser", "email": "test@example.com"}
        mock_db.users.find_one.return_value = mock_user
        
        # Mock existing label
        existing_label = {
            "id": "label123",
            "name": "Original Label",
            "color": "#FF0000",
            "user_id": "test_user_id"
        }
        mock_db.labels.find_one.return_value = existing_label
        mock_db.labels.update_one.return_value = AsyncMock(modified_count=1)
        
        response = client.put("/api/v1/labels/label123", json={
            "name": "Updated Label",
            "color": "#00FF00"
        }, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Label"
        assert data["color"] == "#00FF00"
    
    def test_delete_label_success(self, mock_db, auth_headers):
        """Test successful label deletion"""
        # Mock user authentication
        mock_user = {"id": "test_user_id", "username": "testuser", "email": "test@example.com"}
        mock_db.users.find_one.return_value = mock_user
        
        # Mock existing label
        existing_label = {
            "id": "label123",
            "name": "Label to Delete",
            "user_id": "test_user_id"
        }
        mock_db.labels.find_one.return_value = existing_label
        mock_db.labels.delete_one.return_value = AsyncMock(deleted_count=1)
        
        response = client.delete("/api/v1/labels/label123", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Label deleted successfully"

class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_unauthorized_access(self):
        """Test that protected endpoints require authentication"""
        response = client.get("/api/v1/tasks")
        assert response.status_code == 401
        assert "not authenticated" in response.json()["detail"].lower()
    
    def test_invalid_token(self):
        """Test that invalid tokens are rejected"""
        response = client.get("/api/v1/tasks", headers={"Authorization": "Bearer invalid_token"})
        assert response.status_code == 401
    
    def test_task_not_found(self, mock_db, auth_headers):
        """Test that non-existent tasks return 404"""
        # Mock user authentication
        mock_user = {"id": "test_user_id", "username": "testuser", "email": "test@example.com"}
        mock_db.users.find_one.return_value = mock_user
        
        # Mock task not found
        mock_db.tasks.find_one.return_value = None
        
        response = client.get("/api/v1/tasks/nonexistent", headers=auth_headers)
        assert response.status_code == 404
    
    def test_label_not_found(self, mock_db, auth_headers):
        """Test that non-existent labels return 404"""
        # Mock user authentication
        mock_user = {"id": "test_user_id", "username": "testuser", "email": "test@example.com"}
        mock_db.users.find_one.return_value = mock_user
        
        # Mock label not found
        mock_db.labels.find_one.return_value = None
        
        response = client.get("/api/v1/labels/nonexistent", headers=auth_headers)
        assert response.status_code == 404

class TestAPIHealth:
    """Test basic API health and endpoints"""
    
    def test_root_endpoint(self):
        """Test the root endpoint returns success message"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "TODO API" in data["message"]
    
    def test_health_endpoint(self):
        """Test the health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "endpoints" in data
    
    def test_docs_endpoint(self):
        """Test that API documentation is accessible"""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
