"""User model for authentication and task ownership."""
import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """
    User entity representing a registered account.

    Each user has unique credentials and owns a collection of tasks.
    Users are isolated from each other - they can only access their own tasks.

    Attributes:
        id: Unique identifier (UUID v4) - not auto-increment for security
        email: User's email address (unique, used for login)
        name: User's display name
        password_hash: Bcrypt hashed password (never plaintext)
        created_at: Account creation timestamp
    """

    __tablename__ = "users"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        index=True,
        description="Unique user identifier (UUID v4)"
    )
    email: str = Field(
        unique=True,
        index=True,
        max_length=255,
        description="User's email address (unique, case-insensitive)"
    )
    name: str = Field(
        max_length=100,
        description="User's display name"
    )
    password_hash: str = Field(
        max_length=60,
        description="Bcrypt hashed password (fixed 60 chars)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Account creation timestamp"
    )

    class Config:
        """SQLModel configuration."""
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "name": "John Doe",
                "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyWKL0Kn.mEK",
                "created_at": "2026-01-03T12:00:00"
            }
        }
