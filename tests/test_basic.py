from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_openapi():
    """Test OpenAPI documentation is available."""
    response = client.get("/openapi.json")
    assert response.status_code == 200

def test_docs():
    """Test Swagger UI is available."""
    response = client.get("/docs")
    assert response.status_code == 200
