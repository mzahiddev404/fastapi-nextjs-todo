# =============================================================================
# ERROR HANDLING SYSTEM
# =============================================================================
# Comprehensive error handling with logging, tracking, and user-friendly responses
# Includes error categorization, retry logic, and monitoring integration

import logging
import traceback
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, Union
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
import asyncio
import os

logger = logging.getLogger(__name__)

class ErrorCategory:
    """Error categories for better error handling"""
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    VALIDATION = "validation"
    DATABASE = "database"
    EXTERNAL_SERVICE = "external_service"
    RATE_LIMIT = "rate_limit"
    INTERNAL = "internal"
    NOT_FOUND = "not_found"
    CONFLICT = "conflict"

class ErrorSeverity:
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AppError(Exception):
    """Custom application error with additional context"""
    
    def __init__(
        self,
        message: str,
        category: str = ErrorCategory.INTERNAL,
        severity: str = ErrorSeverity.MEDIUM,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None,
        error_id: Optional[str] = None
    ):
        self.message = message
        self.category = category
        self.severity = severity
        self.status_code = status_code
        self.details = details or {}
        self.error_id = error_id or str(uuid.uuid4())
        super().__init__(message)

class ErrorTracker:
    """Error tracking and logging system"""
    
    def __init__(self):
        self.error_counts = {}
        self.recent_errors = []
        self.max_recent_errors = 100
    
    def track_error(
        self,
        error: Exception,
        request: Optional[Request] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Track an error and return error ID"""
        error_id = str(uuid.uuid4())
        
        # Extract error information
        error_info = {
            "error_id": error_id,
            "timestamp": datetime.utcnow().isoformat(),
            "type": type(error).__name__,
            "message": str(error),
            "traceback": traceback.format_exc(),
            "context": context or {},
        }
        
        # Add request information if available
        if request:
            error_info["request"] = {
                "method": request.method,
                "url": str(request.url),
                "headers": dict(request.headers),
                "client_ip": request.client.host if request.client else None,
            }
        
        # Add to recent errors
        self.recent_errors.append(error_info)
        if len(self.recent_errors) > self.max_recent_errors:
            self.recent_errors.pop(0)
        
        # Update error counts
        error_type = type(error).__name__
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
        
        # Log the error
        self._log_error(error_info)
        
        return error_id
    
    def _log_error(self, error_info: Dict[str, Any]):
        """Log error with appropriate level"""
        error_type = error_info["type"]
        message = error_info["message"]
        error_id = error_info["error_id"]
        
        # Determine log level based on error type
        if error_type in ["AppError"]:
            severity = error_info.get("context", {}).get("severity", ErrorSeverity.MEDIUM)
            if severity == ErrorSeverity.CRITICAL:
                logger.critical(f"[{error_id}] {message}", extra=error_info)
            elif severity == ErrorSeverity.HIGH:
                logger.error(f"[{error_id}] {message}", extra=error_info)
            else:
                logger.warning(f"[{error_id}] {message}", extra=error_info)
        else:
            logger.error(f"[{error_id}] {message}", extra=error_info)
    
    def get_error_stats(self) -> Dict[str, Any]:
        """Get error statistics"""
        return {
            "total_errors": sum(self.error_counts.values()),
            "error_counts": self.error_counts,
            "recent_errors_count": len(self.recent_errors),
            "recent_errors": self.recent_errors[-10:]  # Last 10 errors
        }

# Global error tracker
error_tracker = ErrorTracker()

def create_error_response(
    error: Exception,
    request: Optional[Request] = None,
    include_details: bool = False
) -> JSONResponse:
    """Create a standardized error response"""
    
    # Track the error
    error_id = error_tracker.track_error(error, request)
    
    # Determine response details
    if isinstance(error, AppError):
        status_code = error.status_code
        message = error.message
        category = error.category
        details = error.details if include_details else {}
    elif isinstance(error, HTTPException):
        status_code = error.status_code
        message = error.detail
        category = ErrorCategory.VALIDATION
        details = {}
    else:
        status_code = 500
        message = "Internal server error"
        category = ErrorCategory.INTERNAL
        details = {}
    
    # Create response
    response_data = {
        "error": {
            "id": error_id,
            "message": message,
            "category": category,
            "status_code": status_code,
            "timestamp": datetime.utcnow().isoformat()
        }
    }
    
    # Add details if requested and available
    if include_details and details:
        response_data["error"]["details"] = details
    
    # Add traceback in development
    if os.getenv("ENVIRONMENT") == "development":
        response_data["error"]["traceback"] = traceback.format_exc()
    
    return JSONResponse(
        status_code=status_code,
        content=response_data
    )

async def handle_async_error(
    func,
    *args,
    **kwargs
) -> tuple[bool, Union[Any, Exception]]:
    """Handle async function errors with retry logic"""
    max_retries = 3
    retry_delay = 1  # seconds
    
    for attempt in range(max_retries):
        try:
            result = await func(*args, **kwargs)
            return True, result
        except Exception as e:
            if attempt == max_retries - 1:
                return False, e
            
            # Wait before retry
            await asyncio.sleep(retry_delay * (2 ** attempt))
    
    return False, Exception("Max retries exceeded")

def validate_required_fields(data: Dict[str, Any], required_fields: list[str]) -> None:
    """Validate that required fields are present"""
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    
    if missing_fields:
        raise AppError(
            message=f"Missing required fields: {', '.join(missing_fields)}",
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.LOW,
            status_code=400,
            details={"missing_fields": missing_fields}
        )

def validate_field_types(data: Dict[str, Any], field_types: Dict[str, type]) -> None:
    """Validate field types"""
    type_errors = []
    
    for field, expected_type in field_types.items():
        if field in data and not isinstance(data[field], expected_type):
            type_errors.append({
                "field": field,
                "expected": expected_type.__name__,
                "actual": type(data[field]).__name__
            })
    
    if type_errors:
        raise AppError(
            message="Invalid field types",
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.LOW,
            status_code=400,
            details={"type_errors": type_errors}
        )

def sanitize_error_message(message: str) -> str:
    """Sanitize error message for user display"""
    # Remove sensitive information
    sensitive_patterns = [
        r"password",
        r"token",
        r"secret",
        r"key",
        r"credential"
    ]
    
    import re
    for pattern in sensitive_patterns:
        message = re.sub(pattern, "[REDACTED]", message, flags=re.IGNORECASE)
    
    return message

# Common error responses
def not_found_error(resource: str, identifier: str) -> AppError:
    """Create a not found error"""
    return AppError(
        message=f"{resource} with identifier '{identifier}' not found",
        category=ErrorCategory.NOT_FOUND,
        severity=ErrorSeverity.LOW,
        status_code=404,
        details={"resource": resource, "identifier": identifier}
    )

def validation_error(message: str, details: Optional[Dict[str, Any]] = None) -> AppError:
    """Create a validation error"""
    return AppError(
        message=message,
        category=ErrorCategory.VALIDATION,
        severity=ErrorSeverity.LOW,
        status_code=400,
        details=details
    )

def authentication_error(message: str = "Authentication required") -> AppError:
    """Create an authentication error"""
    return AppError(
        message=message,
        category=ErrorCategory.AUTHENTICATION,
        severity=ErrorSeverity.MEDIUM,
        status_code=401
    )

def authorization_error(message: str = "Insufficient permissions") -> AppError:
    """Create an authorization error"""
    return AppError(
        message=message,
        category=ErrorCategory.AUTHORIZATION,
        severity=ErrorSeverity.MEDIUM,
        status_code=403
    )

def database_error(message: str, details: Optional[Dict[str, Any]] = None) -> AppError:
    """Create a database error"""
    return AppError(
        message=message,
        category=ErrorCategory.DATABASE,
        severity=ErrorSeverity.HIGH,
        status_code=500,
        details=details
    )

def rate_limit_error(message: str = "Rate limit exceeded") -> AppError:
    """Create a rate limit error"""
    return AppError(
        message=message,
        category=ErrorCategory.RATE_LIMIT,
        severity=ErrorSeverity.MEDIUM,
        status_code=429
    )

# Error monitoring and alerting
async def check_error_thresholds():
    """Check if error rates exceed thresholds"""
    stats = error_tracker.get_error_stats()
    
    # Define thresholds
    error_thresholds = {
        "total_errors_per_minute": 100,
        "critical_errors_per_minute": 10,
        "database_errors_per_minute": 20
    }
    
    # Check thresholds (simplified implementation)
    if stats["total_errors"] > error_thresholds["total_errors_per_minute"]:
        logger.critical("Error rate threshold exceeded")
        # In production, send alert to monitoring service
    
    return stats
