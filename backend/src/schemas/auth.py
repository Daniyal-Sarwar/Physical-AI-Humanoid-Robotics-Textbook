"""
Authentication Schemas - Pydantic models for auth request/response validation.

Defines the data contracts for authentication endpoints including
registration, login, and rate limiting.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class RegisterRequest(BaseModel):
    """Request body for user registration."""
    
    email: EmailStr = Field(
        ...,
        description="User email address (used as login identifier)",
        max_length=255,
        examples=["student@university.edu"]
    )
    password: str = Field(
        ...,
        min_length=8,
        description="Password (min 8 chars, at least 1 letter and 1 number)",
        examples=["SecurePass123"]
    )
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password meets strength requirements."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isalpha() for c in v):
            raise ValueError("Password must contain at least one letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        return v


class LoginRequest(BaseModel):
    """Request body for user login."""
    
    email: EmailStr = Field(
        ...,
        description="User email address",
        examples=["student@university.edu"]
    )
    password: str = Field(
        ...,
        description="User password",
        examples=["SecurePass123"]
    )


class UserBasic(BaseModel):
    """Basic user information (public-safe)."""
    
    id: int = Field(..., description="User ID", examples=[1])
    email: str = Field(..., description="User email", examples=["student@university.edu"])
    created_at: datetime = Field(..., description="Account creation date")
    
    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    """Response for successful authentication (register/login)."""
    
    user: UserBasic = Field(..., description="User information")
    message: str = Field(..., description="Success message", examples=["Registration successful"])
    has_profile: bool = Field(
        False,
        description="Whether user has completed the background questionnaire"
    )


class ErrorResponse(BaseModel):
    """Standard error response format."""
    
    error: str = Field(..., description="Error type", examples=["Invalid credentials"])
    detail: Optional[str] = Field(
        None,
        description="Detailed error message",
        examples=["The email or password you entered is incorrect"]
    )
    code: int = Field(..., description="HTTP status code", examples=[401])


class AccountLockedResponse(BaseModel):
    """Response when account is locked due to failed attempts."""
    
    error: str = Field(
        "Account temporarily locked",
        description="Error message"
    )
    detail: str = Field(
        ...,
        description="Detailed explanation",
        examples=["Too many failed login attempts. Try again in 15 minutes."]
    )
    locked_until: datetime = Field(..., description="When the account will be unlocked")
    code: int = Field(423, description="HTTP status code")


class RateLimitStatus(BaseModel):
    """Rate limit status for anonymous users."""
    
    remaining: int = Field(
        ...,
        ge=0,
        le=5,
        description="Remaining requests in current window",
        examples=[3]
    )
    total: int = Field(
        5,
        description="Maximum requests per window",
        examples=[5]
    )
    reset_at: datetime = Field(
        ...,
        description="When the rate limit window resets"
    )
    is_authenticated: bool = Field(
        False,
        description="Always false for this endpoint (auth users have no limit)"
    )


class TokenRefreshResponse(BaseModel):
    """Response for successful token refresh."""
    
    message: str = Field("Token refreshed", description="Success message")


class LogoutResponse(BaseModel):
    """Response for successful logout."""
    
    message: str = Field("Logged out successfully", description="Success message")
