import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_db
from passlib.context import CryptContext
from db_config import TestingSessionLocal, engine, base



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

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

def test_create_user():
    response = client.post(
        "/users/",
        json={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"

def test_create_existing_user():
    response = client.post(
        "/users/",
        json={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already registered"}

def test_login_for_access_token():
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_incorrect_login():
    response = client.post(
        "/token",
        data={"username": "wronguser", "password": "wrongpassword"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect username or password"}
