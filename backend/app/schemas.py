from pydantic import BaseModel
import datetime


class PointBase(BaseModel):
    description: str
    latitude: str
    longitude: str


class PointCreate(PointBase):
    pass


class Point(PointBase):
    id: int
    created_at: datetime.datetime
    user_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
