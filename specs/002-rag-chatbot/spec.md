# Feature Specification: RAG Chatbot with Authentication & Personalization

**Feature Branch**: `002-rag-chatbot`  
**Created**: 2025-12-14  
**Status**: Draft  
**Input**: Build and embed a RAG chatbot within the published book using Google Gemini API, FastAPI, ChromaDB (local vector DB), and SQLite. Include custom JWT authentication, content personalization based on user background, and selection-based Q&A.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ask Questions About Book Content (Priority: P1)

As a reader of the Physical AI textbook, I want to ask questions about the content and receive accurate answers based on the book material, so that I can better understand complex robotics concepts without searching through chapters manually.

**Why this priority**: This is the core value proposition - the RAG chatbot. Without this, there is no product. It enables readers to get instant, contextual help while learning.

**Independent Test**: Can be fully tested by opening any chapter, typing a question related to visible content, and receiving a relevant answer with source citations.

**Acceptance Scenarios**:

1. **Given** a reader is on any chapter page, **When** they click the chat button, **Then** a chat interface opens allowing them to type questions.
2. **Given** a reader asks "What is URDF?", **When** the system processes the query, **Then** it returns an answer derived from the book's content about Unified Robot Description Format with a citation to the source section.
3. **Given** a reader asks about content not in the book, **When** the system processes the query, **Then** it responds with "I can only answer questions about content in this textbook" rather than hallucinating.
4. **Given** a reader asks a follow-up question, **When** the system processes it, **Then** it maintains conversation context from the previous exchange.

---

### User Story 2 - Ask About Selected Text (Priority: P1)

As a reader studying a specific section, I want to highlight text and ask questions about that specific selection, so that I can get targeted explanations without providing full context in my question.

**Why this priority**: This differentiates the chatbot from generic Q&A - it's contextually aware of what the user is reading. Critical for hackathon scoring (mentioned in requirements).

**Independent Test**: Can be tested by highlighting any paragraph, clicking "Ask about selection", and receiving an explanation specific to that highlighted content.

**Acceptance Scenarios**:

1. **Given** a reader highlights a paragraph about inverse kinematics, **When** they click "Ask about this", **Then** the chat interface opens with the selected text as context.
2. **Given** selected text is provided, **When** the reader asks "Explain this in simpler terms", **Then** the response specifically addresses the highlighted content.
3. **Given** a reader selects a code example, **When** they ask "What does this do?", **Then** the response explains that specific code block.

---

### User Story 3 - User Registration with Background Profile (Priority: P2)

As a new reader, I want to create an account and provide information about my software and hardware background, so that the system can personalize content to my experience level.

**Why this priority**: Authentication enables personalization (bonus points) and user progress tracking. Required foundation for P4 and P5 stories.

**Independent Test**: Can be tested by completing the signup flow, answering background questions, and verifying the profile is saved.

**Acceptance Scenarios**:

1. **Given** a visitor clicks "Sign Up", **When** they complete the registration form, **Then** they are presented with background assessment questions.
2. **Given** background questions include: programming experience (none/beginner/intermediate/advanced), familiarity with robotics (none/hobbyist/academic/professional), hardware experience (none/Arduino-level/embedded systems/industrial), **When** user selects their levels, **Then** the profile is saved.
3. **Given** a user completes registration, **When** they sign in later, **Then** their background profile is retrieved and applied.

---

### User Story 4 - User Sign In/Sign Out (Priority: P2)

As a returning reader, I want to sign in to access my personalized experience and sign out when I'm done, so that my learning preferences persist across sessions.

**Why this priority**: Required for personalization to work across sessions. Basic auth functionality.

**Independent Test**: Can be tested by signing in with valid credentials and verifying session persistence, then signing out and verifying session termination.

**Acceptance Scenarios**:

1. **Given** a registered user, **When** they enter valid credentials, **Then** they are signed in and see their personalized interface.
2. **Given** invalid credentials, **When** user attempts sign in, **Then** they see an error message without revealing which field was wrong.
3. **Given** a signed-in user, **When** they click "Sign Out", **Then** their session ends and they return to anonymous reader mode.
4. **Given** a user closes the browser without signing out, **When** they return within 7 days, **Then** their session is still active.

---

### User Story 5 - Personalize Chapter Content (Priority: P3)

As a signed-in reader with a background profile, I want to press a "Personalize" button at the start of each chapter to adapt the content to my experience level, so that I can learn more effectively without content being too basic or too advanced.

**Why this priority**: Major bonus points (50). Differentiating feature that adds significant educational value.

**Independent Test**: Can be tested by a beginner-profile user pressing "Personalize" on a chapter and comparing the output to an advanced-profile user's personalized version of the same chapter.

**Acceptance Scenarios**:

1. **Given** a signed-in user with "beginner" programming background, **When** they click "Personalize" on a chapter, **Then** the content is rewritten with more explanations and simpler terminology.
2. **Given** a signed-in user with "advanced" background, **When** they click "Personalize", **Then** the content omits basic explanations and focuses on nuances.
3. **Given** personalization is requested, **When** the system generates content, **Then** a loading indicator shows progress.
4. **Given** personalized content is generated, **When** the user navigates away and returns, **Then** they can choose between original and personalized versions.

---

### User Story 6 - Translate Chapter to Urdu (Priority: P4)

As an Urdu-speaking reader, I want to translate chapter content to Urdu by pressing a button, so that I can learn in my native language while preserving technical terminology.

