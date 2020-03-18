from os import getenv


SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI",
                                 "sqlite:///:memory:")
# SQLALCHEMY_DATABASE_URI = "postgresql://user:password@postgresserver/db"
