from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int = Field(default=None, primary_key=True, index=True)
    username: str = Field(index=True, unique=True)
    hashed_password: Optional[str] = Field(default=None)
    points_of_interest: List["PointOfInterest"] = Relationship(back_populates="owner")

class PointOfInterest(SQLModel, table=True):
    __tablename__ = "points_of_interest"
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    description: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    created_at: Optional[datetime] = None
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")

    owner: Optional[User] = Relationship(back_populates="points_of_interest")
