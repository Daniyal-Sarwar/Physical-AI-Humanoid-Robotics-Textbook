"""
User Schemas - Pydantic models for user profile request/response validation.

Defines the data contracts for user profile management including
questionnaire creation and updates.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ProgrammingLevel(str, Enum):
    """User's programming experience level."""
    NONE = "none"
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class RoboticsFamiliarity(str, Enum):
    """User's familiarity with robotics."""
    NONE = "none"
    HOBBYIST = "hobbyist"
    ACADEMIC = "academic"
    PROFESSIONAL = "professional"


class HardwareExperience(str, Enum):
    """User's hardware/electronics experience."""
    NONE = "none"
    ARDUINO = "arduino"
    EMBEDDED = "embedded"
    INDUSTRIAL = "industrial"


class LearningGoal(str, Enum):
    """User's primary learning objective."""
    CAREER_CHANGE = "career_change"
    ACADEMIC = "academic"
    HOBBY = "hobby"
    PROFESSIONAL_DEV = "professional_dev"


class ProfileRequest(BaseModel):
    """Request body for creating/updating user profile."""
    
    programming_level: ProgrammingLevel = Field(
        ...,
        description="Self-assessed programming skill level",
        examples=["intermediate"]
    )
    robotics_familiarity: RoboticsFamiliarity = Field(
        ...,
        description="Experience with robotics",
        examples=["hobbyist"]
    )
    hardware_experience: HardwareExperience = Field(
        ...,
        description="Electronics/hardware background",
        examples=["arduino"]
    )
    learning_goal: LearningGoal = Field(
        ...,
        description="Primary reason for learning",
        examples=["academic"]
    )


class ProfileResponse(BaseModel):
    """Response containing user profile information."""
    
    programming_level: str = Field(
        ...,
        description="Programming skill level",
        examples=["intermediate"]
    )
    robotics_familiarity: str = Field(
        ...,
        description="Robotics experience",
        examples=["hobbyist"]
    )
    hardware_experience: str = Field(
        ...,
        description="Hardware experience",
        examples=["arduino"]
    )
    learning_goal: str = Field(
        ...,
        description="Learning objective",
        examples=["academic"]
    )
    updated_at: datetime = Field(
        ...,
        description="Last profile update timestamp"
    )
    
    class Config:
        from_attributes = True


class UserBasic(BaseModel):
    """Basic user information."""
    
    id: int = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    created_at: datetime = Field(..., description="Account creation date")
    
    class Config:
        from_attributes = True


class UserWithProfile(BaseModel):
    """User information with optional profile."""
    
    id: int = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    created_at: datetime = Field(..., description="Account creation date")
    profile: Optional[ProfileResponse] = Field(
        None,
        description="User's background profile (if completed)"
    )
    
    class Config:
        from_attributes = True
