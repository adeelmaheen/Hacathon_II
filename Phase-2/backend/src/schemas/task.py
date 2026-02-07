"""Task request and response schemas."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class TaskCreate(BaseModel):
    """
    Request schema for creating a new task.

    Validates title length and optional description.
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Task title (required, 1-200 characters)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Optional task description (max 1000 characters)"
    )

    @validator('title')
    def title_not_whitespace_only(cls, v: str) -> str:
        """Ensure title is not just whitespace."""
        if not v.strip():
            raise ValueError('Title cannot be whitespace only')
        return v.strip()

    @validator('description')
    def description_optional_trim(cls, v: Optional[str]) -> Optional[str]:
        """Trim description if provided, or return None."""
        if v is None:
            return None
        trimmed = v.strip()
        return trimmed if trimmed else None

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread, and vegetables"
            }
        }


class TaskUpdate(BaseModel):
    """
    Request schema for updating an existing task.

    All fields are optional to support partial updates.
    """

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Updated task title (optional)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Updated task description (optional)"
    )
    completed: Optional[bool] = Field(
        default=None,
        description="Updated completion status (optional)"
    )

    @validator('title')
    def title_not_whitespace_only(cls, v: Optional[str]) -> Optional[str]:
        """Ensure title is not just whitespace if provided."""
        if v is None:
            return None
        if not v.strip():
            raise ValueError('Title cannot be whitespace only')
        return v.strip()

    @validator('description')
    def description_optional_trim(cls, v: Optional[str]) -> Optional[str]:
        """Trim description if provided, or return None."""
        if v is None:
            return None
        trimmed = v.strip()
        return trimmed if trimmed else None

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "completed": True
            }
        }


class TaskResponse(BaseModel):
    """
    Response schema for task data.

    Returns all task fields including timestamps.
    """

    id: int = Field(
        ...,
        description="Task ID"
    )
    user_id: str = Field(
        ...,
        description="Owner user ID"
    )
    title: str = Field(
        ...,
        description="Task title"
    )
    description: Optional[str] = Field(
        default=None,
        description="Task description (null if not provided)"
    )
    completed: bool = Field(
        ...,
        description="Completion status"
    )
    created_at: datetime = Field(
        ...,
        description="Creation timestamp"
    )
    updated_at: datetime = Field(
        ...,
        description="Last update timestamp"
    )

    class Config:
        """Pydantic configuration."""
        from_attributes = True  # Allows conversion from ORM models
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
