from fastapi.logger import logger
from sqlalchemy.exc import IntegrityError

from .database import engine, get_db
from . import models


# init db models
models.Base.metadata.create_all(bind=engine)

# test data
events = [
    {"id": 1, "title": "seminario mimbela"},
    {"id": 2, "title": "seminario herrera"},
    {"id": 3, "title": "seminario lamoneda"},
    {"id": 4, "title": "seminario arizmendi"}
]

users = [
    {"id": 1, "name": "ivan"},
    {"id": 2, "name": "tere"},
    {"id": 3, "name": "leslie"},
    {"id": 4, "name": "irwin"}
]

checkins = [
    {"user_id": 1, "event_id": 1},
    {"user_id": 1, "event_id": 3},
    {"user_id": 2, "event_id": 2},
    {"user_id": 2, "event_id": 4},
    {"user_id": 3, "event_id": 4},
    {"user_id": 4, "event_id": 4}
]

events = [models.Event(**event) for event in events]
users = [models.User(**user) for user in users]
checkins = [models.CheckIn(**checkin) for checkin in checkins]

try:
    logger.info("Inserting testing data...")
    db = next(get_db())
    db.add_all(events+users+checkins)
    db.commit()
except IntegrityError:
    logger.info("Testing data exists.")
