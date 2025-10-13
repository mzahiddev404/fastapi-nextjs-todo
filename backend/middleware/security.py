# =============================================================================
# SECURITY MIDDLEWARE
# =============================================================================
# Implements additional security headers and protections
# Includes CSRF protection, request size limits, and security headers

from fastapi import Request, HTTPException, status
from fastapi.responses import Response
import time
import hashlib
import secrets
from typing import Optional
import os

# Security configuration
MAX_REQUEST_SIZE = int(os.getenv("MAX_REQUEST_SIZE", "10485760"))  # 10MB default
CSRF_SECRET = os.getenv("CSRF_SECRET", secrets.token_urlsafe(32))

class SecurityMiddleware:
    """Security middleware for additional protection"""
    
    def __init__(self):
        self.csrf_tokens = {}  # In production, use Redis or database
    
    async def __call__(self, request: Request, call_next):
        """Process request through security middleware"""
        
        # Check request size
        if hasattr(request, "headers") and "content-length" in request.headers:
            content_length = int(request.headers.get("content-length", 0))
            if content_length > MAX_REQUEST_SIZE:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail="Request entity too large"
                )
        
        # Add security headers
        response = await call_next(request)
        
        # Add security headers to response
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        # Add HSTS header for HTTPS
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # Add CSP header
        csp_policy = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
        response.headers["Content-Security-Policy"] = csp_policy
        
        return response

def generate_csrf_token() -> str:
    """Generate a CSRF token"""
    token = secrets.token_urlsafe(32)
    timestamp = str(int(time.time()))
    data = f"{token}:{timestamp}:{CSRF_SECRET}"
    hash_value = hashlib.sha256(data.encode()).hexdigest()[:16]
    return f"{token}:{hash_value}"

def verify_csrf_token(token: str, max_age: int = 3600) -> bool:
    """Verify a CSRF token"""
    try:
        if not token or ":" not in token:
            return False
        
        token_part, hash_part = token.rsplit(":", 1)
        timestamp = int(token_part.split(":")[1]) if ":" in token_part else 0
        
        # Check if token is expired
        if time.time() - timestamp > max_age:
            return False
        
        # Verify hash
        data = f"{token_part}:{CSRF_SECRET}"
        expected_hash = hashlib.sha256(data.encode()).hexdigest()[:16]
        return hash_part == expected_hash
        
    except Exception:
        return False

def validate_request_origin(request: Request) -> bool:
    """Validate request origin for CSRF protection"""
    origin = request.headers.get("origin")
    referer = request.headers.get("referer")
    host = request.headers.get("host")
    
    if not origin and not referer:
        return False
    
    # Check origin header
    if origin:
        if not origin.startswith(("http://localhost", "https://")):
            return False
    
    # Check referer header
    if referer:
        if not referer.startswith(("http://localhost", "https://")):
            return False
    
    return True

def sanitize_input(data: str) -> str:
    """Basic input sanitization"""
    if not isinstance(data, str):
        return str(data)
    
    # Remove potential XSS vectors
    dangerous_patterns = [
        r"<script[^>]*>.*?</script>",
        r"javascript:",
        r"vbscript:",
        r"onload\s*=",
        r"onerror\s*=",
        r"onclick\s*=",
    ]
    
    import re
    for pattern in dangerous_patterns:
        data = re.sub(pattern, "", data, flags=re.IGNORECASE)
    
    return data.strip()

def validate_file_upload(filename: str, content_type: str) -> bool:
    """Validate file upload for security"""
    # Allowed file extensions
    allowed_extensions = {".jpg", ".jpeg", ".png", ".gif", ".pdf", ".txt", ".doc", ".docx"}
    
    # Allowed content types
    allowed_types = {
        "image/jpeg", "image/png", "image/gif",
        "application/pdf", "text/plain",
        "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    }
    
    # Check file extension
    if not any(filename.lower().endswith(ext) for ext in allowed_extensions):
        return False
    
    # Check content type
    if content_type not in allowed_types:
        return False
    
    return True

# Global security middleware instance
security_middleware = SecurityMiddleware()
