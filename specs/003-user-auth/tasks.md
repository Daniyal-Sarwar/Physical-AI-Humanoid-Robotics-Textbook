# Tasks: User Authentication & Rate-Limited Access

**Input**: Design documents from `/specs/003-user-auth/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: TDD approach - tests included per constitution (Principle II: Testing as Foundation)

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US6)
- All paths relative to repository root

## User Story Mapping

| Story | Priority | Description | Endpoints |
|-------|----------|-------------|-----------|
| US1 | P1 | Anonymous User with Rate Limit | `/rate-limit/status` |
| US2 | P1 | User Registration with Questionnaire | `/auth/register`, `/user/profile` POST |
| US3 | P1 | User Sign In | `/auth/login`, `/auth/me`, `/auth/refresh` |
| US4 | P2 | Password Reset | OUT OF SCOPE (MVP) |
| US5 | P2 | User Sign Out | `/auth/logout` |
| US6 | P3 | Edit Profile/Background | `/user/profile` PUT |

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, dependencies, and configuration

- [x] T001 Create backend project structure per plan.md in `backend/`
- [x] T002 [P] Create `backend/requirements.txt` with FastAPI, python-jose, bcrypt, SQLAlchemy, uvicorn, pydantic
- [x] T003 [P] Create `backend/.env.example` with JWT_SECRET, SESSION_SECRET, SQLITE_DB_PATH placeholders
- [x] T004 [P] Create `backend/src/__init__.py` package initializer
- [x] T005 [P] Implement environment config loader in `backend/src/config.py`
- [x] T006 [P] Create `.gitignore` entries for `backend/data/`, `.env`, `__pycache__/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Foundation

- [x] T007 Implement SQLite database connection and session factory in `backend/src/database.py`
- [x] T008 [P] Create User model in `backend/src/models/user.py` (id, email, password_hash, created_at, last_login, locked_until, failed_attempts)
- [x] T009 [P] Create UserProfile model in `backend/src/models/user_profile.py` (user_id FK, programming_level, robotics_familiarity, hardware_experience, learning_goal, updated_at)
- [x] T010 [P] Create RateLimitRecord model in `backend/src/models/rate_limit.py` (identifier, request_count, window_start, last_request)
- [x] T011 [P] Create AuditLog model in `backend/src/models/audit_log.py` (user_id FK nullable, event_type, ip_address, user_agent, details JSON, timestamp)
- [x] T012 Create models `__init__.py` exporting all models in `backend/src/models/__init__.py`
- [x] T013 Implement database initialization function (create_all tables) in `backend/src/database.py`

### Security Foundation

- [x] T014 [P] Implement password hashing utilities (hash_password, verify_password with bcrypt) in `backend/src/utils/security.py`
- [x] T015 [P] Implement JWT utilities (create_access_token, create_refresh_token, decode_token) in `backend/src/utils/security.py`
- [x] T016 [P] Implement audit logging helper (log_event function) in `backend/src/utils/audit.py`

### Pydantic Schemas Foundation

- [x] T017 [P] Create auth schemas (RegisterRequest, LoginRequest, AuthResponse, ErrorResponse) in `backend/src/schemas/auth.py`
- [x] T018 [P] Create user schemas (ProfileRequest, ProfileResponse, UserBasic, UserWithProfile) in `backend/src/schemas/user.py`
- [x] T019 Create schemas `__init__.py` in `backend/src/schemas/__init__.py`

### API Foundation

- [x] T020 Create FastAPI application entry with CORS, exception handlers in `backend/src/main.py`
- [x] T021 [P] Implement authentication dependency (get_current_user from cookie) in `backend/src/routes/auth.py`
- [x] T022 [P] Implement optional auth dependency (get_current_user_optional) in `backend/src/routes/auth.py`
- [x] T023 Create routes `__init__.py` and register routers in `backend/src/routes/__init__.py`

### Test Infrastructure

- [x] T024 [P] Create pytest configuration and fixtures in `backend/tests/conftest.py`
- [x] T025 [P] Create test database setup (in-memory SQLite) in `backend/tests/conftest.py`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Anonymous User with Rate Limit (Priority: P1) 🎯 MVP

