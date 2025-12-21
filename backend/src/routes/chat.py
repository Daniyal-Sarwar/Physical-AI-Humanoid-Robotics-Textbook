"""
Chat Routes - RAG Chatbot API endpoints.

Provides chat endpoint for Physical AI textbook Q&A.
Uses ChromaDB for vector search and Gemini for response generation.
Rate-limited for anonymous users, unlimited for authenticated users.
"""

from datetime import datetime
from typing import Optional, List
import logging

from fastapi import APIRouter, Depends, Request, Header, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src.config import settings
from src.database import get_db
from src.models.user import User
from src.models.rate_limit import RateLimitRecord
from src.routes.auth import get_current_user_optional
from src.services.rag_service import get_rag_service

logger = logging.getLogger(__name__)

router = APIRouter()


class ChatMessage(BaseModel):
    """Single chat message."""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Chat request payload."""
    message: str = Field(..., min_length=1, max_length=2000, description="User message")
    context: List[ChatMessage] = Field(default=[], description="Previous conversation context")


class SourceInfo(BaseModel):
    """Source reference information."""
    module: str = Field(default="", description="Module name")
    title: str = Field(default="", description="Document title")
    source: str = Field(default="", description="Source file path")


class ChatResponse(BaseModel):
    """Chat response payload."""
    response: str = Field(..., description="Assistant response")
    sources: List[SourceInfo] = Field(default=[], description="Source references")
    used_rag: bool = Field(default=False, description="Whether RAG was used")


def get_identifier(request: Request, fingerprint: Optional[str] = None) -> str:
    """Get identifier for rate limiting."""
    if fingerprint:
        return fingerprint
    
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    
    return request.client.host if request.client else "unknown"


def check_rate_limit(
    db: Session,
    identifier: str,
    is_authenticated: bool
) -> tuple[bool, int]:
    """
    Check and update rate limit for anonymous users.
    
    Returns:
        tuple: (is_allowed, remaining_requests)
    """
    if is_authenticated:
        return True, -1  # Unlimited for authenticated users
    
    record = db.query(RateLimitRecord).filter(
        RateLimitRecord.identifier == identifier
    ).first()
    
    now = datetime.utcnow()
    
    if record is None:
        # Create new record
        record = RateLimitRecord(
            identifier=identifier,
            request_count=1,
            window_start=now,
            last_request=now
        )
        db.add(record)
        db.commit()
        return True, settings.anonymous_rate_limit - 1
    
    # Check if window expired
    if record.is_window_expired(settings.rate_limit_window_hours):
        record.reset_window()
        record.request_count = 1
        record.last_request = now
        db.commit()
        return True, settings.anonymous_rate_limit - 1
    
    # Check if limit exceeded
    if record.request_count >= settings.anonymous_rate_limit:
        return False, 0
    
    # Increment counter
    record.request_count += 1
    record.last_request = now
    db.commit()
    
    return True, settings.anonymous_rate_limit - record.request_count


def handle_greeting(message: str) -> Optional[str]:
# Attribution constant
TRADEMARK = "\n\n---\n*Physical AI Textbook™ — Created by [Daniyal Sarwar](https://github.com/Daniyal-Sarwar)*"


def handle_greeting(message: str) -> Optional[str]:
    """Check for greetings and return appropriate response."""
    greetings = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening"]
    if any(g in message.lower() for g in greetings):
        return """Hello! 👋 I'm your Physical AI learning assistant powered by RAG (Retrieval-Augmented Generation).

I have access to the full textbook content and can help you with:

📚 **Module 1: ROS 2 Fundamentals**
- Nodes, Topics, Services, Actions
- Launch files and parameters

🤖 **Module 2: Digital Twin Simulation**
- Gazebo physics simulation
- URDF/SDF robot descriptions
- Unity integration

🎮 **Module 3: NVIDIA Isaac Platform**
- Isaac Sim on Omniverse
- Replicator for synthetic data
- Isaac ROS perception

🧠 **Module 4: Vision-Language-Action**
- Multimodal models
- Embodied AI concepts
- Natural language robot control

What would you like to learn about?""" + TRADEMARK
    return None


def handle_help(message: str) -> Optional[str]:
    """Check for help request and return appropriate response."""
    if "help" in message.lower() or "what can you" in message.lower():
        return """I can help you learn about Physical AI and Humanoid Robotics!

**How I work:**
I use semantic search to find the most relevant sections from the textbook, then generate a personalized response using AI. I'll cite the sources I use.

**Example questions you can ask:**
- "What are the key components of ROS 2?"
- "How do I create a URDF file for my robot?"
- "Explain the difference between Gazebo and Isaac Sim"
- "What are Vision-Language-Action models?"
- "How does domain randomization work in Isaac Replicator?"

