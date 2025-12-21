"""
FastAPI Application Entry Point

Main application with CORS, exception handlers, and router registration.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.config import settings
from src.database import init_db

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan handler.
    
    Initializes database on startup.
    """
    # Startup
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Application shutting down")


# Create FastAPI application
app = FastAPI(
    title="Physical AI Textbook - Authentication API",
    description="User authentication, registration, and rate limiting API for the Physical AI Humanoid Robotics Textbook. Created by Daniyal Sarwar.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs" if not settings.is_production else None,
    redoc_url="/api/redoc" if not settings.is_production else None,
    contact={
        "name": "Daniyal Sarwar",
        "url": "https://github.com/Daniyal-Sarwar"
    },
    license_info={
        "name": "Created by Daniyal Sarwar",
        "url": "https://github.com/Daniyal-Sarwar/Physical-AI-Humanoid-Robotics-Textbook"
    },
)


# ==============================================================================
# CORS Middleware
# ==============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,  # Required for HttpOnly cookies
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================================================================
# Exception Handlers
# ==============================================================================

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    """Handle Pydantic validation errors."""
    errors = exc.errors()
    detail = "; ".join(
        f"{'.'.join(str(loc) for loc in e['loc'])}: {e['msg']}"
        for e in errors
    )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Validation Error",
            "detail": detail,
            "code": 400
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    
    if settings.debug:
        detail = str(exc)
    else:
        detail = "An unexpected error occurred"
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "detail": detail,
            "code": 500
        }
    )


# ==============================================================================
# Request Logging Middleware
# ==============================================================================

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests."""
    logger.debug(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.debug(f"Response status: {response.status_code}")
    return response


# ==============================================================================
# Router Registration
# ==============================================================================

from src.routes.auth import router as auth_router
from src.routes.user import router as user_router
from src.routes.rate_limit import router as rate_limit_router
from src.routes.chat import router as chat_router

# Register routers with API version prefix
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(user_router, prefix="/api/v1/user", tags=["user"])
app.include_router(rate_limit_router, prefix="/api/v1/rate-limit", tags=["rate-limit"])
app.include_router(chat_router, prefix="/api/v1/chat", tags=["chat"])


# ==============================================================================
# Health Check
# ==============================================================================

@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint for load balancers."""
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/api/v1/health", tags=["health"])
async def api_health_check():
    """API health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}


# ==============================================================================
# Development Server
# ==============================================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=not settings.is_production,
        log_level=settings.log_level.lower(),
    )