**Goal**: Anonymous visitors can use chatbot with 5 requests/24h limit, see remaining count

**Independent Test**: Open site without signing in, make 5 requests, verify 6th is blocked

### Tests for User Story 1

- [x] T026 [P] [US1] Unit test for rate limit service (check_limit, record_request, reset logic) in `backend/tests/unit/test_rate_limit.py`
- [x] T027 [P] [US1] Contract test for GET `/api/v1/rate-limit/status` endpoint in `backend/tests/contract/test_rate_limit_api.py`

### Implementation for User Story 1

- [x] T028 [US1] Implement RateLimitService (check_rate_limit, record_request, get_status) in `backend/src/services/rate_limit.py`
- [x] T029 [US1] Implement GET `/api/v1/rate-limit/status` endpoint in `backend/src/routes/rate_limit.py`
- [x] T030 [US1] Register rate_limit router in `backend/src/main.py`
- [x] T031 [US1] Add RateLimitStatus schema to `backend/src/schemas/auth.py`

### Frontend for User Story 1

- [x] T032 [P] [US1] Create RateLimitBanner component in `src/components/ChatBot/RateLimitBanner.tsx`
- [x] T033 [P] [US1] Create rate limit API service in `src/services/rateLimitService.ts`

**Checkpoint**: Anonymous rate limiting works independently - can demo MVP!

---

## Phase 4: User Story 2 - User Registration with Questionnaire (Priority: P1)

**Goal**: Visitors can create account with email/password, then complete background questionnaire

**Independent Test**: Complete signup flow, verify user and profile saved in database

### Tests for User Story 2

- [x] T034 [P] [US2] Unit test for user service (create_user, validate_password) in `backend/tests/unit/test_user_service.py`
- [x] T035 [P] [US2] Contract test for POST `/api/v1/auth/register` in `backend/tests/contract/test_auth_api.py`
- [x] T036 [P] [US2] Contract test for POST `/api/v1/user/profile` in `backend/tests/contract/test_user_api.py`
- [x] T037 [P] [US2] Integration test for full registration flow in `backend/tests/integration/test_registration_flow.py`

### Implementation for User Story 2

- [x] T038 [US2] Implement UserService (create_user, get_user_by_email, validate_password_strength) in `backend/src/services/user_service.py`
- [x] T039 [US2] Implement ProfileService (create_profile, get_profile) in `backend/src/services/profile_service.py`
- [x] T040 [US2] Implement POST `/api/v1/auth/register` endpoint in `backend/src/routes/auth.py`
- [x] T041 [US2] Implement POST `/api/v1/user/profile` endpoint in `backend/src/routes/user.py`
- [x] T042 [US2] Register user router in `backend/src/main.py`
- [x] T043 [US2] Add audit logging for REGISTRATION event in register endpoint

### Frontend for User Story 2

- [x] T044 [P] [US2] Create SignUpModal component with email/password form in `src/components/Auth/SignUpModal.tsx`
- [x] T045 [P] [US2] Create Questionnaire component with 4 background questions in `src/components/Auth/Questionnaire.tsx`
- [x] T046 [P] [US2] Create auth API service (register, createProfile) in `src/services/authService.ts`
- [x] T047 [US2] Integrate SignUpModal → Questionnaire flow

**Checkpoint**: Users can register and complete questionnaire - profiles saved

---

## Phase 5: User Story 3 - User Sign In (Priority: P1)

**Goal**: Registered users can sign in, get JWT tokens, access unlimited chatbot

**Independent Test**: Sign in with valid credentials, verify JWT cookie set, no rate limit displayed

### Tests for User Story 3

- [x] T048 [P] [US3] Unit test for auth service (authenticate_user, create_tokens, verify_tokens) in `backend/tests/unit/test_auth_service.py`
- [x] T049 [P] [US3] Contract test for POST `/api/v1/auth/login` in `backend/tests/contract/test_auth_api.py`
- [x] T050 [P] [US3] Contract test for GET `/api/v1/auth/me` in `backend/tests/contract/test_auth_api.py`
- [x] T051 [P] [US3] Contract test for POST `/api/v1/auth/refresh` in `backend/tests/contract/test_auth_api.py`
- [x] T052 [P] [US3] Integration test for login with lockout after 5 failures in `backend/tests/integration/test_auth_flow.py`

