import json

from starlette.testclient import TestClient

from .conftest import FAKE_TIME
from .. import app, schemas, auth

client = TestClient(app)

# expected data
checkins_exp = [
    {"user_id": 1, "event_id": 1, "date": "2020-03-19T03:30:00"},
    {"user_id": 1, "event_id": 3, "date": "2020-03-19T03:30:00"},
    {"user_id": 2, "event_id": 2, "date": "2020-03-19T03:30:00"},
    {"user_id": 2, "event_id": 4, "date": "2020-03-19T03:30:00"},
    {"user_id": 3, "event_id": 4, "date": "2020-03-19T03:30:00"},
    {"user_id": 4, "event_id": 4, "date": "2020-03-19T03:30:00"}
]


def test_get_checkins():
    response = client.get("/checkins")
    assert response.status_code == 200
    assert response.json() == checkins_exp

    response = client.get("/checkins", params={"skip": 2})
    assert response.status_code == 200
    assert response.json() == checkins_exp[2:]

    response = client.get("/checkins", params={"skip": -2})
    assert response.status_code == 422

    response = client.get("/checkins", params={"limit": 2})
    assert response.status_code == 200
    assert response.json() == checkins_exp[:2]

    response = client.get("/checkins", params={"limit": -2})
    assert response.status_code == 422

    response = client.get("/checkins", params={"skip": 1, "limit": 2})
    assert response.status_code == 200
    assert response.json() == checkins_exp[1:3]


def test_get_checkin():
    response = client.get("/checkins/1/3")
    assert response.status_code == 200
    assert response.json() == checkins_exp[1]

    response = client.get("/checkins/2/4")
    assert response.status_code == 200
    assert response.json() == checkins_exp[3]

    response = client.get("/checkins/1/13")
    assert response.status_code == 404

    response = client.get("/checkins/13/1")
    assert response.status_code == 404

    response = client.get("/checkins/13/31")
    assert response.status_code == 404


# TODO: monkeymock default time to be FAKE_TIME
# remove object_hook=remove_date exclude={"date"} remove_date
# from assertions
def remove_date(dict_):
    return {k: v for k, v in dict_.items() if k != 'date'}


def test_create_checkin():
    checkin = schemas.CheckIn(user_id=3, event_id=1)
    checkin_db = schemas.CheckInDB(date=FAKE_TIME, **checkin.dict())

    app.dependency_overrides.pop(auth.verify_token, None)

    response = client.post("/checkins", json=checkin.dict())
    assert response.status_code == 401

    app.dependency_overrides[auth.verify_token] = lambda: True

    response = client.post("/checkins", json=checkin.dict())
    assert response.status_code == 201
    assert response.json(object_hook=remove_date) \
        == json.loads(checkin_db.json(exclude={"date"}))

    response = client.post("/checkins", json=checkin.dict())
    assert response.status_code == 400

    response = client.get("/checkins/3/1")
    assert response.status_code == 200
    assert response.json(object_hook=remove_date) \
        == json.loads(checkin_db.json(exclude={"date"}))

    checkin = schemas.CheckIn(user_id=13, event_id=1)
    response = client.post("/checkins", json=checkin.dict())
    assert response.status_code == 400

    checkin = schemas.CheckIn(user_id=1, event_id=13)
    response = client.post("/checkins", json=checkin.dict())
    assert response.status_code == 400

    checkin = schemas.CheckIn(user_id=13, event_id=31)
    response = client.post("/checkins", json=checkin.dict())
    assert response.status_code == 400

    app.dependency_overrides.pop(auth.verify_token, None)


def test_delete_checkin():
    checkin = schemas.CheckIn(user_id=3, event_id=1)
    checkin_db = schemas.CheckInDB(date=FAKE_TIME, **checkin.dict())

    app.dependency_overrides.pop(auth.verify_token, None)

    response = client.delete("/checkins", json=checkin.dict())
    assert response.status_code == 401

    app.dependency_overrides[auth.verify_token] = lambda: True

    response = client.delete("/checkins", json=checkin.dict())
    assert response.status_code == 200
    assert response.json(object_hook=remove_date) \
        == json.loads(checkin_db.json(exclude={"date"}))

    response = client.get("/checkins/3/1")
    assert response.status_code == 404

    checkin = schemas.CheckIn(user_id=13, event_id=1)
    response = client.delete("/checkins", json=checkin.dict())
    assert response.status_code == 400

    checkin = schemas.CheckIn(user_id=1, event_id=13)
    response = client.delete("/checkins", json=checkin.dict())
    assert response.status_code == 400

    checkin = schemas.CheckIn(user_id=13, event_id=31)
    response = client.delete("/checkins", json=checkin.dict())
    assert response.status_code == 400

    app.dependency_overrides.pop(auth.verify_token, None)
