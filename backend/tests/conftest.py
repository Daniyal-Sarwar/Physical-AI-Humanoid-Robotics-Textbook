"""
Pytest Configuration and Fixtures

Provides test database setup, client fixtures, and helper utilities
for testing the authentication API.
"""

import os
import pytest
from typing import Generator, Any

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

# Set test environment before importing app
os.environ["ENVIRONMENT"] = "test"
os.environ["JWT_SECRET"] = "test-secret-key-for-jwt-tokens-min-32-chars"
os.environ["SESSION_SECRET"] = "test-session-secret-key-min-32-chars"
os.environ["SQLITE_DB_PATH"] = "sqlite:///:memory:"
os.environ["DEBUG"] = "true"

from src.database import Base, get_db
from src.main import app


# ==============================================================================
# Test Database Setup
# ==============================================================================

# Create in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Use same connection for all threads
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


def override_get_db() -> Generator[Session, None, None]:
    """Override database dependency for testing."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override the get_db dependency
app.dependency_overrides[get_db] = override_get_db


# ==============================================================================
# Fixtures
# ==============================================================================

@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """
    Create a fresh database for each test.
    
    Creates all tables, yields a session, then drops all tables.
    """
    # Create all tables
    Base.metadata.create_all(bind=test_engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    """
    Create a test client with database session.
    
    Ensures database is initialized before each test.
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def test_user_data() -> dict[str, str]:
    """Sample user data for registration tests."""
    return {
        "email": "test@example.com",
        "password": "TestPass123"
    }


@pytest.fixture
def test_profile_data() -> dict[str, str]:
    """Sample profile data for questionnaire tests."""
    return {
        "programming_level": "intermediate",
        "robotics_familiarity": "hobbyist",
        "hardware_experience": "arduino",
        "learning_goal": "academic"
    }


@pytest.fixture
def registered_user(client: TestClient, test_user_data: dict) -> dict[str, Any]:
    """
    Create a registered user and return user data with cookies.
    
    Returns:
        dict with 'user' data and 'cookies' for authentication
    """
    response = client.post("/api/v1/auth/register", json=test_user_data)
    assert response.status_code == 201
    
    return {
        "user": response.json()["user"],
        "cookies": response.cookies,
        "credentials": test_user_data
    }


@pytest.fixture
def authenticated_client(
    client: TestClient,
    registered_user: dict
) -> TestClient:
    """
    Return a client with authentication cookies set.
    """
    # Copy cookies to client
    for name, value in registered_user["cookies"].items():
        client.cookies.set(name, value)
    
    return client


@pytest.fixture
def user_with_profile(
    authenticated_client: TestClient,
    test_profile_data: dict
) -> dict[str, Any]:
    """
    Create a user with completed profile.
    
    Returns:
        dict with user and profile data
    """
    # Create profile
    response = authenticated_client.post(
        "/api/v1/user/profile",
        json=test_profile_data
    )
    assert response.status_code == 201
    
    # Get user info
    user_response = authenticated_client.get("/api/v1/auth/me")
    assert user_response.status_code == 200
    
    return user_response.json()


# ==============================================================================
# Helper Functions
# ==============================================================================

def create_test_user(
    db: Session,
    email: str = "test@example.com",
    password: str = "TestPass123"
) -> Any:
    """
    Create a test user directly in the database.
    
    Args:
        db: Database session
        email: User email
        password: Plain text password
    
    Returns:
        User model instance
    """
    from src.models.user import User
    from src.utils.security import hash_password
    
    user = User(
        email=email,
        password_hash=hash_password(password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


def get_auth_headers(access_token: str) -> dict[str, str]:
    """
    Create authorization headers with access token.
    
    Note: We use cookies in production, but this helper is for
    cases where header-based auth is needed.
    """
    return {"Authorization": f"Bearer {access_token}"}
