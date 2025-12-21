"""
UserProfile Model - Background information for personalization.

Stores questionnaire responses about user's programming level,
robotics familiarity, hardware experience, and learning goals.
"""

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base

if TYPE_CHECKING:
    from src.models.user import User


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
    ARDUINO = "arduino"  # Arduino/Raspberry Pi
    EMBEDDED = "embedded"  # Embedded Systems
    INDUSTRIAL = "industrial"


class LearningGoal(str, Enum):
    """User's primary learning objective."""
    CAREER_CHANGE = "career_change"
    ACADEMIC = "academic"
    HOBBY = "hobby"
    PROFESSIONAL_DEV = "professional_dev"


class UserProfile(Base):
    """
    User background profile for personalization.
    
    One-to-one relationship with User. Contains questionnaire
    responses used to personalize chatbot interactions.
    
    Attributes:
        id: Primary key
        user_id: Foreign key to users.id (unique, one-to-one)
        programming_level: Self-assessed programming skill
        robotics_familiarity: Experience with robotics
        hardware_experience: Electronics/hardware background
        learning_goal: Primary reason for learning
        updated_at: Last profile update timestamp
    
    Relationships:
        user: Many-to-one with User
    """
    
    __tablename__ = "user_profiles"
    
    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Foreign key - unique constraint enforces one-to-one
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True
    )
    
    # Questionnaire fields
    programming_level: Mapped[str] = mapped_column(String(20), nullable=False)
    robotics_familiarity: Mapped[str] = mapped_column(String(20), nullable=False)
    hardware_experience: Mapped[str] = mapped_column(String(20), nullable=False)
    learning_goal: Mapped[str] = mapped_column(String(30), nullable=False)
    
    # Timestamps
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="profile")
    
    def __repr__(self) -> str:
        return f"<UserProfile(id={self.id}, user_id={self.user_id})>"
    
    def update_timestamp(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()
