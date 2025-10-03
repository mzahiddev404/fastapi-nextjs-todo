"""CRUD operations package."""

from .user import (
    get_user_by_email, get_user_by_id, get_user_by_username,
    create_user, update_user, delete_user, authenticate_user
)
from .task import (
    get_task_by_id, get_tasks_by_user, get_tasks_by_label,
    create_task, update_task, delete_task,
    get_completed_tasks, get_pending_tasks
)
from .label import (
    get_label_by_id, get_labels_by_user, get_label_by_name,
    create_label, update_label, delete_label, get_label_usage_count
)

__all__ = [
    # User CRUD
    "get_user_by_email", "get_user_by_id", "get_user_by_username",
    "create_user", "update_user", "delete_user", "authenticate_user",
    # Task CRUD
    "get_task_by_id", "get_tasks_by_user", "get_tasks_by_label",
    "create_task", "update_task", "delete_task",
    "get_completed_tasks", "get_pending_tasks",
    # Label CRUD
    "get_label_by_id", "get_labels_by_user", "get_label_by_name",
    "create_label", "update_label", "delete_label", "get_label_usage_count"
]
