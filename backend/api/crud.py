from sqlalchemy.orm import Session

from . import models, schemas, auth


# users
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


# events
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
    event = models.Event(**event.dict())

    db.add(event)
    db.commit()

    db_event = get_event_by_title(db, event.title)

    return db_event


def delete_event(db: Session, event_id: int):
    event = get_event(db, event_id)
    if not event:
        raise ValueError("Event not found.")

    db.delete(event)
    db.commit()

    return event


# checkins
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


# admins
def get_admins(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Admin).offset(skip).limit(limit).all()


def get_admin(db: Session, admin_id: int):
    return db.query(models.Admin).get(admin_id)


def get_admin_by_username(db: Session, admin_username: str):
    return db.query(models.Admin).filter(
        models.Admin.username == admin_username
    ).first()


def create_admin(db: Session, admin: schemas.AdminIn):
    if get_admin_by_username(db, admin.username):
        raise ValueError("Admin with that username already registered.")
    hashed_password = auth.hash_password(admin.password)

    admin = models.Admin(hashed_password=hashed_password,
                         **admin.dict(exclude={"password"}))

    db.add(admin)
    db.commit()

    db_admin = get_admin_by_username(db, admin.username)

    return db_admin


def delete_admin(db: Session, admin_id: int):
    admin = get_admin(db, admin_id)
    if not admin:
        raise ValueError("Admin not found.")

    db.delete(admin)
    db.commit()

    return admin


def authenticate_admin(db: Session, username: str, password: str):
    admin = get_admin_by_username(db, username)

    if not admin or not auth.verify_password(password, admin.hashed_password):
        raise ValueError("Invalid authentication credentials.")

    return admin
