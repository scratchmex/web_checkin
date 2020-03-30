from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import crud, auth, schemas
from ..database import yield_db

router = APIRouter()


@router.get("", response_model=schemas.Token)
async def get_current_token(token_payload: dict = Depends(auth.verify_token)):
    return token_payload


@router.post("/auth", response_model=schemas.TokenOut)
async def get_auth_token(form: OAuth2PasswordRequestForm = Depends(),
                         db: Session = Depends(yield_db)):
    try:
        admin = crud.authenticate_admin(db, form.username, form.password)
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = auth.create_admin_token(admin_id=admin.id)
    token_out = auth.format_token(token)

    return token_out


@router.post("/events", response_model=schemas.TokenOut)
async def get_event_token(event_id: int = Body(..., embed=True),
                          admin_token: dict = Depends(auth.verify_token),
                          db: Session = Depends(yield_db)):
    event = crud.get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=400, detail="Event not found.")

    admin_id = admin_token['iss'].split(':')[1]

    token = auth.create_event_token(admin_id=admin_id, event_id=event_id)
    token_out = auth.format_token(token)

    return token_out


@router.post("/checkins", response_model=schemas.TokenOut)
async def get_checkin_token(event_id: int = Body(...),
                            user: schemas.User = Body(..., embed=True),
                            db: Session = Depends(yield_db)):
    event = crud.get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=400, detail="Event not found.")

    try:
        user = schemas.User.from_orm(crud.get_user(db, user.id))
    except ValueError:
        user = schemas.User.from_orm(crud.create_user(db, user))

    token = auth.create_checkin_token(user=user, event_id=event_id)
    token_out = auth.format_token(token)

    return token_out
