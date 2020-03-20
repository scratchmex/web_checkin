import pytest
import datetime

from ..init_db import init_db

FAKE_TIME = datetime.datetime.fromisoformat("2020-03-19T03:30:00")


init_db()


MASTER_KEY = "super secure masterkey"
config.MASTER_KEY = MASTER_KEY

SECRET_KEY = "super secure secretkey"
config.SECRET_KEY = SECRET_KEY


# TODO fix datetime imports from all files
# from models.DEFAULT_DATE
# from auth.create_token
# then check tests/test_:
# checkins, auth
@pytest.fixture(autouse=True)
def patch_datetime_utcnow(monkeypatch):
    class fake_datetime(datetime.datetime):
        @staticmethod
        def utcnow():
            return FAKE_TIME

    monkeypatch.setattr('datetime.datetime', fake_datetime)
    # monkeypatch.setattr(models, 'DEFAULT_DATE', fake_datetime.utcnow)
