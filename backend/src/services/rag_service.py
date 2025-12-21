"""
RAG Service - Retrieval Augmented Generation

Uses ChromaDB for vector storage.
Uses local sentence-transformers for embeddings (no API limits).
Uses Gemini for response generation.
"""

import logging
import time
from typing import Optional, List, Dict, Any
from pathlib import Path

import chromadb
import google.generativeai as genai
from sentence_transformers import SentenceTransformer

from src.config import settings

logger = logging.getLogger(__name__)

# ChromaDB collection name
COLLECTION_NAME = "physical_ai_textbook"

# Local embedding model (no API limits, runs offline)
# all-MiniLM-L6-v2 is fast and good for semantic search
LOCAL_EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Gemini model for chat responses
CHAT_MODEL = "gemini-2.0-flash"

# Whether to use local embeddings (True) or Gemini API (False)
USE_LOCAL_EMBEDDINGS = True

# Rate limiting for Gemini API (when using Gemini embeddings)
EMBEDDING_RATE_LIMIT_DELAY = 2.5  # seconds between embedding requests
MAX_RETRIES = 5
INITIAL_BACKOFF = 5.0


class RAGService:
    """
    RAG Service for Physical AI Textbook chatbot.
    
    Uses ChromaDB for vector storage and semantic search.
    Uses local sentence-transformers for embeddings (no API limits).
    Uses Gemini API for response generation.
    """
    
    def __init__(self, persist_directory: Optional[str] = None):
        """
        Initialize RAG service.
        
        Args:
            persist_directory: Directory to persist ChromaDB data.
                             Defaults to backend/data/chroma/
        """
        self._initialized = False
        self.embedding_model = None
        
        self.api_key = settings.gemini_api_key
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not set - RAG chat responses will be limited")
        
        try:
            # Initialize local embedding model (no API limits!)
            if USE_LOCAL_EMBEDDINGS:
                logger.info(f"Loading local embedding model: {LOCAL_EMBEDDING_MODEL}")
                self.embedding_model = SentenceTransformer(LOCAL_EMBEDDING_MODEL)
                logger.info("Local embedding model loaded successfully")
            
            # Configure Gemini for chat responses (if API key available)
            if self.api_key:
                genai.configure(api_key=self.api_key)
                self.chat_model = genai.GenerativeModel(CHAT_MODEL)
            else:
                self.chat_model = None
            
            # Set up ChromaDB persistence directory
            if persist_directory is None:
                backend_dir = Path(__file__).parent.parent.parent
                persist_directory = str(backend_dir / "data" / "chroma")
            
            # Ensure directory exists
            Path(persist_directory).mkdir(parents=True, exist_ok=True)
            
            # Initialize ChromaDB with persistence (new API)
            self.chroma_client = chromadb.PersistentClient(path=persist_directory)
            
            # Get or create collection
            self.collection = self.chroma_client.get_or_create_collection(
                name=COLLECTION_NAME,
                metadata={"description": "Physical AI Humanoid Robotics Textbook content"}
            )
            
            self._initialized = True
            logger.info(f"RAG Service initialized with {self.collection.count()} documents")
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG service: {e}")
            self._initialized = False
    
    @property
    def is_initialized(self) -> bool:
        """Check if RAG service is properly initialized."""
        return getattr(self, '_initialized', False)
    
    def _get_local_embedding(self, text: str) -> List[float]:
        """Generate embedding using local sentence-transformers model."""
        if self.embedding_model is None:
            raise RuntimeError("Local embedding model not initialized")
        return self.embedding_model.encode(text).tolist()
    
    def _rate_limit_wait(self):
        """Wait to respect Gemini API rate limit (30 RPM)."""
        time.sleep(EMBEDDING_RATE_LIMIT_DELAY)
    
    def _get_embedding_with_retry(self, text: str, doc_id: str = "unknown") -> Optional[List[float]]:
        """
        Generate embedding with retry logic for rate limits.
        
        Uses local embeddings (fast, no limits) or Gemini API (rate limited).
        
        Args:
            text: Text to embed
            doc_id: Document ID for logging
            
        Returns:
            Embedding vector or None if all retries failed
        """
        # Use local embeddings (recommended - no API limits!)
        if USE_LOCAL_EMBEDDINGS and self.embedding_model is not None:
            try:
                return self._get_local_embedding(text)
            except Exception as e:
                logger.error(f"Local embedding failed for {doc_id}: {e}")
                return None
        
        # Fall back to Gemini API embeddings
        for attempt in range(MAX_RETRIES):
            try:
                result = genai.embed_content(
                    model=EMBEDDING_MODEL,
                    content=text,
                    task_type="retrieval_document"
                )
                return result['embedding']
                
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "quota" in error_str.lower() or "rate" in error_str.lower():
                    # Rate limited - backoff exponentially
                    backoff = INITIAL_BACKOFF * (2 ** attempt)
                    logger.warning(f"Rate limited on {doc_id}, attempt {attempt + 1}/{MAX_RETRIES}. Waiting {backoff:.1f}s...")
                    time.sleep(backoff)
                else:
                    # Other error - log and fail
                    logger.error(f"Failed to embed {doc_id}: {e}")
                    return None
        
        logger.error(f"Max retries exceeded for {doc_id}")
        return None
    
    def _get_embedding(self, text: str, apply_rate_limit: bool = False) -> List[float]:
        """
        Generate embedding for text.
        
        Uses local embeddings (fast, no limits) or Gemini API (rate limited).
        
        Args:
            text: Text to embed
            apply_rate_limit: Whether to wait before making the request (Gemini only)
            
        Returns:
            Embedding vector as list of floats
        """
        # Use local embeddings (recommended - no API limits!)
        if USE_LOCAL_EMBEDDINGS and self.embedding_model is not None:
            return self._get_local_embedding(text)
        
        # Fall back to Gemini API
        if apply_rate_limit:
            self._rate_limit_wait()
            
        result = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    
    def _get_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding for query.
        
        Uses local embeddings (fast, no limits) or Gemini API.
        
        Args:
            query: Search query
            
        Returns:
            Embedding vector as list of floats
        """
        # Use local embeddings (recommended - no API limits!)
        if USE_LOCAL_EMBEDDINGS and self.embedding_model is not None:
            return self._get_local_embedding(query)
        
        # Fall back to Gemini API
        result = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=query,
            task_type="retrieval_query"
        )
        return result['embedding']
    
    def add_document(
        self,
        doc_id: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Add a document to the vector store.
        
        Args:
            doc_id: Unique document identifier
            content: Document text content
            metadata: Optional metadata (source, module, title, etc.)
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_initialized:
            logger.error("RAG service not initialized")
            return False
        
        try:
            # Generate embedding
            embedding = self._get_embedding(content)
            
            # Add to collection
            self.collection.add(
                ids=[doc_id],
                embeddings=[embedding],
                documents=[content],
                metadatas=[metadata or {}]
            )
            
            logger.debug(f"Added document {doc_id} to vector store")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add document {doc_id}: {e}")
            return False
    
    def add_documents_batch(
        self,
        documents: List[Dict[str, Any]]
    ) -> int:
        """
        Add multiple documents in batch with rate limiting and retry logic.
        
        Args:
            documents: List of dicts with 'id', 'content', and optional 'metadata'
            
        Returns:
            Number of documents successfully added
        """
        if not self.is_initialized:
            logger.error("RAG service not initialized")
            return 0
        
        ids = []
        embeddings = []
        contents = []
        metadatas = []
        
        total = len(documents)
        failed = 0
        
        logger.info(f"Starting batch embedding of {total} documents (rate limited to ~30 RPM)...")
        start_time = time.time()
        
        for i, doc in enumerate(documents):
            doc_id = doc.get('id', f'doc_{i}')
            
            # Rate limit: wait before each request (except first)
            if i > 0:
                self._rate_limit_wait()
            
            # Get embedding with retry logic
            embedding = self._get_embedding_with_retry(doc['content'], doc_id)
            
            if embedding:
                ids.append(doc_id)
                embeddings.append(embedding)
                contents.append(doc['content'])
                metadatas.append(doc.get('metadata', {}))
            else:
                failed += 1
            
            # Log progress every 10 documents
            if (i + 1) % 10 == 0:
                elapsed = time.time() - start_time
                rate = (i + 1) / elapsed * 60 if elapsed > 0 else 0
                eta = (total - i - 1) / rate * 60 if rate > 0 else 0
                logger.info(f"Progress: {i + 1}/{total} ({rate:.1f} RPM, ETA: {eta:.0f}s)")
        
        # Add all successful embeddings to collection
        if ids:
            try:
                self.collection.add(
                    ids=ids,
                    embeddings=embeddings,
                    documents=contents,
                    metadatas=metadatas
                )
                elapsed = time.time() - start_time
                logger.info(f"Added {len(ids)} documents to vector store in {elapsed:.1f}s ({failed} failed)")
                return len(ids)
            except Exception as e:
                logger.error(f"Failed to add batch: {e}")
                return 0
        
        logger.warning(f"No documents were successfully embedded ({failed} failed)")
        return 0
    
    def search(
        self,
        query: str,
        n_results: int = 3,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant documents using semantic search.
        
        Args:
            query: Search query
            n_results: Number of results to return
            filter_metadata: Optional metadata filter
            
        Returns:
            List of matching documents with scores
        """
        if not self.is_initialized:
            logger.warning("RAG service not initialized - returning empty results")
            return []
        
        try:
            # Generate query embedding
            query_embedding = self._get_query_embedding(query)
            
            # Search collection
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=filter_metadata
            )
            
            # Format results
            documents = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    documents.append({
                        'id': results['ids'][0][i] if results['ids'] else None,
                        'content': doc,
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                        'distance': results['distances'][0][i] if results['distances'] else None
                    })
            
            return documents
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    def generate_response(
        self,
        query: str,
        context_docs: List[Dict[str, Any]],
        user_profile: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a response using Gemini with retrieved context.
        
        Args:
            query: User's question
            context_docs: Retrieved relevant documents
            user_profile: Optional user profile for personalization
            
        Returns:
            Dict with 'response' text and 'sources' list
        """
        if not self.is_initialized:
            return {
                "response": "I'm sorry, the AI service is not available right now. Please check that the GEMINI_API_KEY is configured.",
                "sources": []
            }
        
        # Build context from retrieved documents
        context_parts = []
        sources = []
        
        for doc in context_docs:
            content = doc.get('content', '')
            metadata = doc.get('metadata', {})
            
            # Add to context
            source_info = metadata.get('source', 'textbook')
            module = metadata.get('module', '')
            title = metadata.get('title', '')
            
            context_parts.append(f"[Source: {module} - {title}]\n{content}")
            
            if source_info:
                sources.append({
                    'module': module,
                    'title': title,
                    'source': source_info
                })
        
        context_text = "\n\n---\n\n".join(context_parts)
        
        # Build personalization hint
        personalization = ""
        if user_profile:
            level = user_profile.get('programming_level', 'beginner')
            goal = user_profile.get('learning_goal', 'learning')
            personalization = f"\nThe user is at {level} programming level and their learning goal is {goal}. Adjust your explanation accordingly."
        
        # Build the prompt
        system_prompt = f"""You are an expert AI tutor for the Physical AI Humanoid Robotics Textbook. 
Your role is to help students learn about ROS 2, simulation (Gazebo, Unity), NVIDIA Isaac, and Vision-Language-Action models.

Use the following context from the textbook to answer the question. If the context doesn't contain relevant information, 
say so and provide general guidance based on your knowledge of robotics.

Be concise but thorough. Use examples when helpful. Reference specific modules or sections when relevant.
{personalization}

CONTEXT FROM TEXTBOOK:
{context_text}

---

USER QUESTION: {query}

Provide a helpful, educational response:"""

        try:
            # Generate response with Gemini
            response = self.chat_model.generate_content(system_prompt)
            
            return {
                "response": response.text,
                "sources": sources
            }
            
        except Exception as e:
            error_str = str(e).lower()
            logger.error(f"Failed to generate response: {e}")
            
            # User-friendly error messages based on error type
            if "429" in str(e) or "quota" in error_str or "rate" in error_str:
                if "daily" in error_str or "limit: 0" in error_str:
                    user_message = "⚠️ Daily API quota has been exceeded. Please try again tomorrow or contact the administrator."
                else:
                    user_message = "⚠️ Too many requests. Please wait a moment and try again."
            elif "401" in str(e) or "403" in str(e) or "api key" in error_str or "authentication" in error_str:
                user_message = "⚠️ API authentication failed. Please contact the administrator."
            elif "timeout" in error_str or "timed out" in error_str:
                user_message = "⚠️ Request timed out. Please try again."
            elif "connection" in error_str or "network" in error_str:
                user_message = "⚠️ Connection failed. Please check your internet and try again."
            elif "404" in str(e) or "not found" in error_str:
                user_message = "⚠️ AI model not available. Please contact the administrator."
            else:
                user_message = "⚠️ Unable to generate a response right now. Please try again later."
            
            return {
                "response": user_message,
                "sources": [],
                "error": True
            }
    
    def chat(
        self,
        query: str,
        user_profile: Optional[Dict[str, Any]] = None,
        n_context_docs: int = 3
    ) -> Dict[str, Any]:
        """
        Complete RAG pipeline: search + generate response.
        
        Args:
            query: User's question
            user_profile: Optional user profile for personalization
            n_context_docs: Number of context documents to retrieve
            
        Returns:
            Dict with 'response', 'sources', and 'context_used'
        """
        # Search for relevant documents
        context_docs = self.search(query, n_results=n_context_docs)
        
        # Generate response
        result = self.generate_response(query, context_docs, user_profile)
        
        # Add context info
        result['context_used'] = len(context_docs) > 0
        
        return result
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store."""
        if not self.is_initialized:
            return {"initialized": False, "document_count": 0}
        
        return {
            "initialized": True,
            "document_count": self.collection.count(),
            "collection_name": COLLECTION_NAME
        }
    
    def clear_collection(self) -> bool:
        """Clear all documents from the collection."""
        if not self.is_initialized:
            return False
        
        try:
            # Delete and recreate collection
            self.chroma_client.delete_collection(COLLECTION_NAME)
            self.collection = self.chroma_client.create_collection(
                name=COLLECTION_NAME,
                metadata={"description": "Physical AI Humanoid Robotics Textbook content"}
            )
            logger.info("Cleared vector store collection")
            return True
        except Exception as e:
            logger.error(f"Failed to clear collection: {e}")
            return False


# Singleton instance
_rag_service: Optional[RAGService] = None


def get_rag_service() -> RAGService:
    """Get or create the RAG service singleton."""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service
