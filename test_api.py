
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Welcome to Student Management API"
    }


def test_invalid_student():
    response = client.get("/students/999999")

    assert response.status_code == 404


def test_sync():
    response = client.get("/sync")

    assert response.status_code == 200


def test_async():
    response = client.get("/async")

    assert response.status_code == 200
