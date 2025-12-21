"""
Rate Limit Routes - Endpoints for anonymous user rate limiting.

Provides rate limit status endpoint for anonymous users
to check their remaining chatbot requests.
"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Request, Header
from sqlalchemy.orm import Session

from src.config import settings
from src.database import get_db
from src.models.user import User
from src.models.rate_limit import RateLimitRecord
from src.schemas.auth import RateLimitStatus
from src.routes.auth import get_current_user_optional


router = APIRouter()


def get_identifier(request: Request, fingerprint: Optional[str] = None) -> str:
    """
    Get identifier for rate limiting.
    
    Uses browser fingerprint if provided, otherwise falls back to IP address.
    
    Args:
        request: FastAPI request
        fingerprint: Optional browser fingerprint from X-Fingerprint header
    
    Returns:
        str: Identifier for rate limiting
    """
    if fingerprint:
        return fingerprint
    
    # Fall back to IP address
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    
    return request.client.host if request.client else "unknown"


@router.get(
    "/status",
    response_model=RateLimitStatus,
)
async def get_rate_limit_status(
    request: Request,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
    x_fingerprint: Optional[str] = Header(default=None),
):
    """
    Get rate limit status for anonymous user.
    
    Returns remaining requests and reset time for anonymous users.
    Authenticated users are not rate limited (returns max values).
    """
    # Authenticated users have no rate limit
    if current_user is not None:
        return RateLimitStatus(
            remaining=settings.anonymous_rate_limit,
            total=settings.anonymous_rate_limit,
            reset_at=datetime.utcnow(),
            is_authenticated=True,
        )
    
    # Get identifier for anonymous user
    identifier = get_identifier(request, x_fingerprint)
    
    # Find existing rate limit record
    record = db.query(RateLimitRecord).filter(
        RateLimitRecord.identifier == identifier
    ).first()
    
    if record is None:
        # No record - user has full quota
        return RateLimitStatus(
            remaining=settings.anonymous_rate_limit,
            total=settings.anonymous_rate_limit,
            reset_at=datetime.utcnow(),
            is_authenticated=False,
        )
    
    # Check if window has expired
    if record.is_window_expired(settings.rate_limit_window_hours):
        # Window expired - user has full quota
        return RateLimitStatus(
            remaining=settings.anonymous_rate_limit,
            total=settings.anonymous_rate_limit,
            reset_at=datetime.utcnow(),
            is_authenticated=False,
        )
    
    # Calculate remaining requests
    remaining = max(0, settings.anonymous_rate_limit - record.request_count)
    reset_at = record.get_reset_time(settings.rate_limit_window_hours)
    
    return RateLimitStatus(
        remaining=remaining,
        total=settings.anonymous_rate_limit,
        reset_at=reset_at,
        is_authenticated=False,
    )
