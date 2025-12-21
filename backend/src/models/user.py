"""
User Model - Primary account entity for registered users.

Handles user authentication data including email, password hash,
account lockout, and failed login attempt tracking.
"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional, List

from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base

if TYPE_CHECKING:
    from src.models.user_profile import UserProfile
    from src.models.audit_log import AuditLog


class User(Base):
    """
    User account entity.
    
    Attributes:
        id: Primary key
        email: Unique email address (login identifier)
        password_hash: bcrypt hashed password (60+ chars)
        created_at: Account creation timestamp
        last_login: Last successful login timestamp
        locked_until: Account lockout expiry (NULL = not locked)
        failed_attempts: Consecutive failed login attempts
    
    Relationships:
        profile: One-to-one with UserProfile
        audit_logs: One-to-many with AuditLog
    
    State Transitions:
        [Created] → [Active] → [Locked] → [Active]
    """
    
    __tablename__ = "users"
    
    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Authentication fields
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(72), nullable=False)  # bcrypt = 60 chars + buffer
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Account lockout
    locked_until: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    failed_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    # Relationships
    profile: Mapped[Optional["UserProfile"]] = relationship(
        "UserProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    audit_logs: Mapped[List["AuditLog"]] = relationship(
        "AuditLog",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"
    
    @property
    def is_locked(self) -> bool:
        """Check if account is currently locked."""
        if self.locked_until is None:
            return False
        return datetime.utcnow() < self.locked_until
    
    def reset_failed_attempts(self) -> None:
        """Reset failed login attempts counter."""
        self.failed_attempts = 0
        self.locked_until = None
    
    def increment_failed_attempts(self) -> int:
        """
        Increment failed login attempts counter.
        
        Returns:
            int: Updated failed attempts count
        """
        self.failed_attempts += 1
        return self.failed_attempts
