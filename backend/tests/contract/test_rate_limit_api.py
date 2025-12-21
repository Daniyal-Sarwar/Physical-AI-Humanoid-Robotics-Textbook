"""
Contract Tests for Rate Limit API

Tests the GET /api/v1/rate-limit/status endpoint against
the OpenAPI contract.
"""

import pytest
from fastapi.testclient import TestClient


class TestRateLimitStatusEndpoint:
    """Contract tests for GET /api/v1/rate-limit/status."""
    
    def test_status_returns_200(self, client: TestClient):
        """Endpoint should return 200 OK."""
        response = client.get("/api/v1/rate-limit/status")
        assert response.status_code == 200
    
    def test_status_response_schema(self, client: TestClient):
        """Response should match RateLimitStatus schema."""
        response = client.get("/api/v1/rate-limit/status")
        data = response.json()
        
        # Required fields
        assert "remaining" in data
        assert "total" in data
        assert "reset_at" in data
        assert "is_authenticated" in data
        
        # Type checks
        assert isinstance(data["remaining"], int)
        assert isinstance(data["total"], int)
        assert isinstance(data["reset_at"], str)
        assert isinstance(data["is_authenticated"], bool)
    
    def test_status_anonymous_user(self, client: TestClient):
        """Anonymous user should get rate limit status."""
        response = client.get("/api/v1/rate-limit/status")
        data = response.json()
        
        assert data["is_authenticated"] is False
        assert data["remaining"] <= 5
        assert data["total"] == 5
    
    def test_status_with_fingerprint(self, client: TestClient):
        """Fingerprint header should be accepted."""
        response = client.get(
            "/api/v1/rate-limit/status",
            headers={"X-Fingerprint": "test-fingerprint-123"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["remaining"] == 5  # New fingerprint has full quota
    
    def test_status_authenticated_user(
        self,
        authenticated_client: TestClient
    ):
        """Authenticated user should have no rate limit."""
        response = authenticated_client.get("/api/v1/rate-limit/status")
        data = response.json()
        
        # Authenticated users are not rate limited
        assert response.status_code == 200
        assert data["remaining"] == 5
        assert data["total"] == 5
    
    def test_remaining_within_bounds(self, client: TestClient):
        """Remaining should be between 0 and total."""
        response = client.get("/api/v1/rate-limit/status")
        data = response.json()
        
        assert 0 <= data["remaining"] <= data["total"]
    
    def test_reset_at_is_valid_datetime(self, client: TestClient):
        """reset_at should be a valid ISO datetime string."""
        from datetime import datetime
        
        response = client.get("/api/v1/rate-limit/status")
        data = response.json()
        
        # Should parse without error
        datetime.fromisoformat(data["reset_at"].replace("Z", "+00:00"))
