"""Authentication service for user registration, login, and logout."""
from typing import Optional

from fastapi import HTTPException, status
from sqlmodel import Session, select

from src.models.user import User
from src.schemas.auth import RegisterRequest, LoginRequest, UserResponse
from src.utils.security import hash_password, verify_password, create_access_token


class AuthService:
    """
    Authentication service handling user registration, login, and logout.

    This service implements the business logic for authentication operations
    while maintaining user data isolation and security best practices.
    """

    @staticmethod
    def register_user(
        session: Session,
        registration_data: RegisterRequest
    ) -> User:
        """
        Register a new user account.

        Args:
            session: Database session
            registration_data: Registration request with email, name, password

        Returns:
            Created User object

        Raises:
            HTTPException: 409 if email already exists
            HTTPException: 400 if validation fails
        """
        # Check if email already exists (case-insensitive)
        existing_user = session.exec(
            select(User).where(User.email == registration_data.email.lower())
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        # Hash the password
        password_hash = hash_password(registration_data.password)

        # Create new user
        new_user = User(
            email=registration_data.email.lower(),
            name=registration_data.name,
            password_hash=password_hash
        )

        # Save to database
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return new_user

    @staticmethod
    def authenticate_user(
        session: Session,
        login_data: LoginRequest
    ) -> tuple[User, str]:
        """
        Authenticate user credentials and generate JWT token.

        Args:
            session: Database session
            login_data: Login request with email and password

        Returns:
            Tuple of (User object, JWT access token)

        Raises:
            HTTPException: 401 if credentials are invalid
        """
        # Find user by email (case-insensitive)
        user = session.exec(
            select(User).where(User.email == login_data.email.lower())
        ).first()

        # Generic error message for security (don't reveal if email exists)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        # Verify password
        if not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        # Generate JWT token
        access_token = create_access_token(data={"sub": user.id})

        return user, access_token

    @staticmethod
    def logout_user() -> dict:
        """
        Logout user by clearing authentication.

        Since we're using JWT with HTTPOnly cookies, the actual logout
        happens on the client side by clearing the cookie. This endpoint
        provides a confirmation response.

        Returns:
            Success message dictionary
        """
        return {"message": "Successfully logged out"}

    @staticmethod
    def get_user_by_id(session: Session, user_id: str) -> Optional[User]:
        """
        Get user by ID.

        Args:
            session: Database session
            user_id: User UUID

        Returns:
            User object if found, None otherwise
        """
        return session.get(User, user_id)
