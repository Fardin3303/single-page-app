from pydantic import BaseModel, ConfigDict
import datetime


class PointBase(BaseModel):
    """
    Base model for a point.
    """
    description: str
    latitude: str
    longitude: str


class PointCreate(PointBase):
    """
    Model for creating a point.
    Inherits from PointBase.
    """
    id: int
    created_at: datetime.datetime


class Point(PointBase):
    """
    Model for a point.
    Inherits from PointBase.
    """
    id: int
    created_at: datetime.datetime
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class PointUpdate(BaseModel):
    """
    Model for updating a point.
    """
    description: str

class UserBase(BaseModel):
    """
    Base model for a user.
    """
    username: str


class UserCreate(UserBase):
    """
    Model for creating a user.
    Inherits from UserBase.
    """
    password: str


class User(UserBase):
    """
    Model for a user.
    Inherits from UserBase.
    """
    id: int

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """
    Model for a token.
    """
    access_token: str
    token_type: str
