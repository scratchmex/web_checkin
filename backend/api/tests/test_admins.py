from starlette.testclient import TestClient

from .. import app, schemas, auth

client = TestClient(app)


admins_exp = [
    {"id": 1, "name": "iv g", "username": "ivan"},
    {"id": 2, "name": "te c", "username": "tere"},
    {"id": 3, "name": "le q", "username": "leslie"}
]


def test_get_admins():
    response = client.get("/admins")
    assert response.status_code == 200
    assert response.json() == admins_exp

    response = client.get("/admins", params={"skip": 2})
    assert response.status_code == 200
    assert response.json() == admins_exp[2:]

    response = client.get("/admins", params={"skip": -2})
    assert response.status_code == 422

    response = client.get("/admins", params={"limit": 2})
    assert response.status_code == 200
    assert response.json() == admins_exp[:2]

    response = client.get("/admins", params={"limit": -2})
    assert response.status_code == 422

    response = client.get("/admins", params={"skip": 1, "limit": 2})
    assert response.status_code == 200
    assert response.json() == admins_exp[1:3]


def test_get_admin():
    response = client.get("/admins/1")
    assert response.status_code == 200
    assert response.json() == admins_exp[0]

    response = client.get("/admins/2")
    assert response.status_code == 200
    assert response.json() == admins_exp[1]

    response = client.get("/admins/99")
    assert response.status_code == 404


def test_create_admin():
    admin = schemas.AdminIn(
        name="ri z",
        username="ricardo",
        password="secure password"
    )
    admin_out = schemas.AdminOut(id=4, **admin.dict())

    app.dependency_overrides.pop(auth.verify_token, None)

    response = client.post("/admins", json=admin.dict())
    assert response.status_code == 401

    app.dependency_overrides[auth.verify_token] = lambda: True

    response = client.post("/admins", json=admin.dict())
    assert response.status_code == 201
    assert response.json() == admin_out

    response = client.get(f"/admins/{admin_out.id}")
    assert response.status_code == 200
    assert response.json() == admin_out

    response = client.post("/admins", json=admin.dict())
    assert response.status_code == 400

    app.dependency_overrides.pop(auth.verify_token, None)


def test_delete_admin():
    admin = schemas.AdminIn(
        name="ri z",
        username="ricardo",
        password="secure password"
    )
    admin_out = schemas.AdminOut(id=4, **admin.dict())

    app.dependency_overrides.pop(auth.verify_token, None)

    response = client.delete(f"/admins/{admin_out.id}")
    assert response.status_code == 401

    app.dependency_overrides[auth.verify_token] = lambda: True

    response = client.delete(f"/admins/{admin_out.id}")
    assert response.status_code == 200
    assert response.json() == admin_out

    response = client.get(f"/admins/{admin_out.id}")
    assert response.status_code == 404

    response = client.delete(f"/admins/{admin_out.id}")
    assert response.status_code == 400

    app.dependency_overrides.pop(auth.verify_token, None)
