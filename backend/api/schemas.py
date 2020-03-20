from typing import List

import datetime
from pydantic import BaseModel  # pylint: disable=no-name-in-module


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


class EventOut(Event):
    id: int


class UserDB(User):
    events_attended: List[EventOut]


class EventDB(Event):
    id: int
    attendants: List[User]


class CheckInDB(CheckIn):
    date: datetime.datetime
