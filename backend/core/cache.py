# =============================================================================
# CACHING SYSTEM
# =============================================================================
# Redis-based caching system for improved performance
# Implements cache-aside pattern with TTL support

import json
import redis
import os
import asyncio
from typing import Optional, Any, Union
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class CacheManager:
    """Redis-based cache manager with fallback to in-memory cache"""
    
    def __init__(self):
        self.redis_client = None
        self.memory_cache = {}  # Fallback cache
        self._initialize_redis()
    
    def _initialize_redis(self):
        """Initialize Redis connection"""
        try:
            redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            self.redis_client.ping()  # Test connection
            logger.info("✅ Redis cache connected successfully")
        except Exception as e:
            logger.warning(f"⚠️ Redis not available, using memory cache: {e}")
            self.redis_client = None
    
    def _serialize_value(self, value: Any) -> str:
        """Serialize value for storage"""
        if isinstance(value, (str, int, float, bool)):
            return json.dumps(value)
        return json.dumps(value, default=str)
    
    def _deserialize_value(self, value: str) -> Any:
        """Deserialize value from storage"""
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            if self.redis_client:
                value = self.redis_client.get(key)
                return self._deserialize_value(value) if value else None
            else:
                return self.memory_cache.get(key)
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {e}")
            return None
    
    async def set(
        self, 
        key: str, 
        value: Any, 
        ttl: Optional[Union[int, timedelta]] = None
    ) -> bool:
        """Set value in cache with optional TTL"""
        try:
            serialized_value = self._serialize_value(value)
            
            if self.redis_client:
                if ttl:
                    if isinstance(ttl, timedelta):
                        ttl = int(ttl.total_seconds())
                    return self.redis_client.setex(key, ttl, serialized_value)
                else:
                    return self.redis_client.set(key, serialized_value)
            else:
                self.memory_cache[key] = value
                return True
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete value from cache"""
        try:
            if self.redis_client:
                return bool(self.redis_client.delete(key))
            else:
                return self.memory_cache.pop(key, None) is not None
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        try:
            if self.redis_client:
                return bool(self.redis_client.exists(key))
            else:
                return key in self.memory_cache
        except Exception as e:
            logger.error(f"Cache exists error for key {key}: {e}")
            return False
    
    async def clear_pattern(self, pattern: str) -> int:
        """Clear all keys matching pattern"""
        try:
            if self.redis_client:
                keys = self.redis_client.keys(pattern)
                if keys:
                    return self.redis_client.delete(*keys)
                return 0
            else:
                # For memory cache, we need to iterate
                keys_to_delete = [k for k in self.memory_cache.keys() if pattern.replace('*', '') in k]
                for key in keys_to_delete:
                    del self.memory_cache[key]
                return len(keys_to_delete)
        except Exception as e:
            logger.error(f"Cache clear pattern error for {pattern}: {e}")
            return 0
    
    async def get_or_set(
        self, 
        key: str, 
        factory_func, 
        ttl: Optional[Union[int, timedelta]] = None
    ) -> Any:
        """Get value from cache or set it using factory function"""
        value = await self.get(key)
        if value is not None:
            return value
        
        # Value not in cache, generate it
        try:
            if asyncio.iscoroutinefunction(factory_func):
                value = await factory_func()
            else:
                value = factory_func()
            
            await self.set(key, value, ttl)
            return value
        except Exception as e:
            logger.error(f"Cache get_or_set error for key {key}: {e}")
            raise

# Global cache instance
cache = CacheManager()

# Cache key generators
def user_cache_key(user_id: str) -> str:
    """Generate cache key for user data"""
    return f"user:{user_id}"

def tasks_cache_key(user_id: str) -> str:
    """Generate cache key for user tasks"""
    return f"tasks:{user_id}"

def task_cache_key(task_id: str) -> str:
    """Generate cache key for specific task"""
    return f"task:{task_id}"

def labels_cache_key(user_id: str) -> str:
    """Generate cache key for user labels"""
    return f"labels:{user_id}"

def task_stats_cache_key(user_id: str) -> str:
    """Generate cache key for task statistics"""
    return f"task_stats:{user_id}"

# Cache decorators
def cache_result(ttl: Optional[Union[int, timedelta]] = None, key_func=None):
    """Decorator to cache function results"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            result = await cache.get(cache_key)
            if result is not None:
                return result
            
            # Execute function and cache result
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            
            await cache.set(cache_key, result, ttl)
            return result
        
        return wrapper
    return decorator

# Cache invalidation helpers
async def invalidate_user_cache(user_id: str):
    """Invalidate all cache entries for a user"""
    patterns = [
        f"user:{user_id}",
        f"tasks:{user_id}",
        f"labels:{user_id}",
        f"task_stats:{user_id}",
    ]
    
    for pattern in patterns:
        await cache.clear_pattern(pattern)

async def invalidate_task_cache(task_id: str, user_id: str):
    """Invalidate cache entries for a specific task"""
    await cache.delete(f"task:{task_id}")
    await cache.delete(f"tasks:{user_id}")
    await cache.delete(f"task_stats:{user_id}")

async def invalidate_label_cache(user_id: str):
    """Invalidate cache entries for user labels"""
    await cache.delete(f"labels:{user_id}")

# Health check
async def cache_health_check() -> dict:
    """Check cache system health"""
    try:
        test_key = "health_check"
        test_value = "ok"
        
        # Test set and get
        await cache.set(test_key, test_value, ttl=10)
        retrieved_value = await cache.get(test_key)
        await cache.delete(test_key)
        
        return {
            "status": "healthy" if retrieved_value == test_value else "unhealthy",
            "type": "redis" if cache.redis_client else "memory",
            "test_passed": retrieved_value == test_value
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "type": "memory",
            "error": str(e),
            "test_passed": False
        }
