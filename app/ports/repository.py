from abc import ABC
from typing import Any, Optional

from app.ports.db_connection import DBConnection
from app.ports.storage_connection import StorageConnection


class Repository(ABC):
    def __init__(
        self,
        db: Optional[DBConnection] = None,
        storage: Optional[StorageConnection] = None,
    ):
        self.db = db
        self.storage = storage

    def create(self, obj_in: Any, **kwargs):
        raise NotImplementedError

    def read(self, id: Any, **kwargs):
        raise NotImplementedError

    def read_multi(self, filters: Optional[dict] = None, **kwargs):
        raise NotImplementedError
