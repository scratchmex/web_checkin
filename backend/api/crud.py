from sqlalchemy.orm import Session

from . import models, schemas


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id):
    return db.query(models.User).filter(
        models.Event.id == user_id
    ).first()


def create_user(db: Session, user: schemas.User):
    db_user = models.User(**user.dict())

    db.add(db_user)
    db.commit()

    return db_user


def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()


def get_event(db: Session, event_id: int):
    return db.query(models.Event).filter(
        models.Event.id == event_id
    ).first()


def get_event_by_title(db: Session, event_title: str):
    return db.query(models.Event).filter(
        models.Event.title == event_title
    ).first()


def create_event(db: Session, event: schemas.Event):
    db_event = models.Event(**event.dict(exclude={'id'}))

    db.add(db_event)
    db.commit()

    return db_event


def create_checkin(db: Session, checkin: schemas.CheckIn):
    user = db.query(models.User) \
             .filter(models.User.id == checkin.user_id).first()
    event = db.query(models.Event) \
              .filter(models.Event.id == checkin.event_id).first()

    event.attendants.append(user)

    return checkin


def get_checkin(db: Session, checkin: schemas.CheckIn):
    return db.query(models.CheckIn).filter(
        models.CheckIn.user_id == checkin.user_id,
        models.CheckIn.event_id == checkin.event_id
    ).first()


def get_checkins(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CheckIn).offset(skip).limit(limit).all()
