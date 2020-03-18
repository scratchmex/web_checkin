from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.logger import logger
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from . import schemas, models, crud
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# test data
events = [
    {"id": 1, "title": "seminario mimbela"},
    {"id": 2, "title": "seminario herrera"},
    {"id": 3, "title": "seminario lamoneda"},
    {"id": 4, "title": "seminario arizmendi"}
]

users = [
    {"id": 1, "name": "ivan"},
    {"id": 2, "name": "tere"},
    {"id": 3, "name": "leslie"},
    {"id": 4, "name": "irwin"}
]

checkins = [
    {"user_id": 1, "event_id": 1},
    {"user_id": 1, "event_id": 3},
    {"user_id": 2, "event_id": 2},
    {"user_id": 2, "event_id": 4},
    {"user_id": 3, "event_id": 4},
    {"user_id": 4, "event_id": 4}
]

events = [models.Event(**event) for event in events]
users = [models.User(**user) for user in users]
checkins = [models.CheckIn(**checkin) for checkin in checkins]

try:
    logger.info("Inserting testing data...")
    db = next(get_db())
    db.add_all(events+users+checkins)
    db.commit()
except IntegrityError:
    logger.info("Testing data exists.")


@app.get("/", response_model=schemas.Message)
async def root():
    return {"message": "Hello there!. Inquiring?."}


@app.get("/users",
         response_model=List[schemas.UserDB],
         tags=["users"])
async def get_users(skip: int = 0, limit: int = 100,
                    db: Session = Depends(get_db)):
    """All users should return here."""
    users = crud.get_users(db, skip=skip, limit=limit)

    return users


@app.get("/users/{id}",
         response_model=schemas.UserDB,
         tags=["users"])
async def get_user(id: int, db: Session = Depends(get_db)):
    """User information."""
    user = crud.get_user(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return user


@app.post("/users",
          response_model=schemas.User,
          status_code=201,
          tags=["users"])
async def create_user(user: schemas.User, db: Session = Depends(get_db)):
    """Here you create users."""
    if crud.get_user(db, user.id):
        raise HTTPException(status_code=400, detail="User already registered.")
    new_user = crud.create_user(db, user)

    return new_user


@app.get("/events",
         response_model=List[schemas.EventDB],
         tags=["events"])
async def get_events(skip: int = 0, limit: int = 100,
                     db: Session = Depends(get_db)):
    """All events should return here."""
    events = crud.get_events(db, skip=skip, limit=limit)

    return events


@app.get("/events/{id}",
         response_model=schemas.EventDB,
         tags=["events"])
async def get_event(id: int, db: Session = Depends(get_db)):
    """Event information."""
    event = crud.get_event(db, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found.")

    return event


@app.post("/events",
          response_model=schemas.Event,
          status_code=201,
          tags=["events"])
async def create_event(event: schemas.Event, db: Session = Depends(get_db)):
    """Here you add events."""
    if crud.get_event_by_title(db, event.title):
        raise HTTPException(status_code=400,
                            detail="Event already registered.")
    new_event = crud.create_event(db, event)

    return new_event


@app.get("/checkins",
         response_model=List[schemas.CheckIn],
         tags=["checkins"])
async def get_checkins(skip: int = 0, limit: int = 100,
                       db: Session = Depends(get_db)):
    """Here you add events."""
    checkins = crud.get_checkins(db, skip=skip, limit=limit)

    return checkins


@app.post("/checkins/{id}",
          response_model=schemas.Event,
          status_code=201,
          tags=["checkins"])
async def create_checkin(checkin: schemas.CheckIn,
                         db: Session = Depends(get_db)):
    """Here you add events."""
    if crud.get_checkin(db, checkin):
        raise HTTPException(status_code=400,
                            detail="Check-in already registered.")
    checkin = crud.create_checkin(db, checkin)

    return checkin
