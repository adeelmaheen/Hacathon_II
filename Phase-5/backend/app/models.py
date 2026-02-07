"""Database models for User and Task."""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum


class Priority(str, Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class RecurrencePattern(str, Enum):
    """Recurrence patterns for tasks."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    CUSTOM = "custom"


class User(SQLModel, table=True):
    """User model for authentication."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str
    name: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Task(SQLModel, table=True):
    """Task model for todo items with advanced features."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    title: str = Field(min_length=1, max_length=200, index=True)
    description: str = Field(default="", max_length=1000)
    completed: bool = Field(default=False, index=True)
    
    # Advanced features
    priority: str = Field(default="medium", index=True)  # low, medium, high, urgent
    tags: Optional[str] = Field(default=None)  # JSON array of strings
    due_date: Optional[datetime] = Field(default=None, index=True)
    reminder_time: Optional[datetime] = Field(default=None)
    
    # Recurrence fields
    recurrence_pattern: Optional[str] = Field(default=None)  # daily, weekly, monthly, yearly, custom
    recurrence_interval: Optional[int] = Field(default=None)  # e.g., every 2 days
    next_due_date: Optional[datetime] = Field(default=None)
    parent_task_id: Optional[int] = Field(default=None, foreign_key="task.id")  # For recurring task chain
    
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Conversation(SQLModel, table=True):
    """Conversation model for chat sessions."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Message(SQLModel, table=True):
    """Message model for chat messages."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    role: str = Field(max_length=20)  # "user" or "assistant"
    content: str = Field(max_length=5000)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class RecurringTask(SQLModel, table=True):
    """Recurring task configuration."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id", index=True, unique=True)
    pattern: str = Field(max_length=50)  # daily, weekly, monthly, yearly, custom
    interval: int = Field(default=1)  # e.g., every 2 days
    last_created_at: Optional[datetime] = Field(default=None)
    next_due_date: Optional[datetime] = Field(default=None, index=True)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Reminder(SQLModel, table=True):
    """Reminder for tasks with due dates."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id", index=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    remind_at: datetime = Field(index=True)
    sent: bool = Field(default=False, index=True)
    sent_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

