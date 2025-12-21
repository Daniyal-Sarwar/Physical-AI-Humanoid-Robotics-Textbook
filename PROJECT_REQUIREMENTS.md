# 🔑 Project Requirements: What I Need From You

This document lists all the external services and credentials required for the RAG Chatbot.

## ✅ Simplified Tech Stack

We're using a **minimal external dependency** approach:

| Component | Solution | External Service? |
|-----------|----------|-------------------|
| Vector DB | ChromaDB | ❌ No (local/in-app) |
| LLM/Embeddings | Google Gemini | ✅ Yes (API key needed) |
| User Database | SQLite | ❌ No (local file) |
| Authentication | Custom JWT | ❌ No (self-contained) |

---

## ⚠️ CRITICAL: Security Reminder

**NEVER share credentials directly in chat.** Instead:
1. Create a `.env` file in the project root
2. Copy values from `.env.example`
3. Fill in your actual credentials locally

---

## 1. Google Gemini API (Required for RAG Chatbot)

**What it's for**: Generating embeddings for vector search and powering chat responses.

**What I need**:
- [ ] Google Gemini API Key

**How to get it**:
1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Sign in with your Google account
3. Click "Get API key" → "Create API key"
4. Copy the key

**Cost**: **FREE tier available!** 
- 60 requests per minute
- 1 million tokens per minute
- Perfect for this project

**Environment variable**:
```
GEMINI_API_KEY=your-gemini-api-key-here
```

---

## 2. JWT Secret (Required for Auth - Self-Generated)

**What it's for**: Signing authentication tokens for user sessions.

**What I need**:
- [ ] A randomly generated secret string (you generate this yourself)

**How to generate**:
```bash
# Run this command in terminal:
openssl rand -hex 32

# Or use Python:
python -c "import secrets; print(secrets.token_hex(32))"
```

**Environment variable**:
```
JWT_SECRET=your-64-character-random-string-here
```

---

## 3. Session Secret (Required for Auth - Self-Generated)

**What it's for**: Encrypting session cookies.

**How to generate**: Same as JWT Secret, but use a different value.

**Environment variable**:
```
SESSION_SECRET=your-different-64-character-random-string-here
```

---

## 📋 Checklist Summary

| Requirement | Type | Status |
|-------------|------|--------|
| Gemini API Key | External service | ⬜ Pending |
| JWT Secret | Self-generated | ⬜ Pending |
| Session Secret | Self-generated | ⬜ Pending |

**Total external services needed: 1 (Gemini only!)**

---

## 🏗️ What's Included Locally (No Setup Needed)

These components run entirely within the app - no external accounts required:

### ChromaDB (Vector Database)
- Runs embedded in the Python app
- Stores vectors in local files (`./chroma_db/`)
- No cloud service, no API keys
- Automatically persists data

### SQLite (User Database)
- Single file database (`./data/users.db`)
- Stores: users, profiles, sessions, rate limits
- No server setup required
- Automatically created on first run

### Custom JWT Authentication
- Self-contained auth system
- No external auth provider
- Tokens signed with your secret
- Sessions stored in SQLite

---

## 🚀 Quick Start

Once you have your Gemini API key:

1. **Create `.env` file** in `backend/` folder:
```bash
cd backend
cp .env.example .env
```

2. **Fill in your values**:
```env
# Required - Get from Google AI Studio
GEMINI_API_KEY=your-gemini-api-key

# Required - Generate yourself (openssl rand -hex 32)
JWT_SECRET=your-random-64-char-string
SESSION_SECRET=your-different-random-64-char-string

# Optional - Defaults work fine
ENVIRONMENT=development
```

3. **Tell me you're ready** and I'll start building!

---

## ❓ Confirmation Needed

Please confirm:

1. **Gemini API**: Do you have access to Google AI Studio?
   - [ ] Yes, I can get an API key
   - [ ] No, I need help

2. **Rate limit for anonymous users**: Is 5 requests per 24 hours still correct?
   - [ ] Yes, 5 requests/24h
   - [ ] Different: _____ requests per _____

3. **Ready to proceed?**
   - [ ] Yes, I have my Gemini API key ready
   - [ ] Not yet, I need to set it up first

---

## 📦 Dependencies (Auto-installed)

These Python packages will be installed automatically:

```
fastapi          # Web framework
uvicorn          # ASGI server
chromadb         # Vector database (local)
google-generativeai  # Gemini API client
python-jose      # JWT tokens
passlib          # Password hashing
python-multipart # Form handling
```

**No Qdrant. No Postgres. No Better-Auth. Just simple, local solutions!**
