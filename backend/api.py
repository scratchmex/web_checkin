from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello there!. Inquiring?."}


@app.get("/events")
async def get_events():
    return {"message": "All events should return here."}


@app.post("/events")
async def create_event():
    return {
        "message": f"Here you add events.",
        "data": "Body here"
    }


@app.get("/events/{id}")
async def get_event(id: int):
    return {"message": f"Event[{id}] information."}


@app.get("/user/{id}")
async def get_user(id: int):
    return {"message": f"User[{id}] information"}


@app.post("/user")
async def create_user():
    return {
        "message": f"Here you create users.",
        "id": "return user id",
        "data": "Body here."
    }
