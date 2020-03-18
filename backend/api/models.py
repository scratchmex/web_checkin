from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class CheckIn(Base):
    __tablename__ = "checkin"

    user_id = Column('user_id', Integer, ForeignKey('users.id'),
                     primary_key=True)
    event_id = Column('event_id', Integer, ForeignKey('events.id'),
                      primary_key=True)
    date = Column('date', DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    events_attended = relationship(
        "Event",
        secondary="checkin",
        back_populates="attendants"
    )


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    title = Column(String, unique=True)
    attendants = relationship(
        "User",
        secondary="checkin",
        back_populates="events_attended"
    )
