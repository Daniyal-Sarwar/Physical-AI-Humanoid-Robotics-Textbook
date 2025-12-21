"""
Auth Service - Business logic for authentication.

Handles user authentication, token management, and account lockout.
"""

from datetime import datetime, timedelta
from typing import Optional, Tuple

from sqlalchemy.orm import Session

from src.config import settings
from src.models.user import User
from src.utils.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_user_id_from_token,
)


class AuthService:
    """
    Service for authentication operations.
    
    Handles login, token creation/validation, and account lockout.
    """
    
    # Lockout configuration
    MAX_FAILED_ATTEMPTS = 5
    LOCKOUT_DURATION_MINUTES = 15
    
    def __init__(self, db: Session):
        self.db = db
    
    def authenticate_user(
        self,
        email: str,
        password: str,
    ) -> Tuple[Optional[User], Optional[str]]:
        """
        Authenticate user with email and password.
        
        Args:
            email: User email
            password: Plain text password
        
        Returns:
            Tuple of (user, error_message) - user is None if auth failed
        """
        # Find user
        user = self.db.query(User).filter(User.email == email.lower()).first()
        
        if user is None:
            return None, "Invalid credentials"
        
        # Check if account is locked
        if self.is_account_locked(user):
            return None, f"Account locked until {user.locked_until.isoformat()}"
        
        # Verify password
        if not verify_password(password, user.password_hash):
            self._handle_failed_login(user)
            return None, "Invalid credentials"
        
        # Successful login - reset failed attempts
        self._handle_successful_login(user)
        
        return user, None
    
    def is_account_locked(self, user: User) -> bool:
        """
        Check if user account is locked.
        
        Args:
            user: User to check
        
        Returns:
            bool: True if account is locked
        """
        return user.is_locked
    
    def check_account_locked(self, user: User) -> Tuple[bool, Optional[datetime]]:
        """
        Check if account is locked and return unlock time.
        
        Args:
            user: User to check
        
        Returns:
            Tuple of (is_locked, locked_until)
        """
        if user.locked_until is None:
            return False, None
        
        if datetime.utcnow() >= user.locked_until:
            # Lock expired - clear it
            user.locked_until = None
            user.failed_attempts = 0
            self.db.commit()
            return False, None
        
        return True, user.locked_until
    
    def _handle_failed_login(self, user: User) -> None:
        """
        Handle a failed login attempt.
        
        Increments failed attempt counter and locks account if threshold reached.
        """
        user.failed_attempts += 1
        
        if user.failed_attempts >= self.MAX_FAILED_ATTEMPTS:
            user.locked_until = datetime.utcnow() + timedelta(
                minutes=self.LOCKOUT_DURATION_MINUTES
            )
        
        self.db.commit()
    
    def _handle_successful_login(self, user: User) -> None:
        """
        Handle a successful login.
        
        Resets failed attempt counter and updates last login.
        """
        user.failed_attempts = 0
        user.locked_until = None
        user.last_login = datetime.utcnow()
        self.db.commit()
    
    def create_tokens(self, user: User) -> Tuple[str, str]:
        """
        Create access and refresh tokens for user.
        
        Args:
            user: User to create tokens for
        
        Returns:
            Tuple of (access_token, refresh_token)
        """
        token_data = {"sub": str(user.id)}
        
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        
        return access_token, refresh_token
    
    def verify_access_token(self, token: str) -> Optional[int]:
        """
        Verify access token and return user ID.
        
        Args:
            token: JWT access token
        
        Returns:
            User ID if valid, None otherwise
        """
        return get_user_id_from_token(token, token_type="access")
    
    def verify_refresh_token(self, token: str) -> Optional[int]:
        """
        Verify refresh token and return user ID.
        
        Args:
            token: JWT refresh token
        
        Returns:
            User ID if valid, None otherwise
        """
        return get_user_id_from_token(token, token_type="refresh")
    
    def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        """
        Create new access token from refresh token.
        
        Args:
            refresh_token: Valid refresh token
        
        Returns:
            New access token if refresh token is valid, None otherwise
        """
        user_id = self.verify_refresh_token(refresh_token)
        if user_id is None:
            return None
        
        # Verify user still exists
        user = self.db.query(User).filter(User.id == user_id).first()
        if user is None:
            return None
        
        token_data = {"sub": str(user.id)}
        return create_access_token(token_data)
    
    def get_user_from_token(self, token: str, token_type: str = "access") -> Optional[User]:
        """
        Get user from JWT token.
        
        Args:
            token: JWT token
            token_type: Type of token ("access" or "refresh")
        
        Returns:
            User if token is valid, None otherwise
        """
        user_id = get_user_id_from_token(token, token_type)
        if user_id is None:
            return None
        
        return self.db.query(User).filter(User.id == user_id).first()
