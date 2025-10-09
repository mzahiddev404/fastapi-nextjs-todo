# crud/__init__.py
from .user import UserCRUD
from .task import TaskCRUD
from .label import LabelCRUD

__all__ = ["UserCRUD", "TaskCRUD", "LabelCRUD"]
