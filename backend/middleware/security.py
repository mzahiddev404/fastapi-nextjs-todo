# =============================================================================
# SECURITY MIDDLEWARE
# =============================================================================
# Implements security headers and request size limits
# Provides protection against common web vulnerabilities

from fastapi import Request, HTTPException, status
import os

# Security configuration
MAX_REQUEST_SIZE = int(os.getenv("MAX_REQUEST_SIZE", "10485760"))  # 10MB default


async def security_middleware(request: Request, call_next):
    """
    Security middleware that adds security headers and validates request size
    
    Features:
    - Request size validation
    - Security headers (XSS, Content-Type, Frame options, etc.)
    - HSTS for HTTPS
    - Content Security Policy
    """
    
    # Check request size to prevent large payload attacks
    if hasattr(request, "headers") and "content-length" in request.headers:
        content_length = int(request.headers.get("content-length", 0))
        if content_length > MAX_REQUEST_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="Request entity too large"
            )
    
    # Process the request
    response = await call_next(request)
    
    # Add security headers to response
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    
    # Add HSTS header for HTTPS (only in production)
    if request.url.scheme == "https":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    # Add Content Security Policy header
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
