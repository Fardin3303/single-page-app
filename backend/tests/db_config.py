from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app import models


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base = SQLModel

base.metadata.create_all(bind=engine)

def override_get_db():
    """
    Override the get_db dependency to use the TestingSessionLocal database.
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def override_get_current_user():
    """
    Override the get_current_user dependency to use the TestingSessionLocal database and return the first user.
    """
    try:
        db = TestingSessionLocal()
        user = db.query(models.User).first()
        if user is None:
            raise Exception("Test user not found")
        return user
    finally:
        db.close()
