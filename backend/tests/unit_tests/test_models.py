import pytest
from datetime import datetime
from sqlalchemy import create_engine
import sys
import os
from sqlmodel import Session

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.models import User, PointOfInterest
from unit_tests.db_config import SQLALCHEMY_DATABASE_URL, base

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


@pytest.fixture(scope="function")
def session():
    """
    Fixture that creates a new session for each test function.
    """
    session = Session(engine)
    yield session
    session.rollback()


def test_create_user(session):
    """
    Test case for creating a new user.
    """
    user = User(username="testuser", hashed_password="hashed_password")
    session.add(user)
    session.commit()

    retrieved_user = session.get(User, user.id)
    assert retrieved_user is not None
    assert retrieved_user.username == "testuser"
    assert retrieved_user.hashed_password == "hashed_password"


def test_create_point_of_interest(session):
    """
    Test case for creating a new point of interest.
    """
    user = User(username="testuser2", hashed_password="hashed_password")
    session.add(user)
    session.commit()

    poi = PointOfInterest(
        description="Test POI",
        latitude="12.34",
        longitude="56.78",
        created_at=datetime.now(),
        user_id=user.id,
    )
    session.add(poi)
    session.commit()

    retrieved_poi = session.get(PointOfInterest, poi.id)
    assert retrieved_poi is not None
    assert retrieved_poi.description == "Test POI"
    assert retrieved_poi.latitude == "12.34"
    assert retrieved_poi.longitude == "56.78"
    assert retrieved_poi.user_id == user.id


def test_relationship(session):
    """
    Test case for testing the relationship between user and point of interest.
    """
    user = User(username="testuser3", hashed_password="hashed_password")
    poi = PointOfInterest(
        description="Test POI",
        latitude="12.34",
        longitude="56.78",
        created_at=datetime.now(),
    )
    user.points_of_interest.append(poi)

    poi2 = PointOfInterest(
        description="Test POI 2",
        latitude="12.34",
        longitude="56.78",
        created_at=datetime.now(),
    )
    user.points_of_interest.append(poi2)
    session.add(user)
    session.commit()

    retrieved_user = session.get(User, user.id)
    assert len(retrieved_user.points_of_interest) == 2
    assert retrieved_user.points_of_interest[0].description == "Test POI"


def test_retrieve_non_existent_user(session):
    """
    Test case for retrieving a non-existent user.
    """
    non_existent_user = session.get(User, 9999)
    assert non_existent_user is None


def test_retrieve_non_existent_poi(session):
    """
    Test case for retrieving a non-existent point of interest.
    """
    non_existent_poi = session.get(PointOfInterest, 9999)
    assert non_existent_poi is None


def test_update_user(session):
    """
    Test case for updating a user.
    """
    user = User(username="testuser_update", hashed_password="hashed_password")
    session.add(user)
    session.commit()

    user.username = "updated_user"
    session.commit()

    retrieved_user = session.get(User, user.id)
    assert retrieved_user.username == "updated_user"


def test_delete_user(session):
    """
    Test case for deleting a user.
    """
    user = User(username="testuser_delete", hashed_password="hashed_password")
    session.add(user)
    session.commit()

    session.delete(user)
    session.commit()

    retrieved_user = session.get(User, user.id)
    assert retrieved_user is None


def test_update_point_of_interest(session):
    """
    Test case for updating a point of interest.
    """
    user = User(username="testuser_poi_update", hashed_password="hashed_password")
    session.add(user)
    session.commit()

    poi = PointOfInterest(
        description="Test POI",
        latitude="12.34",
        longitude="56.78",
        created_at=datetime.now(),
        user_id=user.id,
    )
    session.add(poi)
    session.commit()

    poi.description = "Updated POI"
    session.commit()

    retrieved_poi = session.get(PointOfInterest, poi.id)
    assert retrieved_poi.description == "Updated POI"


def test_delete_point_of_interest(session):
    """
    Test case for deleting a point of interest.
    """
    user = User(username="testuser_poi_delete", hashed_password="hashed_password")
    session.add(user)
    session.commit()

    poi = PointOfInterest(
        description="Test POI",
        latitude="12.34",
        longitude="56.78",
        created_at=datetime.now(),
        user_id=user.id,
    )
    session.add(poi)
    session.commit()

    session.delete(poi)
    session.commit()

    retrieved_poi = session.get(PointOfInterest, poi.id)
    assert retrieved_poi is None
