# =============================================================================
# ERROR HANDLING UTILITIES
# =============================================================================
# Simplified error handling with proper HTTP status codes and messages

import logging
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class AppError(Exception):
    """Custom application error with HTTP status code"""
    
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        self.error_id = str(uuid.uuid4())
        super().__init__(message)


def create_error_response(
    error: Exception,
    request: Optional[Request] = None,
    include_traceback: bool = False
) -> JSONResponse:
    """Create a standardized error response"""
    
    # Generate error ID for tracking
    error_id = str(uuid.uuid4())
    
    # Determine response details
    if isinstance(error, AppError):
        status_code = error.status_code
        message = error.message
        details = error.details
        error_id = error.error_id
    elif isinstance(error, HTTPException):
        status_code = error.status_code
        message = error.detail
        details = {}
    else:
        status_code = 500
        message = "Internal server error"
        details = {}
    
    # Log the error
    logger.error(f"[{error_id}] {message}", extra={
        "error_id": error_id,
        "status_code": status_code,
        "error_type": type(error).__name__,
        "request_url": str(request.url) if request else None
    })
    
    # Create response
    response_data = {
        "error": {
            "id": error_id,
            "message": message,
            "status_code": status_code,
            "timestamp": datetime.utcnow().isoformat()
        }
    }
    
    # Add details if available
    if details:
        response_data["error"]["details"] = details
    
    # Add traceback in development mode
    if include_traceback:
        import traceback
        response_data["error"]["traceback"] = traceback.format_exc()
    
    return JSONResponse(
        status_code=status_code,
        content=response_data
    )


# Common error factory functions
def not_found_error(resource: str, identifier: str = "") -> AppError:
    """Create a not found error"""
    message = f"{resource} not found"
    if identifier:
        message += f" (ID: {identifier})"
    
    return AppError(
        message=message,
        status_code=404,
        details={"resource": resource, "identifier": identifier}
    )


def validation_error(message: str, details: Optional[Dict[str, Any]] = None) -> AppError:
    """Create a validation error"""
    return AppError(
        message=message,
        status_code=400,
        details=details or {}
    )


def authentication_error(message: str = "Authentication required") -> AppError:
    """Create an authentication error"""
    return AppError(
        message=message,
        status_code=401
    )


def authorization_error(message: str = "Insufficient permissions") -> AppError:
    """Create an authorization error"""
    return AppError(
        message=message,
        status_code=403
    )


def database_error(message: str, details: Optional[Dict[str, Any]] = None) -> AppError:
    """Create a database error"""
    return AppError(
        message=message,
        status_code=500,
        details=details or {}
    )


def conflict_error(message: str, details: Optional[Dict[str, Any]] = None) -> AppError:
    """Create a conflict error (e.g., duplicate resource)"""
    return AppError(
        message=message,
        status_code=409,
        details=details or {}
    )


def rate_limit_error(message: str = "Rate limit exceeded") -> AppError:
    """Create a rate limit error"""
    return AppError(
        message=message,
        status_code=429
    )


def validate_required_fields(data: Dict[str, Any], required_fields: list[str]) -> None:
    """Validate that required fields are present"""
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    
    if missing_fields:
        raise validation_error(
            message=f"Missing required fields: {', '.join(missing_fields)}",
            details={"missing_fields": missing_fields}
        )


def sanitize_error_message(message: str) -> str:
    """Sanitize error message to remove sensitive information"""
    import re
    
    sensitive_patterns = [
        (r'password["\']?\s*:\s*["\']?[^"\']*["\']?', 'password: [REDACTED]'),
        (r'token["\']?\s*:\s*["\']?[^"\']*["\']?', 'token: [REDACTED]'),
        (r'secret["\']?\s*:\s*["\']?[^"\']*["\']?', 'secret: [REDACTED]'),
        (r'key["\']?\s*:\s*["\']?[^"\']*["\']?', 'key: [REDACTED]'),
    ]
    
    sanitized = message
    for pattern, replacement in sensitive_patterns:
        sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)
    
    return sanitized
