from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext
import traceback

from app import custom_logging

LOGGER = custom_logging.get_logger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def handle_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            LOGGER.error(f"An error occurred in {func.__name__}: {e}")
            traceback.print_exc()
            return None

    return wrapper


@handle_exception
def get_user(db: Session, user_id: int) -> models.User | None:
    """
    Retrieve a user from the database by user ID.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to retrieve.

    Returns:
        models.User: The user object if found, None otherwise.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


@handle_exception
def get_user_by_username(db: Session, username: str) -> models.User | None:
    """
    Retrieve a user from the database by username.

    Args:
        db (Session): The database session.
        username (str): The username of the user to retrieve.

    Returns:
        models.User: The user object if found, None otherwise.
    """
    return db.query(models.User).filter(models.User.username == username).first()


@handle_exception
def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    Create a new user in the database.

    Args:
        db (Session): The database session.
        user (schemas.UserCreate): The user data to create.

    Returns:
        models.User: The created user object.
    """
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    LOGGER.info(f"User {user.username} created")
    return db_user


@handle_exception
def create_point(
    db: Session, point: schemas.PointCreate, user_id: int
) -> models.PointOfInterest:
    """
    Create a new point of interest in the database.

    Args:
        db (Session): The database session.
        point (schemas.PointCreate): The point of interest data to create.
        user_id (int): The ID of the user who owns the point of interest.

    Returns:
        models.PointOfInterest: The created point of interest object.
    """
    db_point = models.PointOfInterest(**point.model_dump(), user_id=user_id)
    db.add(db_point)
    db.commit()
    db.refresh(db_point)
    return db_point


@handle_exception
def get_points(db: Session) -> list[models.PointOfInterest]:
    """
    Retrieve all points of interest from the database.

    Args:
        db (Session): The database session.

    Returns:
        List[models.PointOfInterest]: A list of all points of interest.
    """
    return db.query(models.PointOfInterest).all()


@handle_exception
def get_points_by_user(db: Session, user_id: int) -> list[models.PointOfInterest]:
    """
    Retrieve all points of interest owned by a user from the database.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user.

    Returns:
        List[models.PointOfInterest]: A list of points of interest owned by the user.
    """
    return (
        db.query(models.PointOfInterest)
        .filter(models.PointOfInterest.user_id == user_id)
        .all()
    )


@handle_exception
def get_point_by_id(db: Session, point_id: int) -> models.PointOfInterest | None:
    """
    Retrieve a point of interest from the database by ID.

    Args:
        db (Session): The database session.
        point_id (int): The ID of the point of interest to retrieve.

    Returns:
        models.PointOfInterest: The point of interest object if found, None otherwise.
    """
    return (
        db.query(models.PointOfInterest)
        .filter(models.PointOfInterest.id == point_id)
        .first()
    )


@handle_exception
def delete_point(
    db: Session, point_id: int, user_id: int
) -> models.PointOfInterest | None:
    """
    Delete a point of interest from the database.

    Args:
        db (Session): The database session.
        point_id (int): The ID of the point of interest to delete.
        user_id (int): The ID of the user who owns the point of interest.

    Returns:
        models.PointOfInterest: The deleted point of interest object if found, None otherwise.
    """
    db_point = (
        db.query(models.PointOfInterest)
        .filter(
            models.PointOfInterest.id == point_id,
            models.PointOfInterest.user_id == user_id,
        )
        .first()
    )
    if db_point:
        db.delete(db_point)
        db.commit()
    return db_point


@handle_exception
def edit_point_description(
    db: Session, point_id: int, user_id: int, description: str
) -> models.PointOfInterest | None:
    """
    Edit the description of a point of interest in the database.

    Args:
        db (Session): The database session.
        point_id (int): The ID of the point of interest to edit.
        user_id (int): The ID of the user who owns the point of interest.
        description (str): The new description for the point of interest.

    Returns:
        models.PointOfInterest: The edited point of interest object if found, None otherwise.
    """
    db_point = (
        db.query(models.PointOfInterest)
        .filter(
            models.PointOfInterest.id == point_id,
            models.PointOfInterest.user_id == user_id,
        )
        .first()
    )
    if db_point:
        db_point.description = description
        db.commit()
    return db_point
