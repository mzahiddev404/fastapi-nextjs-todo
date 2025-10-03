"""API v1 package."""

from .auth import router as auth_router
from .tasks import router as tasks_router
from .labels import router as labels_router

__all__ = ["auth_router", "tasks_router", "labels_router"]
