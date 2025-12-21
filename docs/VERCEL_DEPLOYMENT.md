# Vercel Deployment Guide

## Overview

This project consists of two parts:
- **Frontend**: Docusaurus static site
- **Backend**: FastAPI Python API

---

## Frontend (Docusaurus) - Vercel

### Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `REACT_APP_BACKEND_URL` | ✅ Yes | Backend API URL | `https://your-backend.vercel.app` |

### Build Settings

| Setting | Value |
|---------|-------|
| Framework Preset | Other |
| Build Command | `npm run build` |
| Output Directory | `build` |
| Install Command | `npm ci` |
| Node Version | 20.x |

---

## Backend (FastAPI) - Vercel Serverless / Railway / Render

### Required Secrets (Environment Variables)

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `JWT_SECRET` | ✅ **Yes** | Secret key for JWT token signing. **Must be a strong random string (32+ chars)** | `dev-secret-change-in-production` |
| `SESSION_SECRET` | ✅ **Yes** | Secret key for session management. **Must be a strong random string (32+ chars)** | `dev-session-secret-change-in-production` |
| `GEMINI_API_KEY` | ✅ **Yes** | Google Gemini API key for RAG chatbot | `None` |
| `ENVIRONMENT` | ✅ **Yes** | Set to `production` for deployment | `development` |

### Optional Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `FRONTEND_URL` | Recommended | Allowed CORS origin (your Vercel frontend URL) | `http://localhost:3000` |
| `DEBUG` | No | Enable debug mode | `False` |
| `LOG_LEVEL` | No | Logging level | `INFO` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | JWT access token expiry | `15` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | No | JWT refresh token expiry | `7` |
| `JWT_EXPIRATION_SECONDS` | No | JWT total expiration | `604800` (7 days) |
| `ANONYMOUS_RATE_LIMIT` | No | Anonymous user rate limit | `5` |
| `RATE_LIMIT_WINDOW_HOURS` | No | Rate limit window | `24` |
| `SQLITE_DB_PATH` | No | SQLite database path | `sqlite:///./data/users.db` |
| `CHROMA_PERSIST_DIR` | No | ChromaDB storage directory | `./chroma_db` |
| `CHROMA_COLLECTION_NAME` | No | ChromaDB collection name | `physical_ai_textbook` |
| `HOST` | No | Server host | `0.0.0.0` |
| `PORT` | No | Server port | `8000` |

---

## How to Generate Secure Secrets

### Option 1: Using OpenSSL
```bash
openssl rand -hex 32
```

### Option 2: Using Python
```python
import secrets
print(secrets.token_hex(32))
```

### Option 3: Online Generator
Use a secure random string generator with 64+ characters.

---

## Vercel Configuration Steps

### 1. Frontend Deployment

1. Connect your GitHub repo to Vercel
2. Set **Root Directory** to `/` (project root)
3. Add Environment Variables:
   ```
   REACT_APP_BACKEND_URL = https://your-backend-url.com
   ```
4. Deploy

### 2. Backend Deployment (if using Vercel Serverless)

Create `vercel.json` in `/backend`:
```json
{
  "builds": [
    {
      "src": "src/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "src/main.py"
    }
  ]
}
```

Add all required environment variables in Vercel Dashboard → Settings → Environment Variables.

---

## Production Checklist

- [ ] `JWT_SECRET` is a unique, strong random string (not the default)
- [ ] `SESSION_SECRET` is a unique, strong random string (not the default)
- [ ] `ENVIRONMENT` is set to `production`
- [ ] `GEMINI_API_KEY` is valid and has quota
- [ ] `FRONTEND_URL` matches your deployed frontend URL
- [ ] CORS is properly configured for your domains

---

## Quick Copy-Paste Template

```env
# Required - CHANGE THESE!
JWT_SECRET=your-32-char-random-string-here
SESSION_SECRET=your-32-char-random-string-here
GEMINI_API_KEY=your-gemini-api-key
ENVIRONMENT=production

# Recommended
FRONTEND_URL=https://your-frontend.vercel.app

# Optional (defaults are fine)
DEBUG=False
LOG_LEVEL=INFO
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```
