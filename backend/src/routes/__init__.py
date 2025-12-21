"""Routes package - FastAPI route handlers."""

from src.routes.auth import router as auth_router
from src.routes.user import router as user_router
from src.routes.rate_limit import router as rate_limit_router
from src.routes.chat import router as chat_router

__all__ = [
    "auth_router",
    "user_router",
    "rate_limit_router",
    "chat_router",
]
