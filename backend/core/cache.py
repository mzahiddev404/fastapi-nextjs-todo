# =============================================================================
# SIMPLE IN-MEMORY CACHING SYSTEM
# =============================================================================
# Lightweight in-memory caching for improved performance
# Note: Redis can be added later for production if needed

import asyncio
from typing import Optional, Any, Union, Callable
from datetime import timedelta, datetime
import logging

logger = logging.getLogger(__name__)


class SimpleCache:
    """Simple in-memory cache with TTL support"""
    
    def __init__(self):
        self._cache: dict[str, tuple[Any, Optional[datetime]]] = {}
        logger.info("✅ In-memory cache initialized")
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            if key in self._cache:
                value, expires_at = self._cache[key]
                
                # Check if expired
                if expires_at and datetime.utcnow() > expires_at:
                    del self._cache[key]
                    return None
                
                return value
            return None
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {e}")
            return None
    
    async def set(
        self, 
        key: str, 
        value: Any, 
        ttl: Optional[Union[int, timedelta]] = None
    ) -> bool:
        """Set value in cache with optional TTL (in seconds or timedelta)"""
        try:
            expires_at = None
            if ttl:
                if isinstance(ttl, timedelta):
                    expires_at = datetime.utcnow() + ttl
                else:
                    expires_at = datetime.utcnow() + timedelta(seconds=ttl)
            
            self._cache[key] = (value, expires_at)
            return True
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete value from cache"""
        try:
            if key in self._cache:
                del self._cache[key]
                return True
            return False
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache (and is not expired)"""
        value = await self.get(key)
        return value is not None
    
    async def clear_pattern(self, pattern: str) -> int:
        """Clear all keys matching pattern (simple string matching)"""
        try:
            pattern_str = pattern.replace('*', '')
            keys_to_delete = [k for k in self._cache.keys() if pattern_str in k]
            
            for key in keys_to_delete:
                del self._cache[key]
            
            return len(keys_to_delete)
        except Exception as e:
            logger.error(f"Cache clear pattern error for {pattern}: {e}")
            return 0
    
    async def clear_all(self) -> bool:
        """Clear all cache entries"""
        try:
            self._cache.clear()
            return True
        except Exception as e:
            logger.error(f"Cache clear all error: {e}")
            return False
    
    async def get_or_set(
        self, 
        key: str, 
        factory_func: Callable, 
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
    
    def size(self) -> int:
        """Get current cache size"""
        return len(self._cache)


# Global cache instance
cache = SimpleCache()


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


# Cache invalidation helpers
async def invalidate_user_cache(user_id: str):
    """Invalidate all cache entries for a user"""
    await cache.clear_pattern(f"user:{user_id}*")
    await cache.clear_pattern(f"tasks:{user_id}*")
    await cache.clear_pattern(f"labels:{user_id}*")
    await cache.clear_pattern(f"task_stats:{user_id}*")


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
            "type": "memory",
            "size": cache.size(),
            "test_passed": retrieved_value == test_value
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "type": "memory",
            "error": str(e),
            "test_passed": False
        }
