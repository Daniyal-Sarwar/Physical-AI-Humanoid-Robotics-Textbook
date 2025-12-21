# Feature Specification: User Authentication & Rate-Limited Access

**Feature Branch**: `003-user-auth`  
**Created**: 2025-12-14  
**Status**: Draft  
**Input**: User authentication with signup questionnaire for personalization, rate limiting for anonymous users (5 requests/24h), and full chatbot access for authenticated users.

## Clarifications

### Session 2025-12-17

- Q: How should the system handle JWT token storage on the client side? → A: HttpOnly cookie (server sets, browser auto-sends, XSS-resistant)
- Q: What is the expected maximum number of registered users for initial deployment? → A: < 100 users (small pilot/demo)
- Q: When a user's JWT token expires during an active session, what should happen? → A: Silent refresh (auto-renew token if within 7-day window)
- Q: If the same user signs in from multiple devices/browsers simultaneously, what should happen? → A: Allow multiple concurrent sessions (each device independent)
- Q: What level of authentication logging should be implemented? → A: Full audit trail (login, logout, failed attempts, lockouts, IP, user agent, profile changes)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Anonymous User with Rate Limit (Priority: P1)

As an anonymous visitor, I want to try the chatbot with limited requests so that I can evaluate its usefulness before creating an account.

**Why this priority**: This is the entry point for all users. Rate limiting protects the system while allowing trial usage.

**Independent Test**: Can be tested by opening the site without signing in, making 5 chatbot requests, and verifying the 6th request is blocked with a clear message.

**Acceptance Scenarios**:

1. **Given** an anonymous visitor, **When** they ask their first question, **Then** they see a response along with a counter showing "4 free questions remaining today".
2. **Given** an anonymous visitor has used 5 requests, **When** they try to ask another question, **Then** they see a message: "You've used all 5 free questions for today. Sign up for unlimited access!"
3. **Given** an anonymous visitor was rate-limited yesterday, **When** 24 hours pass, **Then** their counter resets to 5 free requests.
4. **Given** an anonymous visitor, **When** they view the chat interface, **Then** they see a prompt encouraging signup with benefits listed.

---

### User Story 2 - User Registration with Background Questionnaire (Priority: P1)

As a new visitor, I want to create an account and answer questions about my background so that the system can personalize content for my experience level.

**Why this priority**: Core authentication functionality. Questionnaire data enables personalization (bonus points).

**Independent Test**: Can be tested by completing the full signup flow and verifying all data is saved correctly.

**Acceptance Scenarios**:

1. **Given** a visitor clicks "Sign Up", **When** they enter email and password, **Then** they proceed to the background questionnaire.
2. **Given** the questionnaire is displayed, **When** the user sees the questions, **Then** they include:
   - Programming experience (None / Beginner / Intermediate / Advanced)
   - Robotics familiarity (None / Hobbyist / Academic / Professional)
   - Hardware experience (None / Arduino/Raspberry Pi / Embedded Systems / Industrial)
   - Primary learning goal (Career change / Academic study / Hobby / Professional development)
3. **Given** user completes the questionnaire, **When** they submit, **Then** their profile is saved and they are redirected to the book with full access.

---

### User Story 3 - User Sign In (Priority: P1)

As a registered user, I want to sign in to access unlimited chatbot queries and personalization features.

**Why this priority**: Essential for returning users to access their benefits.

**Independent Test**: Can be tested by signing in with valid credentials and verifying unlimited chatbot access.

**Acceptance Scenarios**:

1. **Given** a registered user, **When** they enter valid credentials, **Then** they are signed in and see "Welcome back, [name]!".
2. **Given** a signed-in user, **When** they use the chatbot, **Then** there is no rate limit displayed or enforced.
3. **Given** invalid credentials, **When** user attempts sign in, **Then** they see "Invalid email or password" (not specifying which is wrong).
4. **Given** 5 failed login attempts, **When** user tries again, **Then** they are temporarily locked out for 15 minutes.

---

### User Story 4 - Password Reset (Priority: P2)

As a user who forgot my password, I want to reset it securely so that I can regain access to my account.

**Why this priority**: Standard auth requirement for user experience.

**Independent Test**: Can be tested by requesting password reset and completing the flow.

**Acceptance Scenarios**:

1. **Given** a user clicks "Forgot Password", **When** they enter their email, **Then** they receive a reset link within 2 minutes.
2. **Given** a reset link is received, **When** clicked within 1 hour, **Then** user can set a new password.
3. **Given** a reset link older than 1 hour, **When** clicked, **Then** user sees "This link has expired. Please request a new one."

---

### User Story 5 - User Sign Out (Priority: P2)

As a signed-in user, I want to sign out so that my session is secure on shared devices.

**Why this priority**: Basic security requirement.

**Independent Test**: Can be tested by signing out and verifying session termination.

**Acceptance Scenarios**:

1. **Given** a signed-in user, **When** they click "Sign Out", **Then** their session ends and they return to anonymous mode.
2. **Given** a user signed out, **When** they try to access personalization, **Then** they are prompted to sign in.