### Implementation for User Story 3

- [x] T053 [US3] Implement AuthService (authenticate_user, handle_failed_login, check_account_locked) in `backend/src/services/auth_service.py`
- [x] T054 [US3] Implement POST `/api/v1/auth/login` endpoint with HttpOnly cookie response in `backend/src/routes/auth.py`
- [x] T055 [US3] Implement GET `/api/v1/auth/me` endpoint (get current user + profile) in `backend/src/routes/auth.py`
- [x] T056 [US3] Implement POST `/api/v1/auth/refresh` endpoint (silent token refresh) in `backend/src/routes/auth.py`
- [x] T057 [US3] Add audit logging for LOGIN_SUCCESS, LOGIN_FAILED, ACCOUNT_LOCKED events
- [x] T058 [US3] Implement account lockout logic (5 failures → 15 min lock) in AuthService

### Frontend for User Story 3

- [x] T059 [P] [US3] Create SignInModal component in `src/components/Auth/SignInModal.tsx`
- [x] T060 [P] [US3] Create AuthContext for global auth state in `src/components/Auth/AuthContext.tsx`
- [x] T061 [US3] Add login, logout, refresh, getCurrentUser to `src/services/authService.ts`
- [x] T062 [US3] Integrate AuthContext with Docusaurus layout

**Checkpoint**: Users can sign in, JWT stored in HttpOnly cookie, auth state managed

---

## Phase 6: User Story 5 - User Sign Out (Priority: P2)

**Goal**: Signed-in users can sign out, session terminated, return to anonymous mode

**Independent Test**: Click sign out, verify cookies cleared, redirected to anonymous state

### Tests for User Story 5

- [x] T063 [P] [US5] Contract test for POST `/api/v1/auth/logout` in `backend/tests/contract/test_auth_api.py`
- [x] T064 [P] [US5] Integration test for logout flow in `backend/tests/integration/test_auth_flow.py`

### Implementation for User Story 5

- [x] T065 [US5] Implement POST `/api/v1/auth/logout` endpoint (clear cookies) in `backend/src/routes/auth.py`
- [x] T066 [US5] Add audit logging for LOGOUT event

### Frontend for User Story 5

- [x] T067 [US5] Add sign out button and handler in `src/components/Auth/AuthContext.tsx`
- [x] T068 [US5] Update UI to show anonymous state after logout

**Checkpoint**: Users can sign out securely

---

## Phase 7: User Story 6 - Edit Profile/Background (Priority: P3)

**Goal**: Signed-in users can update their background questionnaire answers

**Independent Test**: Navigate to profile settings, change answers, verify saved

### Tests for User Story 6

- [x] T069 [P] [US6] Contract test for PUT `/api/v1/user/profile` in `backend/tests/contract/test_user_api.py`
- [x] T070 [P] [US6] Integration test for profile update flow in `backend/tests/integration/test_user_flow.py`

### Implementation for User Story 6

- [x] T071 [US6] Implement update_profile in ProfileService in `backend/src/services/profile_service.py`
- [x] T072 [US6] Implement PUT `/api/v1/user/profile` endpoint in `backend/src/routes/user.py`
- [x] T073 [US6] Add audit logging for PROFILE_UPDATED event

### Frontend for User Story 6

- [x] T074 [P] [US6] Create ProfileSettings component in `src/components/Auth/ProfileSettings.tsx`
- [x] T075 [US6] Add updateProfile to `src/services/authService.ts`

**Checkpoint**: Users can edit their background profile

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Security hardening, documentation, final validation

