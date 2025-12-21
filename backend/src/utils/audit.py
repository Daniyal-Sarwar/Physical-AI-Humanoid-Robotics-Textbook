"""
Audit Logging Utilities - Helper functions for audit trail.

Provides convenient functions to log authentication events
to the AuditLog table.
"""

from typing import Optional, Any

from sqlalchemy.orm import Session

from src.models.audit_log import AuditLog, AuditEventType


def log_event(
    db: Session,
    event_type: AuditEventType,
    user_id: Optional[int] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    details: Optional[dict[str, Any]] = None,
    commit: bool = True,
) -> AuditLog:
    """
    Log an audit event to the database.
    
    Args:
        db: Database session
        event_type: Type of event to log
        user_id: User ID (optional, NULL for anonymous events)
        ip_address: Client IP address
        user_agent: Browser user agent string
        details: Additional event-specific details (JSON)
        commit: Whether to commit the transaction (default: True)
    
    Returns:
        AuditLog: Created audit log entry
    
    Example:
        log_event(
            db,
            AuditEventType.LOGIN_SUCCESS,
            user_id=1,
            ip_address="192.168.1.1",
            user_agent="Mozilla/5.0...",
            details={"method": "password"}
        )
    """
    audit_log = AuditLog.create(
        event_type=event_type,
        user_id=user_id,
        ip_address=ip_address,
        user_agent=user_agent,
        details=details,
    )
    
    db.add(audit_log)
    
    if commit:
        db.commit()
        db.refresh(audit_log)
    
    return audit_log


def log_login_success(
    db: Session,
    user_id: int,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> AuditLog:
    """Log a successful login event."""
    return log_event(
        db,
        AuditEventType.LOGIN_SUCCESS,
        user_id=user_id,
        ip_address=ip_address,
        user_agent=user_agent,
    )


def log_login_failed(
    db: Session,
    email: str,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    reason: str = "invalid_credentials",
) -> AuditLog:
    """Log a failed login attempt."""
    return log_event(
        db,
        AuditEventType.LOGIN_FAILED,
        ip_address=ip_address,
        user_agent=user_agent,
        details={"email": email, "reason": reason},
    )


def log_logout(
    db: Session,
    user_id: int,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> AuditLog:
    """Log a logout event."""
    return log_event(
        db,
        AuditEventType.LOGOUT,
        user_id=user_id,
        ip_address=ip_address,
        user_agent=user_agent,
    )


def log_registration(
    db: Session,
    user_id: int,
    email: str,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> AuditLog:
    """Log a new user registration."""
    return log_event(
        db,
        AuditEventType.REGISTRATION,
        user_id=user_id,
        ip_address=ip_address,
        user_agent=user_agent,
        details={"email": email},
    )


def log_account_locked(
    db: Session,
    user_id: int,
    failed_attempts: int,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> AuditLog:
    """Log an account lockout event."""
    return log_event(
        db,
        AuditEventType.ACCOUNT_LOCKED,
        user_id=user_id,
        ip_address=ip_address,
        user_agent=user_agent,
        details={"failed_attempts": failed_attempts},
    )


def log_profile_created(
    db: Session,
    user_id: int,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> AuditLog:
    """Log a profile creation event."""
    return log_event(
        db,
        AuditEventType.PROFILE_CREATED,
        user_id=user_id,
        ip_address=ip_address,
        user_agent=user_agent,
    )


def log_profile_updated(
    db: Session,
    user_id: int,
    changes: dict[str, Any],
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> AuditLog:
    """Log a profile update event."""
    return log_event(
        db,
        AuditEventType.PROFILE_UPDATED,
        user_id=user_id,
        ip_address=ip_address,
        user_agent=user_agent,
        details={"changes": changes},
    )


def log_token_refreshed(
    db: Session,
    user_id: int,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> AuditLog:
    """Log a token refresh event."""
    return log_event(
        db,
        AuditEventType.TOKEN_REFRESHED,
        user_id=user_id,
        ip_address=ip_address,
        user_agent=user_agent,
    )
