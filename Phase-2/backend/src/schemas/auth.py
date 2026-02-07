"""Authentication request and response schemas."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator


class RegisterRequest(BaseModel):
    """
    Request schema for user registration.

    Validates email format, name requirements, and password strength.
    """

    email: EmailStr = Field(
        ...,
        description="User's email address (unique identifier)"
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="User's display name"
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=72,
        description="Password (8-72 characters, will be hashed)"
    )

    @validator('name')
    def name_not_whitespace_only(cls, v: str) -> str:
        """Ensure name is not just whitespace."""
        if not v.strip():
            raise ValueError('Name cannot be whitespace only')
        return v.strip()

    @validator('email')
    def email_lowercase(cls, v: str) -> str:
        """Normalize email to lowercase for case-insensitive uniqueness."""
        return v.lower()

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "name": "John Doe",
                "password": "securepassword123"
            }
        }


class LoginRequest(BaseModel):
    """
    Request schema for user login.

    Simple email and password validation.
    """

    email: EmailStr = Field(
        ...,
        description="User's email address"
    )
    password: str = Field(
        ...,
        description="User's password"
    )

    @validator('email')
    def email_lowercase(cls, v: str) -> str:
        """Normalize email to lowercase."""
        return v.lower()

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }


class UserResponse(BaseModel):
    """
    Response schema for user data.

    Excludes sensitive fields like password_hash.
    """

    id: str = Field(
        ...,
        description="Unique user identifier (UUID)"
    )
    email: str = Field(
        ...,
        description="User's email address"
    )
    name: str = Field(
        ...,
        description="User's display name"
    )
    created_at: datetime = Field(
        ...,
        description="Account creation timestamp"
    )

    class Config:
        """Pydantic configuration."""
        from_attributes = True  # Allows conversion from ORM models
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "name": "John Doe",
                "created_at": "2026-01-03T12:00:00"
            }
        }


class TokenResponse(BaseModel):
    """
    Response schema for authentication tokens.

    Returns JWT access token and user information.
    """

    access_token: str = Field(
        ...,
        description="JWT access token"
    )
    token_type: str = Field(
        default="bearer",
        description="Token type (always 'bearer')"
    )
    user: UserResponse = Field(
        ...,
        description="Authenticated user information"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "email": "user@example.com",
                    "name": "John Doe",
                    "created_at": "2026-01-03T12:00:00"
                }
            }
        }
