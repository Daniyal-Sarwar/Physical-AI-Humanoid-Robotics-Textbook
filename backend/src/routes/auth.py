"""
Authentication Routes - Endpoints for user authentication.

Provides registration, login, logout, refresh, and user info endpoints.
JWT tokens are stored in HttpOnly cookies for XSS protection.
"""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response, Request, status, Cookie
from sqlalchemy.orm import Session

from src.config import settings
from src.database import get_db
from src.models.user import User
from src.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    AuthResponse,
    ErrorResponse,
    AccountLockedResponse,
    TokenRefreshResponse,
    LogoutResponse,
)
from src.schemas.user import UserBasic, UserWithProfile, ProfileResponse
from src.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_user_id_from_token,
)
from src.utils.audit import (
    log_registration,
    log_login_success,
    log_login_failed,
    log_logout,
    log_account_locked,
    log_token_refreshed,
)


router = APIRouter()


# ==============================================================================
# Cookie Configuration
# ==============================================================================

COOKIE_SETTINGS = {
    "httponly": True,
    "secure": settings.is_production,  # HTTPS only in production
    "samesite": "lax",
    "path": "/",
}


def set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    """Set authentication cookies on response."""
    # Access token - short lived (15 min)
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=settings.access_token_expire_minutes * 60,
        **COOKIE_SETTINGS
    )
    
    # Refresh token - long lived (7 days)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
        **COOKIE_SETTINGS
    )


def clear_auth_cookies(response: Response) -> None:
    """Clear authentication cookies on response."""
    response.delete_cookie(key="access_token", path="/")
    response.delete_cookie(key="refresh_token", path="/")


# ==============================================================================
# Authentication Dependencies
# ==============================================================================

def get_client_info(request: Request) -> tuple[Optional[str], Optional[str]]:
    """Extract client IP and user agent from request."""
    # Get IP address (handle proxies)
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        ip_address = forwarded.split(",")[0].strip()
    else:
        ip_address = request.client.host if request.client else None
    
    user_agent = request.headers.get("User-Agent")
    
    return ip_address, user_agent


async def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
    access_token: Optional[str] = Cookie(default=None),
) -> User:
    """
    Get current authenticated user from access token cookie.
    
    Raises:
        HTTPException: 401 if not authenticated or invalid token
    """
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    user_id = get_user_id_from_token(access_token, token_type="access")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user


async def get_current_user_optional(
    request: Request,
    db: Session = Depends(get_db),
    access_token: Optional[str] = Cookie(default=None),
) -> Optional[User]:
    """
    Get current user if authenticated, None otherwise.
    
    Does not raise exceptions - returns None for unauthenticated requests.
    """
    if not access_token:
        return None
    
    user_id = get_user_id_from_token(access_token, token_type="access")
    if user_id is None:
        return None
    
    return db.query(User).filter(User.id == user_id).first()


# ==============================================================================
# Endpoints
# ==============================================================================

@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Validation error"},
        409: {"model": ErrorResponse, "description": "Email already registered"},
    }
)
async def register_user(
    data: RegisterRequest,
    response: Response,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Register a new user account.
    
    Creates a new user with email and password. Returns JWT tokens
    in HttpOnly cookies.
    """
    ip_address, user_agent = get_client_info(request)
    
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    # Create user
    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Log registration event
    log_registration(
        db,
        user_id=user.id,
        email=user.email,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    
    # Create tokens
    token_data = {"sub": str(user.id)}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    # Set cookies
    set_auth_cookies(response, access_token, refresh_token)
    
    return AuthResponse(
        user=UserBasic.model_validate(user),
        message="Registration successful",
        has_profile=False,
    )


@router.post(
    "/login",
    response_model=AuthResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid credentials"},
        423: {"model": AccountLockedResponse, "description": "Account locked"},
    }
)
async def login_user(
    data: LoginRequest,
    response: Response,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Sign in with email and password.
    
    Authenticates user and returns JWT tokens in HttpOnly cookies.
    Account is locked after 5 failed attempts for 15 minutes.
    """
    ip_address, user_agent = get_client_info(request)
    
    # Find user
    user = db.query(User).filter(User.email == data.email).first()
    
    if not user:
        # Log failed attempt (user not found)
        log_login_failed(
            db,
            email=data.email,
            ip_address=ip_address,
            user_agent=user_agent,
            reason="user_not_found",
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Check if account is locked
    if user.is_locked:
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail=f"Account temporarily locked. Try again after {user.locked_until.isoformat()}"
        )
    
    # Verify password
    if not verify_password(data.password, user.password_hash):
        # Increment failed attempts
        failed_count = user.increment_failed_attempts()
        
        # Lock account after 5 failures
        if failed_count >= 5:
            user.locked_until = datetime.utcnow() + timedelta(minutes=15)
            log_account_locked(
                db,
                user_id=user.id,
                failed_attempts=failed_count,
                ip_address=ip_address,
                user_agent=user_agent,
            )
        
        db.commit()
        
        log_login_failed(
            db,
            email=data.email,
            ip_address=ip_address,
            user_agent=user_agent,
            reason="invalid_password",
        )
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Successful login - reset failed attempts
    user.reset_failed_attempts()
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Log successful login
    log_login_success(
        db,
        user_id=user.id,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    
    # Create tokens
    token_data = {"sub": str(user.id)}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    # Set cookies
    set_auth_cookies(response, access_token, refresh_token)
    
    return AuthResponse(
        user=UserBasic.model_validate(user),
        message="Login successful",
        has_profile=user.profile is not None,
    )


@router.post(
    "/logout",
    response_model=LogoutResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated"},
    }
)
async def logout_user(
    response: Response,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Sign out and terminate session.
    
    Clears authentication cookies and logs the logout event.
    """
    ip_address, user_agent = get_client_info(request)
    
    # Log logout event
    log_logout(
        db,
        user_id=current_user.id,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    
    # Clear cookies
    clear_auth_cookies(response)
    
    return LogoutResponse(message="Logged out successfully")


@router.post(
    "/refresh",
    response_model=TokenRefreshResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid or expired refresh token"},
    }
)
async def refresh_token(
    response: Response,
    request: Request,
    db: Session = Depends(get_db),
    refresh_token: Optional[str] = Cookie(default=None),
):
    """
    Refresh access token using refresh token.
    
    Called automatically by frontend when access token expires (401).
    """
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing"
        )
    
    user_id = get_user_id_from_token(refresh_token, token_type="refresh")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    ip_address, user_agent = get_client_info(request)
    
    # Log token refresh
    log_token_refreshed(
        db,
        user_id=user.id,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    
    # Create new access token only
    token_data = {"sub": str(user.id)}
    new_access_token = create_access_token(token_data)
    
    # Set new access token cookie
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        max_age=settings.access_token_expire_minutes * 60,
        **COOKIE_SETTINGS
    )
    
    return TokenRefreshResponse(message="Token refreshed")


@router.get(
    "/me",
    response_model=UserWithProfile,
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated"},
    }
)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    """
    Get current authenticated user's info and profile.
    """
    profile_response = None
    if current_user.profile:
        profile_response = ProfileResponse.model_validate(current_user.profile)
    
    return UserWithProfile(
        id=current_user.id,
        email=current_user.email,
        created_at=current_user.created_at,
        profile=profile_response,
    )
