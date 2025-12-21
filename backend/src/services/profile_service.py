"""
Profile Service - Business logic for user profile management.

Handles profile creation, retrieval, and updates.
"""

from typing import Optional, Tuple

from sqlalchemy.orm import Session

from src.models.user import User
from src.models.user_profile import UserProfile
from src.schemas.user import ProfileRequest


class ProfileService:
    """
    Service for managing user profiles.
    
    Provides methods for creating and updating background questionnaire data.
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_profile(
        self,
        user: User,
        data: ProfileRequest,
    ) -> Tuple[Optional[UserProfile], Optional[str]]:
        """
        Create a new user profile.
        
        Args:
            user: User to create profile for
            data: Profile data from questionnaire
        
        Returns:
            Tuple of (profile, error_message) - profile is None if creation failed
        """
        # Check if profile already exists
        if user.profile is not None:
            return None, "Profile already exists"
        
        # Create profile
        profile = UserProfile(
            user_id=user.id,
            programming_level=data.programming_level.value,
            robotics_familiarity=data.robotics_familiarity.value,
            hardware_experience=data.hardware_experience.value,
            learning_goal=data.learning_goal.value,
        )
        
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        
        return profile, None
    
    def get_profile(self, user: User) -> Optional[UserProfile]:
        """
        Get user's profile.
        
        Args:
            user: User to get profile for
        
        Returns:
            UserProfile if exists, None otherwise
        """
        return user.profile
    
    def get_profile_by_user_id(self, user_id: int) -> Optional[UserProfile]:
        """
        Get profile by user ID.
        
        Args:
            user_id: User ID
        
        Returns:
            UserProfile if exists, None otherwise
        """
        return self.db.query(UserProfile).filter(
            UserProfile.user_id == user_id
        ).first()
    
    def update_profile(
        self,
        user: User,
        data: ProfileRequest,
    ) -> Tuple[Optional[UserProfile], Optional[str], dict]:
        """
        Update user's profile.
        
        Args:
            user: User to update profile for
            data: Updated profile data
        
        Returns:
            Tuple of (profile, error_message, changes_dict)
        """
        profile = user.profile
        
        if profile is None:
            return None, "Profile not found", {}
        
        # Track changes
        changes = {}
        
        if profile.programming_level != data.programming_level.value:
            changes["programming_level"] = {
                "from": profile.programming_level,
                "to": data.programming_level.value
            }
            profile.programming_level = data.programming_level.value
        
        if profile.robotics_familiarity != data.robotics_familiarity.value:
            changes["robotics_familiarity"] = {
                "from": profile.robotics_familiarity,
                "to": data.robotics_familiarity.value
            }
            profile.robotics_familiarity = data.robotics_familiarity.value
        
        if profile.hardware_experience != data.hardware_experience.value:
            changes["hardware_experience"] = {
                "from": profile.hardware_experience,
                "to": data.hardware_experience.value
            }
            profile.hardware_experience = data.hardware_experience.value
        
        if profile.learning_goal != data.learning_goal.value:
            changes["learning_goal"] = {
                "from": profile.learning_goal,
                "to": data.learning_goal.value
            }
            profile.learning_goal = data.learning_goal.value
        
        if changes:
            profile.update_timestamp()
        
        self.db.commit()
        self.db.refresh(profile)
        
        return profile, None, changes
