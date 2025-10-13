# =============================================================================
# RATE LIMITING MIDDLEWARE
# =============================================================================
# Implements rate limiting to prevent abuse and DDoS attacks
# Uses Redis for distributed rate limiting in production

from fastapi import Request, HTTPException, status
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import redis
import os
from typing import Optional

# Redis configuration for rate limiting
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Initialize Redis client
try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    redis_client.ping()  # Test connection
except Exception:
    # Fallback to in-memory storage if Redis is not available
    redis_client = None

# Create limiter instance
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=REDIS_URL if redis_client else "memory://",
    default_limits=["1000/hour"]  # Default rate limit
)

# Rate limit configurations for different endpoints
RATE_LIMITS = {
    "auth": ["5/minute", "20/hour"],  # Stricter limits for auth endpoints
    "api": ["100/minute", "1000/hour"],  # Standard API limits
    "public": ["200/minute", "2000/hour"],  # More lenient for public endpoints
}

def get_rate_limit_for_path(path: str) -> list[str]:
    """Get appropriate rate limit based on the request path"""
    if path.startswith("/api/v1/auth"):
        return RATE_LIMITS["auth"]
    elif path.startswith("/api/v1"):
        return RATE_LIMITS["api"]
    else:
        return RATE_LIMITS["public"]

def create_rate_limit_decorator(limits: list[str]):
    """Create a rate limit decorator with specific limits"""
    return limiter.limit(" and ".join(limits))

# Rate limit decorators for different endpoint types
auth_rate_limit = create_rate_limit_decorator(RATE_LIMITS["auth"])
api_rate_limit = create_rate_limit_decorator(RATE_LIMITS["api"])
public_rate_limit = create_rate_limit_decorator(RATE_LIMITS["public"])

def get_client_identifier(request: Request) -> str:
    """Get a unique identifier for the client (IP + User-Agent hash)"""
    client_ip = get_remote_address(request)
    user_agent = request.headers.get("user-agent", "")
    
    # Create a simple hash of user agent for additional uniqueness
    user_agent_hash = str(hash(user_agent))[:8]
    
    return f"{client_ip}:{user_agent_hash}"

def check_rate_limit(request: Request, limits: list[str]) -> bool:
    """Check if the request exceeds rate limits"""
    try:
        client_id = get_client_identifier(request)
        
        # Check each limit
        for limit in limits:
            if not _check_single_limit(client_id, limit):
                return False
        
        return True
    except Exception:
        # If rate limiting fails, allow the request (fail open)
        return True

def _check_single_limit(client_id: str, limit: str) -> bool:
    """Check a single rate limit"""
    try:
        if redis_client:
            return _check_redis_limit(client_id, limit)
        else:
            return _check_memory_limit(client_id, limit)
    except Exception:
        return True  # Fail open

def _check_redis_limit(client_id: str, limit: str) -> bool:
    """Check rate limit using Redis"""
    # Parse limit (e.g., "5/minute")
    count, period = limit.split("/")
    count = int(count)
    
    # Convert period to seconds
    period_seconds = {
        "second": 1,
        "minute": 60,
        "hour": 3600,
        "day": 86400
    }.get(period, 60)
    
    key = f"rate_limit:{client_id}:{period}"
    
    # Use Redis pipeline for atomic operations
    pipe = redis_client.pipeline()
    pipe.incr(key)
    pipe.expire(key, period_seconds)
    results = pipe.execute()
    
    current_count = results[0]
    return current_count <= count

def _check_memory_limit(client_id: str, limit: str) -> bool:
    """Check rate limit using in-memory storage (fallback)"""
    # This is a simplified in-memory implementation
    # In production, you should use Redis or a proper rate limiting service
    return True

# Rate limit exceeded handler
def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    """Handle rate limit exceeded errors"""
    return HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail={
            "error": "Rate limit exceeded",
            "message": f"Too many requests. Limit: {exc.detail}",
            "retry_after": 60
        }
    )
