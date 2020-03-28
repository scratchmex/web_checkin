from typing import List

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, crud, auth
from ..database import get_db

router = APIRouter()


@router.get("", response_model=List[schemas.EventDB])
async def get_events(skip: int = Query(0, ge=0),
                     limit: int = Query(100, ge=0),
                     db: Session = Depends(get_db)):
    """All events should return here."""
    events = crud.get_events(db, skip=skip, limit=limit)

    return events


@router.get("/{id}", response_model=schemas.EventDB)
async def get_event(id: int, db: Session = Depends(get_db)):
    """Event information."""
    event = crud.get_event(db, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found.")

    return event


@router.post("", response_model=schemas.Event, status_code=201)
async def create_event(event: schemas.Event, db: Session = Depends(get_db),
                       token_out: schemas.TokenOut
                       = Depends(auth.validate_token)):
    """Here you add events."""
    try:
        new_event = crud.create_event(db, event)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return new_event


@router.delete("/{id}", response_model=schemas.EventDB)
async def delete_event(id: int, db: Session = Depends(get_db),
                       token_out: schemas.TokenOut
                       = Depends(auth.validate_token)):
    """Here you delete events."""
    try:
        old_event = crud.delete_event(db, id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return old_event
