"""
User Routes - Endpoints for user profile management.

Provides profile creation and update endpoints for the
background questionnaire.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.user import User
from src.models.user_profile import UserProfile
from src.schemas.auth import ErrorResponse
from src.schemas.user import ProfileRequest, ProfileResponse
from src.routes.auth import get_current_user, get_client_info
from src.utils.audit import log_profile_created, log_profile_updated


router = APIRouter()


@router.post(
    "/profile",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Validation error"},
        401: {"model": ErrorResponse, "description": "Not authenticated"},
        409: {"model": ErrorResponse, "description": "Profile already exists"},
    }
)
async def create_profile(
    data: ProfileRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create user profile (questionnaire).
    
    Save background questionnaire answers. Called after registration.
    User must be authenticated and not have an existing profile.
    """
    ip_address, user_agent = get_client_info(request)
    
    # Check if profile already exists
    if current_user.profile is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Profile already exists. Use PUT to update."
        )
    
    # Create profile
    profile = UserProfile(
        user_id=current_user.id,
        programming_level=data.programming_level.value,
        robotics_familiarity=data.robotics_familiarity.value,
        hardware_experience=data.hardware_experience.value,
        learning_goal=data.learning_goal.value,
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    
    # Log profile creation
    log_profile_created(
        db,
        user_id=current_user.id,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    
    return ProfileResponse.model_validate(profile)


@router.put(
    "/profile",
    response_model=ProfileResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Validation error"},
        401: {"model": ErrorResponse, "description": "Not authenticated"},
        404: {"model": ErrorResponse, "description": "Profile not found"},
    }
)
async def update_profile(
    data: ProfileRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update user profile.
    
    Update background questionnaire answers. User must have
    an existing profile.
    """
    ip_address, user_agent = get_client_info(request)
    
    # Get existing profile
    profile = current_user.profile
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Use POST to create."
        )
    
    # Track changes for audit log
    changes = {}
    if profile.programming_level != data.programming_level.value:
        changes["programming_level"] = {
            "from": profile.programming_level,
            "to": data.programming_level.value
        }
    if profile.robotics_familiarity != data.robotics_familiarity.value:
        changes["robotics_familiarity"] = {
            "from": profile.robotics_familiarity,
            "to": data.robotics_familiarity.value
        }
    if profile.hardware_experience != data.hardware_experience.value:
        changes["hardware_experience"] = {
            "from": profile.hardware_experience,
            "to": data.hardware_experience.value
        }
    if profile.learning_goal != data.learning_goal.value:
        changes["learning_goal"] = {
            "from": profile.learning_goal,
            "to": data.learning_goal.value
        }
    
    # Update profile
    profile.programming_level = data.programming_level.value
    profile.robotics_familiarity = data.robotics_familiarity.value
    profile.hardware_experience = data.hardware_experience.value
    profile.learning_goal = data.learning_goal.value
    profile.update_timestamp()
    
    db.commit()
    db.refresh(profile)
    
    # Log profile update (only if there were changes)
    if changes:
        log_profile_updated(
            db,
            user_id=current_user.id,
            changes=changes,
            ip_address=ip_address,
            user_agent=user_agent,
        )
    
    return ProfileResponse.model_validate(profile)


@router.get(
    "/profile",
    response_model=ProfileResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated"},
        404: {"model": ErrorResponse, "description": "Profile not found"},
    }
)
async def get_profile(
    current_user: User = Depends(get_current_user),
):
    """
    Get current user's profile.
    """
    if current_user.profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    return ProfileResponse.model_validate(current_user.profile)
