"""
Unit Tests for Auth Service

Tests the AuthService business logic including:
- User authentication
- Token creation and verification
- Account lockout
"""

import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.models.user import User
from src.services.auth_service import AuthService
from src.utils.security import hash_password


class TestAuthService:
    """Tests for AuthService."""
    
    @pytest.fixture
    def test_user(self, db: Session) -> User:
        """Create a test user."""
        user = User(
            email="auth@example.com",
            password_hash=hash_password("TestPass123")
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def test_authenticate_user_success(self, db: Session, test_user: User):
        """Should authenticate with valid credentials."""
        service = AuthService(db)
        
        user, error = service.authenticate_user(
            email="auth@example.com",
            password="TestPass123"
        )
        
        assert user is not None
        assert error is None
        assert user.id == test_user.id
    
    def test_authenticate_user_wrong_password(self, db: Session, test_user: User):
        """Should reject wrong password."""
        service = AuthService(db)
        
        user, error = service.authenticate_user(
            email="auth@example.com",
            password="WrongPass123"
        )
        
        assert user is None
        assert error == "Invalid credentials"
    
    def test_authenticate_user_wrong_email(self, db: Session, test_user: User):
        """Should reject wrong email."""
        service = AuthService(db)
        
        user, error = service.authenticate_user(
            email="wrong@example.com",
            password="TestPass123"
        )
        
        assert user is None
        assert error == "Invalid credentials"
    
    def test_authenticate_user_case_insensitive_email(self, db: Session, test_user: User):
        """Email should be case insensitive."""
        service = AuthService(db)
        
        user, error = service.authenticate_user(
            email="AUTH@EXAMPLE.COM",
            password="TestPass123"
        )
        
        assert user is not None
    
    def test_failed_login_increments_counter(self, db: Session, test_user: User):
        """Failed login should increment failed_attempts."""
        service = AuthService(db)
        
        # First failed attempt
        service.authenticate_user("auth@example.com", "wrong")
        
        db.refresh(test_user)
        assert test_user.failed_attempts == 1
        
        # Second failed attempt
        service.authenticate_user("auth@example.com", "wrong")
        
        db.refresh(test_user)
        assert test_user.failed_attempts == 2
    
    def test_successful_login_resets_counter(self, db: Session, test_user: User):
        """Successful login should reset failed_attempts."""
        service = AuthService(db)
        
        # Create some failed attempts
        test_user.failed_attempts = 3
        db.commit()
        
        # Successful login
        service.authenticate_user("auth@example.com", "TestPass123")
        
        db.refresh(test_user)
        assert test_user.failed_attempts == 0
    
    def test_account_locks_after_5_failures(self, db: Session, test_user: User):
        """Account should lock after 5 failed attempts."""
        service = AuthService(db)
        
        # Make 5 failed attempts
        for _ in range(5):
            service.authenticate_user("auth@example.com", "wrong")
        
        db.refresh(test_user)
        assert test_user.locked_until is not None
        assert test_user.failed_attempts == 5
    
    def test_locked_account_rejected(self, db: Session, test_user: User):
        """Locked account should be rejected even with correct password."""
        service = AuthService(db)
        
        # Lock the account
        test_user.locked_until = datetime.utcnow() + timedelta(minutes=15)
        db.commit()
        
        user, error = service.authenticate_user(
            "auth@example.com",
            "TestPass123"
        )
        
        assert user is None
        assert "locked" in error.lower()
    
    def test_is_account_locked(self, db: Session, test_user: User):
        """Should correctly detect locked accounts."""
        service = AuthService(db)
        
        assert service.is_account_locked(test_user) is False
        
        test_user.locked_until = datetime.utcnow() + timedelta(minutes=15)
        db.commit()
        
        assert service.is_account_locked(test_user) is True
    
    def test_create_tokens(self, db: Session, test_user: User):
        """Should create valid access and refresh tokens."""
        service = AuthService(db)
        
        access_token, refresh_token = service.create_tokens(test_user)
        
        assert access_token is not None
        assert refresh_token is not None
        assert access_token != refresh_token
    
    def test_verify_access_token(self, db: Session, test_user: User):
        """Should verify valid access token."""
        service = AuthService(db)
        
        access_token, _ = service.create_tokens(test_user)
        
        user_id = service.verify_access_token(access_token)
        
        assert user_id == test_user.id
    
    def test_verify_refresh_token(self, db: Session, test_user: User):
        """Should verify valid refresh token."""
        service = AuthService(db)
        
        _, refresh_token = service.create_tokens(test_user)
        
        user_id = service.verify_refresh_token(refresh_token)
        
        assert user_id == test_user.id
    
    def test_verify_invalid_token(self, db: Session):
        """Should reject invalid token."""
        service = AuthService(db)
        
        user_id = service.verify_access_token("invalid-token")
        
        assert user_id is None
    
    def test_refresh_access_token(self, db: Session, test_user: User):
        """Should create new access token from refresh token."""
        service = AuthService(db)
        
        _, refresh_token = service.create_tokens(test_user)
        
        new_access_token = service.refresh_access_token(refresh_token)
        
        assert new_access_token is not None
        
        # Verify the new token works
        user_id = service.verify_access_token(new_access_token)
        assert user_id == test_user.id
    
    def test_refresh_invalid_token(self, db: Session):
        """Should reject invalid refresh token."""
        service = AuthService(db)
        
        new_access_token = service.refresh_access_token("invalid-token")
        
        assert new_access_token is None
    
    def test_get_user_from_token(self, db: Session, test_user: User):
        """Should get user from valid token."""
        service = AuthService(db)
        
        access_token, _ = service.create_tokens(test_user)
        
        user = service.get_user_from_token(access_token)
        
        assert user is not None
        assert user.id == test_user.id
