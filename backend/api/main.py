from fastapi import FastAPI

from .routes import root, users, events, checkins


app = FastAPI()


app.include_router(
    root.router
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
