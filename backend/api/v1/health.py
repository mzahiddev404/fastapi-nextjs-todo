# =============================================================================
# HEALTH CHECK API ROUTES
# =============================================================================
# Comprehensive health check endpoints for monitoring and diagnostics
# Provides detailed system status and performance metrics

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import asyncio
import psutil
import os
import time
from typing import Dict, Any, Optional

from core.db import get_database
from core.cache import cache_health_check
from models.user import User
from models.task import Task
from models.label import Label

router = APIRouter()

class HealthChecker:
    """Health check utilities"""
    
    @staticmethod
    async def check_database() -> Dict[str, Any]:
        """Check database connectivity and performance"""
        try:
            start_time = time.time()
            
            # Test database connection
            db = await get_database().__anext__()
            
            # Test basic operations
            user_count = await User.count()
            task_count = await Task.count()
            label_count = await Label.count()
            
            # Test a simple query
            await User.find_one()
            
            response_time = (time.time() - start_time) * 1000  # Convert to ms
            
            return {
                "status": "healthy",
                "response_time_ms": round(response_time, 2),
                "collections": {
                    "users": user_count,
                    "tasks": task_count,
                    "labels": label_count
                }
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "response_time_ms": None
            }
    
    @staticmethod
    async def check_cache() -> Dict[str, Any]:
        """Check cache system health"""
        return await cache_health_check()
    
    @staticmethod
    def check_system_resources() -> Dict[str, Any]:
        """Check system resource usage"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            
            # Disk usage
            disk = psutil.disk_usage('/')
            
            # Process info
            process = psutil.Process()
            process_memory = process.memory_info()
            
            return {
                "status": "healthy",
                "cpu_percent": cpu_percent,
                "memory": {
                    "total_gb": round(memory.total / (1024**3), 2),
                    "available_gb": round(memory.available / (1024**3), 2),
                    "used_percent": memory.percent
                },
                "disk": {
                    "total_gb": round(disk.total / (1024**3), 2),
                    "free_gb": round(disk.free / (1024**3), 2),
                    "used_percent": round((disk.used / disk.total) * 100, 2)
                },
                "process": {
                    "memory_mb": round(process_memory.rss / (1024**2), 2),
                    "cpu_percent": process.cpu_percent()
                }
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    @staticmethod
    def check_environment() -> Dict[str, Any]:
        """Check environment configuration"""
        required_vars = [
            "JWT_SECRET",
            "MONGODB_URL"
        ]
        
        optional_vars = [
            "REDIS_URL",
            "ENVIRONMENT",
            "JWT_EXPIRE_MINUTES",
            "JWT_REFRESH_EXPIRE_DAYS"
        ]
        
        missing_required = []
        missing_optional = []
        
        for var in required_vars:
            if not os.getenv(var):
                missing_required.append(var)
        
        for var in optional_vars:
            if not os.getenv(var):
                missing_optional.append(var)
        
        status = "healthy" if not missing_required else "unhealthy"
        
        return {
            "status": status,
            "required_variables": {
                "missing": missing_required,
                "present": [var for var in required_vars if var not in missing_required]
            },
            "optional_variables": {
                "missing": missing_optional,
                "present": [var for var in optional_vars if var not in missing_optional]
            }
        }

@router.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "TODO API",
        "version": "1.0.0"
    }

@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with system metrics"""
    start_time = time.time()
    
    # Run all health checks in parallel
    db_check, cache_check, system_check, env_check = await asyncio.gather(
        HealthChecker.check_database(),
        HealthChecker.check_cache(),
        asyncio.to_thread(HealthChecker.check_system_resources),
        asyncio.to_thread(HealthChecker.check_environment),
        return_exceptions=True
    )
    
    # Calculate overall health
    checks = [db_check, cache_check, system_check, env_check]
    healthy_checks = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "healthy")
    total_checks = len(checks)
    
    overall_status = "healthy" if healthy_checks == total_checks else "degraded"
    
    response_time = (time.time() - start_time) * 1000
    
    return {
        "status": overall_status,
        "timestamp": datetime.utcnow().isoformat(),
        "service": "TODO API",
        "version": "1.0.0",
        "response_time_ms": round(response_time, 2),
        "checks": {
            "database": db_check if not isinstance(db_check, Exception) else {"status": "error", "error": str(db_check)},
            "cache": cache_check if not isinstance(cache_check, Exception) else {"status": "error", "error": str(cache_check)},
            "system": system_check if not isinstance(system_check, Exception) else {"status": "error", "error": str(system_check)},
            "environment": env_check if not isinstance(env_check, Exception) else {"status": "error", "error": str(env_check)}
        },
        "summary": {
            "healthy_checks": healthy_checks,
            "total_checks": total_checks,
            "health_percentage": round((healthy_checks / total_checks) * 100, 1)
        }
    }

@router.get("/health/ready")
async def readiness_check():
    """Kubernetes readiness probe endpoint"""
    try:
        # Check if database is accessible
        db_check = await HealthChecker.check_database()
        
        if db_check["status"] != "healthy":
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database not ready"
            )
        
        return {"status": "ready"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service not ready: {str(e)}"
        )

@router.get("/health/live")
async def liveness_check():
    """Kubernetes liveness probe endpoint"""
    return {"status": "alive"}

@router.get("/health/metrics")
async def metrics():
    """Application metrics endpoint"""
    try:
        # Get basic metrics
        user_count = await User.count()
        task_count = await Task.count()
        label_count = await Label.count()
        
        # Get task status distribution
        pipeline = [
            {"$group": {"_id": "$status", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        status_distribution = await Task.get_motor_collection().aggregate(pipeline).to_list(None)
        
        # Get system resources
        system_resources = HealthChecker.check_system_resources()
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "application": {
                "users": user_count,
                "tasks": task_count,
                "labels": label_count,
                "task_status_distribution": status_distribution
            },
            "system": system_resources
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get metrics: {str(e)}"
        )

@router.get("/health/version")
async def version_info():
    """Version and build information"""
    return {
        "service": "TODO API",
        "version": "1.0.0",
        "build_date": datetime.utcnow().isoformat(),
        "environment": os.getenv("ENVIRONMENT", "development"),
        "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
        "features": [
            "authentication",
            "task_management",
            "label_management",
            "rate_limiting",
            "caching",
            "health_checks"
        ]
    }
