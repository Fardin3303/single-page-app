from pydantic import BaseModel, ConfigDict
import datetime


class PointBase(BaseModel):
    description: str
    latitude: str
    longitude: str


class PointCreate(PointBase):
    id: int
    created_at: datetime.datetime


class Point(PointBase):
    id: int
    created_at: datetime.datetime
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str
