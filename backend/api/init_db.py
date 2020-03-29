from fastapi.logger import logger
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from .database import engine, db_session_scope
from . import models


date = datetime(2020, 3, 19, 3, 30)

# test data
events = [
    {"id": 1, "date": date, "title": "seminario mimbela"},
    {"id": 2, "date": date, "title": "seminario herrera"},
    {"id": 3, "date": date, "title": "seminario lamoneda"},
    {"id": 4, "date": date, "title": "seminario arizmendi"}
]

users = [
    {"id": 1, "name": "ivan"},
    {"id": 2, "name": "tere"},
    {"id": 3, "name": "leslie"},
    {"id": 4, "name": "irwin"}
]

checkins = [
    {"user_id": 1, "event_id": 1, "date": date},
    {"user_id": 1, "event_id": 3, "date": date},
    {"user_id": 2, "event_id": 2, "date": date},
    {"user_id": 2, "event_id": 4, "date": date},
    {"user_id": 3, "event_id": 4, "date": date},
    {"user_id": 4, "event_id": 4, "date": date}
]


events_models = [models.Event(**event) for event in events]
users_models = [models.User(**user) for user in users]
checkins_models = [models.CheckIn(**checkin) for checkin in checkins]


def init_db():
    try:
        # init db models
        logger.info("Inserting db models...")
        models.Base.metadata.create_all(bind=engine)

        logger.info("Inserting testing data...")
        with db_session_scope() as db:
            db.add_all(events_models+users_models+checkins_models)
    except IntegrityError:
        logger.info("Testing data exists.")
