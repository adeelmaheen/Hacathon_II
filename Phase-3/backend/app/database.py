"""Database connection and session management."""
from sqlmodel import SQLModel, create_engine, Session
from app.config import settings

# Create database engine
import os
engine = create_engine(
    settings.DATABASE_URL,
    echo=os.getenv("ENVIRONMENT", "development") == "development",  # Log SQL queries only in development
    pool_pre_ping=True,  # Verify connections before using
)


def init_db():
    """Initialize database tables."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get database session."""
    with Session(engine) as session:
        yield session

