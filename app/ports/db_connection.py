import contextlib
from abc import ABC


class DBConnection(ABC):
    @contextlib.contextmanager
    def transaction(self):
        raise NotImplementedError

    def init_db(self):
        raise NotImplementedError

    def rollback(self):
        raise NotImplementedError
