"""
Security Utilities - Password hashing and JWT token management.

Provides bcrypt password hashing and JWT token creation/validation
using HttpOnly cookie storage strategy.
"""

from datetime import datetime, timedelta
from typing import Optional, Any

import bcrypt
from jose import jwt, JWTError

from src.config import settings


# ==============================================================================
# Password Hashing (bcrypt)
# ==============================================================================

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Uses 12 rounds (2^12 = 4096 iterations) for security.
    
    Args:
        password: Plain text password
    
    Returns:
        str: bcrypt hash (60 characters)
    """
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: bcrypt hash to compare against
    
    Returns:
        bool: True if password matches
    """
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )
    except Exception:
        # Invalid hash format or other error
        return False


# ==============================================================================
# JWT Token Management
# ==============================================================================

def create_access_token(
    data: dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.
    
    Access tokens have a short lifetime (default: 15 minutes) and are
    used for API authentication.
    
    Args:
        data: Payload data to encode (must include "sub" for user ID)
        expires_delta: Optional custom expiration time
    
    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    
    to_encode.update({
        "exp": expire,
        "type": "access",
        "iat": datetime.utcnow(),
    })
    
    return jwt.encode(
        to_encode,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm
    )


def create_refresh_token(
    data: dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT refresh token.
    
    Refresh tokens have a longer lifetime (default: 7 days) and are
    used to obtain new access tokens without re-authentication.
    
    Args:
        data: Payload data to encode (must include "sub" for user ID)
        expires_delta: Optional custom expiration time
    
    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=settings.refresh_token_expire_days
        )
    
    to_encode.update({
        "exp": expire,
        "type": "refresh",
        "iat": datetime.utcnow(),
    })
    
    return jwt.encode(
        to_encode,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm
    )


def decode_token(token: str, token_type: str = "access") -> Optional[dict[str, Any]]:
    """
    Decode and validate a JWT token.
    
    Args:
        token: Encoded JWT token
        token_type: Expected token type ("access" or "refresh")
    
    Returns:
        dict: Decoded payload if valid, None if invalid
    
    Raises:
        None: Returns None on any validation error
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )
        
        # Verify token type
        if payload.get("type") != token_type:
            return None
        
        # Verify expiration (handled by jose, but double-check)
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
            return None
        
        return payload
    
    except JWTError:
        return None
    except Exception:
        return None


def get_user_id_from_token(token: str, token_type: str = "access") -> Optional[int]:
    """
    Extract user ID from a JWT token.
    
    Convenience function that decodes the token and extracts
    the "sub" claim as an integer user ID.
    
    Args:
        token: Encoded JWT token
        token_type: Expected token type ("access" or "refresh")
    
    Returns:
        int: User ID if valid, None if invalid
    """
    payload = decode_token(token, token_type)
    if payload is None:
        return None
    
    sub = payload.get("sub")
    if sub is None:
        return None
    
    try:
        return int(sub)
    except (ValueError, TypeError):
        return None


# ==============================================================================
# Password Validation
# ==============================================================================

def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    """
    Validate password meets strength requirements.
    
    Requirements:
    - Minimum 8 characters
    - At least 1 letter
    - At least 1 number
    
    Args:
        password: Password to validate
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    has_letter = any(c.isalpha() for c in password)
    has_number = any(c.isdigit() for c in password)
    
    if not has_letter:
        return False, "Password must contain at least one letter"
    
    if not has_number:
        return False, "Password must contain at least one number"
    
    return True, None
