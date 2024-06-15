import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_db
from tests.unit_tests.db_config import TestingSessionLocal, engine, base, override_get_db


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def clear_data_after_tests(request):
    """
    Fixture that clears the data in the database after running the tests.
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
def test_db():
    """
    Fixture that creates the necessary database tables for testing.
    """
    base.metadata.create_all(bind=engine)
    yield
    base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Fixture that provides a TestingSessionLocal instance for each test function.
    """
    session = TestingSessionLocal()
    yield session
    session.close()


def test_create_user():
    """
    Test case for creating a new user.
    """
    response = client.post(
        "/users/", json={"username": "testuser3", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser3"


def test_create_existing_user():
    """
    Test case for creating a user with an existing username.
    """
    response = client.post(
        "/users/", json={"username": "testuser3", "password": "testpassword"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already registered"}


def test_login_for_access_token():
    """
    Test case for logging in and obtaining an access token.
    """
    response = client.post(
        "/token", data={"username": "testuser3", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_incorrect_login():
    """
    Test case for logging in with incorrect credentials.
    """
    response = client.post(
        "/token", data={"username": "wronguser", "password": "wrongpassword"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect username or password"}
