from typing import List

from fastapi import FastAPI, Depends, Body, HTTPException
from sqlalchemy.orm import Session

from . import schemas, crud
from .database import get_db


app = FastAPI()


@app.get("/", response_model=schemas.Message)
async def root():
    return {"message": "Hello there!. Inquiring?."}


@app.get("/users",
         response_model=List[schemas.UserDB],
         tags=["users"])
async def get_users(skip: int = Body(0, ge=0),
                    limit: int = Body(100, ge=0),
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
    try:
        new_user = crud.create_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return new_user


@app.delete("/users/{id}",
            response_model=schemas.UserDB,
            tags=["users"])
async def delete_user(id: int, db: Session = Depends(get_db)):
    """Here you delete users."""
    try:
        old_user = crud.delete_user(db, id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return old_user


@app.get("/events",
         response_model=List[schemas.EventDB],
         tags=["events"])
async def get_events(skip: int = Body(0, ge=0),
                     limit: int = Body(100, ge=0),
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
    try:
        new_event = crud.create_event(db, event)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return new_event


@app.delete("/events/{id}",
            response_model=schemas.EventDB,
            tags=["events"])
async def delete_event(id: int, db: Session = Depends(get_db)):
    """Here you delete events."""
    try:
        old_event = crud.delete_event(db, id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return old_event


@app.get("/checkins",
         response_model=List[schemas.CheckInDB],
         tags=["checkins"])
async def get_checkins(skip: int = Body(0, ge=0),
                       limit: int = Body(100, ge=0),
                       db: Session = Depends(get_db)):
    """Here you get check-ins."""
    checkins = crud.get_checkins(db, skip=skip, limit=limit)

    return checkins


@app.get("/checkins/{user_id}/{event_id}",
         response_model=schemas.CheckInDB,
         tags=["checkins"])
async def get_checkin(user_id: int, event_id: int,
                      db: Session = Depends(get_db)):
    """Here you get a check-in."""
    checkin = schemas.CheckIn(user_id=user_id, event_id=event_id)
    checkin = crud.get_checkin(db, checkin)
    if not checkin:
        raise HTTPException(status_code=404, detail="Check-in not found.")

    return checkin


@app.post("/checkins",
          response_model=schemas.CheckInDB,
          status_code=201,
          tags=["checkins"])
async def create_checkin(checkin: schemas.CheckIn,
                         db: Session = Depends(get_db)):
    """Here you add a check-in."""
    try:
        checkin = crud.create_checkin(db, checkin)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return checkin


@app.delete("/checkins",
            response_model=schemas.CheckInDB,
            status_code=200,
            tags=["checkins"])
async def delete_checkin(checkin: schemas.CheckIn,
                         db: Session = Depends(get_db)):
    """Here you delete a check-in."""
    try:
        old_checkin = crud.delete_checkin(db, checkin)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return old_checkin
