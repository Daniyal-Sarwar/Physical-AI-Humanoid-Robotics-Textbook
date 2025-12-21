# Research: User Authentication & Rate-Limited Access

**Feature Branch**: `003-user-auth`  
**Date**: 2025-12-17  
**Status**: Complete

## Research Tasks

### 1. JWT Authentication with HttpOnly Cookies (FastAPI)

**Decision**: Use `python-jose` for JWT encoding/decoding with HttpOnly cookie storage

**Rationale**:
- `python-jose` is battle-tested, well-maintained, and recommended by FastAPI docs
- HttpOnly cookies prevent XSS attacks (JavaScript cannot access token)
- Cookies are automatically sent with requests (no manual header management)
- FastAPI's `Response.set_cookie()` makes implementation straightforward

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| localStorage | Vulnerable to XSS attacks |
| Session-based auth | More server state to manage, less scalable |
| OAuth2 password flow (Bearer) | Requires frontend to manage tokens, XSS risk |

**Implementation Pattern**:
```python
from jose import jwt
from fastapi import Response

# On login success
response.set_cookie(
    key="access_token",
    value=f"Bearer {token}",
    httponly=True,
    secure=True,  # HTTPS only
    samesite="lax",
    max_age=7 * 24 * 60 * 60  # 7 days
)
```

### 2. Password Hashing with bcrypt

**Decision**: Use `bcrypt` library with 12 rounds (work factor)

**Rationale**:
- bcrypt is industry standard for password hashing
- 12 rounds provides good security/performance balance (~300ms hash time)
- Built-in salt generation (no separate salt storage needed)
- Constitution mandates bcrypt (Principle X)

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| Argon2 | More complex setup, bcrypt is sufficient for < 100 users |
| PBKDF2 | Less resistant to GPU attacks than bcrypt |
| SHA-256 + salt | Not designed for passwords, too fast |

**Implementation Pattern**:
```python
import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(12)).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())
```

### 3. SQLite for User Storage

**Decision**: Use SQLite with SQLAlchemy ORM

**Rationale**:
- Pilot scale (< 100 users) - SQLite is more than sufficient
- Zero deployment complexity (single file database)
- SQLAlchemy provides ORM and migration support
- Avoids external database dependencies

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| PostgreSQL | Overkill for < 100 users, deployment complexity |
| Raw SQL | Loses ORM benefits, harder to maintain |
| JSON file | No ACID, no query capabilities |

**Implementation Pattern**:
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./data/users.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
```

### 4. Rate Limiting Strategy

**Decision**: Sliding window counter with browser fingerprint + IP fallback

**Rationale**:
- Sliding window is more accurate than fixed window
- Browser fingerprint (via cookie) provides user-specific tracking
- IP fallback handles cookie-cleared scenarios
- Simple to implement with SQLite

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| Redis-based | Adds external dependency for simple use case |
| Token bucket | More complex, not needed for simple 5/24h limit |
| IP-only | Users behind NAT would share limits unfairly |

**Implementation Pattern**:
```python
def check_rate_limit(identifier: str) -> tuple[bool, int]:
    """Returns (allowed: bool, remaining: int)"""
    window_start = datetime.utcnow() - timedelta(hours=24)
    count = db.query(RateLimitRecord).filter(
        RateLimitRecord.identifier == identifier,
        RateLimitRecord.timestamp >= window_start
    ).count()
    return (count < 5, max(0, 5 - count))
```

### 5. Silent Token Refresh Strategy

**Decision**: Dual-token approach with short-lived access token + long-lived refresh token

**Rationale**:
- Access token expires in 15 minutes (limits exposure)
- Refresh token valid for 7 days (stored in separate HttpOnly cookie)
- Frontend interceptor handles 401 → refresh → retry automatically
- Revocation possible by invalidating refresh token in DB

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| Single long-lived token | Higher security risk if compromised |
| Session-based refresh | Requires server-side session state |
| Manual refresh | Poor UX, user sees logout unexpectedly |

**Implementation Pattern**:
```python
# Two cookies set on login
response.set_cookie("access_token", access_jwt, max_age=15*60)  # 15 min
response.set_cookie("refresh_token", refresh_jwt, max_age=7*24*60*60)  # 7 days
```

### 6. Audit Logging Strategy

**Decision**: Structured JSON logging to SQLite + file rotation

**Rationale**:
- Full audit trail required per FR-023
- SQLite table for queryable logs
- JSON format for structured data (IP, user agent, details)
- File backup for debugging

**Events to Log**:
- `LOGIN_SUCCESS`, `LOGIN_FAILED`, `LOGOUT`
- `ACCOUNT_LOCKED`, `ACCOUNT_UNLOCKED`
- `REGISTRATION`, `PROFILE_UPDATED`
- `TOKEN_REFRESHED`, `TOKEN_REVOKED`

**Implementation Pattern**:
```python
class AuditLog(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    event_type = Column(String(50), nullable=False)
    ip_address = Column(String(45))  # IPv6 length
    user_agent = Column(String(500))
    details = Column(JSON)  # Flexible additional data
    timestamp = Column(DateTime, default=datetime.utcnow)
```

## Dependencies Finalized

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | ^0.109.0 | Web framework |
| python-jose[cryptography] | ^3.3.0 | JWT encoding/decoding |
| bcrypt | ^4.1.0 | Password hashing |
| sqlalchemy | ^2.0.0 | ORM for SQLite |
| pydantic | ^2.5.0 | Request/response validation |
| uvicorn | ^0.27.0 | ASGI server |

## Security Checklist

- [x] Passwords hashed with bcrypt (12 rounds)
- [x] JWT stored in HttpOnly cookies
- [x] HTTPS enforced (Secure cookie flag)
- [x] SameSite=Lax to prevent CSRF
- [x] Account lockout after 5 failed attempts
- [x] Full audit logging enabled
- [x] Input validation via Pydantic
- [x] No secrets in code (env variables)

## Open Questions Resolved

| Question | Resolution |
|----------|------------|
| JWT storage | HttpOnly cookies (clarification session) |
| User scale | < 100 (clarification session) |
| Token expiry handling | Silent refresh (clarification session) |
| Concurrent sessions | Allow multiple (clarification session) |
| Logging level | Full audit trail (clarification session) |
