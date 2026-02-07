"""Task model for todo items."""
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    """
    Task entity representing a todo item.

    Each task belongs to a single user (user_id FK) and contains
    title, optional description, completion status, and timestamps.

    Attributes:
        id: Auto-increment primary key
        user_id: Foreign key to users table (UUID string)
        title: Task title (1-200 characters)
        description: Optional detailed description (0-1000 characters)
        completed: Completion status (default False)
        created_at: Task creation timestamp
        updated_at: Last update timestamp
    """

    __tablename__ = "tasks"

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Auto-increment task ID"
    )
    user_id: str = Field(
        foreign_key="users.id",
        index=True,
        description="Owner user ID (UUID)"
    )
    title: str = Field(
        max_length=200,
        min_length=1,
        description="Task title (required)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Optional task description"
    )
    completed: bool = Field(
        default=False,
        index=True,
        description="Completion status"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Task creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp"
    )

    class Config:
        """SQLModel configuration."""
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread, and vegetables",
                "completed": False,
                "created_at": "2026-01-03T12:00:00",
                "updated_at": "2026-01-03T12:00:00"
            }
        }
