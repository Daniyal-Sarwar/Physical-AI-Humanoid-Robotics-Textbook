"""
RateLimitRecord Model - Tracks anonymous user chatbot requests.

Implements sliding window rate limiting for anonymous users,
allowing 5 requests per 24-hour window.
"""

from datetime import datetime

from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class RateLimitRecord(Base):
    """
    Rate limit tracking for anonymous users.
    
    Tracks chatbot requests by browser fingerprint or IP address.
    Used to enforce 5 requests per 24-hour window for anonymous users.
    
    Attributes:
        id: Primary key
        identifier: Fingerprint hash or IP address
        request_count: Number of requests in current window
        window_start: Start of 24-hour window
        last_request: Timestamp of most recent request
    
    Cleanup Policy:
        Records older than 48 hours can be deleted (background job)
    """
    
    __tablename__ = "rate_limit_records"
    
    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Identifier (fingerprint hash or IP)
    identifier: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    
    # Rate limit tracking
    request_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    window_start: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    last_request: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    def __repr__(self) -> str:
        return f"<RateLimitRecord(id={self.id}, identifier={self.identifier[:8]}..., count={self.request_count})>"
    
    def is_window_expired(self, window_hours: int = 24) -> bool:
        """
        Check if the rate limit window has expired.
        
        Args:
            window_hours: Window duration in hours (default: 24)
        
        Returns:
            bool: True if window has expired
        """
        from datetime import timedelta
        window_duration = timedelta(hours=window_hours)
        return datetime.utcnow() > (self.window_start + window_duration)
    
    def reset_window(self) -> None:
        """Reset the rate limit window to now with count = 1."""
        self.window_start = datetime.utcnow()
        self.last_request = datetime.utcnow()
        self.request_count = 1
    
    def increment(self) -> int:
        """
        Increment the request count.
        
        Returns:
            int: Updated request count
        """
        self.request_count += 1
        self.last_request = datetime.utcnow()
        return self.request_count
    
    def get_reset_time(self, window_hours: int = 24) -> datetime:
        """
        Get the time when the rate limit window resets.
        
        Args:
            window_hours: Window duration in hours (default: 24)
        
        Returns:
            datetime: Reset timestamp
        """
        from datetime import timedelta
        return self.window_start + timedelta(hours=window_hours)
