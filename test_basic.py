from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_openapi():
    r = client.get("/openapi.json")
    assert r.status_code == 200

def test_health():
    r = client.get("/docs")
    assert r.status_code == 200
