import datetime
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str


class Event(BaseModel):
    id: int
    date: datetime.date
    title: str
