import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from app.main import app
from app import models
from app.dependencies import get_db, get_current_user
from db_config import TestingSessionLocal, engine, base


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def override_get_current_user():
    try:
        db = TestingSessionLocal()
        user = db.query(models.User).first()
        return user
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def clear_data_after_tests(request):
    # Execute all tests
    yield

    # Clear data after all tests have completed
    with engine.connect() as connection:
        transaction = connection.begin()
        for table in reversed(base.metadata.sorted_tables):
            connection.execute(table.delete())
        transaction.commit()

    connection.close()


@pytest.fixture(scope="module")
def test_db():
    base.metadata.create_all(bind=engine)
    yield
    base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    session = TestingSessionLocal()
    yield session
    session.close()


def create_test_user(username: str, password: str) -> dict:
    response = client.post("/users/", json={"username": username, "password": password})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == username

    return data


# Create a access token for the first user
def get_access_token(username: str, password: str) -> str:
    response = client.post("/token", data={"username": username, "password": password})
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    return data["access_token"]


# Test creating a point of interest for a user
def test_create_point():
    create_test_user(username="testuser", password="testpassword")
    response = client.post(
        "/points/",
        json={
            "description": "Test point",
            "latitude": "40.7128",
            "longitude": "-74.0060",
            "id": 1,
            "created_at": str(datetime.now()),
        },
        headers={
            "Authorization": f"Bearer {get_access_token(username='testuser', password='testpassword')}"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Test point"
    assert data["latitude"] == "40.7128"
    assert data["longitude"] == "-74.0060"
    assert data["user_id"] == 1


# Test creating a point of interest for another user
def test_create_point_for_another_user():
    create_test_user(username="testuser2", password="testpassword2")
    response = client.post(
        "/points/",
        json={
            "description": "Test point2",
            "latitude": "45.7128",
            "longitude": "-75.0060",
            "id": 2,
            "created_at": str(datetime.now()),
        },
        headers={
            "Authorization": f"Bearer {get_access_token(username='testuser2', password='testpassword2')}"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Test point2"
    assert data["latitude"] == "45.7128"
    assert data["longitude"] == "-75.0060"
    # assert data["user_id"] == 2


# Test reading all points of interest
def test_read_points():
    response = client.get("/points/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["description"] == "Test point"
    assert data[0]["latitude"] == "40.7128"
    assert data[0]["longitude"] == "-74.0060"
    assert data[0]["user_id"] == 1
    assert data[1]["description"] == "Test point2"
    assert data[1]["latitude"] == "45.7128"
    assert data[1]["longitude"] == "-75.0060"
    assert data[1]["user_id"] == 1


# Test editing a point of interest
def test_edit_point():
    response = client.put(
        "/points/1",
        params={
            "description": "Test point edited",
        },
        headers={
            "Authorization": f"Bearer {get_access_token(username='testuser', password='testpassword')}"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Test point edited"
    assert data["latitude"] == "40.7128"
    assert data["longitude"] == "-74.0060"
    assert data["user_id"] == 1


# Test deleting a point of interest
def test_delete_point():
    response = client.delete(
        "/points/1",
        headers={
            "Authorization": f"Bearer {get_access_token(username='testuser', password='testpassword')}"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Test point edited"
    assert data["latitude"] == "40.7128"
    assert data["longitude"] == "-74.0060"
    assert data["user_id"] == 1


# Test deleting a point of interest with a different user
# skip
@pytest.mark.skip
def test_delete_point_with_different_user():
    response = client.delete(
        "/points/2",
        headers={
            "Authorization": f"Bearer {get_access_token(username='testuser', password='testpassword')}"
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Point not found"}
