"""
Unit Tests for Rate Limit Service

Tests the RateLimitService business logic including:
- Rate limit checking
- Request recording
- Window expiry and reset
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import patch

from sqlalchemy.orm import Session

from src.models.rate_limit import RateLimitRecord
from src.services.rate_limit import RateLimitService


class TestRateLimitService:
    """Tests for RateLimitService."""
    
    def test_check_rate_limit_new_user(self, db: Session):
        """New users should have full quota."""
        service = RateLimitService(db)
        
        is_allowed, remaining, reset_at = service.check_rate_limit("new-user-123")
        
        assert is_allowed is True
        assert remaining == 4  # 5 - 1 for current request
    
    def test_check_rate_limit_under_limit(self, db: Session):
        """Users under limit should be allowed."""
        service = RateLimitService(db)
        identifier = "under-limit-user"
        
        # Record some requests
        for _ in range(3):
            service.record_request(identifier)
        
        # Check limit
        is_allowed, remaining, reset_at = service.check_rate_limit(identifier)
        
        assert is_allowed is True
        assert remaining == 1  # 5 - 3 - 1 for current
    
    def test_check_rate_limit_at_limit(self, db: Session):
        """Users at limit should be blocked."""
        service = RateLimitService(db)
        identifier = "at-limit-user"
        
        # Use up all requests
        for _ in range(5):
            service.record_request(identifier)
        
        # Check limit
        is_allowed, remaining, reset_at = service.check_rate_limit(identifier)
        
        assert is_allowed is False
        assert remaining == 0
    
    def test_record_request_increments_count(self, db: Session):
        """Recording a request should increment the counter."""
        service = RateLimitService(db)
        identifier = "increment-test"
        
        # First request
        is_allowed1, remaining1, _ = service.record_request(identifier)
        assert is_allowed1 is True
        assert remaining1 == 4
        
        # Second request
        is_allowed2, remaining2, _ = service.record_request(identifier)
        assert is_allowed2 is True
        assert remaining2 == 3
    
    def test_record_request_blocks_after_limit(self, db: Session):
        """Recording should be blocked after limit is reached."""
        service = RateLimitService(db)
        identifier = "block-test"
        
        # Use up all requests
        for i in range(5):
            is_allowed, remaining, _ = service.record_request(identifier)
            assert is_allowed is True
        
        # Next request should be blocked
        is_allowed, remaining, _ = service.record_request(identifier)
        assert is_allowed is False
        assert remaining == 0
    
    def test_window_expiry_resets_count(self, db: Session):
        """Expired window should reset the count."""
        service = RateLimitService(db)
        identifier = "expiry-test"
        
        # Create a record with old window
        record = RateLimitRecord(
            identifier=identifier,
            request_count=5,
            window_start=datetime.utcnow() - timedelta(hours=25),
            last_request=datetime.utcnow() - timedelta(hours=25),
        )
        db.add(record)
        db.commit()
        
        # Check limit - should be reset
        is_allowed, remaining, _ = service.check_rate_limit(identifier)
        
        assert is_allowed is True
        assert remaining == 4  # Fresh window
    
    def test_get_status_without_record(self, db: Session):
        """Status for new user should show full quota."""
        service = RateLimitService(db)
        
        remaining, total, reset_at = service.get_status("no-record-user")
        
        assert remaining == 5
        assert total == 5
    
    def test_get_status_with_usage(self, db: Session):
        """Status should reflect current usage."""
        service = RateLimitService(db)
        identifier = "status-test"
        
        # Use some requests
        for _ in range(2):
            service.record_request(identifier)
        
        remaining, total, reset_at = service.get_status(identifier)
        
        assert remaining == 3
        assert total == 5
    
    def test_reset_limit(self, db: Session):
        """Admin reset should clear the count."""
        service = RateLimitService(db)
        identifier = "reset-test"
        
        # Use up all requests
        for _ in range(5):
            service.record_request(identifier)
        
        # Reset
        service.reset_limit(identifier)
        
        # Check status
        remaining, total, reset_at = service.get_status(identifier)
        
        assert remaining == 5
    
    def test_cleanup_expired_records(self, db: Session):
        """Cleanup should remove old records."""
        service = RateLimitService(db)
        
        # Create old records
        old_record = RateLimitRecord(
            identifier="old-record",
            request_count=3,
            window_start=datetime.utcnow() - timedelta(hours=72),
            last_request=datetime.utcnow() - timedelta(hours=72),
        )
        db.add(old_record)
        
        # Create recent record
        recent_record = RateLimitRecord(
            identifier="recent-record",
            request_count=2,
            window_start=datetime.utcnow() - timedelta(hours=12),
            last_request=datetime.utcnow() - timedelta(hours=12),
        )
        db.add(recent_record)
        db.commit()
        
        # Cleanup
        deleted = service.cleanup_expired(hours=48)
        
        assert deleted == 1
        
        # Verify recent record still exists
        remaining, _, _ = service.get_status("recent-record")
        assert remaining == 3  # 5 - 2
