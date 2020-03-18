from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from . import config


engine = create_engine(
    config.SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False} if  # only for SQLite
        config.SQLALCHEMY_DATABASE_URI.startswith('sqlite') else {},  # noqa
    echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db() -> Session:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
