from typing import List

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, crud, auth
from ..database import yield_db

router = APIRouter()


@router.get("", response_model=List[schemas.EventOut])
async def get_events(skip: int = Query(0, ge=0),
                     limit: int = Query(100, ge=0),
                     db: Session = Depends(yield_db)):
    """All events should return here."""
    events = crud.get_events(db, skip=skip, limit=limit)

    return events


@router.get("/{id}", response_model=schemas.EventOut)
async def get_event(id: int, db: Session = Depends(yield_db)):
    """Event information."""
    event = crud.get_event(db, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found.")

    return event


@router.get("/{id}/users", response_model=List[schemas.User])
async def get_event_attendants(id: int, db: Session = Depends(yield_db)):
    """Users who have attended to the event."""
    event = crud.get_event(db, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found.")

    return event.attendants


@router.post("", response_model=schemas.EventOut, status_code=201,
             dependencies=[Depends(auth.verify_token)])
async def create_event(event: schemas.Event,
                       db: Session = Depends(yield_db)):
    """Here you add events."""
    try:
        new_event = crud.create_event(db, event)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return new_event


@router.delete("/{id}", response_model=schemas.EventOut,
               dependencies=[Depends(auth.verify_token)])
async def delete_event(id: int, db: Session = Depends(yield_db)):
    """Here you delete events."""
    try:
        old_event = crud.delete_event(db, id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return old_event
