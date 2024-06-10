from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.dependencies import get_db, get_current_user
from typing import List

router = APIRouter()


@router.post("/points/", response_model=schemas.Point)
def create_point(
    point: schemas.PointCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> schemas.Point:
    """
    Create a new point.

    Args:
        point (schemas.PointCreate): The data for the new point.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (models.User, optional): The current user. Defaults to Depends(get_current_user).

    Returns:
        schemas.Point: The created point.
    """
    return crud.create_point(db=db, point=point, user_id=current_user.id)


@router.get("/points/", response_model=List[schemas.Point])
def read_points(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> List[schemas.Point]:
    """
    Read a list of points.

    Args:
        skip (int, optional): Number of points to skip. Defaults to 0.
        limit (int, optional): Maximum number of points to retrieve. Defaults to 10.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        List[schemas.Point]: The list of points.
    """
    points = crud.get_points(db)
    return points


@router.delete("/points/{point_id}", response_model=schemas.Point)
def delete_point(
    point_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> schemas.Point:
    """
    Delete a point.

    Args:
        point_id (int): The ID of the point to delete.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (models.User, optional): The current user. Defaults to Depends(get_current_user).

    Returns:
        schemas.Point: The deleted point.
    
    Raises:
        HTTPException: If the point is not found or if the user is not authorized to delete the point.
    """
    db_point = crud.get_point_by_id(db=db, point_id=point_id)
    
    if db_point is None:
        raise HTTPException(status_code=404, detail="Point not found")
    
    if db_point.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this point")
    
    deleted_point = crud.delete_point(db=db, point_id=point_id, user_id=current_user.id)
    return deleted_point


@router.put("/points/{point_id}", response_model=schemas.Point)
def update_point(
    point_id: int,
    description: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> schemas.Point:
    """
    Update a point's description.

    Args:
        point_id (int): The ID of the point to update.
        description (str): The new description for the point.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (models.User, optional): The current user. Defaults to Depends(get_current_user).

    Returns:
        schemas.Point: The updated point.
    
    Raises:
        HTTPException: If the point is not found or if the user is not authorized to update the point.
    """

    db_point = crud.get_point_by_id(db=db, point_id=point_id)
    if db_point is None:
        raise HTTPException(status_code=404, detail="Point not found")
    if db_point.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this point")

    updated_point = crud.edit_point_description(db=db, point_id=point_id, description=description, user_id=current_user.id)
    return updated_point