**Why this priority**: Bonus points (50). Serves Pakistani/Indian user base. Technical terms remain in English for searchability.

**Independent Test**: Can be tested by pressing "Translate to Urdu" and verifying the output is readable Urdu with English technical terms intact.

**Acceptance Scenarios**:

1. **Given** a reader on any chapter, **When** they click "Translate to Urdu", **Then** the content is translated with technical terms (ROS, URDF, etc.) preserved in English.
2. **Given** translation is in progress, **When** the user waits, **Then** a loading indicator shows progress.
3. **Given** translated content is displayed, **When** the user clicks "Show Original", **Then** they return to the English version.

---

### Edge Cases

- What happens when the vector database returns no relevant results for a query?
  - System responds with "I couldn't find relevant information in the textbook. Try rephrasing your question or ask about a different topic."
- What happens when the user's session expires mid-conversation?
  - Chat history is preserved locally, and user is prompted to sign in again to continue personalized features.
- What happens when personalization or translation takes too long (>30 seconds)?
  - User sees a timeout message with option to retry or continue with original content.
- What happens when a user tries to access personalization without being signed in?
  - User sees a prompt to sign in or create an account, with explanation of benefits.
- What happens when rate limits are exceeded?
  - User sees "You've made many requests. Please wait a moment before trying again." with countdown.

## Requirements *(mandatory)*

### Functional Requirements

**RAG Chatbot Core**:
- **FR-001**: System MUST embed a chat interface accessible from every page of the book.
- **FR-002**: System MUST process user questions and return answers derived only from book content.
- **FR-003**: System MUST cite the source section/chapter for each answer provided.
- **FR-004**: System MUST respond with "I don't know" variant when query has no relevant content match (similarity score below threshold).
- **FR-005**: System MUST maintain conversation context within a session (last 5 exchanges minimum).
- **FR-006**: System MUST support text selection mode where highlighted text becomes query context.

**Authentication**:
- **FR-007**: System MUST allow users to register with email and password.
- **FR-008**: System MUST collect user background during signup: programming experience, robotics familiarity, hardware experience.
- **FR-009**: System MUST support secure sign-in with JWT session persistence (7 days).
- **FR-010**: System MUST allow users to sign out and terminate their session.
- **FR-011**: System MUST hash passwords securely using bcrypt (never store plaintext).

**Personalization**:
- **FR-012**: System MUST provide a "Personalize" button on each chapter for signed-in users.
- **FR-013**: System MUST adapt content complexity based on user's stored background profile.
- **FR-014**: System MUST preserve original content and allow switching between versions.
- **FR-015**: System MUST store personalized content for retrieval without regeneration.

**Translation**:
- **FR-016**: System MUST provide a "Translate to Urdu" button on each chapter.
- **FR-017**: System MUST preserve technical terminology in English during translation.
- **FR-018**: System MUST allow toggling between translated and original content.

**Security & Performance**:
- **FR-019**: System MUST implement rate limiting on all chatbot and personalization endpoints.
- **FR-020**: System MUST validate and sanitize all user inputs before processing.
- **FR-021**: System MUST respond to chat queries within 3 seconds (95th percentile).

### Key Entities

- **User**: Represents a registered reader. Attributes: email, hashed password, created date, last login.
- **UserProfile**: Represents user's background. Attributes: programming level, robotics familiarity, hardware experience, preferred language.
- **ChatSession**: Represents a conversation. Attributes: user reference (optional), messages, created date, last activity.
- **ChatMessage**: Individual message in a session. Attributes: role (user/assistant), content, timestamp, source citations.
- **PersonalizedContent**: Cached personalized chapter. Attributes: user reference, chapter identifier, content, profile snapshot, generated date.
- **ContentChunk**: Vector-indexed book content. Attributes: chapter reference, section, text content, embedding vector (stored in ChromaDB).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can ask a question and receive a relevant answer within 3 seconds (95th percentile).
- **SC-002**: 90% of chatbot answers correctly cite the source chapter/section.
- **SC-003**: Users can complete account registration in under 2 minutes.
- **SC-004**: Personalized content generation completes within 15 seconds.
- **SC-005**: System handles 50 concurrent users without degradation.
- **SC-006**: Zero instances of chatbot hallucination (answers containing information not in the book).
- **SC-007**: 80% of users who try the chatbot ask at least 3 questions (engagement).
- **SC-008**: Translation preserves 100% of technical terms in English.

## Assumptions

- Book content is complete and indexed before chatbot deployment.
- Google Gemini API availability is stable with <1% downtime (free tier: 60 requests/minute).
- Users have modern browsers (Chrome, Firefox, Safari, Edge - last 2 versions).
- ChromaDB local storage provides sufficient capacity for book content (~100MB vectors).
- SQLite provides sufficient performance for user data and chat history.
- JWT authentication provides reliable session management.

## Dependencies

- Docusaurus frontend (completed in 001-physical-ai-textbook).
- Google Gemini API for embeddings (text-embedding-004) and chat completions.
- ChromaDB for local vector storage.
- SQLite for user data storage.
- Custom JWT authentication (python-jose, bcrypt).

## Out of Scope

- Mobile native apps (web-only for this phase).
- Offline mode for chatbot.
- Multi-language support beyond English and Urdu.
- User-generated content or comments.
- Admin dashboard for content management.
- Payment/subscription features.
- Social login (OAuth with Google/GitHub) - future enhancement.
- Email verification - future enhancement.
