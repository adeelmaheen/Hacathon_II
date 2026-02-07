"""
Database connection and session management.
Provides SQLModel engine and session factory.
"""
from sqlmodel import create_engine, Session
from sqlalchemy.orm import sessionmaker
from .config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.ENVIRONMENT == "development",
    pool_pre_ping=True,  # Verify connections before using
    pool_size=5,
    max_overflow=10,
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session,
)


def get_session():
    """
    Dependency function to get database session.
    Yields a session and ensures it's closed after use.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
