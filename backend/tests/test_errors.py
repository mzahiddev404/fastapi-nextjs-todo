"""
Error handling tests for the TODO application.
Tests various error scenarios and edge cases.
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

class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_invalid_json_request(self, mock_db, auth_headers):
        """Test handling of invalid JSON in request body"""
        response = client.post(
            "/api/v1/tasks",
            data="invalid json",
            headers={**auth_headers, "Content-Type": "application/json"}
        )
        
        assert response.status_code == 422
    
    def test_missing_required_fields(self, mock_db, auth_headers):
        """Test handling of missing required fields"""
        response = client.post("/api/v1/tasks", json={
            "description": "Missing title"
        }, headers=auth_headers)
        
        assert response.status_code == 422
        assert "title" in str(response.json())
    
    def test_invalid_field_types(self, mock_db, auth_headers):
        """Test handling of invalid field types"""
        response = client.post("/api/v1/tasks", json={
            "title": 123,  # Should be string
            "description": "Valid description"
        }, headers=auth_headers)
        
        assert response.status_code == 422
    
    def test_invalid_email_format(self, mock_db):
        """Test handling of invalid email format"""
        response = client.post("/api/v1/auth/signup", json={
            "username": "testuser",
            "email": "invalid-email",
            "password": "testpassword123"
        })
        
        assert response.status_code == 422
        assert "email" in str(response.json())
    
    def test_short_password(self, mock_db):
        """Test handling of short password"""
        response = client.post("/api/v1/auth/signup", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "123"  # Too short
        })
        
        assert response.status_code == 422
    
    def test_invalid_task_status(self, mock_db, auth_headers):
        """Test handling of invalid task status"""
        # Mock database response
        mock_task = {
            "id": "task123",
            "title": "Test Task",
            "user_id": "test_user_id"
        }
        mock_db.tasks.find_one.return_value = mock_task
        
        response = client.put("/api/v1/tasks/task123", json={
            "status": "invalid_status"
        }, headers=auth_headers)
        
        assert response.status_code == 422
    
    def test_invalid_date_format(self, mock_db, auth_headers):
        """Test handling of invalid date format"""
        response = client.post("/api/v1/tasks", json={
            "title": "Test Task",
            "due_date": "invalid-date"
        }, headers=auth_headers)
        
        assert response.status_code == 422
    
    def test_database_connection_error(self, mock_db, auth_headers):
        """Test handling of database connection errors"""
        # Mock database error
        mock_db.tasks.find.side_effect = Exception("Database connection failed")
        
        response = client.get("/api/v1/tasks", headers=auth_headers)
        
        assert response.status_code == 500
    
    def test_unauthorized_access(self, mock_db):
        """Test handling of unauthorized access"""
        response = client.get("/api/v1/tasks")
        
        assert response.status_code == 401
    
    def test_invalid_token_format(self, mock_db):
        """Test handling of invalid token format"""
        response = client.get("/api/v1/tasks", headers={
            "Authorization": "Invalid token format"
        })
        
        assert response.status_code == 401
    
    def test_expired_token(self, mock_db):
        """Test handling of expired token"""
        # Create an expired token
        expired_token = create_access_token(
            data={"sub": "test_user_id"},
            expires_delta=timedelta(seconds=-1)  # Expired
        )
        
        response = client.get("/api/v1/tasks", headers={
            "Authorization": f"Bearer {expired_token}"
        })
        
        assert response.status_code == 401
    
    def test_nonexistent_endpoint(self, mock_db):
        """Test handling of non-existent endpoints"""
        response = client.get("/api/v1/nonexistent")
        
        assert response.status_code == 404
    
    def test_method_not_allowed(self, mock_db, auth_headers):
        """Test handling of unsupported HTTP methods"""
        response = client.patch("/api/v1/tasks", json={
            "title": "Test Task"
        }, headers=auth_headers)
        
        assert response.status_code == 405
    
    def test_large_request_body(self, mock_db, auth_headers):
        """Test handling of large request body"""
        large_description = "x" * 10000  # Very large description
        
        response = client.post("/api/v1/tasks", json={
            "title": "Test Task",
            "description": large_description
        }, headers=auth_headers)
        
        # Should either succeed or return 413 (Payload Too Large)
        assert response.status_code in [200, 201, 413]
    
    def test_special_characters_in_input(self, mock_db, auth_headers):
        """Test handling of special characters in input"""
        response = client.post("/api/v1/tasks", json={
            "title": "Test Task with special chars: !@#$%^&*()",
            "description": "Description with émojis 🚀 and unicode"
        }, headers=auth_headers)
        
        assert response.status_code in [200, 201, 422]
    
    def test_empty_request_body(self, mock_db, auth_headers):
        """Test handling of empty request body"""
        response = client.post("/api/v1/tasks", json={}, headers=auth_headers)
        
        assert response.status_code == 422
    
    def test_malformed_json(self, mock_db, auth_headers):
        """Test handling of malformed JSON"""
        response = client.post(
            "/api/v1/tasks",
            data='{"title": "Test", "description": }',  # Missing value
            headers={**auth_headers, "Content-Type": "application/json"}
        )
        
        assert response.status_code == 422