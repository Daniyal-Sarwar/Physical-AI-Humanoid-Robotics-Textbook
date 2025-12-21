"""
Integration Tests for Registration Flow

Tests the complete user registration workflow:
- Register → Create Profile → Verify stored data
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.models.user import User
from src.models.user_profile import UserProfile


class TestRegistrationIntegration:
    """Integration tests for registration."""
    
    def test_registration_creates_user_in_db(
        self,
        client: TestClient,
        test_user_data: dict,
        db: Session
    ):
        """Registration should create user in database."""
        response = client.post("/api/v1/auth/register", json=test_user_data)
        
        assert response.status_code == 201
        
        # Verify in database
        user = db.query(User).filter(User.email == test_user_data["email"]).first()
        assert user is not None
        assert user.email == test_user_data["email"]
        assert user.password_hash != test_user_data["password"]  # Should be hashed
    
    def test_profile_creation_stores_data(
        self,
        client: TestClient,
        test_user_data: dict,
        test_profile_data: dict,
        db: Session
    ):
        """Profile creation should store data in database."""
        # Register
        client.post("/api/v1/auth/register", json=test_user_data)
        
        # Create profile
        response = client.post("/api/v1/user/profile", json=test_profile_data)
        assert response.status_code == 201
        
        # Verify in database
        user = db.query(User).filter(User.email == test_user_data["email"]).first()
        profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
        
        assert profile is not None
        assert profile.programming_level == test_profile_data["programming_level"]
        assert profile.robotics_familiarity == test_profile_data["robotics_familiarity"]
    
    def test_full_registration_with_all_profile_options(
        self,
        client: TestClient,
        test_user_data: dict
    ):
        """Test all valid profile enum combinations."""
        # Register
        client.post("/api/v1/auth/register", json=test_user_data)
        
        # Test each programming level
        for level in ["none", "beginner", "intermediate", "advanced"]:
            profile_data = {
                "programming_level": level,
                "robotics_familiarity": "hobbyist",
                "hardware_experience": "arduino",
                "learning_goal": "academic"
            }
            
            # Update profile
            response = client.put("/api/v1/user/profile", json=profile_data)
            
            # First time needs POST
            if response.status_code == 404:
                response = client.post("/api/v1/user/profile", json=profile_data)
            
            assert response.status_code in [200, 201]
            assert response.json()["programming_level"] == level
