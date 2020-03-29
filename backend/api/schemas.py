from typing import List, Any

import datetime
from pydantic import BaseModel  # pylint: disable=no-name-in-module


# Base schemas
class Message(BaseModel):
    message: str


class BaseItem(BaseModel):
    class Config:
        orm_mode = True


class User(BaseItem):
    id: int
    name: str


class Event(BaseItem):
    date: datetime.datetime
    title: str


class CheckIn(BaseItem):
    user_id: int
    event_id: int


class Token(BaseItem):
    sub: str
    iss: str
    exp: int
    iat: int
    data: Any = None


class Admin(BaseItem):
    name: str
    username: str


# In schemas
class AdminIn(Admin):
    password: str


# Out schemas
class EventOut(Event):
    id: int


class AdminOut(Admin):
    id: int


# DB schemas
class UserDB(User):
    attended_events: List[EventOut]


class EventDB(Event):
    id: int
    attendants: List[User]


class CheckInDB(CheckIn):
    date: datetime.datetime


class AdminDB(AdminOut):
    hashed_password: str
