"""
Task management API tests for the TODO application.
Tests task CRUD operations and status management.
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

class TestTaskManagement:
    """Test task management endpoints"""
    
    def test_create_task_success(self, mock_db, auth_headers):
        """Test successful task creation"""
        # Mock database response
        mock_db.tasks.insert_one.return_value = AsyncMock(inserted_id="task123")
        
        response = client.post("/api/v1/tasks", json={
            "title": "Test Task",
            "description": "Test task description",
            "due_date": "2024-12-31T23:59:59"
        }, headers=auth_headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["description"] == "Test task description"
        assert data["status"] == "pending"
    
    def test_create_task_unauthorized(self, mock_db):
        """Test task creation without authentication"""
        response = client.post("/api/v1/tasks", json={
            "title": "Test Task",
            "description": "Test task description"
        })
        
        assert response.status_code == 401
    
    def test_get_tasks_success(self, mock_db, auth_headers):
        """Test getting user tasks"""
        # Mock database response
        mock_tasks = [
            {
                "id": "task1",
                "title": "Task 1",
                "description": "Description 1",
                "status": "pending",
                "user_id": "test_user_id",
                "label_ids": [],
                "due_date": None,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "id": "task2",
                "title": "Task 2",
                "description": "Description 2",
                "status": "completed",
                "user_id": "test_user_id",
                "label_ids": [],
                "due_date": None,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        ]
        mock_db.tasks.find.return_value.to_list.return_value = mock_tasks
        
        response = client.get("/api/v1/tasks", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["title"] == "Task 1"
        assert data[1]["title"] == "Task 2"
    
    def test_get_tasks_with_status_filter(self, mock_db, auth_headers):
        """Test getting tasks filtered by status"""
        # Mock database response
        mock_tasks = [
            {
                "id": "task1",
                "title": "Pending Task",
                "description": "Description",
                "status": "pending",
                "user_id": "test_user_id",
                "label_ids": [],
                "due_date": None,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        ]
        mock_db.tasks.find.return_value.to_list.return_value = mock_tasks
        
        response = client.get("/api/v1/tasks?status=pending", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["status"] == "pending"
    
    def test_get_task_by_id_success(self, mock_db, auth_headers):
        """Test getting a specific task by ID"""
        # Mock database response
        mock_task = {
            "id": "task123",
            "title": "Test Task",
            "description": "Test description",
            "status": "pending",
            "user_id": "test_user_id",
            "label_ids": [],
            "due_date": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        mock_db.tasks.find_one.return_value = mock_task
        
        response = client.get("/api/v1/tasks/task123", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "task123"
        assert data["title"] == "Test Task"
    
    def test_get_task_by_id_not_found(self, mock_db, auth_headers):
        """Test getting a non-existent task"""
        # Mock database response - task not found
        mock_db.tasks.find_one.return_value = None
        
        response = client.get("/api/v1/tasks/nonexistent", headers=auth_headers)
        
        assert response.status_code == 404
        assert "Task not found" in response.json()["detail"]
    
    def test_get_task_by_id_unauthorized(self, mock_db, auth_headers):
        """Test getting a task belonging to another user"""
        # Mock database response - task belongs to different user
        mock_task = {
            "id": "task123",
            "title": "Other User's Task",
            "user_id": "other_user_id"
        }
        mock_db.tasks.find_one.return_value = mock_task
        
        response = client.get("/api/v1/tasks/task123", headers=auth_headers)
        
        assert response.status_code == 403
        assert "Not authorized to access this task" in response.json()["detail"]
    
    def test_update_task_success(self, mock_db, auth_headers):
        """Test successful task update"""
        # Mock database responses
        mock_task = {
            "id": "task123",
            "title": "Original Title",
            "description": "Original description",
            "status": "pending",
            "user_id": "test_user_id",
            "label_ids": [],
            "due_date": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        mock_db.tasks.find_one.return_value = mock_task
        mock_db.tasks.update_one.return_value = AsyncMock(modified_count=1)
        
        response = client.put("/api/v1/tasks/task123", json={
            "title": "Updated Title",
            "description": "Updated description",
            "status": "in_progress"
        }, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["description"] == "Updated description"
        assert data["status"] == "in_progress"
    
    def test_update_task_not_found(self, mock_db, auth_headers):
        """Test updating a non-existent task"""
        # Mock database response - task not found
        mock_db.tasks.find_one.return_value = None
        
        response = client.put("/api/v1/tasks/nonexistent", json={
            "title": "Updated Title"
        }, headers=auth_headers)
        
        assert response.status_code == 404
        assert "Task not found" in response.json()["detail"]
    
    def test_delete_task_success(self, mock_db, auth_headers):
        """Test successful task deletion"""
        # Mock database responses
        mock_task = {
            "id": "task123",
            "title": "Test Task",
            "user_id": "test_user_id"
        }
        mock_db.tasks.find_one.return_value = mock_task
        mock_db.tasks.delete_one.return_value = AsyncMock(deleted_count=1)
        
        response = client.delete("/api/v1/tasks/task123", headers=auth_headers)
        
        assert response.status_code == 200
        assert "Task deleted successfully" in response.json()["message"]
    
    def test_delete_task_not_found(self, mock_db, auth_headers):
        """Test deleting a non-existent task"""
        # Mock database response - task not found
        mock_db.tasks.find_one.return_value = None
        
        response = client.delete("/api/v1/tasks/nonexistent", headers=auth_headers)
        
        assert response.status_code == 404
        assert "Task not found" in response.json()["detail"]
    
    def test_get_task_stats_success(self, mock_db, auth_headers):
        """Test getting task statistics"""
        # Mock database response
        mock_tasks = [
            {"status": "pending"},
            {"status": "pending"},
            {"status": "in_progress"},
            {"status": "completed"},
            {"status": "completed"}
        ]
        mock_db.tasks.find.return_value.to_list.return_value = mock_tasks
        
        response = client.get("/api/v1/tasks/stats", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 5
        assert data["pending"] == 2
        assert data["in_progress"] == 1
        assert data["completed"] == 2