# Data Model: User Authentication & Rate-Limited Access

**Feature Branch**: `003-user-auth`  
**Date**: 2025-12-17  
**Database**: SQLite (`./data/users.db`)

## Entity Relationship Diagram

```
┌─────────────────┐       ┌─────────────────────┐
│      User       │       │     UserProfile     │
├─────────────────┤       ├─────────────────────┤
│ id (PK)         │──1:1──│ id (PK)             │
│ email (unique)  │       │ user_id (FK)        │
│ password_hash   │       │ programming_level   │
│ created_at      │       │ robotics_familiarity│
│ last_login      │       │ hardware_experience │
│ locked_until    │       │ learning_goal       │
│ failed_attempts │       │ updated_at          │
└────────┬────────┘       └─────────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────┐       ┌─────────────────────┐
│    AuditLog     │       │   RateLimitRecord   │
├─────────────────┤       ├─────────────────────┤
│ id (PK)         │       │ id (PK)             │
│ user_id (FK?)   │       │ identifier          │
│ event_type      │       │ request_count       │
│ ip_address      │       │ window_start        │
│ user_agent      │       │ last_request        │
│ details (JSON)  │       └─────────────────────┘
│ timestamp       │
└─────────────────┘
```

## Entity Definitions

### User

Primary account entity for registered users.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | INTEGER | PK, AUTO | Primary key |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | User email (login identifier) |
| `password_hash` | VARCHAR(72) | NOT NULL | bcrypt hash (60 chars + buffer) |
| `created_at` | DATETIME | NOT NULL, DEFAULT NOW | Account creation timestamp |
| `last_login` | DATETIME | NULL | Last successful login |
| `locked_until` | DATETIME | NULL | Account lockout expiry (NULL = not locked) |
| `failed_attempts` | INTEGER | NOT NULL, DEFAULT 0 | Consecutive failed login attempts |

**Indexes**:
- `ix_users_email` on `email` (unique)

**Validation Rules**:
- Email: Valid email format, max 255 chars
- Password (before hashing): Min 8 chars, at least 1 letter, at least 1 number

**State Transitions**:
```
[Created] → [Active] → [Locked] → [Active]
                ↓
           [Deleted] (future)
```

### UserProfile

Background information for personalization.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | INTEGER | PK, AUTO | Primary key |
| `user_id` | INTEGER | FK(users.id), UNIQUE, NOT NULL | One-to-one with User |
| `programming_level` | VARCHAR(20) | NOT NULL | Enum: none, beginner, intermediate, advanced |
| `robotics_familiarity` | VARCHAR(20) | NOT NULL | Enum: none, hobbyist, academic, professional |
| `hardware_experience` | VARCHAR(20) | NOT NULL | Enum: none, arduino, embedded, industrial |
| `learning_goal` | VARCHAR(30) | NOT NULL | Enum: career_change, academic, hobby, professional_dev |
| `updated_at` | DATETIME | NOT NULL, DEFAULT NOW | Last profile update |

**Indexes**:
- `ix_user_profiles_user_id` on `user_id` (unique)

**Enums**:
```python
class ProgrammingLevel(str, Enum):
    NONE = "none"
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class RoboticsFamiliarity(str, Enum):
    NONE = "none"
    HOBBYIST = "hobbyist"
    ACADEMIC = "academic"
    PROFESSIONAL = "professional"

class HardwareExperience(str, Enum):
    NONE = "none"
    ARDUINO = "arduino"  # Arduino/Raspberry Pi
    EMBEDDED = "embedded"  # Embedded Systems
    INDUSTRIAL = "industrial"

class LearningGoal(str, Enum):
    CAREER_CHANGE = "career_change"
    ACADEMIC = "academic"
    HOBBY = "hobby"
    PROFESSIONAL_DEV = "professional_dev"
```

### RateLimitRecord

Tracks anonymous user chatbot requests for rate limiting.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | INTEGER | PK, AUTO | Primary key |
| `identifier` | VARCHAR(64) | NOT NULL | Fingerprint hash or IP address |
| `request_count` | INTEGER | NOT NULL, DEFAULT 1 | Requests in current window |
| `window_start` | DATETIME | NOT NULL | Start of 24-hour window |
| `last_request` | DATETIME | NOT NULL | Last request timestamp |

**Indexes**:
- `ix_rate_limits_identifier` on `identifier`
- `ix_rate_limits_window_start` on `window_start` (for cleanup)

**Cleanup Policy**: Records older than 48 hours can be deleted (background job).

### AuditLog

Full audit trail of authentication events.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | INTEGER | PK, AUTO | Primary key |
| `user_id` | INTEGER | FK(users.id), NULL | User reference (NULL for anonymous events) |
| `event_type` | VARCHAR(30) | NOT NULL | Event type enum |
| `ip_address` | VARCHAR(45) | NULL | IPv4 or IPv6 address |
| `user_agent` | VARCHAR(500) | NULL | Browser user agent string |
| `details` | JSON | NULL | Additional event-specific data |
| `timestamp` | DATETIME | NOT NULL, DEFAULT NOW | Event timestamp |

**Indexes**:
- `ix_audit_logs_user_id` on `user_id`
- `ix_audit_logs_event_type` on `event_type`
- `ix_audit_logs_timestamp` on `timestamp`

**Event Types**:
```python
class AuditEventType(str, Enum):
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILED = "login_failed"
    LOGOUT = "logout"
    REGISTRATION = "registration"
    ACCOUNT_LOCKED = "account_locked"
    ACCOUNT_UNLOCKED = "account_unlocked"
    PROFILE_CREATED = "profile_created"
    PROFILE_UPDATED = "profile_updated"
    TOKEN_REFRESHED = "token_refreshed"
    PASSWORD_CHANGED = "password_changed"  # Future
```

## SQLAlchemy Models

```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(72), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    locked_until = Column(DateTime, nullable=True)
    failed_attempts = Column(Integer, nullable=False, default=0)
    
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    audit_logs = relationship("AuditLog", back_populates="user")

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    programming_level = Column(String(20), nullable=False)
    robotics_familiarity = Column(String(20), nullable=False)
    hardware_experience = Column(String(20), nullable=False)
    learning_goal = Column(String(30), nullable=False)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    user = relationship("User", back_populates="profile")

class RateLimitRecord(Base):
    __tablename__ = "rate_limit_records"
    
    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String(64), nullable=False, index=True)
    request_count = Column(Integer, nullable=False, default=1)
    window_start = Column(DateTime, nullable=False, index=True)
    last_request = Column(DateTime, nullable=False)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    event_type = Column(String(30), nullable=False, index=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    details = Column(JSON, nullable=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    user = relationship("User", back_populates="audit_logs")
```

## Database Initialization

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Ensure data directory exists
os.makedirs("./data", exist_ok=True)

DATABASE_URL = os.getenv("SQLITE_DB_PATH", "sqlite:///./data/users.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite specific
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency for FastAPI routes"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## Migration Notes

- Initial schema created via `Base.metadata.create_all()`
- For future migrations, consider Alembic if schema evolves
- SQLite supports ALTER TABLE for simple column additions
