from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from .routes import root, users, events, checkins, admins, token


middlewares = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=['GET', 'POST', 'DELETE'],
        allow_headers=['*']
    )
]

app = FastAPI(middleware=middlewares)


app.include_router(
    root.router
)

app.include_router(
    admins.router,
    prefix="/admins",
    tags=["admins"]
)

app.include_router(
    token.router,
    prefix="/token",
    tags=["token"]
)

app.include_router(
    users.router,
    prefix="/users",
    tags=["users"]
)

app.include_router(
    events.router,
    prefix="/events",
    tags=["events"]
)

app.include_router(
    checkins.router,
    prefix="/checkins",
    tags=["checkins"]
)
