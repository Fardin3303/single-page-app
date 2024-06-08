from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.dependencies import get_db, get_current_user
from typing import List

router = APIRouter()

@router.post("/points/", response_model=schemas.Point)
def create_point(point: schemas.PointCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_point(db=db, point=point, user_id=current_user.id)

@router.get("/points/", response_model=List[schemas.Point])
def read_points(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    points = crud.get_points(db)
    return points

@router.delete("/points/{point_id}", response_model=schemas.Point)
def delete_point(point_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_point = crud.delete_point(db=db, point_id=point_id, user_id=current_user.id)
    if db_point is None:
        raise HTTPException(status_code=404, detail="Point not found")
    return db_point
