"""
Contract Tests for Authentication API

Tests the auth endpoints against the OpenAPI contract:
- POST /api/v1/auth/register
- POST /api/v1/auth/login
- POST /api/v1/auth/logout
- POST /api/v1/auth/refresh
- GET /api/v1/auth/me
"""

import pytest
from fastapi.testclient import TestClient


class TestRegisterEndpoint:
    """Contract tests for POST /api/v1/auth/register."""
    
    def test_register_returns_201(self, client: TestClient, test_user_data: dict):
        """Successful registration should return 201."""
        response = client.post("/api/v1/auth/register", json=test_user_data)
        assert response.status_code == 201
    
    def test_register_response_schema(self, client: TestClient, test_user_data: dict):
        """Response should match AuthResponse schema."""
        response = client.post("/api/v1/auth/register", json=test_user_data)
        data = response.json()
        
        # Required fields
        assert "user" in data
        assert "message" in data
        assert "has_profile" in data
        
        # User fields
        assert "id" in data["user"]
        assert "email" in data["user"]
        assert "created_at" in data["user"]
        
        assert data["has_profile"] is False
    
    def test_register_sets_cookies(self, client: TestClient, test_user_data: dict):
        """Registration should set auth cookies."""
        response = client.post("/api/v1/auth/register", json=test_user_data)
        
        assert "access_token" in response.cookies
        assert "refresh_token" in response.cookies
    
    def test_register_duplicate_email_409(self, client: TestClient, test_user_data: dict):
        """Duplicate email should return 409."""
        # First registration
        client.post("/api/v1/auth/register", json=test_user_data)
        
        # Duplicate
        response = client.post("/api/v1/auth/register", json=test_user_data)
        
        assert response.status_code == 409
    
    def test_register_invalid_email_400(self, client: TestClient):
        """Invalid email should return 400."""
        response = client.post("/api/v1/auth/register", json={
            "email": "not-an-email",
            "password": "ValidPass123"
        })
        
        assert response.status_code == 422  # Pydantic validation error
    
    def test_register_weak_password_400(self, client: TestClient):
        """Weak password should return 400/422."""
        response = client.post("/api/v1/auth/register", json={
            "email": "test@example.com",
            "password": "weak"
        })
        
        assert response.status_code == 422


class TestLoginEndpoint:
    """Contract tests for POST /api/v1/auth/login."""
    
    def test_login_returns_200(
        self,
        client: TestClient,
        test_user_data: dict
    ):
        """Successful login should return 200."""
        # Register first
        client.post("/api/v1/auth/register", json=test_user_data)
        
        # Login
        response = client.post("/api/v1/auth/login", json=test_user_data)
        
        assert response.status_code == 200
    
    def test_login_response_schema(
        self,
        client: TestClient,
        test_user_data: dict
    ):
        """Response should match AuthResponse schema."""
        client.post("/api/v1/auth/register", json=test_user_data)
        response = client.post("/api/v1/auth/login", json=test_user_data)
        data = response.json()
        
        assert "user" in data
        assert "message" in data
        assert "has_profile" in data
    
    def test_login_sets_cookies(
        self,
        client: TestClient,
        test_user_data: dict
    ):
        """Login should set auth cookies."""
        client.post("/api/v1/auth/register", json=test_user_data)
        response = client.post("/api/v1/auth/login", json=test_user_data)
        
        assert "access_token" in response.cookies
        assert "refresh_token" in response.cookies
    
    def test_login_invalid_credentials_401(self, client: TestClient, test_user_data: dict):
        """Invalid credentials should return 401."""
        client.post("/api/v1/auth/register", json=test_user_data)
        
        response = client.post("/api/v1/auth/login", json={
            "email": test_user_data["email"],
            "password": "WrongPassword123"
        })
        
        assert response.status_code == 401
    
    def test_login_nonexistent_user_401(self, client: TestClient):
        """Non-existent user should return 401."""
        response = client.post("/api/v1/auth/login", json={
            "email": "nonexistent@example.com",
            "password": "SomePass123"
        })
        
        assert response.status_code == 401


class TestLogoutEndpoint:
    """Contract tests for POST /api/v1/auth/logout."""
    
    def test_logout_returns_200(self, authenticated_client: TestClient):
        """Successful logout should return 200."""
        response = authenticated_client.post("/api/v1/auth/logout")
        assert response.status_code == 200
    
    def test_logout_response_schema(self, authenticated_client: TestClient):
        """Response should contain message."""
        response = authenticated_client.post("/api/v1/auth/logout")
        data = response.json()
        
        assert "message" in data
    
    def test_logout_unauthenticated_401(self, client: TestClient):
        """Unauthenticated logout should return 401."""
        response = client.post("/api/v1/auth/logout")
        assert response.status_code == 401


class TestRefreshEndpoint:
    """Contract tests for POST /api/v1/auth/refresh."""
    
    def test_refresh_returns_200(
        self,
        client: TestClient,
        registered_user: dict
    ):
        """Successful refresh should return 200."""
        # Use refresh token
        client.cookies.set("refresh_token", registered_user["cookies"]["refresh_token"])
        
        response = client.post("/api/v1/auth/refresh")
        
        assert response.status_code == 200
    
    def test_refresh_response_schema(
        self,
        client: TestClient,
        registered_user: dict
    ):
        """Response should contain message."""
        client.cookies.set("refresh_token", registered_user["cookies"]["refresh_token"])
        
        response = client.post("/api/v1/auth/refresh")
        data = response.json()
        
        assert "message" in data
    
    def test_refresh_no_token_401(self, client: TestClient):
        """Missing refresh token should return 401."""
        response = client.post("/api/v1/auth/refresh")
        assert response.status_code == 401
    
    def test_refresh_invalid_token_401(self, client: TestClient):
        """Invalid refresh token should return 401."""
        client.cookies.set("refresh_token", "invalid-token")
        
        response = client.post("/api/v1/auth/refresh")
        
        assert response.status_code == 401


class TestMeEndpoint:
    """Contract tests for GET /api/v1/auth/me."""
    
    def test_me_returns_200(self, authenticated_client: TestClient):
        """Authenticated user should get 200."""
        response = authenticated_client.get("/api/v1/auth/me")
        assert response.status_code == 200
    
    def test_me_response_schema(self, authenticated_client: TestClient):
        """Response should match UserWithProfile schema."""
        response = authenticated_client.get("/api/v1/auth/me")
        data = response.json()
        
        assert "id" in data
        assert "email" in data
        assert "created_at" in data
        assert "profile" in data  # Can be null
    
    def test_me_unauthenticated_401(self, client: TestClient):
        """Unauthenticated request should return 401."""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401
    
    def test_me_with_profile(self, user_with_profile: dict):
        """User with profile should have profile in response."""
        assert user_with_profile["profile"] is not None
        assert "programming_level" in user_with_profile["profile"]
