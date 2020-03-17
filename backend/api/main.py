from fastapi import FastAPI
from .models import User, Event

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello there!. Inquiring?."}


@app.get("/events")
async def get_events():
    return {"message": "All events should return here."}


@app.post("/events")
async def create_event(event: Event):
    return {
        "message": f"Here you add events.",
        "data": event
    }


@app.get("/events/{id}")
async def get_event(id: int):
    return {"message": f"Event[{id}] information."}


@app.get("/user/{id}")
async def get_user(id: int):
    return {"message": f"User[{id}] information"}


@app.post("/user")
async def create_user(user: User):
    return {
        "message": f"Here you create users.",
        "id": user.id,
        "data": user
    }
