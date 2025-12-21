"""Test RAG functionality."""
import requests
import sys

BASE_URL = "http://localhost:8001/api/v1"

def test_stats():
    """Check RAG stats."""
    print("Testing /chat/stats...")
    try:
        r = requests.get(f"{BASE_URL}/chat/stats", timeout=10)
        print(f"Status: {r.status_code}")
        print(f"Response: {r.json()}")
        return r.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_chat(query: str):
    """Test chat query."""
    print(f"\nTesting chat with query: '{query}'")
    try:
        r = requests.post(
            f"{BASE_URL}/chat/",
            json={"message": query},
            timeout=60
        )
        print(f"Status: {r.status_code}")
        data = r.json()
        print(f"Response: {data.get('response', data)[:500]}...")
        if data.get('sources'):
            print(f"Sources: {len(data['sources'])} documents")
        return r.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("RAG Test Suite")
    print("=" * 50)
    
    # Test stats
    if not test_stats():
        print("\n❌ Stats check failed. Is the server running?")
        sys.exit(1)
    
    # Test chat
    queries = [
        "What is ROS2?",
        "Explain digital twin simulation",
        "What is NVIDIA Isaac?"
    ]
    
    for query in queries:
        test_chat(query)
    
    print("\n✅ All tests completed!")
