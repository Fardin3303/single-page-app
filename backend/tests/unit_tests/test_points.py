import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from app.main import app
from app.models import User, PointOfInterest
from app.dependencies import get_db, get_current_user
from datetime import datetime
from tests.unit_tests.db_config import SQLALCHEMY_DATABASE_URL, base


# Override the get_db dependency to use a test database
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SQLModel.metadata.create_all(bind=engine)


def override_get_db():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


app.dependency_overrides[get_db] = override_get_db


# Mock current user dependency
def override_get_current_user():
    return User(id=1, username="testuser", hashed_password="hashed_password")


app.dependency_overrides[get_current_user] = override_get_current_user


@pytest.fixture(scope="session", autouse=True)
def clear_data_after_tests(request):
    """
    Fixture to clear the data from the database after running the tests.
    """
    yield
    try:
        with engine.connect() as connection:
            transaction = connection.begin()
            for table in reversed(base.metadata.sorted_tables):
                connection.execute(table.delete())
            transaction.commit()
        connection.close()
    except Exception as e:
        print(e)


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def session():
    session = Session(engine)
    yield session
    session.rollback()


@pytest.fixture(scope="module")
def test_user(session):
    user = User(username="testuser", hashed_password="hashed_password")
    session.add(user)
    session.commit()
    return user


def test_create_point(client, session, test_user):
    point_data = {
        "description": "Test Point",
        "latitude": "12.34",
        "longitude": "56.78",
        "created_at": datetime.now().isoformat(),
    }

    response = client.post("/points/", json=point_data)

    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Test Point"
    assert data["latitude"] == "12.34"
    assert data["longitude"] == "56.78"
    assert data["user_id"] == test_user.id


def test_read_points(client, session, test_user):
    response = client.get("/points/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_delete_point(client, session, test_user):
    point = PointOfInterest(
        description="Test Point to Delete",
        latitude="12.34",
        longitude="56.78",
        created_at=datetime.now(),
        user_id=test_user.id,
    )
    session.add(point)
    session.commit()

    response = client.delete(f"/points/{point.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Test Point to Delete"


def test_update_point(client, session, test_user):
    point = PointOfInterest(
        description="Test Point to Update",
        latitude="12.34",
        longitude="56.78",
        created_at=datetime.now(),
        user_id=test_user.id,
    )
    session.add(point)
    session.commit()

    update_data = {"description": "Updated Test Point"}

    response = client.put(f"/points/{point.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Updated Test Point"


def test_delete_non_existent_point(client, session, test_user):
    response = client.delete("/points/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Point not found"


def test_update_non_existent_point(client, session, test_user):
    update_data = {"description": "Non-existent Point"}
    response = client.put("/points/9999", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Point not found"


def test_unauthorized_delete_point(client, session, test_user):
    another_user = User(username="anotheruser", hashed_password="hashed_password")
    session.add(another_user)
    session.commit()

    point = PointOfInterest(
        description="Another User's Point",
        latitude="12.34",
        longitude="56.78",
        created_at=datetime.now(),
        user_id=another_user.id,
    )
    session.add(point)
    session.commit()

    response = client.delete(f"/points/{point.id}")
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized to delete this point"


def test_unauthorized_update_point(client, session, test_user):
    another_user = User(username="anotheruser2", hashed_password="hashed_password")
    session.add(another_user)
    session.commit()

    point = PointOfInterest(
        description="Another User's Point",
        latitude="12.34",
        longitude="56.78",
        created_at=datetime.now(),
        user_id=another_user.id,
    )
    session.add(point)
    session.commit()

    update_data = {"description": "Attempt to update another user's point"}

    response = client.put(f"/points/{point.id}", json=update_data)
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized to update this point"
