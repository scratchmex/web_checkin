import pytest

from datetime import timedelta
from jwt import PyJWTError

from .conftest import MASTER_KEY
from .. import auth, config


def test_bcrypt_hashing():
    plain_passwd = "testing here"

    hashed_passwd = '$2b$12$0xipc97HYrV/0PnfCxsQ..x9waIUZmneXptYXqoGHZW9eQGjzxHFG'  # noqa
    assert auth.verify_password(plain_passwd, hashed_passwd)

    new_hashed_passwd = auth.hash_password(plain_passwd)
    assert auth.verify_password(plain_passwd, new_hashed_passwd)


def test_masterkey():
    assert auth.is_masterkey(MASTER_KEY)


# TODO uncomment iat assertion and import FAKE_TIME
def test_JWT():
    payload = {
        "iss": "who issued the token",
        "sub": "the subject of the token here",
        "data": "important data here hmm"
    }
    token = auth.create_token(payload)
    token_decoded = auth.decode_token(token)

    with pytest.raises(PyJWTError):
        # expired at FAKE_DATE token but valid
        auth.decode_token("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODQ2MTAyMDAsImlhdCI6MTU4NDYxMDIwMH0.sz90TIqG6oQOXU4ov52sx4Oxs6JhH6CHk727DdngRN0")  # noqa

    # assert token_decoded.get("iat") == int(FAKE_TIME.timestamp())

    exp = token_decoded.get("exp", 0) - token_decoded.get("iat", 0)
    assert timedelta(seconds=exp) == timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)  # noqa

    for k in payload:
        assert payload[k] == token_decoded[k]
