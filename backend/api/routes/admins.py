from typing import List

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import yield_db

router = APIRouter()


@router.get("", response_model=List[schemas.AdminOut])
async def get_admins(skip: int = Query(0, ge=0), limit: int = Query(100, ge=0),
                     db: Session = Depends(yield_db)):
    """All admins should return here"""
    admins = crud.get_admins(db, skip=skip, limit=limit)

    return admins


@router.get("/{id}", response_model=schemas.AdminOut)
async def get_admin(id: int, db: Session = Depends(yield_db)):
    """Admin information."""
    admin = crud.get_admin(db, id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found.")

    return admin


@router.post("", response_model=schemas.AdminOut, status_code=201)
async def create_admin(admin: schemas.AdminIn,
                       db: Session = Depends(yield_db)):
    """Here you create admins."""
    try:
        new_admin = crud.create_admin(db, admin)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return new_admin


@router.delete("/{id}", response_model=schemas.AdminOut)
async def delete_admin(id: int,
                       db: Session = Depends(yield_db)):
    """Here you delete admins."""
    try:
        old_admin = crud.delete_admin(db, id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return old_admin
