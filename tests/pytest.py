import json
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from db import get_db
from models import base, course, student, enrollment

# --- Setup in-memory test DB ---
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base.Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


# --- Tests ---

def test_create_student():
    response = client.post("/students", json={"name": "Alice", "email": "alice@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"


def test_create_course():
    response = client.post("/courses", json={"title": "Python 101", "capacity": 1})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Python 101"
    assert data["capacity"] == 1


def test_enrollment_prevent_duplicate():
    # Create a student
    s = client.post("/students", json={"name": "Bob", "email": "bob@example.com"}).json()
    # Create a course
    c = client.post("/courses", json={"title": "Data Science", "capacity": 2}).json()
    # First enrollment
    r1 = client.post("/enrollments", json={"student_id": s["id"], "course_id": c["id"]})
    assert r1.status_code == 200
    # Duplicate enrollment should fail
    r2 = client.post("/enrollments", json={"student_id": s["id"], "course_id": c["id"]})
    assert r2.status_code == 400
    assert "already enrolled" in r2.json()["detail"]


def test_enrollment_capacity():
    # Course with capacity=1
    course_resp = client.post("/courses", json={"title": "ML Basics", "capacity": 1}).json()
    course_id = course_resp["id"]

    # Two students
    s1 = client.post("/students", json={"name": "Stu1", "email": "stu1@example.com"}).json()
    s2 = client.post("/students", json={"name": "Stu2", "email": "stu2@example.com"}).json()

    # First student enrolls → success
    r1 = client.post("/enrollments", json={"student_id": s1["id"], "course_id": course_id})
    assert r1.status_code == 200

    # Second student enrolls → fail
    r2 = client.post("/enrollments", json={"student_id": s2["id"], "course_id": course_id})
    assert r2.status_code == 400
    assert "capacity" in r2.json()["detail"]


def test_import_scraped_json(tmp_path):
    # Create a temporary scraped.json
    sample_data = [
        {"title": "Python Book", "url": "https://example.com/book", "category": "Books", "price": 20.5}
    ]
    file_path = tmp_path / "scraped.json"
    file_path.write_text(json.dumps(sample_data))

    # Replace with test file
    from api import routes
    routes.SCRAPED_JSON_PATH = str(file_path)

    # Call import endpoint
    resp = client.post("/import/scraped")
    assert resp.status_code == 200
    assert "imported successfully" in resp.json()["message"]
