from typing import List

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, crud, auth
from ..database import get_db

router = APIRouter()


@router.get("", response_model=List[schemas.CheckInDB])
async def get_checkins(skip: int = Query(0, ge=0),
                       limit: int = Query(100, ge=0),
                       db: Session = Depends(get_db)):
    """Here you get check-ins."""
    checkins = crud.get_checkins(db, skip=skip, limit=limit)

    return checkins


@router.get("/{user_id}/{event_id}", response_model=schemas.CheckInDB)
async def get_checkin(user_id: int, event_id: int,
                      db: Session = Depends(get_db)):
    """Here you get a check-in."""
    checkin = schemas.CheckIn(user_id=user_id, event_id=event_id)
    checkin = crud.get_checkin(db, checkin)
    if not checkin:
        raise HTTPException(status_code=404, detail="Check-in not found.")

    return checkin


@router.post("", response_model=schemas.CheckInDB, status_code=201)
async def create_checkin(checkin: schemas.CheckIn,
                         db: Session = Depends(get_db),
                         token_out: schemas.TokenOut
                         = Depends(auth.validate_token)):
    """Here you add a check-in."""
    try:
        checkin = crud.create_checkin(db, checkin)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return checkin


@router.delete("", response_model=schemas.CheckInDB)
async def delete_checkin(checkin: schemas.CheckIn,
                         db: Session = Depends(get_db),
                         token_out: schemas.TokenOut
                         = Depends(auth.validate_token)):
    """Here you delete a check-in."""
    try:
        old_checkin = crud.delete_checkin(db, checkin)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return old_checkin
