"""
FastAPI dependency injection functions.
Provides database session and current user authentication.
"""
from typing import Generator, Optional
from fastapi import Depends, HTTPException, status, Cookie
from sqlmodel import Session, select
from ..db import get_session
from ..utils.security import decode_access_token


async def get_current_user(
    access_token: Optional[str] = Cookie(None),
    session: Session = Depends(get_session)
) -> str:
    """
    Dependency to get currently authenticated user ID.
    Validates JWT token from HTTPOnly cookie or Authorization header.

    Args:
        access_token: JWT token from HTTPOnly cookie
        session: Database session

    Returns:
        User ID (UUID string)

    Raises:
        HTTPException: 401 if token is missing or invalid
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Extract token from cookie (Bearer prefix if present)
    token = access_token
    if token and token.startswith("Bearer "):
        token = token[7:]

    if not token:
        raise credentials_exception

    # Decode JWT token
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    # Import User model here to avoid circular imports
    from ..models.user import User

    # Verify user exists in database
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()

    if user is None:
        raise credentials_exception

    # Return just the user_id for use in services
    return user_id
