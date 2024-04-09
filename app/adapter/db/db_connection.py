import contextlib
from typing import Callable, List, Optional

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from app.ports.db_connection import DBConnection


class DBException(Exception):
    pass


class DBIntegrityError(DBException):
    pass


class SessionNotInitialised(DBException):
    pass


class SQLALchemyDBConnection(DBConnection):
    def __init__(
        self,
        database_uri: str,
        engine_args: Optional[dict] = None,
        session_args: Optional[dict] = None,
        post_commit_hooks: Optional[List[Callable]] = None,
    ):
        assert database_uri
        self.database_uri = database_uri

        self.engine_args = engine_args or dict(
            pool_pre_ping=True,
            pool_size=20,
            max_overflow=0,
            pool_recycle=10,
            pool_timeout=5,
            future=True,
            echo=True,
        )

        self.session_args = session_args or dict(
            expire_on_commit=False, autoflush=False
        )
        self.engine = self.create_engine()
        self._sessions: List[Session] = []
        if post_commit_hooks is None:
            self._post_commit_hooks = self._get_default_commit_hooks()
        else:
            self._post_commit_hooks = post_commit_hooks

    def _get_default_commit_hooks(self):
        return []

    @property
    def session(self) -> Session:
        if not self._sessions:
            raise SessionNotInitialised
        return self._sessions[-1]

    def init_db(self):
        from .model.base import Base

        Base.metadata.drop_all(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def create_engine(self):
        sqlite_fk_enforce = self.engine_args.pop("sqlite_fk_enforce", None)
        engine = create_engine(self.database_uri, **self.engine_args)

        if sqlite_fk_enforce:

            def _fk_pragma_on_connect(dbapi_con, con_record):
                dbapi_con.execute("pragma foreign_keys=ON")

            from sqlalchemy import event

            event.listen(engine, "connect", _fk_pragma_on_connect)
        return engine

    def session_maker(self):
        engine = self.session_args.get("bind")
        if not engine:
            engine = self.engine

        return sessionmaker(bind=engine, **self.session_args)

    @contextlib.contextmanager
    def transaction(self):
        try:
            Session = self.session_maker()
            with Session() as session:
                self._sessions.append(session)
                try:
                    yield session
                    session.commit()
                    self.post_commit_hooks(session)
                finally:
                    self._sessions.pop()
        except SQLAlchemyError as err:
            raise DBIntegrityError(str(err))

    def rollback(self):
        self.session.rollback()

    def post_commit_hooks(self, session):
        for hook in self._post_commit_hooks:
            hook(session)
