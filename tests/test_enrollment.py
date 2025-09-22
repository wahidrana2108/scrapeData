from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_student():
    response = client.post("/students", json={"name": "Test Student", "email": "test@student.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Student"

def test_create_course():
    response = client.post("/courses", json={"name": "Math", "capacity": 2})
    assert response.status_code == 200
    data = response.json()
    assert data["capacity"] == 2
