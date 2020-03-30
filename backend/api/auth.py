
import jwt

from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends
from passlib.hash import bcrypt
from jwt import PyJWTError
from datetime import datetime, timedelta

from . import config, schemas


# Hash passwords
def hash_password(password):
    return bcrypt.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt.verify(plain_password, hashed_password)


# Auth masterkey
def is_masterkey(key: str):
    return key == config.MASTER_KEY


# Token with JWT
def create_token(to_encode: dict, expires_delta: timedelta = None):
    if not expires_delta:
        expires_delta = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    iat = datetime.now()
    exp = iat+expires_delta
    token = schemas.Token(
        iat=int(iat.timestamp()),
        exp=int(exp.timestamp()),
        **to_encode
    )

    encoded_jwt = jwt.encode(token.dict(), config.SECRET_KEY,
                             algorithm=config.JWT_ALGORITHM)

    return encoded_jwt.decode("utf")


def decode_token(token: str):
    try:
        payload = jwt.decode(token, config.SECRET_KEY,
                             algorithms=config.JWT_ALGORITHM)
    except PyJWTError:
        raise

    return payload


# create special token type
def create_admin_token(*, admin_id: int):
    payload = {
        "iss": f"admin:{admin_id}",
        "sub": "admin:auth",
    }
    token = create_token(payload)

    return token


def create_event_token(*, admin_id: int, event_id: int):
    payload = {
        "iss": f"admin:{admin_id}",
        "sub": f"event:{event_id}",
    }
    token = create_token(payload)

    return token


def create_checkin_token(*, user: schemas.User, event_id: int):
    payload = {
        "iss": f"user:{user.id}",
        "sub": f"checkin:{event_id}",
        "data": user.dict(include={"name"})
    }
    token = create_token(payload)

    return token


def format_token(token: str):
    try:
        payload = decode_token(token)
    except PyJWTError:
        raise

    exp = payload["exp"]
    iat = payload["iat"]
    token_out = schemas.TokenOut(
        access_token=token,
        expires_in=exp-iat
    )

    return token_out


# oauth scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token/auth")


# authentication depends
def verify_token(token: str = Depends(oauth2_scheme)) -> schemas.Token:
    if is_masterkey(token):
        payload = {
            "iss": "admin:0",
            "sub": "admin:auth",
            "iat": int(datetime.now().timestamp()),
            "exp": int(datetime.now().timestamp())
        }

        return payload

    try:
        payload = decode_token(token)
    except PyJWTError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload
