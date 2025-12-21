# Physical AI Textbook - Backend API

Authentication and rate limiting API for the Physical AI Humanoid Robotics Textbook.

## Features

- **User Authentication**: JWT-based authentication with HttpOnly cookies
- **User Registration**: Email/password registration with background questionnaire
- **Rate Limiting**: 5 requests per 24 hours for anonymous users
- **Profile Management**: User profile creation and updates
- **Audit Logging**: Full audit trail of authentication events
- **Account Security**: Account lockout after 5 failed login attempts

## Tech Stack

- **Framework**: FastAPI with Python 3.11+
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: python-jose (JWT), bcrypt (password hashing)
- **Validation**: Pydantic v2
- **Testing**: pytest

## Quick Start

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and set your secrets
# Generate secrets with: python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Run the Server

```bash
# Development mode with auto-reload
uvicorn src.main:app --reload --port 8000

# Or run directly
python -m src.main
```

### 5. Access API Documentation

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Sign in |
| POST | `/api/v1/auth/logout` | Sign out |
| POST | `/api/v1/auth/refresh` | Refresh access token |
| GET | `/api/v1/auth/me` | Get current user |

### User Profile

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/user/profile` | Create profile (questionnaire) |
| PUT | `/api/v1/user/profile` | Update profile |
| GET | `/api/v1/user/profile` | Get profile |

### Rate Limiting

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/rate-limit/status` | Get rate limit status |

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_auth_service.py -v
```

## Project Structure

```
backend/
├── src/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Environment configuration
│   ├── database.py          # SQLite connection
│   ├── models/              # SQLAlchemy models
│   │   ├── user.py
│   │   ├── user_profile.py
│   │   ├── rate_limit.py
│   │   └── audit_log.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── auth.py
│   │   └── user.py
│   ├── routes/              # API endpoints
│   │   ├── auth.py
│   │   ├── user.py
│   │   └── rate_limit.py
│   ├── services/            # Business logic
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── profile_service.py
│   │   └── rate_limit.py
│   └── utils/               # Utilities
│       ├── security.py      # Password & JWT
│       └── audit.py         # Audit logging
├── tests/
│   ├── conftest.py          # Test fixtures
│   ├── unit/                # Unit tests
│   ├── contract/            # API contract tests
│   └── integration/         # Integration tests
├── data/                    # SQLite database (gitignored)
├── requirements.txt
└── .env.example
```

## Security

- Passwords hashed with bcrypt (12 rounds)
- JWT tokens stored in HttpOnly cookies
- HTTPS required in production
- Account lockout after 5 failed attempts
- Full audit logging of auth events

## License

MIT
