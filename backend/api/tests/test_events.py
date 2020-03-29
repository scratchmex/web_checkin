import json

from starlette.testclient import TestClient

from .. import app, schemas

client = TestClient(app)

# expected data
events_exp = [
    {"id": 1, "date": "2020-03-19T03:30:00", "title": "seminario mimbela"},
    {"id": 2, "date": "2020-03-19T03:30:00", "title": "seminario herrera"},
    {"id": 3, "date": "2020-03-19T03:30:00", "title": "seminario lamoneda"},
    {"id": 4, "date": "2020-03-19T03:30:00", "title": "seminario arizmendi"}
]

events_attendants_exp = [
    [{"id": 1, "name": "ivan"}],
    [{"id": 2, "name": "tere"}],
    [{"id": 1, "name": "ivan"}],
    [{"id": 2, "name": "tere"}, {"id": 3, "name": "leslie"}, {"id": 4, "name": "irwin"}]  # noqa
]


def test_get_events():
    response = client.get("/events")
    assert response.status_code == 200
    assert response.json() == events_exp

    response = client.get("/events", params={"skip": 2})
    assert response.status_code == 200
    assert response.json() == events_exp[2:]

    response = client.get("/events", params={"skip": -2})
    assert response.status_code == 422

    response = client.get("/events", params={"limit": 2})
    assert response.status_code == 200
    assert response.json() == events_exp[:2]

    response = client.get("/events", params={"limit": -2})
    assert response.status_code == 422

    response = client.get("/events", params={"skip": 1, "limit": 2})
    assert response.status_code == 200
    assert response.json() == events_exp[1:3]


def test_get_event():
    response = client.get("/events/1")
    assert response.status_code == 200
    assert response.json() == events_exp[0]

    response = client.get("/events/2")
    assert response.status_code == 200
    assert response.json() == events_exp[1]

    response = client.get("/events/99")
    assert response.status_code == 404


def test_get_event_attendants():
    response = client.get("/events/3/users")
    assert response.status_code == 200
    assert response.json() == events_attendants_exp[2]

    response = client.get("/events/4/users")
    assert response.status_code == 200
    assert response.json() == events_attendants_exp[3]

    response = client.get("/events/99/users")
    assert response.status_code == 404


def test_create_event():
    event = schemas.Event(title="seminario suave",
                          date="2020-03-20T03:30:00")
    event_out = schemas.EventOut(id=5, **event.dict())

    response = client.post("/events", data=event.json())
    assert response.status_code == 201
    assert response.json() == json.loads(event_out.json())

    response = client.get("/events/5")
    assert response.status_code == 200
    assert response.json() == json.loads(event_out.json())

    event = schemas.Event(id=1, title="seminario mimbela",
                          date="2020-03-19T03:30:00")
    response = client.post("/events", data=event.json())
    assert response.status_code == 400


def test_delete_event():
    event = schemas.Event(title="seminario suave",
                          date="2020-03-20T03:30:00")
    event_out = schemas.EventOut(id=5, **event.dict())

    response = client.delete(f"/events/{event_out.id}")
    assert response.status_code == 200
    assert response.json() == json.loads(event_out.json())

    response = client.get("/events/5")
    assert response.status_code == 404

    response = client.delete(f"/events/{event_out.id}")
    assert response.status_code == 400
