from starlette.testclient import TestClient

from .. import app, schemas, auth

client = TestClient(app)

# expected data
users_exp = [
    {"id": 1, "name": "ivan"},
    {"id": 2, "name": "tere"},
    {"id": 3, "name": "leslie"},
    {"id": 4, "name": "irwin"}
]

users_attended_events_exp = [
    [
        {"id": 1, "date": "2020-03-19T03:30:00", "title": "seminario mimbela"},
        {"id": 3, "date": "2020-03-19T03:30:00", "title": "seminario lamoneda"}
    ],
    [
        {"id": 2, "date": "2020-03-19T03:30:00", "title": "seminario herrera"},
        {"id": 4, "date": "2020-03-19T03:30:00", "title": "seminario arizmendi"}  # noqa
    ],
    [
        {"id": 4, "date": "2020-03-19T03:30:00", "title": "seminario arizmendi"}  # noqa
    ],
    [
        {"id": 4, "date": "2020-03-19T03:30:00", "title": "seminario arizmendi"}  # noqa
    ]
]


def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == users_exp

    response = client.get("/users", params={"skip": 2})
    assert response.status_code == 200
    assert response.json() == users_exp[2:]

    response = client.get("/users", params={"skip": -2})
    assert response.status_code == 422

    response = client.get("/users", params={"limit": 2})
    assert response.status_code == 200
    assert response.json() == users_exp[:2]

    response = client.get("/users", params={"limit": -2})
    assert response.status_code == 422

    response = client.get("/users", params={"skip": 1, "limit": 2})
    assert response.status_code == 200
    assert response.json() == users_exp[1:3]


def test_get_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == users_exp[0]

    response = client.get("/users/2")
    assert response.status_code == 200
    assert response.json() == users_exp[1]

    response = client.get("/users/99")
    assert response.status_code == 404


def test_get_user_attended_events():
    response = client.get("/users/1/events")
    assert response.status_code == 200
    assert response.json() == users_attended_events_exp[0]

    response = client.get("/users/2/events")
    assert response.status_code == 200
    assert response.json() == users_attended_events_exp[1]

    response = client.get("/users/99/events")
    assert response.status_code == 404


def test_create_user():
    user = schemas.User(id=13, name="ricardo")

    app.dependency_overrides.pop(auth.verify_token, None)

    response = client.post("/users", json=user.dict())
    assert response.status_code == 401

    app.dependency_overrides[auth.verify_token] = lambda: True

    response = client.post("/users", json=user.dict())
    assert response.status_code == 201
    assert response.json() == user

    response = client.get("/users/13")
    assert response.status_code == 200
    assert response.json() == user

    user = schemas.User(id=4, name="irwin")
    response = client.post("/users", json=user.dict())
    assert response.status_code == 400

    app.dependency_overrides.pop(auth.verify_token, None)


def test_delete_user():
    user = schemas.User(id=13, name="ricardo")

    app.dependency_overrides.pop(auth.verify_token, None)

    response = client.delete(f"/users/{user.id}")
    assert response.status_code == 401

    app.dependency_overrides[auth.verify_token] = lambda: True

    response = client.delete(f"/users/{user.id}")
    assert response.status_code == 200
    assert response.json() == user

    response = client.get("/users/13")
    assert response.status_code == 404

    response = client.delete(f"/users/{user.id}")
    assert response.status_code == 400

    app.dependency_overrides.pop(auth.verify_token, None)
