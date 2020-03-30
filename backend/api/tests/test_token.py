from starlette.testclient import TestClient
from datetime import datetime

from ..init_db import default_password
from .. import app, schemas, config, auth

client = TestClient(app)


def test_get_current_token():
    token = config.MASTER_KEY

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/token", headers=headers)
    assert response.status_code == 200
    assert schemas.Token(**response.json())

    headers = {"Authorization": "Bearer blahblah"}
    response = client.get("/token", headers=headers)
    assert response.status_code == 401
    assert response.headers.get("WWW-Authenticate") == "Bearer"


def test_get_auth_token():
    payload = {"username": "ivan", "password": default_password}
    response = client.post("/token/auth", data=payload)
    assert response.status_code == 200

    headers = {"Authorization": f"Bearer {response.json()['access_token']}"}
    response = client.get("/token", headers=headers)
    assert response.status_code == 200

    payload = {"username": "non existant", "password": default_password}
    response = client.post("/token/auth", data=payload)
    assert response.status_code == 401

    payload = {"username": "ivan", "password": "wrong password"}
    response = client.post("/token/auth", data=payload)
    assert response.status_code == 401


def test_get_event_token():
    event_id = 3
    fake_admin_token = {
        "iss": "admin:0",
        "sub": "admin:auth",
        "iat": int(datetime.now().timestamp()),
        "exp": int(datetime.now().timestamp())
    }

    app.dependency_overrides.pop(auth.verify_token, None)

    response = client.post("/token/events", json={"event_id": event_id})
    assert response.status_code == 401

    app.dependency_overrides[auth.verify_token] = lambda: fake_admin_token

    response = client.post("/token/events", json={"event_id": event_id})
    assert response.status_code == 200

    headers = {"Authorization": f"Bearer {response.json()['access_token']}"}
    response = client.get("/token", headers=headers)
    assert response.status_code == 200

    response = client.post("/token/events", json={"event_id": 99})
    assert response.status_code == 400

    app.dependency_overrides.pop(auth.verify_token, None)


def test_get_checkin_token():
    event_id = 3
    new_user = schemas.User(id=13, name="ricardo")

    body = {"event_id": event_id, "user": new_user.dict()}
    response = client.post("/token/checkins", json=body)
    assert response.status_code == 200

    headers = {"Authorization": f"Bearer {response.json()['access_token']}"}
    response = client.get("/token", headers=headers)
    assert response.status_code == 200

    response = client.get(f"/users/{new_user.id}")
    assert response.status_code == 200
    assert response.json() == new_user

    non_new_user = {"id": new_user.id, "name": "el ricardo"}
    body = {"event_id": event_id, "user": non_new_user}
    response = client.post("/token/checkins", json=body)
    assert response.status_code == 200

    app.dependency_overrides[auth.verify_token] = lambda: True

    response = client.delete(f"/users/{new_user.id}")
    assert response.status_code == 200
    assert response.json() == new_user

    app.dependency_overrides.pop(auth.verify_token, None)

    body = {"event_id": 99, "user": new_user.dict()}
    response = client.post("/token/checkins", json=body)
    assert response.status_code == 400
