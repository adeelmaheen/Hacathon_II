"""JWT authentication utilities."""
from datetime import datetime, timedelta
from typing import Optional
import hashlib
import bcrypt
from jose import JWTError, jwt
from app.config import settings


def _preprocess_password(password: str) -> bytes:
    """Preprocess password to handle bcrypt's 72-byte limit.
    
    Hash with SHA256 first to get a fixed 32-byte binary output,
    then bcrypt that hash. This allows passwords of any length.
    """
    # Hash with SHA256 to get fixed 32-byte binary output
    return hashlib.sha256(password.encode('utf-8')).digest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    # Preprocess the password the same way we hash it
    processed_password = _preprocess_password(plain_password)
    # hashed_password is already a bcrypt hash string, so we can verify directly
    try:
        return bcrypt.checkpw(processed_password, hashed_password.encode('utf-8'))
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """Hash a password.
    
    Uses SHA256 first to handle bcrypt's 72-byte limit,
    then bcrypts the SHA256 hash.
    """
    processed_password = _preprocess_password(password)
    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(processed_password, salt)
    return hashed.decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """Decode and verify a JWT token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

