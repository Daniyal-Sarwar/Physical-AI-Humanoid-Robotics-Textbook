"""
Contract Tests for User Profile API

Tests the user profile endpoints against the OpenAPI contract:
- POST /api/v1/user/profile
- PUT /api/v1/user/profile
- GET /api/v1/user/profile
"""

import pytest
from fastapi.testclient import TestClient


class TestCreateProfileEndpoint:
    """Contract tests for POST /api/v1/user/profile."""
    
    def test_create_profile_returns_201(
        self,
        authenticated_client: TestClient,
        test_profile_data: dict
    ):
        """Successful profile creation should return 201."""
        response = authenticated_client.post(
            "/api/v1/user/profile",
            json=test_profile_data
        )
        assert response.status_code == 201
    
    def test_create_profile_response_schema(
        self,
        authenticated_client: TestClient,
        test_profile_data: dict
    ):
        """Response should match ProfileResponse schema."""
        response = authenticated_client.post(
            "/api/v1/user/profile",
            json=test_profile_data
        )
        data = response.json()
        
        assert "programming_level" in data
        assert "robotics_familiarity" in data
        assert "hardware_experience" in data
        assert "learning_goal" in data
        assert "updated_at" in data
    
    def test_create_profile_duplicate_409(
        self,
        authenticated_client: TestClient,
        test_profile_data: dict
    ):
        """Creating duplicate profile should return 409."""
        # Create first
        authenticated_client.post("/api/v1/user/profile", json=test_profile_data)
        
        # Try duplicate
        response = authenticated_client.post(
            "/api/v1/user/profile",
            json=test_profile_data
        )
        
        assert response.status_code == 409
    
    def test_create_profile_unauthenticated_401(
        self,
        client: TestClient,
        test_profile_data: dict
    ):
        """Unauthenticated request should return 401."""
        response = client.post("/api/v1/user/profile", json=test_profile_data)
        assert response.status_code == 401
    
    def test_create_profile_invalid_enum_422(
        self,
        authenticated_client: TestClient
    ):
        """Invalid enum value should return 422."""
        response = authenticated_client.post("/api/v1/user/profile", json={
            "programming_level": "invalid_value",
            "robotics_familiarity": "hobbyist",
            "hardware_experience": "arduino",
            "learning_goal": "academic"
        })
        
        assert response.status_code == 422


class TestUpdateProfileEndpoint:
    """Contract tests for PUT /api/v1/user/profile."""
    
    def test_update_profile_returns_200(
        self,
        authenticated_client: TestClient,
        test_profile_data: dict
    ):
        """Successful update should return 200."""
        # Create profile first
        authenticated_client.post("/api/v1/user/profile", json=test_profile_data)
        
        # Update
        updated_data = test_profile_data.copy()
        updated_data["programming_level"] = "advanced"
        
        response = authenticated_client.put(
            "/api/v1/user/profile",
            json=updated_data
        )
        
        assert response.status_code == 200
    
    def test_update_profile_response_schema(
        self,
        authenticated_client: TestClient,
        test_profile_data: dict
    ):
        """Response should match ProfileResponse schema."""
        authenticated_client.post("/api/v1/user/profile", json=test_profile_data)
        
        response = authenticated_client.put(
            "/api/v1/user/profile",
            json=test_profile_data
        )
        data = response.json()
        
        assert "programming_level" in data
        assert "updated_at" in data
    
    def test_update_profile_no_profile_404(
        self,
        authenticated_client: TestClient,
        test_profile_data: dict
    ):
        """Update without existing profile should return 404."""
        response = authenticated_client.put(
            "/api/v1/user/profile",
            json=test_profile_data
        )
        
        assert response.status_code == 404
    
    def test_update_profile_unauthenticated_401(
        self,
        client: TestClient,
        test_profile_data: dict
    ):
        """Unauthenticated request should return 401."""
        response = client.put("/api/v1/user/profile", json=test_profile_data)
        assert response.status_code == 401


class TestGetProfileEndpoint:
    """Contract tests for GET /api/v1/user/profile."""
    
    def test_get_profile_returns_200(
        self,
        authenticated_client: TestClient,
        test_profile_data: dict
    ):
        """Successful get should return 200."""
        authenticated_client.post("/api/v1/user/profile", json=test_profile_data)
        
        response = authenticated_client.get("/api/v1/user/profile")
        
        assert response.status_code == 200
    
    def test_get_profile_response_schema(
        self,
        authenticated_client: TestClient,
        test_profile_data: dict
    ):
        """Response should match ProfileResponse schema."""
        authenticated_client.post("/api/v1/user/profile", json=test_profile_data)
        
        response = authenticated_client.get("/api/v1/user/profile")
        data = response.json()
        
        assert data["programming_level"] == test_profile_data["programming_level"]
        assert data["robotics_familiarity"] == test_profile_data["robotics_familiarity"]
    
    def test_get_profile_no_profile_404(
        self,
        authenticated_client: TestClient
    ):
        """Get without profile should return 404."""
        response = authenticated_client.get("/api/v1/user/profile")
        assert response.status_code == 404
    
    def test_get_profile_unauthenticated_401(self, client: TestClient):
        """Unauthenticated request should return 401."""
        response = client.get("/api/v1/user/profile")
        assert response.status_code == 401