Just ask any question about the textbook topics!""" + TRADEMARK
    return None


def generate_response_with_rag(
    message: str,
    user_profile: Optional[dict] = None
) -> tuple[str, List[dict], bool]:
    """
    Generate response using RAG service.
    
    Returns:
        tuple: (response_text, sources, used_rag)
    """
    rag_service = get_rag_service()
    
    # Check for special messages first
    greeting_response = handle_greeting(message)
    if greeting_response:
        return greeting_response, [], False
    
    help_response = handle_help(message)
    if help_response:
        return help_response, [], False
    
    # Check if RAG service is available
    if not rag_service.is_initialized:
        logger.warning("RAG service not initialized, using fallback response")
        return (
            "I'm sorry, but my knowledge base is not fully configured yet. "
            "Please make sure the GEMINI_API_KEY is set and the textbook content has been ingested. "
            "Try asking the administrator to run the content ingestion script.",
            [],
            False
        )
    
    # Check if we have documents
    stats = rag_service.get_stats()
    if stats.get("document_count", 0) == 0:
        logger.warning("No documents in RAG store")
        return (
            "I don't have any textbook content loaded yet. "
            "Please ask the administrator to run the content ingestion to load the textbook into my knowledge base.",
            [],
            False
        )
    
    # Use RAG to generate response
    try:
        result = rag_service.chat(
            query=message,
            user_profile=user_profile,
            n_context_docs=4
        )
        
        response_text = result.get("response", "I couldn't generate a response.")
        # Add trademark to all AI-generated responses
        response_text = response_text + TRADEMARK
        
        return (
            response_text,
            result.get("sources", []),
            result.get("context_used", False)
        )
        
    except Exception as e:
        error_str = str(e).lower()
        logger.error(f"RAG generation failed: {e}")
        
        # User-friendly error messages
        if "429" in str(e) or "quota" in error_str or "rate" in error_str:
            if "limit: 0" in error_str or "daily" in error_str:
                msg = "⚠️ Daily API quota exceeded. Please try again tomorrow."
            else:
                msg = "⚠️ Too many requests. Please wait a moment and try again."
        elif "timeout" in error_str:
            msg = "⚠️ Request timed out. Please try again."
        else:
            msg = "⚠️ Unable to generate a response. Please try again later."
        
        return (msg, [], False)


@router.post(
    "",
    response_model=ChatResponse,
    summary="Send chat message",
    description="Send a message to the RAG chatbot. Uses semantic search and Gemini for responses."
)
async def chat(
    request: Request,
    chat_request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
    x_fingerprint: Optional[str] = Header(default=None),
):
    """
    Process chat message and return AI response.
    
    - Anonymous users: Rate-limited to 5 requests per 24 hours
    - Authenticated users: Unlimited requests with personalized responses
    """
    is_authenticated = current_user is not None
    identifier = get_identifier(request, x_fingerprint)
    
    # Check rate limit
    is_allowed, remaining = check_rate_limit(db, identifier, is_authenticated)
    
    if not is_allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please sign up for unlimited access!",
            headers={"X-RateLimit-Remaining": "0"}
        )
    
    # Get user profile for personalization (if authenticated)
    user_profile = None
    if current_user and hasattr(current_user, 'profile') and current_user.profile:
        user_profile = {
            "programming_level": current_user.profile.programming_level,
            "robotics_familiarity": current_user.profile.robotics_familiarity,
            "hardware_experience": current_user.profile.hardware_experience,
            "learning_goal": current_user.profile.learning_goal,
        }
    
    # Generate response using RAG
    response_text, sources, used_rag = generate_response_with_rag(
        chat_request.message,
        user_profile
    )
    
    # Convert sources to SourceInfo objects
    source_infos = [
        SourceInfo(
            module=s.get("module", ""),
            title=s.get("title", ""),
            source=s.get("source", "")
        )
        for s in sources
    ]
    
    return ChatResponse(
        response=response_text,
        sources=source_infos,
        used_rag=used_rag
    )


@router.get(
    "/stats",
    summary="Get RAG stats",
    description="Get statistics about the RAG knowledge base."
)
async def get_stats():
    """Get RAG service statistics."""
    rag_service = get_rag_service()
    return rag_service.get_stats()


@router.post(
    "/ingest",
    summary="Ingest textbook content",
    description="Trigger ingestion of textbook content into the RAG knowledge base."
)
async def ingest_content(
    clear_existing: bool = False,
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    """
    Ingest textbook content into vector store.
    
    Note: In production, this should be admin-only.
    """
    from src.services.content_ingest import ingest_textbook_content
    
    result = ingest_textbook_content(clear_existing=clear_existing)
    
    return result
