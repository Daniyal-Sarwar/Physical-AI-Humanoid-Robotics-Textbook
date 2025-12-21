"""
Database Configuration and Session Management

Provides SQLite connection, session factory, and database initialization.
"""

import os
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session, declarative_base

from src.config import settings


# Ensure data directory exists
def ensure_data_directory() -> None:
    """Create the data directory if it doesn't exist."""
    # Extract path from sqlite:///./data/users.db format
    db_path = settings.sqlite_connection_string.replace("sqlite:///", "")
    data_dir = os.path.dirname(db_path)
    if data_dir:
        os.makedirs(data_dir, exist_ok=True)


# Create data directory
ensure_data_directory()

# SQLAlchemy base class for all models
Base = declarative_base()

# Create database engine
engine = create_engine(
    settings.sqlite_connection_string,
    connect_args={"check_same_thread": False},  # SQLite specific
    echo=settings.debug,  # Log SQL queries in debug mode
)


# Enable foreign key constraints for SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Enable foreign key support for SQLite."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """
    Initialize the database by creating all tables.
    
    Should be called once at application startup.
    """
    # Import all models to ensure they're registered with Base
    from src.models import User, UserProfile, RateLimitRecord, AuditLog
    
    # Create all tables
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Get a database session.
    
    Use as a FastAPI dependency:
        @app.get("/")
        def endpoint(db: Session = Depends(get_db)):
            ...
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context() -> Generator[Session, None, None]:
    """
    Context manager for database sessions.
    
    Use for non-FastAPI code:
        with get_db_context() as db:
            ...
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
