"""
Rate Limit Service - Business logic for anonymous user rate limiting.

Implements sliding window rate limiting for anonymous chatbot users.
"""

from datetime import datetime
from typing import Optional, Tuple

from sqlalchemy.orm import Session

from src.config import settings
from src.models.rate_limit import RateLimitRecord


class RateLimitService:
    """
    Service for managing rate limits on anonymous users.
    
    Implements a sliding window counter algorithm with:
    - 5 requests per 24-hour window (configurable)
    - Browser fingerprint or IP address as identifier
    - Automatic window reset after expiry
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.max_requests = settings.anonymous_rate_limit
        self.window_hours = settings.rate_limit_window_hours
    
    def get_or_create_record(self, identifier: str) -> RateLimitRecord:
        """
        Get existing rate limit record or create new one.
        
        Args:
            identifier: Browser fingerprint or IP address
        
        Returns:
            RateLimitRecord: Rate limit record for identifier
        """
        record = self.db.query(RateLimitRecord).filter(
            RateLimitRecord.identifier == identifier
        ).first()
        
        if record is None:
            record = RateLimitRecord(
                identifier=identifier,
                request_count=0,
                window_start=datetime.utcnow(),
                last_request=datetime.utcnow(),
            )
            self.db.add(record)
            self.db.commit()
            self.db.refresh(record)
        
        return record
    
    def check_rate_limit(self, identifier: str) -> Tuple[bool, int, datetime]:
        """
        Check if request is allowed under rate limit.
        
        Args:
            identifier: Browser fingerprint or IP address
        
        Returns:
            Tuple of (is_allowed, remaining_requests, reset_time)
        """
        record = self.get_or_create_record(identifier)
        
        # Check if window has expired
        if record.is_window_expired(self.window_hours):
            # Reset window
            record.reset_window()
            self.db.commit()
            
            remaining = self.max_requests - 1  # Account for current request
            reset_at = record.get_reset_time(self.window_hours)
            return True, remaining, reset_at
        
        # Check if under limit
        remaining = self.max_requests - record.request_count
        reset_at = record.get_reset_time(self.window_hours)
        
        if remaining > 0:
            return True, remaining - 1, reset_at  # Account for current request
        else:
            return False, 0, reset_at
    
    def record_request(self, identifier: str) -> Tuple[bool, int, datetime]:
        """
        Record a request and check rate limit.
        
        This method atomically checks the limit and records the request.
        Use this when actually making a chatbot request.
        
        Args:
            identifier: Browser fingerprint or IP address
        
        Returns:
            Tuple of (is_allowed, remaining_requests, reset_time)
        """
        record = self.get_or_create_record(identifier)
        
        # Check if window has expired
        if record.is_window_expired(self.window_hours):
            record.reset_window()
            self.db.commit()
            
            remaining = self.max_requests - 1
            reset_at = record.get_reset_time(self.window_hours)
            return True, remaining, reset_at
        
        # Check if under limit
        if record.request_count >= self.max_requests:
            reset_at = record.get_reset_time(self.window_hours)
            return False, 0, reset_at
        
        # Increment counter
        record.increment()
        self.db.commit()
        
        remaining = max(0, self.max_requests - record.request_count)
        reset_at = record.get_reset_time(self.window_hours)
        
        return True, remaining, reset_at
    
    def get_status(self, identifier: str) -> Tuple[int, int, datetime]:
        """
        Get current rate limit status without recording a request.
        
        Args:
            identifier: Browser fingerprint or IP address
        
        Returns:
            Tuple of (remaining_requests, total_requests, reset_time)
        """
        record = self.db.query(RateLimitRecord).filter(
            RateLimitRecord.identifier == identifier
        ).first()
        
        if record is None:
            return self.max_requests, self.max_requests, datetime.utcnow()
        
        if record.is_window_expired(self.window_hours):
            return self.max_requests, self.max_requests, datetime.utcnow()
        
        remaining = max(0, self.max_requests - record.request_count)
        reset_at = record.get_reset_time(self.window_hours)
        
        return remaining, self.max_requests, reset_at
    
    def reset_limit(self, identifier: str) -> None:
        """
        Reset rate limit for an identifier (admin function).
        
        Args:
            identifier: Browser fingerprint or IP address
        """
        record = self.db.query(RateLimitRecord).filter(
            RateLimitRecord.identifier == identifier
        ).first()
        
        if record:
            record.reset_window()
            record.request_count = 0
            self.db.commit()
    
    def cleanup_expired(self, hours: int = 48) -> int:
        """
        Delete expired rate limit records (cleanup job).
        
        Args:
            hours: Delete records older than this many hours
        
        Returns:
            int: Number of records deleted
        """
        from datetime import timedelta
        
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        
        deleted = self.db.query(RateLimitRecord).filter(
            RateLimitRecord.window_start < cutoff
        ).delete()
        
        self.db.commit()
        
        return deleted
