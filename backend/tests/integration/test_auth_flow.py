"""
Integration Tests for Authentication Flow

Tests the complete authentication workflows:
- Registration → Login → Logout
- Login lockout after failed attempts
- Token refresh flow
"""

import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.models.user import User
from src.utils.security import hash_password


class TestRegistrationFlow:
    """Integration tests for registration flow."""
    
    def test_complete_registration_flow(
        self,
        client: TestClient,
        test_user_data: dict,
        test_profile_data: dict
    ):
        """Test complete: Register → Create Profile → Get User."""
        # Step 1: Register
        register_response = client.post(
            "/api/v1/auth/register",
            json=test_user_data
        )
        assert register_response.status_code == 201
        assert register_response.json()["has_profile"] is False
        
        # Step 2: Create profile
        profile_response = client.post(
            "/api/v1/user/profile",
            json=test_profile_data
        )
        assert profile_response.status_code == 201
        
        # Step 3: Get user with profile
        me_response = client.get("/api/v1/auth/me")
        assert me_response.status_code == 200
        
        user_data = me_response.json()
        assert user_data["email"] == test_user_data["email"]
        assert user_data["profile"] is not None
        assert user_data["profile"]["programming_level"] == test_profile_data["programming_level"]


class TestLoginFlow:
    """Integration tests for login flow."""
    
    def test_complete_login_logout_flow(
        self,
        client: TestClient,
        test_user_data: dict
    ):
        """Test complete: Register → Logout → Login → Get User."""
        # Register
        client.post("/api/v1/auth/register", json=test_user_data)
        
        # Logout
        logout_response = client.post("/api/v1/auth/logout")
        assert logout_response.status_code == 200
        
        # Should be logged out now
        me_response = client.get("/api/v1/auth/me")
        assert me_response.status_code == 401
        
        # Login again
        login_response = client.post("/api/v1/auth/login", json=test_user_data)
        assert login_response.status_code == 200
        
        # Should be logged in
        me_response = client.get("/api/v1/auth/me")
        assert me_response.status_code == 200


class TestAccountLockout:
    """Integration tests for account lockout."""
    
    def test_lockout_after_5_failed_attempts(
        self,
        client: TestClient,
        db: Session
    ):
        """Account should lock after 5 failed login attempts."""
        # Create user directly
        user = User(
            email="lockout@example.com",
            password_hash=hash_password("CorrectPass123")
        )
        db.add(user)
        db.commit()
        
        # Make 5 failed attempts
        for i in range(5):
            response = client.post("/api/v1/auth/login", json={
                "email": "lockout@example.com",
                "password": "WrongPass123"
            })
            assert response.status_code == 401, f"Attempt {i+1} should fail"
        
        # 6th attempt should show locked
        response = client.post("/api/v1/auth/login", json={
            "email": "lockout@example.com",
            "password": "CorrectPass123"  # Even correct password
        })
        
        assert response.status_code == 423  # Locked
    
    def test_correct_password_resets_counter(
        self,
        client: TestClient,
        db: Session
    ):
        """Correct password should reset failed attempts counter."""
        # Create user
        user = User(
            email="reset@example.com",
            password_hash=hash_password("CorrectPass123")
        )
        db.add(user)
        db.commit()
        
        # Make 3 failed attempts
        for _ in range(3):
            client.post("/api/v1/auth/login", json={
                "email": "reset@example.com",
                "password": "WrongPass123"
            })
        
        # Successful login
        response = client.post("/api/v1/auth/login", json={
            "email": "reset@example.com",
            "password": "CorrectPass123"
        })
        assert response.status_code == 200
        
        # Verify counter reset
        db.refresh(user)
        assert user.failed_attempts == 0


class TestTokenRefreshFlow:
    """Integration tests for token refresh."""
    
    def test_refresh_token_flow(
        self,
        client: TestClient,
        test_user_data: dict
    ):
        """Test token refresh flow."""
        # Register (gets both tokens)
        register_response = client.post(
            "/api/v1/auth/register",
            json=test_user_data
        )
        refresh_token = register_response.cookies.get("refresh_token")
        
        # Clear access token (simulate expiry)
        client.cookies.delete("access_token")
        
        # Should fail now
        me_response = client.get("/api/v1/auth/me")
        assert me_response.status_code == 401
        
        # Refresh
        client.cookies.set("refresh_token", refresh_token)
        refresh_response = client.post("/api/v1/auth/refresh")
        assert refresh_response.status_code == 200
        
        # Should work now
        me_response = client.get("/api/v1/auth/me")
        assert me_response.status_code == 200


class TestAuthFlow:
    """General authentication flow tests."""
    
    def test_cookies_are_httponly(
        self,
        client: TestClient,
        test_user_data: dict
    ):
        """Auth cookies should be HttpOnly."""
        response = client.post("/api/v1/auth/register", json=test_user_data)
        
        # Check Set-Cookie headers for HttpOnly
        # Use get_list() for httpx compatibility
        set_cookie_headers = response.headers.get_list("set-cookie")
        
        for header in set_cookie_headers:
            if "access_token" in header or "refresh_token" in header:
                assert "httponly" in header.lower()
