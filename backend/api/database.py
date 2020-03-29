from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

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
@contextmanager
def db_session_scope() -> Session:
    """Provide a transactional scope around a series of operations."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise
    finally:
        session.close()


def yield_db() -> Session:
    with db_session_scope() as db:
        yield db
