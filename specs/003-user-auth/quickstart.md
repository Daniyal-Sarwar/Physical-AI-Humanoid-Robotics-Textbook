# Quickstart: User Authentication & Rate-Limited Access

**Feature Branch**: `003-user-auth`  
**Date**: 2025-12-17

## Prerequisites

- Python 3.11+
- Node.js 18+ (for frontend)
- Git

## Environment Setup

### 1. Clone and checkout feature branch

```bash
git checkout 003-user-auth
```

### 2. Create backend environment

```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
# Copy example and edit
cp .env.example .env
```

Edit `.env` with your values:

```env
# Required secrets (generate secure random strings)
JWT_SECRET=your-32-char-minimum-random-secret-here
SESSION_SECRET=another-32-char-minimum-random-secret

# Database (default is fine for development)
SQLITE_DB_PATH=sqlite:///./data/users.db

# JWT Configuration
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS (adjust for your frontend URL)
CORS_ORIGINS=http://localhost:3000
```

**Generate secure secrets:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4. Initialize database

```bash
# Creates ./data/users.db with all tables
python -c "from src.database import init_db; init_db()"
```

### 5. Start backend server

```bash
uvicorn src.main:app --reload --port 8000
```

Backend now running at: http://localhost:8000

- API docs: http://localhost:8000/docs
- OpenAPI spec: http://localhost:8000/openapi.json

### 6. Start frontend (separate terminal)

```bash
cd ..  # Return to repo root
npm install
npm start
```

Frontend now running at: http://localhost:3000

## API Quick Reference

### Register New User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "SecurePass123"}' \
  -c cookies.txt
```

### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "SecurePass123"}' \
  -c cookies.txt
```

### Get Current User (authenticated)
```bash
curl http://localhost:8000/api/v1/auth/me \
  -b cookies.txt
```

### Create Profile (questionnaire)
```bash
curl -X POST http://localhost:8000/api/v1/user/profile \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "programming_level": "intermediate",
    "robotics_familiarity": "hobbyist",
    "hardware_experience": "arduino",
    "learning_goal": "academic"
  }'
```

### Check Rate Limit (anonymous)
```bash
curl http://localhost:8000/api/v1/rate-limit/status \
  -H "X-Fingerprint: test-fingerprint-123"
```

### Logout
```bash
curl -X POST http://localhost:8000/api/v1/auth/logout \
  -b cookies.txt \
  -c cookies.txt
```

## Running Tests

### Backend Tests
```bash
cd backend

# All tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Specific test file
pytest tests/unit/test_auth_service.py -v
```

### Security Scan
```bash
# Snyk code scan (requires Snyk CLI)
snyk code test

# Dependency audit
snyk test
```

## Project Structure

```
backend/
├── src/
│   ├── main.py          # FastAPI app entry
│   ├── config.py        # Environment config
│   ├── database.py      # SQLite setup
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── routes/          # API endpoints
│   ├── services/        # Business logic
│   └── utils/           # Helpers
├── tests/
├── data/                # SQLite database (gitignored)
├── requirements.txt
└── .env.example

src/
├── components/Auth/     # React auth components
└── services/authService.ts
```

## Common Issues

### "check_same_thread" SQLite error
Add `connect_args={"check_same_thread": False}` to engine creation.

### CORS errors
Ensure `CORS_ORIGINS` in `.env` matches your frontend URL exactly.

### JWT decode errors
Ensure `JWT_SECRET` is the same across server restarts.

### Cookie not sent
Check that frontend and backend are on same domain (or use proper CORS credentials).

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks
2. Implement backend models and routes (TDD)
3. Implement frontend auth components
4. Integration testing
5. Security scan with Snyk
