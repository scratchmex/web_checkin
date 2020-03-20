import pytest
import datetime

from ..init_db import init_db

FAKE_TIME = datetime.datetime.fromisoformat("2020-03-19T03:30:00")


init_db()


# todo: fix path models.DEFAULT_DATE
@pytest.fixture(autouse=True)
def patch_datetime_utcnow(monkeypatch):
    class fake_datetime(datetime.datetime):
        @staticmethod
        def utcnow():
            return FAKE_TIME

    monkeypatch.setattr('datetime.datetime', fake_datetime)
    # monkeypatch.setattr(models, 'DEFAULT_DATE', fake_datetime.utcnow)
