from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine

from contextlib import contextmanager

from settings import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(str(settings.db.url), echo=settings.db.echo)
session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)


def __db_session_gen():
    db = session_maker()
    try:
        yield db
    finally:
        db.close()


def get_db():
    return __db_session_gen()


@contextmanager
def db_session():
    yield from __db_session_gen()
