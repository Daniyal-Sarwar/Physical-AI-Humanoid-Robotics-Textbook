"""
Content Ingestion Service

Parses MDX files from the docs/ directory and ingests them into ChromaDB.
Chunks content for optimal retrieval and preserves metadata.
"""

import os
import re
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import json

logger = logging.getLogger(__name__)

# Chunk size for splitting documents (in characters)
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 200

# Module mapping for friendly names
MODULE_NAMES = {
    "module-1-ros2": "Module 1: ROS 2 Fundamentals",
    "module-2-simulation": "Module 2: Digital Twin Simulation",
    "module-3-isaac": "Module 3: NVIDIA Isaac Platform",
    "module-4-vla": "Module 4: Vision-Language-Action Models"
}


def clean_mdx_content(content: str) -> str:
    """
    Clean MDX content by removing JSX components, imports, and formatting.
    
    Args:
        content: Raw MDX content
        
    Returns:
        Cleaned plain text
    """
    # Remove MDX imports
    content = re.sub(r'^import\s+.*$', '', content, flags=re.MULTILINE)
    
    # Remove JSX/TSX components like <Component />
    content = re.sub(r'<[A-Z][^>]*/?>', '', content)
    content = re.sub(r'</[A-Z][^>]*>', '', content)
    
    # Remove JSX expressions like {expression}
    content = re.sub(r'\{[^}]+\}', '', content)
    
    # Remove code block language specifiers but keep content
    content = re.sub(r'```\w+', '```', content)
    
    # Remove frontmatter (YAML between ---)
    content = re.sub(r'^---[\s\S]*?---', '', content)
    
    # Remove HTML comments
    content = re.sub(r'<!--[\s\S]*?-->', '', content)
    
    # Normalize whitespace
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = content.strip()
    
    return content


def extract_title_from_mdx(content: str, filename: str) -> str:
    """
    Extract title from MDX content.
    
    Args:
        content: MDX content
        filename: Filename as fallback
        
    Returns:
        Document title
    """
    # Try to find title in frontmatter
    frontmatter_match = re.search(r'^---[\s\S]*?title:\s*["\']?([^"\'\n]+)["\']?[\s\S]*?---', content)
    if frontmatter_match:
        return frontmatter_match.group(1).strip()
    
    # Try to find first H1 header
    h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if h1_match:
        return h1_match.group(1).strip()
    
    # Use filename as fallback
    name = Path(filename).stem
    # Remove number prefix like "01-"
    name = re.sub(r'^\d+-', '', name)
    # Convert to title case
    return name.replace('-', ' ').replace('_', ' ').title()


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """
    Split text into overlapping chunks.
    
    Args:
        text: Text to chunk
        chunk_size: Maximum chunk size
        overlap: Overlap between chunks
        
    Returns:
        List of text chunks
    """
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # Try to break at sentence boundary
        if end < len(text):
            # Look for sentence endings
            for boundary in ['. ', '.\n', '? ', '?\n', '! ', '!\n', '\n\n']:
                last_boundary = text.rfind(boundary, start, end)
                if last_boundary > start + chunk_size // 2:
                    end = last_boundary + len(boundary)
                    break
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        start = end - overlap
    
    return chunks


def parse_mdx_file(filepath: Path) -> List[Dict[str, Any]]:
    """
    Parse an MDX file and return chunked documents.
    
    Args:
        filepath: Path to MDX file
        
    Returns:
        List of document chunks with metadata
    """
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        logger.error(f"Failed to read {filepath}: {e}")
        return []
    
    # Extract metadata
    title = extract_title_from_mdx(content, filepath.name)
    
    # Determine module from path
    module_dir = filepath.parent.name
    module_name = MODULE_NAMES.get(module_dir, module_dir)
    
    # Clean content
    cleaned = clean_mdx_content(content)
    
    if not cleaned:
        logger.warning(f"No content after cleaning {filepath}")
        return []
    
    # Chunk the content
    chunks = chunk_text(cleaned)
    
    documents = []
    for i, chunk in enumerate(chunks):
        doc_id = f"{module_dir}/{filepath.stem}_chunk_{i}"
        documents.append({
            "id": doc_id,
            "content": chunk,
            "metadata": {
                "source": str(filepath.relative_to(filepath.parent.parent.parent)),
                "module": module_name,
                "module_dir": module_dir,
                "title": title,
                "chunk_index": i,
                "total_chunks": len(chunks),
                "filename": filepath.name
            }
        })
    
    return documents


