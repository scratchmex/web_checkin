
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


def verify_masterkey(key: str):
    if is_masterkey(key):
        return True

    return HTTPException(status_code=401, detail="¿?")


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

    return encoded_jwt


def decode_token(token: str):
    try:
        payload = jwt.decode(token, config.SECRET_KEY,
                             algorithms=[config.JWT_ALGORITHM])
    except PyJWTError:
        raise

    return payload


# oauth scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")


# oauth operations
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
    except PyJWTError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


# authentication depends
def verify_authentication(token: str = Depends(oauth2_scheme)) -> bool:
    if verify_masterkey(token):
        return True

    if verify_token(token):
        return True
