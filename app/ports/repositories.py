from abc import ABC
from typing import Optional

from app.ports.db_connection import DBConnection
from app.ports.storage_connection import StorageConnection

from .repository import Repository


class Repositories(ABC):
    def __init__(
        self,
        db: Optional[DBConnection] = None,
        storage: Optional[StorageConnection] = None,
    ):
        self.db: Optional[DBConnection] = db
        self.storage: Optional[StorageConnection] = storage

    def commit(self):
        raise NotImplementedError

    def rollback(self):
        raise NotImplementedError

    @property
    def quote(self) -> Repository:
        raise NotImplementedError

    @property
    def insured_property(self) -> Repository:
        raise NotImplementedError

    @property
    def occupancy_rate(self) -> Repository:
        raise NotImplementedError
