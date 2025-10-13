"""
Label management API tests for the TODO application.
Tests label CRUD operations and task associations.
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

class TestLabelManagement:
    """Test label management endpoints"""
    
    def test_create_label_success(self, mock_db, auth_headers):
        """Test successful label creation"""
        # Mock database response
        mock_db.labels.insert_one.return_value = AsyncMock(inserted_id="label123")
        
        response = client.post("/api/v1/labels", json={
            "name": "Work",
            "color": "#FF5733"
        }, headers=auth_headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Work"
        assert data["color"] == "#FF5733"
    
    def test_create_label_unauthorized(self, mock_db):
        """Test label creation without authentication"""
        response = client.post("/api/v1/labels", json={
            "name": "Work",
            "color": "#FF5733"
        })
        
        assert response.status_code == 401
    
    def test_create_label_duplicate_name(self, mock_db, auth_headers):
        """Test creating label with duplicate name"""
        # Mock database response - label name already exists
        mock_db.labels.find_one.return_value = {"name": "Work", "user_id": "test_user_id"}
        
        response = client.post("/api/v1/labels", json={
            "name": "Work",
            "color": "#FF5733"
        }, headers=auth_headers)
        
        assert response.status_code == 400
        assert "Label name already exists" in response.json()["detail"]
    
    def test_get_labels_success(self, mock_db, auth_headers):
        """Test getting user labels"""
        # Mock database response
        mock_labels = [
            {
                "id": "label1",
                "name": "Work",
                "color": "#FF5733",
                "user_id": "test_user_id",
                "created_at": datetime.utcnow(),
                "task_count": 3
            },
            {
                "id": "label2",
                "name": "Personal",
                "color": "#33FF57",
                "user_id": "test_user_id",
                "created_at": datetime.utcnow(),
                "task_count": 1
            }
        ]
        mock_db.labels.aggregate.return_value.to_list.return_value = mock_labels
        
        response = client.get("/api/v1/labels", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "Work"
        assert data[1]["name"] == "Personal"
        assert data[0]["task_count"] == 3
    
    def test_get_label_by_id_success(self, mock_db, auth_headers):
        """Test getting a specific label by ID"""
        # Mock database response
        mock_label = {
            "id": "label123",
            "name": "Work",
            "color": "#FF5733",
            "user_id": "test_user_id",
            "created_at": datetime.utcnow()
        }
        mock_db.labels.find_one.return_value = mock_label
        
        response = client.get("/api/v1/labels/label123", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "label123"
        assert data["name"] == "Work"
    
    def test_get_label_by_id_not_found(self, mock_db, auth_headers):
        """Test getting a non-existent label"""
        # Mock database response - label not found
        mock_db.labels.find_one.return_value = None
        
        response = client.get("/api/v1/labels/nonexistent", headers=auth_headers)
        
        assert response.status_code == 404
        assert "Label not found" in response.json()["detail"]
    
    def test_get_label_by_id_unauthorized(self, mock_db, auth_headers):
        """Test getting a label belonging to another user"""
        # Mock database response - label belongs to different user
        mock_label = {
            "id": "label123",
            "name": "Other User's Label",
            "user_id": "other_user_id"
        }
        mock_db.labels.find_one.return_value = mock_label
        
        response = client.get("/api/v1/labels/label123", headers=auth_headers)
        
        assert response.status_code == 403
        assert "Not authorized to access this label" in response.json()["detail"]
    
    def test_update_label_success(self, mock_db, auth_headers):
        """Test successful label update"""
        # Mock database responses
        mock_label = {
            "id": "label123",
            "name": "Original Name",
            "color": "#FF5733",
            "user_id": "test_user_id",
            "created_at": datetime.utcnow()
        }
        mock_db.labels.find_one.return_value = mock_label
        mock_db.labels.update_one.return_value = AsyncMock(modified_count=1)
        
        response = client.put("/api/v1/labels/label123", json={
            "name": "Updated Name",
            "color": "#33FF57"
        }, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["color"] == "#33FF57"
    
    def test_update_label_not_found(self, mock_db, auth_headers):
        """Test updating a non-existent label"""
        # Mock database response - label not found
        mock_db.labels.find_one.return_value = None
        
        response = client.put("/api/v1/labels/nonexistent", json={
            "name": "Updated Name"
        }, headers=auth_headers)
        
        assert response.status_code == 404
        assert "Label not found" in response.json()["detail"]
    
    def test_delete_label_success(self, mock_db, auth_headers):
        """Test successful label deletion"""
        # Mock database responses
        mock_label = {
            "id": "label123",
            "name": "Test Label",
            "user_id": "test_user_id"
        }
        mock_db.labels.find_one.return_value = mock_label
        mock_db.labels.delete_one.return_value = AsyncMock(deleted_count=1)
        
        response = client.delete("/api/v1/labels/label123", headers=auth_headers)
        
        assert response.status_code == 200
        assert "Label deleted successfully" in response.json()["message"]
    
    def test_delete_label_not_found(self, mock_db, auth_headers):
        """Test deleting a non-existent label"""
        # Mock database response - label not found
        mock_db.labels.find_one.return_value = None
        
        response = client.delete("/api/v1/labels/nonexistent", headers=auth_headers)
        
        assert response.status_code == 404
        assert "Label not found" in response.json()["detail"]
    
    def test_delete_label_with_tasks(self, mock_db, auth_headers):
        """Test deleting a label that has associated tasks"""
        # Mock database responses
        mock_label = {
            "id": "label123",
            "name": "Work",
            "user_id": "test_user_id"
        }
        mock_db.labels.find_one.return_value = mock_label
        mock_db.tasks.count_documents.return_value = 2  # Has 2 associated tasks
        
        response = client.delete("/api/v1/labels/label123", headers=auth_headers)
        
        assert response.status_code == 400
        assert "Cannot delete label with associated tasks" in response.json()["detail"]