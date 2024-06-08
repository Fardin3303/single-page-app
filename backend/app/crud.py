from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_point(db: Session, point: schemas.PointCreate, user_id: int):
    db_point = models.PointOfInterest(**point.dict(), user_id=user_id)
    db.add(db_point)
    db.commit()
    db.refresh(db_point)
    return db_point


def get_points(db: Session):
    return db.query(models.PointOfInterest).all()


def get_points_by_user(db: Session, user_id: int):
    return (
        db.query(models.PointOfInterest)
        .filter(models.PointOfInterest.user_id == user_id)
        .all()
    )


def delete_point(db: Session, point_id: int, user_id: int):
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
