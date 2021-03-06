import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base

DEFAULT_DATE = datetime.datetime.utcnow


class CheckIn(Base):
    __tablename__ = "checkin"

    user_id = Column('user_id', Integer, ForeignKey('users.id'),
                     primary_key=True)
    event_id = Column('event_id', Integer, ForeignKey('events.id'),
                      primary_key=True)
    date = Column('date', DateTime, default=DEFAULT_DATE)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    attended_events = relationship(
        "Event",
        secondary="checkin",
        back_populates="attendants"
    )


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=DEFAULT_DATE)
    title = Column(String, unique=True)
    attendants = relationship(
        "User",
        secondary="checkin",
        back_populates="attended_events"
    )


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String, unique=True)
    hashed_password = Column(String)