def discover_mdx_files(docs_dir: Path) -> List[Path]:
    """
    Discover all MDX files in the docs directory.
    
    Args:
        docs_dir: Path to docs directory
        
    Returns:
        List of MDX file paths
    """
    mdx_files = []
    
    # Look in module directories
    for module_dir in docs_dir.iterdir():
        if module_dir.is_dir() and module_dir.name.startswith('module-'):
            for mdx_file in module_dir.glob('*.mdx'):
                mdx_files.append(mdx_file)
    
    # Also include top-level docs
    for mdx_file in docs_dir.glob('*.mdx'):
        mdx_files.append(mdx_file)
    
    for md_file in docs_dir.glob('*.md'):
        mdx_files.append(md_file)
    
    return sorted(mdx_files)


def ingest_textbook_content(
    docs_dir: Optional[str] = None,
    clear_existing: bool = False
) -> Dict[str, Any]:
    """
    Ingest all textbook content into the RAG vector store.
    
    Args:
        docs_dir: Path to docs directory. Defaults to repo docs/
        clear_existing: Whether to clear existing documents first
        
    Returns:
        Ingestion statistics
    """
    from .rag_service import get_rag_service
    
    rag_service = get_rag_service()
    
    if not rag_service.is_initialized:
        return {
            "success": False,
            "error": "RAG service not initialized. Check GEMINI_API_KEY.",
            "documents_added": 0
        }
    
    # Determine docs directory
    if docs_dir is None:
        # Default to repo root docs/
        backend_dir = Path(__file__).parent.parent.parent
        docs_path = backend_dir.parent / "docs"
    else:
        docs_path = Path(docs_dir)
    
    if not docs_path.exists():
        return {
            "success": False,
            "error": f"Docs directory not found: {docs_path}",
            "documents_added": 0
        }
    
    # Clear existing if requested
    if clear_existing:
        rag_service.clear_collection()
        logger.info("Cleared existing documents")
    
    # Discover MDX files
    mdx_files = discover_mdx_files(docs_path)
    logger.info(f"Found {len(mdx_files)} MDX/MD files to process")
    
    # Parse and collect all documents
    all_documents = []
    files_processed = 0
    
    for mdx_file in mdx_files:
        docs = parse_mdx_file(mdx_file)
        if docs:
            all_documents.extend(docs)
            files_processed += 1
            logger.debug(f"Parsed {mdx_file.name}: {len(docs)} chunks")
    
    # Batch add to vector store
    if all_documents:
        added = rag_service.add_documents_batch(all_documents)
    else:
        added = 0
    
    stats = rag_service.get_stats()
    
    return {
        "success": True,
        "files_found": len(mdx_files),
        "files_processed": files_processed,
        "chunks_created": len(all_documents),
        "documents_added": added,
        "total_in_store": stats.get("document_count", 0)
    }


def get_ingestion_status() -> Dict[str, Any]:
    """Get current ingestion status."""
    from .rag_service import get_rag_service
    
    rag_service = get_rag_service()
    return rag_service.get_stats()


# CLI for manual ingestion
if __name__ == "__main__":
    import sys
    from dotenv import load_dotenv
    
    # Load environment variables
    backend_dir = Path(__file__).parent.parent.parent
    load_dotenv(backend_dir / ".env")
    
    logging.basicConfig(level=logging.INFO)
    
    print("Starting content ingestion...")
    
    # Check for --clear flag
    clear = "--clear" in sys.argv
    
    result = ingest_textbook_content(clear_existing=clear)
    
    print(f"\nIngestion Results:")
    print(f"  Success: {result.get('success')}")
    print(f"  Files found: {result.get('files_found', 0)}")
    print(f"  Files processed: {result.get('files_processed', 0)}")
    print(f"  Chunks created: {result.get('chunks_created', 0)}")
    print(f"  Documents added: {result.get('documents_added', 0)}")
    print(f"  Total in store: {result.get('total_in_store', 0)}")
    
    if not result.get('success'):
        print(f"  Error: {result.get('error')}")
        sys.exit(1)
