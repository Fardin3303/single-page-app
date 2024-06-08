from database import SessionLocal
from fastapi import Depends
from sqlalchemy.orm import Session
import models

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(db: Session = Depends(get_db)):
    user = db.query(models.User).first()
    return user