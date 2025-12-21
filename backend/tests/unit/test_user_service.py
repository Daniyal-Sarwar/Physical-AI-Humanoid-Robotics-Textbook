"""
Unit Tests for User Service

Tests the UserService business logic including:
- User creation
- Email validation
- Password validation
"""

import pytest
from sqlalchemy.orm import Session

from src.models.user import User
from src.services.user_service import UserService


class TestUserService:
    """Tests for UserService."""
    
    def test_create_user_success(self, db: Session):
        """Should create user with valid data."""
        service = UserService(db)
        
        user, error = service.create_user(
            email="test@example.com",
            password="ValidPass123"
        )
        
        assert user is not None
        assert error is None
        assert user.email == "test@example.com"
        assert user.id is not None
    
    def test_create_user_email_normalized(self, db: Session):
        """Email should be lowercased and trimmed."""
        service = UserService(db)
        
        user, error = service.create_user(
            email="  TEST@Example.COM  ",
            password="ValidPass123"
        )
        
        assert user is not None
        assert user.email == "test@example.com"
    
    def test_create_user_duplicate_email(self, db: Session):
        """Should reject duplicate email."""
        service = UserService(db)
        
        # Create first user
        user1, _ = service.create_user(
            email="test@example.com",
            password="ValidPass123"
        )
        assert user1 is not None
        
        # Try to create duplicate
        user2, error = service.create_user(
            email="test@example.com",
            password="DifferentPass123"
        )
        
        assert user2 is None
        assert error == "Email already registered"
    
    def test_create_user_invalid_email(self, db: Session):
        """Should reject invalid email format."""
        service = UserService(db)
        
        user, error = service.create_user(
            email="not-an-email",
            password="ValidPass123"
        )
        
        assert user is None
        assert error == "Invalid email format"
    
    def test_create_user_password_too_short(self, db: Session):
        """Should reject password shorter than 8 chars."""
        service = UserService(db)
        
        user, error = service.create_user(
            email="test@example.com",
            password="Short1"
        )
        
        assert user is None
        assert "at least 8 characters" in error
    
    def test_create_user_password_no_letter(self, db: Session):
        """Should reject password without letters."""
        service = UserService(db)
        
        user, error = service.create_user(
            email="test@example.com",
            password="12345678"
        )
        
        assert user is None
        assert "letter" in error.lower()
    
    def test_create_user_password_no_number(self, db: Session):
        """Should reject password without numbers."""
        service = UserService(db)
        
        user, error = service.create_user(
            email="test@example.com",
            password="NoNumbers"
        )
        
        assert user is None
        assert "number" in error.lower()
    
    def test_get_user_by_email(self, db: Session):
        """Should find user by email."""
        service = UserService(db)
        
        # Create user
        service.create_user(
            email="find@example.com",
            password="FindMe123"
        )
        
        # Find user
        user = service.get_user_by_email("find@example.com")
        
        assert user is not None
        assert user.email == "find@example.com"
    
    def test_get_user_by_email_not_found(self, db: Session):
        """Should return None for non-existent email."""
        service = UserService(db)
        
        user = service.get_user_by_email("nonexistent@example.com")
        
        assert user is None
    
    def test_get_user_by_email_case_insensitive(self, db: Session):
        """Email lookup should be case insensitive."""
        service = UserService(db)
        
        # Create user
        service.create_user(
            email="test@example.com",
            password="TestPass123"
        )
        
        # Find with different case
        user = service.get_user_by_email("TEST@EXAMPLE.COM")
        
        assert user is not None
        assert user.email == "test@example.com"
    
    def test_get_user_by_id(self, db: Session):
        """Should find user by ID."""
        service = UserService(db)
        
        # Create user
        created_user, _ = service.create_user(
            email="test@example.com",
            password="TestPass123"
        )
        
        # Find by ID
        user = service.get_user_by_id(created_user.id)
        
        assert user is not None
        assert user.email == "test@example.com"
    
    def test_get_user_by_id_not_found(self, db: Session):
        """Should return None for non-existent ID."""
        service = UserService(db)
        
        user = service.get_user_by_id(99999)
        
        assert user is None
    
    def test_password_is_hashed(self, db: Session):
        """Password should be hashed, not stored in plain text."""
        service = UserService(db)
        
        user, _ = service.create_user(
            email="test@example.com",
            password="SecretPass123"
        )
        
        assert user.password_hash != "SecretPass123"
        assert user.password_hash.startswith("$2b$")  # bcrypt prefix
