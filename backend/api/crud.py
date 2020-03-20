from sqlalchemy.orm import Session

from . import models, schemas


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id):
    return db.query(models.User).get(user_id)


def create_user(db: Session, user: schemas.User):
    if get_user(db, user.id):
        raise ValueError("User already registered.")
    db_user = models.User(**user.dict())

    db.add(db_user)
    db.commit()

    return db_user


def delete_user(db: Session, user_id: int):
    user = db.query(models.User).get(user_id)
    if not user:
        raise ValueError("User not found.")

    db.delete(user)
    db.commit()

    return user


def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()


def get_event(db: Session, event_id: int):
    return db.query(models.Event).get(event_id)


def get_event_by_title(db: Session, event_title: str):
    return db.query(models.Event).filter(
        models.Event.title == event_title
    ).first()


def create_event(db: Session, event: schemas.Event):
    if get_event_by_title(db, event.title):
        raise ValueError("Event with that title already registered.")
    db_event = models.Event(**event.dict(exclude={'id'}))

    db.add(db_event)
    db.commit()

    return db_event


def delete_event(db: Session, event_id: int):
    event = get_event(db, event_id)
    if not event:
        raise ValueError("Event not found.")

    db.delete(event)
    db.commit()

    return event


def get_checkins(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CheckIn).offset(skip).limit(limit).all()


def get_checkin(db: Session, checkin: schemas.CheckIn):
    return db.query(models.CheckIn).filter(
        models.CheckIn.user_id == checkin.user_id,
        models.CheckIn.event_id == checkin.event_id
    ).first()


def create_checkin(db: Session, checkin: schemas.CheckIn):
    if get_checkin(db, checkin):
        raise ValueError("Check-in already registered.")
    user = get_user(db, checkin.user_id)
    if not user:
        raise ValueError("No user with that id registered.")
    event = get_event(db, checkin.event_id)
    if not event:
        raise ValueError("No event with that id registered.")

    event.attendants.append(user)
    db.commit()

    checkin_db = get_checkin(db, checkin)

    return checkin_db


def delete_checkin(db: Session, checkin: schemas.CheckIn):
    checkin = get_checkin(db, checkin)
    if not checkin:
        raise ValueError("Check-in not found.")

    db.delete(checkin)
    db.commit()

    return checkin
