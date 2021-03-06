from typing import List

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, crud, auth
from ..database import yield_db

router = APIRouter()


@router.get("", response_model=List[schemas.User])
async def get_users(skip: int = Query(0, ge=0),
                    limit: int = Query(100, ge=0),
                    db: Session = Depends(yield_db)):
    """All users should return here."""
    users = crud.get_users(db, skip=skip, limit=limit)

    return users


@router.get("/{id}", response_model=schemas.User)
async def get_user(id: int, db: Session = Depends(yield_db)):
    """User information."""
    user = crud.get_user(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return user


@router.get("/{id}/events", response_model=List[schemas.EventOut])
async def get_user_attended_events(id: int, db: Session = Depends(yield_db)):
    """Events the user have attended."""
    user = crud.get_user(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return user.attended_events


@router.post("", response_model=schemas.User, status_code=201,
             dependencies=[Depends(auth.verify_token)])
async def create_user(user: schemas.User,
                      db: Session = Depends(yield_db)):
    """Here you create users."""
    try:
        new_user = crud.create_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return new_user


@router.delete("/{id}", response_model=schemas.User,
               dependencies=[Depends(auth.verify_token)])
async def delete_user(id: int, db: Session = Depends(yield_db)):
    """Here you delete users."""
    try:
        old_user = crud.delete_user(db, id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return old_user
