"""
AuditLog Model - Full audit trail of authentication events.

Records all authentication-related events including logins,
failed attempts, account lockouts, and profile changes.
"""

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional, Any, Dict

from sqlalchemy import Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base

if TYPE_CHECKING:
    from src.models.user import User


class AuditEventType(str, Enum):
    """Types of auditable authentication events."""
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILED = "login_failed"
    LOGOUT = "logout"
    REGISTRATION = "registration"
    ACCOUNT_LOCKED = "account_locked"
    ACCOUNT_UNLOCKED = "account_unlocked"
    PROFILE_CREATED = "profile_created"
    PROFILE_UPDATED = "profile_updated"
    TOKEN_REFRESHED = "token_refreshed"
    PASSWORD_CHANGED = "password_changed"  # Future


class AuditLog(Base):
    """
    Audit log entry for authentication events.
    
    Records all authentication-related events with user context,
    client information, and event-specific details.
    
    Attributes:
        id: Primary key
        user_id: Foreign key to users.id (NULL for anonymous events)
        event_type: Type of event from AuditEventType enum
        ip_address: Client IP address (IPv4 or IPv6)
        user_agent: Browser user agent string
        details: JSON object with event-specific data
        timestamp: Event timestamp
    
    Relationships:
        user: Many-to-one with User (optional)
    """
    
    __tablename__ = "audit_logs"
    
    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # User reference (optional - NULL for anonymous events)
    user_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    # Event information
    event_type: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)  # IPv6 max length
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    details: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    
    # Timestamp
    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True
    )
    
    # Relationships
    user: Mapped[Optional["User"]] = relationship("User", back_populates="audit_logs")
    
    def __repr__(self) -> str:
        user_info = f"user_id={self.user_id}" if self.user_id else "anonymous"
        return f"<AuditLog(id={self.id}, {user_info}, event={self.event_type})>"
    
    @classmethod
    def create(
        cls,
        event_type: AuditEventType,
        user_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
    ) -> "AuditLog":
        """
        Create a new audit log entry.
        
        Args:
            event_type: Type of event
            user_id: User ID (optional)
            ip_address: Client IP address
            user_agent: Browser user agent
            details: Additional event details
        
        Returns:
            AuditLog: New audit log instance
        """
        return cls(
            event_type=event_type.value,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details,
        )
