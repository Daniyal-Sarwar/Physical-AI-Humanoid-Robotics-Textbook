# Implementation Plan: User Authentication & Rate-Limited Access

**Branch**: `003-user-auth` | **Date**: 2025-12-17 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-user-auth/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement user authentication with JWT-based sessions, background questionnaire for personalization, and rate limiting for anonymous users (5 requests/24h). The system uses custom JWT authentication with HttpOnly cookies, SQLite for user data, and full audit logging. Authenticated users get unlimited chatbot access and personalization features.

## Technical Context

**Language/Version**: Python 3.11, TypeScript 5.x (frontend)  
**Primary Dependencies**: FastAPI, python-jose (JWT), bcrypt, SQLite3, React (Docusaurus)  
**Storage**: SQLite (local file: `./data/users.db`)  
**Testing**: pytest (backend), Jest (frontend)  
**Target Platform**: Linux server (backend), Modern browsers (frontend)
**Project Type**: web (frontend + backend)  
**Performance Goals**: Sign-in < 5 seconds, API response < 200ms p95  
**Constraints**: < 100 users (pilot scale), HttpOnly cookies for JWT storage  
**Scale/Scope**: < 100 registered users, 5 entities, 8 API endpoints

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Security First | ✅ PASS | bcrypt password hashing (FR-020), JWT HttpOnly cookies (FR-024), input validation (FR-022), full audit logging (FR-023), HTTPS required (FR-021) |
| II. Testing as Foundation | ✅ PASS | Contract tests for all 8 endpoints, unit tests for auth logic, integration tests for user flows |
| V. Consistency & Standards | ✅ PASS | RESTful API design, consistent error format, Pydantic models |
| VII. Code Example Quality | ✅ PASS | Backend structure follows constitution template |
| IX. RAG Chatbot Integration | ✅ PASS | Rate limiting integrated (5/24h anonymous, unlimited auth) |
| X. Authentication Standards | ✅ PASS | Custom JWT auth, bcrypt hashing, 7-day session expiry, background questionnaire |

**Gate Result**: ✅ ALL GATES PASS - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/003-user-auth/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (OpenAPI specs)
└── tasks.md             # Phase 2 output (created by /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── main.py              # FastAPI application entry
│   ├── config.py            # Environment configuration
│   ├── database.py          # SQLite connection & session
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User, UserProfile SQLAlchemy models
│   │   ├── session.py       # Session model (JWT tracking)
│   │   ├── rate_limit.py    # RateLimitRecord model
│   │   └── audit_log.py     # AuditLog model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py          # Pydantic request/response schemas
│   │   └── user.py          # User profile schemas
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py          # /api/v1/auth/* endpoints
│   │   └── user.py          # /api/v1/user/* endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py  # JWT, password hashing logic
│   │   ├── user_service.py  # User CRUD operations
│   │   └── rate_limit.py    # Rate limiting logic
│   └── utils/
│       ├── __init__.py
│       ├── security.py      # Password hashing, JWT utils
│       └── audit.py         # Audit logging helper
├── tests/
│   ├── unit/
│   │   ├── test_auth_service.py
│   │   └── test_rate_limit.py
│   ├── integration/
│   │   ├── test_auth_flow.py
│   │   └── test_user_flow.py
│   └── contract/
│       └── test_api_contracts.py
├── data/                    # SQLite database directory (gitignored)
├── requirements.txt
└── .env.example

src/
├── components/
│   ├── Auth/
│   │   ├── SignInModal.tsx
│   │   ├── SignUpModal.tsx
│   │   ├── Questionnaire.tsx
│   │   └── AuthContext.tsx
│   └── ChatBot/
│       └── RateLimitBanner.tsx
└── services/
    └── authService.ts       # Frontend auth API calls
```

**Structure Decision**: Web application with FastAPI backend and React/Docusaurus frontend. Backend follows constitution template with models/routes/services separation. Frontend adds Auth components to existing Docusaurus structure.

## Complexity Tracking

> **No violations detected. All gates passed.**