---

### User Story 6 - Edit Profile/Background (Priority: P3)

As a signed-in user, I want to update my background information so that personalization stays relevant as I learn.

**Why this priority**: Nice-to-have for users who progress in their learning journey.

**Independent Test**: Can be tested by changing profile settings and verifying personalization updates.

**Acceptance Scenarios**:

1. **Given** a signed-in user, **When** they navigate to Profile Settings, **Then** they can edit their background questionnaire answers.
2. **Given** updated background, **When** user requests personalization, **Then** new content reflects updated experience level.

---

### Edge Cases

- What happens when a user tries to register with an existing email?
  - System shows "An account with this email already exists. Sign in instead?"
- What happens when anonymous rate limit tracking fails (e.g., cookies cleared)?
  - Fall back to IP-based tracking with same 5 request/24h limit.
- What happens when user's session expires?
  - User is gracefully returned to anonymous mode with prompt to sign in again.

## Requirements *(mandatory)*

### Functional Requirements

**Anonymous Access & Rate Limiting**:
- **FR-001**: System MUST allow anonymous users to access the chatbot.
- **FR-002**: System MUST limit anonymous users to 5 chatbot requests per 24-hour period.
- **FR-003**: System MUST display remaining free requests to anonymous users.
- **FR-004**: System MUST reset anonymous rate limits after 24 hours from first request.
- **FR-005**: System MUST track anonymous users via browser fingerprint/cookies with IP fallback.

**Registration**:
- **FR-006**: System MUST allow registration with email and password.
- **FR-007**: System MUST enforce password requirements: minimum 8 characters, at least one number, one letter.
- **FR-008**: System MUST present background questionnaire after email/password entry.
- **FR-009**: System MUST collect: programming experience, robotics familiarity, hardware experience, learning goal.
- **FR-010**: System MUST prevent duplicate registrations with same email.

**Authentication**:
- **FR-011**: System MUST support secure sign-in with email and password.
- **FR-012**: System MUST maintain sessions for 7 days of inactivity.
- **FR-013**: System MUST implement account lockout after 5 failed login attempts (15 minutes).
- **FR-014**: System MUST allow users to sign out and terminate session.
- **FR-015**: System MUST silently refresh expired JWT tokens if within 7-day session window.
- **FR-016**: System MUST allow multiple concurrent sessions per user (each device independent).

**Authenticated User Benefits**:
- **FR-017**: System MUST provide unlimited chatbot access to authenticated users.
- **FR-018**: System MUST enable personalization features only for authenticated users.
- **FR-019**: System MUST enable translation features only for authenticated users.

**Security**:
- **FR-020**: System MUST hash passwords using bcrypt (never store plaintext).
- **FR-021**: System MUST use HTTPS for all authentication endpoints.
- **FR-022**: System MUST validate and sanitize all user inputs.
- **FR-023**: System MUST log full audit trail: login, logout, failed attempts, lockouts, IP address, user agent, and profile changes.
- **FR-024**: System MUST store JWT tokens in HttpOnly cookies (XSS-resistant, auto-sent by browser).

### Key Entities

- **User**: Registered account. Attributes: email, hashed password, created date, last login, account locked until.
- **UserProfile**: Background information. Attributes: programming level, robotics familiarity, hardware experience, learning goal, updated date.
- **Session**: Active JWT session. Attributes: user reference, token, created date, expires date.
- **RateLimitRecord**: Anonymous usage tracking. Attributes: identifier (fingerprint/IP), request count, window start time.
- **AuditLog**: Full audit trail. Attributes: user reference (nullable), event type, IP address, user agent, details JSON, timestamp.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Anonymous users can make exactly 5 chatbot requests within 24 hours.
- **SC-002**: Users can complete registration (including questionnaire) in under 3 minutes.
- **SC-003**: Sign-in process completes in under 5 seconds.
- **SC-004**: 100% of passwords are stored using secure hashing (verified via security audit).
- **SC-005**: Zero unauthorized access to authenticated-only features by anonymous users.
- **SC-006**: 80% of anonymous users who hit rate limit subsequently sign up.
- **SC-007**: Account lockout triggers after exactly 5 failed login attempts.

## Assumptions

- Browser cookies/localStorage are available for most users.
- IP-based fallback provides reasonable accuracy for rate limiting.
- SQLite provides sufficient performance for user data storage.
- JWT tokens provide secure session management.
- Expected user base: < 100 users (pilot/demo scale); SQLite is adequate.

## Dependencies

- Custom JWT authentication (python-jose library).
- SQLite for user data storage (local file).
- Frontend components from Docusaurus (already in 001-physical-ai-textbook).

## Out of Scope

- Email verification (simplified for MVP - can add later).
- Password reset via email (simplified for MVP).
- Social login (Google, GitHub OAuth) - future enhancement.
- Two-factor authentication (2FA) - future enhancement.
- Account deletion/GDPR data export - future enhancement.
- Admin user management dashboard.
- Organization/team accounts.
