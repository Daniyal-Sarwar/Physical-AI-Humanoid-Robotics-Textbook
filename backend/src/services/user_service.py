"""
User Service - Business logic for user account management.

Handles user creation, retrieval, and password validation.
"""

import re
from typing import Optional, Tuple

from sqlalchemy.orm import Session

from src.models.user import User
from src.utils.security import hash_password, validate_password_strength


class UserService:
    """
    Service for managing user accounts.
    
    Provides methods for user creation, retrieval, and validation.
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, email: str, password: str) -> Tuple[Optional[User], Optional[str]]:
        """
        Create a new user account.
        
        Args:
            email: User email address
            password: Plain text password
        
        Returns:
            Tuple of (user, error_message) - user is None if creation failed
        """
        # Validate email format
        email = email.lower().strip()
        if not self._is_valid_email(email):
            return None, "Invalid email format"
        
        # Check if email exists
        if self.get_user_by_email(email) is not None:
            return None, "Email already registered"
        
        # Validate password strength
        is_valid, error = validate_password_strength(password)
        if not is_valid:
            return None, error
        
        # Create user
        user = User(
            email=email,
            password_hash=hash_password(password),
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user, None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email address.
        
        Args:
            email: User email address
        
        Returns:
            User if found, None otherwise
        """
        email = email.lower().strip()
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
        
        Returns:
            User if found, None otherwise
        """
        return self.db.query(User).filter(User.id == user_id).first()
    
    def _is_valid_email(self, email: str) -> bool:
        """
        Validate email format.
        
        Args:
            email: Email address to validate
        
        Returns:
            bool: True if valid email format
        """
        # Basic email regex pattern
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def update_last_login(self, user: User) -> None:
        """
        Update user's last login timestamp.
        
        Args:
            user: User to update
        """
        from datetime import datetime
        user.last_login = datetime.utcnow()
        self.db.commit()
