"""Authentication API endpoints."""
from fastapi import APIRouter, Depends, Response, status
from sqlmodel import Session

from src.api.deps import get_session
from src.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from src.services.auth_service import AuthService

router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account",
    description="Create a new user account with email, name, and password. Email must be unique."
)
def register(
    registration_data: RegisterRequest,
    session: Session = Depends(get_session)
) -> UserResponse:
    """
    Register a new user account.

    - **email**: Unique email address (case-insensitive)
    - **name**: User's display name (1-100 characters)
    - **password**: Password (8-72 characters, will be hashed with bcrypt)

    Returns user information excluding password_hash.

    Raises:
        409 Conflict: If email already exists
        400 Bad Request: If validation fails
    """
    user = AuthService.register_user(session, registration_data)

    # Convert ORM model to response schema
    return UserResponse.model_validate(user)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login with email and password",
    description="Authenticate user and receive JWT access token in HTTPOnly cookie"
)
def login(
    login_data: LoginRequest,
    response: Response,
    session: Session = Depends(get_session)
) -> TokenResponse:
    """
    Authenticate user credentials and generate JWT token.

    - **email**: User's email address
    - **password**: User's password

    Returns JWT access token in HTTPOnly cookie for security.

    Raises:
        401 Unauthorized: If credentials are incorrect
    """
    user, access_token = AuthService.authenticate_user(session, login_data)

    # Set HTTPOnly cookie with JWT token
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=True,  # HTTPS only in production
        samesite="lax",
        max_age=86400  # 24 hours
    )

    # Also return token in response body for localStorage option
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )


@router.post(
    "/logout",
    summary="Logout current user",
    description="Clear authentication cookie and logout user"
)
def logout(response: Response) -> dict:
    """
    Logout user by clearing authentication cookie.

    For JWT-based auth, this clears the HTTPOnly cookie.
    The client should also clear any localStorage tokens.

    Returns:
        Success message
    """
    # Clear the HTTPOnly cookie
    response.delete_cookie(key="access_token")

    return AuthService.logout_user()
