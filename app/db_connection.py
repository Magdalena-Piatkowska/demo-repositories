from sqlalchemy import create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.session import Session

from .config import DB_URL

engine = create_engine(DB_URL, pool_size=500, max_overflow=0, echo=True, future=True)
session_factory = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)
ScopedSession = scoped_session(session_factory)


async def get_session() -> Session:
    try:
        session = ScopedSession()
        return session
    finally:
        session.close()
