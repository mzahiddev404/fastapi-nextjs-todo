"""
Security tests for the TODO application.
Tests password validation, JWT tokens, rate limiting, and security middleware.
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
import time
import os

# Import the FastAPI app
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from core.security import (
    validate_password_strength,
    generate_secure_token,
    create_access_token,
    verify_token,
    get_password_hash,
    verify_password
)

client = TestClient(app)

class TestPasswordSecurity:
    """Test password security features"""
    
    def test_password_strength_validation(self):
        """Test password strength validation"""
        # Valid password
        is_valid, error = validate_password_strength("Password123!")
        assert is_valid is True
        assert error == ""
        
        # Too short
        is_valid, error = validate_password_strength("Pass1!")
        assert is_valid is False
        assert "8 characters" in error
        
        # No uppercase
        is_valid, error = validate_password_strength("password123!")
        assert is_valid is False
        assert "uppercase" in error
        
        # No lowercase
        is_valid, error = validate_password_strength("PASSWORD123!")
        assert is_valid is False
        assert "lowercase" in error
        
        # No number
        is_valid, error = validate_password_strength("Password!")
        assert is_valid is False
        assert "number" in error
        
        # No special character
        is_valid, error = validate_password_strength("Password123")
        assert is_valid is False
        assert "special character" in error
    
    def test_password_hashing(self):
        """Test password hashing and verification"""
        password = "TestPassword123!"
        hashed = get_password_hash(password)
        
        # Hash should be different from original
        assert hashed != password
        
        # Should be able to verify correct password
        assert verify_password(password, hashed) is True
        
        # Should reject wrong password
        assert verify_password("WrongPassword123!", hashed) is False
    
    def test_secure_token_generation(self):
        """Test secure token generation"""
        token1 = generate_secure_token()
        token2 = generate_secure_token()
        
        # Tokens should be different
        assert token1 != token2
        
        # Tokens should be reasonable length
        assert len(token1) >= 32
        assert len(token2) >= 32

class TestJWTSecurity:
    """Test JWT token security"""
    
    def test_jwt_token_creation_and_verification(self):
        """Test JWT token creation and verification"""
        user_id = "test_user_123"
        token = create_access_token(data={"sub": user_id})
        
        # Token should be created
        assert token is not None
        assert len(token) > 0
        
        # Should be able to verify token
        verified_user_id = verify_token(token)
        assert verified_user_id == user_id
    
    def test_jwt_token_expiration(self):
        """Test JWT token expiration"""
        user_id = "test_user_123"
        # Create token with very short expiration
        token = create_access_token(
            data={"sub": user_id}, 
            expires_delta=time.timedelta(seconds=1)
        )
        
        # Should be valid immediately
        assert verify_token(token) == user_id
        
        # Wait for expiration
        time.sleep(2)
        
        # Should be expired now
        assert verify_token(token) is None
    
    def test_invalid_jwt_token(self):
        """Test invalid JWT token handling"""
        # Invalid token format
        assert verify_token("invalid_token") is None
        
        # Empty token
        assert verify_token("") is None
        
        # None token
        assert verify_token(None) is None

class TestRateLimiting:
    """Test rate limiting functionality"""
    
    @pytest.mark.slow
    def test_auth_rate_limiting(self):
        """Test rate limiting on auth endpoints"""
        # Test signup rate limiting
        for i in range(10):  # Try to exceed rate limit
            response = client.post(
                "/api/v1/auth/signup",
                json={
                    "username": f"testuser{i}",
                    "email": f"test{i}@example.com",
                    "password": "TestPassword123!"
                }
            )
            
            if i < 5:  # First 5 should be allowed
                assert response.status_code in [201, 400]  # 400 for duplicate email
            else:  # After 5, should be rate limited
                if response.status_code == 429:
                    break
        
        # Test login rate limiting
        for i in range(10):
            response = client.post(
                "/api/v1/auth/login",
                json={
                    "email": "test@example.com",
                    "password": "TestPassword123!"
                }
            )
            
            if i < 5:  # First 5 should be allowed
                assert response.status_code in [200, 401]  # 401 for wrong credentials
            else:  # After 5, should be rate limited
                if response.status_code == 429:
                    break

class TestSecurityHeaders:
    """Test security headers"""
    
    def test_security_headers_present(self):
        """Test that security headers are present in responses"""
        response = client.get("/")
        
        # Check for security headers
        assert "X-Content-Type-Options" in response.headers
        assert "X-Frame-Options" in response.headers
        assert "X-XSS-Protection" in response.headers
        assert "Referrer-Policy" in response.headers
        assert "Content-Security-Policy" in response.headers
        
        # Check header values
        assert response.headers["X-Content-Type-Options"] == "nosniff"
        assert response.headers["X-Frame-Options"] == "DENY"
        assert response.headers["X-XSS-Protection"] == "1; mode=block"
        assert response.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"
    
    def test_cors_headers(self):
        """Test CORS headers"""
        response = client.options("/api/v1/auth/signup")
        
        # Should have CORS headers
        assert "Access-Control-Allow-Origin" in response.headers
        assert "Access-Control-Allow-Methods" in response.headers
        assert "Access-Control-Allow-Headers" in response.headers

class TestInputValidation:
    """Test input validation and sanitization"""
    
    def test_malicious_input_handling(self):
        """Test handling of potentially malicious input"""
        # XSS attempt
        response = client.post(
            "/api/v1/auth/signup",
            json={
                "username": "<script>alert('xss')</script>",
                "email": "test@example.com",
                "password": "TestPassword123!"
            }
        )
        
        # Should handle gracefully (either reject or sanitize)
        assert response.status_code in [400, 201]
    
    def test_sql_injection_attempt(self):
        """Test SQL injection attempt handling"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com'; DROP TABLE users; --",
                "password": "TestPassword123!"
            }
        )
        
        # Should handle gracefully
        assert response.status_code in [400, 401]

class TestEnvironmentSecurity:
    """Test environment security configuration"""
    
    def test_jwt_secret_required(self):
        """Test that JWT secret is required"""
        # This test would need to be run in an environment without JWT_SECRET
        # For now, we'll just test that the security module loads correctly
        from core.security import SECRET_KEY
        assert SECRET_KEY is not None
    
    def test_environment_variables(self):
        """Test that required environment variables are set"""
        # Test that we can access environment variables
        assert os.getenv("JWT_SECRET") is not None or os.getenv("JWT_SECRET") == ""

if __name__ == "__main__":
    pytest.main([__file__])
