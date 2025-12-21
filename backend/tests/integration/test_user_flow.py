"""
Integration Tests for User Profile Flow

Tests the complete profile management workflow:
- Create profile → Update profile → Verify changes
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class TestProfileIntegration:
    """Integration tests for profile management."""
    
    def test_profile_update_changes_values(
        self,
        authenticated_client: TestClient,
        test_profile_data: dict
    ):
        """Profile update should change stored values."""
        # Create profile
        authenticated_client.post("/api/v1/user/profile", json=test_profile_data)
        
        # Update with new values
        updated_data = {
            "programming_level": "advanced",
            "robotics_familiarity": "professional",
            "hardware_experience": "industrial",
            "learning_goal": "professional_dev"
        }
        
        response = authenticated_client.put(
            "/api/v1/user/profile",
            json=updated_data
        )
        
        assert response.status_code == 200
        assert response.json()["programming_level"] == "advanced"
        assert response.json()["robotics_familiarity"] == "professional"
        
        # Verify persisted
        get_response = authenticated_client.get("/api/v1/user/profile")
        assert get_response.json()["programming_level"] == "advanced"
    
    def test_profile_accessible_via_me_endpoint(
        self,
        authenticated_client: TestClient,
        test_profile_data: dict
    ):
        """Profile should be accessible via /auth/me endpoint."""
        # Create profile
        authenticated_client.post("/api/v1/user/profile", json=test_profile_data)
        
        # Get via /auth/me
        response = authenticated_client.get("/api/v1/auth/me")
        
        assert response.status_code == 200
        assert response.json()["profile"] is not None
        assert response.json()["profile"]["programming_level"] == test_profile_data["programming_level"]
    
    def test_profile_update_updates_timestamp(
        self,
        authenticated_client: TestClient,
        test_profile_data: dict
    ):
        """Profile update should update the updated_at timestamp."""
        # Create profile
        create_response = authenticated_client.post(
            "/api/v1/user/profile",
            json=test_profile_data
        )
        original_timestamp = create_response.json()["updated_at"]
        
        # Update with different values
        updated_data = test_profile_data.copy()
        updated_data["programming_level"] = "advanced"
        
        import time
        time.sleep(0.1)  # Small delay to ensure timestamp changes
        
        update_response = authenticated_client.put(
            "/api/v1/user/profile",
            json=updated_data
        )
        
        new_timestamp = update_response.json()["updated_at"]
        
        # Timestamps should be different
        assert new_timestamp != original_timestamp
