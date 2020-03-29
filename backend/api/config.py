from os import getenv


SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI",
                                 "sqlite:///:memory:")
# SQLALCHEMY_DATABASE_URI = "postgresql://user:password@postgresserver/db"
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = getenv("SECRET_KEY",
                    "6ce179a45c3a2a3fba4c96dc25eb03548103b5de01692fa3534ea2c5ee349e04")  # noqa
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

MASTER_KEY = getenv("MASTER_KEY", "dcc806d5a1")
