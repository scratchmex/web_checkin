import datetime
from pydantic import BaseModel


class Message(BaseModel):
    message: str = None


class User(BaseModel):
    id: int = None
    name: str


class Event(BaseModel):
    id: int = None
    date: datetime.date
    title: str
