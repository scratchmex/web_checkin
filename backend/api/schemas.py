from typing import List

import datetime
from pydantic import BaseModel  # pylint: disable=no-name-in-module


class Message(BaseModel):
    message: str = None


class BaseItem(BaseModel):
    class Config:
        orm_mode = True


class User(BaseItem):
    id: int
    name: str


class Event(BaseItem):
    id: int = None
    date: datetime.date = None
    title: str


class CheckIn(BaseItem):
    user_id: int
    event_id: int


class UserDB(User):
    events_attended: List[Event]


class EventDB(Event):
    attendants: List[User]
