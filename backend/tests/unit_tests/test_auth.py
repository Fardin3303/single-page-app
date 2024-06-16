import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlmodel import Session
from app.main import app
from app.dependencies import get_db
from app.crud import create_user as crud_create_user
from app.schemas import UserCreate
from tests.unit_tests.db_config import base, SQLALCHEMY_DATABASE_URL


engine = create_engine(SQLALCHEMY_DATABASE_URL)

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

def override_get_db():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def session():
    session = Session(engine)
    yield session
    session.rollback()

def test_create_user(client):
    user_data = {
        "username": "testuser_auth",
        "password": "testpassword"
    }
    
    response = client.post("/users/", json=user_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == user_data["username"]
    assert "id" in data

def test_create_existing_user(client, session):
    user_data = {
        "username": "existinguser",
        "password": "testpassword"
    }
    
    # Create user directly in the session
    crud_create_user(session, UserCreate(**user_data))
    
    response = client.post("/users/", json=user_data)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"

def test_login_for_access_token(client, session):
    user_data = {
        "username": "loginuser",
        "password": "loginpassword"
    }
    
    # Create user directly in the session
    crud_create_user(session, UserCreate(**user_data))
    
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }
    
    response = client.post("/token", data=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_for_access_token_invalid_credentials(client):
    login_data = {
        "username": "nonexistentuser",
        "password": "wrongpassword"
    }
    
    response = client.post("/token", data=login_data)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect username or password"