- [x] T076 [P] Run Snyk code scan on `backend/src/` - fix critical/high issues
- [x] T077 [P] Run Snyk dependency audit on `backend/requirements.txt` - fix vulnerabilities
- [x] T078 [P] Add API documentation comments for OpenAPI auto-generation in route files
- [x] T079 [P] Update `backend/README.md` with setup and run instructions
- [x] T080 Validate all endpoints against `specs/003-user-auth/contracts/openapi.yaml`
- [x] T081 Run full test suite and verify 80%+ coverage
- [x] T082 Test quickstart.md instructions end-to-end
- [x] T083 [P] Add request logging middleware for debugging in `backend/src/main.py`

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Setup ──────────────────────────────► No dependencies
     │
     ▼
Phase 2: Foundational ───────────────────────► Depends on Setup
     │
     ├──────────────────────────────────────────────────────────┐
     │                                                          │
     ▼                    ▼                    ▼                 ▼
Phase 3: US1 ──────► Phase 4: US2 ──────► Phase 5: US3 ───► Phase 6: US5
(Rate Limit)         (Registration)       (Sign In)         (Sign Out)
     │                    │                    │                 │
     │                    │                    │                 ▼
     │                    │                    │            Phase 7: US6
     │                    │                    │            (Edit Profile)
     │                    │                    │                 │
     └────────────────────┴────────────────────┴─────────────────┘
                                   │
                                   ▼
                         Phase 8: Polish
```

### User Story Independence

| Story | Can Start After | Dependencies |
|-------|-----------------|--------------|
| US1 | Phase 2 | None - fully independent |
| US2 | Phase 2 | None - fully independent |
| US3 | Phase 2 | None - fully independent |
| US5 | Phase 2 | Requires US3 auth context |
| US6 | Phase 2 | Requires US2 profile creation |

### Parallel Opportunities

**Within Phase 2 (Foundational)**:
- T008, T009, T010, T011 (all models) can run in parallel
- T014, T015, T016 (security utils) can run in parallel
- T017, T018 (schemas) can run in parallel

**Across User Stories** (after Phase 2):
- US1, US2, US3 can all start simultaneously if team capacity allows
- All tasks marked [P] within each story can run in parallel

---

## Parallel Example: Phase 2 Models

```bash
# Launch all model tasks together:
Task: "T008 [P] Create User model in backend/src/models/user.py"
Task: "T009 [P] Create UserProfile model in backend/src/models/user_profile.py"
Task: "T010 [P] Create RateLimitRecord model in backend/src/models/rate_limit.py"
Task: "T011 [P] Create AuditLog model in backend/src/models/audit_log.py"
```

## Parallel Example: User Story 2 Tests

```bash
# Launch all US2 tests together:
Task: "T034 [P] [US2] Unit test for user service"
Task: "T035 [P] [US2] Contract test for POST /api/v1/auth/register"
Task: "T036 [P] [US2] Contract test for POST /api/v1/user/profile"
Task: "T037 [P] [US2] Integration test for full registration flow"
```

---

## Implementation Strategy

### MVP First (User Stories 1-3 Only)

1. ✅ Complete Phase 1: Setup
2. ✅ Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. ✅ Complete Phase 3: US1 - Rate Limiting (anonymous can try chatbot)
4. ✅ Complete Phase 4: US2 - Registration (users can sign up)
5. ✅ Complete Phase 5: US3 - Sign In (users can authenticate)
6. ✅ Complete Phase 6: US5 - Sign Out
7. ✅ Complete Phase 7: US6 - Edit Profile
8. ✅ **93/93 Backend Tests Passing** - Backend validated
9. ✅ **Frontend Implementation Complete** - All components created
10. ✅ **Phase 8 Polish Complete** - Production-ready

### Incremental Delivery

| Increment | Stories | Value Delivered |
|-----------|---------|-----------------|
| MVP | US1 + US2 + US3 | Core auth with rate limiting |
| +1 | + US5 | Sign out capability |
| +2 | + US6 | Profile editing |
| Final | + Polish | Production-ready |

---

## Notes

- Password Reset (US4) is OUT OF SCOPE per spec.md
- All backend tests use pytest with in-memory SQLite
- Frontend uses existing Docusaurus structure from 001-physical-ai-textbook
- JWT stored in HttpOnly cookies (XSS-resistant)
- Full audit logging enabled per FR-023
- Snyk security scans required before merge (Principle I)
