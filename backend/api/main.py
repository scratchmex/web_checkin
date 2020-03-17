from typing import List

from fastapi import FastAPI
from .models import Message, User, Event

app = FastAPI()


@app.get("/", response_model=Message)
async def root():
    return {"message": "Hello there!. Inquiring?."}


@app.get("/events", response_model=List[Event], tags=["events"])
async def get_events():
    return {"message": "All events should return here."}


@app.post("/events", response_model=Event, tags=["events"])
async def create_event(event: Event):
    return {
        "message": f"Here you add events.",
        **event.dict()
    }


@app.get("/events/{id}", tags=["events"])
async def get_event(id: int):
    return {"message": f"Event[{id}] information."}


@app.get("/user/{id}", tags=["user"])
async def get_user(id: int):
    return {"message": f"User[{id}] information"}


@app.post("/user", response_model=User, tags=["user"])
async def create_user(user: User):
    return {
        "message": f"Here you create users.",
        **user.dict()
    }
