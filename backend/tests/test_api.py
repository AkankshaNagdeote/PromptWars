import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """
    Test the health endpoint for availability.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

# A basic test for the chat endpoint structure.
# Actual LLM calls should be mocked in a real test suite to preserve API quotas.
def test_chat_endpoint_validation():
    """
    Test that the chat endpoint correctly validates missing inputs.
    """
    response = client.post("/api/chat", json={})
    assert response.status_code == 422 # Unprocessable Entity
